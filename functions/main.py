# ===================================================================
# === main.py (FINAL CORRECTED & BULLETPROOF VERSION) ===
# ===================================================================

import os
import traceback
from firebase_functions import https_fn
from firebase_admin import initialize_app
from google.cloud import documentai, dlp_v2
import vertexai
from vertexai.generative_models import GenerativeModel

# --- Initialize Admin SDK ---
initialize_app()

# ===================================================================
# === Helper Functions (These are solid) ===
# ===================================================================

def extract_text_with_docai(project_id, location, processor_id, file_content, mime_type):
    print("Step 1: Starting Document AI.")
    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=opts)
    name = client.processor_.path(project_id, location, processor_id)
    raw_document = documentai.RawDocument(content=file_content, mime_type=mime_type)
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    print("Step 1: Document AI successful.")
    return result.document.text

def sanitize_text_with_dlp(project_id, text_to_redact):
    print("Step 2: Starting DLP.")
    dlp_client = dlp_v2.DlpServiceClient()
    parent = f"projects/{project_id}"
    item = {"value": text_to_redact}
    info_types = [{"name": "PERSON_NAME"}, {"name": "PHONE_NUMBER"}, {"name": "STREET_ADDRESS"}, {"name": "EMAIL_ADDRESS"}]
    inspect_config = {"info_types": info_types}
    deidentify_config = {"info_type_transformations": {"transformations": [{"primitive_transformation": {"replace_with_info_type_config": {}}}]}}
    request = dlp_v2.DeidentifyContentRequest(parent=parent, inspect_config=inspect_config, deidentify_config=deidentify_config, item=item)
    response = dlp_client.deidentify_content(request=request)
    print("Step 2: DLP successful.")
    return response.item.value

def analyze_document_with_gemini(project_id, location, sanitized_text):
    print("Step 3: Starting Gemini Analysis.")
    vertexai.init(project=project_id, location=location)
    gemini_model = GenerativeModel("gemini-1.5-pro-preview-0409")
    prompt = f"""
    You are an expert legal assistant. Your task is to simplify the following legal document.
    Provide a clear, structured analysis using Markdown.
    ---
    {sanitized_text}
    ---
    """
    response = gemini_model.generate_content(prompt)
    print("Step 3: Gemini Analysis successful.")
    return response.text

# ===================================================================
# === The Main Cloud Function ===
# ===================================================================

@https_fn.on_request(cors=https_fn.options.CorsOptions(cors_origins="*", cors_methods=["post"]))
def analyze_legal_document(req: https_fn.Request) -> https_fn.Response:
    """
    This is the main entry point. It handles the incoming file,
    runs the full AI pipeline, and returns the final analysis.
    """
    try:
        print("New request received.")
        
        if 'file' not in req.files:
            raise ValueError("No file part in the request.")
            
        uploaded_file = req.files['file']
        file_content = uploaded_file.read()
        mime_type = uploaded_file.content_type
        
        PROJECT_ID = os.environ.get("GCLOUD_PROJECT")
        LOCATION = "us-central1"
        DOCAI_PROCESSOR_ID = "c42849c05c8c73d9" # Your processor ID
        DOCAI_LOCATION = "us" 
        
        extracted_text = extract_text_with_docai(PROJECT_ID, DOCAI_LOCATION, DOCAI_PROCESSOR_ID, file_content, mime_type)
        sanitized_text = sanitize_text_with_dlp(PROJECT_ID, extracted_text)
        final_analysis = analyze_document_with_gemini(PROJECT_ID, LOCATION, sanitized_text)
        
        print("Pipeline complete. Returning successful response.")
        return https_fn.Response(
            f'{{"analysis": "{final_analysis}"}}',
            status=200,
            headers={"Content-Type": "application/json"}
        )

    except Exception as e:
        print(f"CRITICAL ERROR in pipeline: {e}")
        traceback.print_exc()
        raise https_fn.HttpsError(
            code=https_fn.HttpsErrorCode.INTERNAL,
            message=f"An unexpected server error occurred: {e}"
        )