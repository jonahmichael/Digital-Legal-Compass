# ===================================================================
# === main.py (ROBUST VERSION) for Firebase Cloud Functions ===
# ===================================================================

import os
from firebase_functions import https_fn, options
from firebase_admin import initialize_app, get_app
from google.cloud import documentai, dlp_v2
import vertexai
from vertexai.generative_models import GenerativeModel

# --- We will initialize the apps LAZILY (inside the function) ---
# This is a global flag to ensure initialization only happens once per container instance.
_initialized = False


# ===================================================================
# === Helper Functions (These are unchanged) ===
# ===================================================================

def extract_text_with_docai(project_id, location, processor_id, file_content, mime_type):
    """Processes a document using the Document AI API."""
    print("Step 1: Starting Document AI text extraction.")
    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=opts)
    name = client.processor_path(project_id, location, processor_id)
    raw_document = documentai.RawDocument(content=file_content, mime_type=mime_type)
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    
    try:
        result = client.process_document(request=request)
        print("Step 1: Document AI extraction successful.")
        return result.document.text
    except Exception as e:
        print(f"Error during Document AI processing: {e}")
        raise https_fn.HttpsError(code="internal", message="Failed to process document with Document AI.")

def sanitize_text_with_dlp(project_id, text_to_redact):
    """Uses the Cloud DLP API to inspect and redact sensitive information."""
    print("Step 2: Starting DLP sanitization.")
    dlp_client = dlp_v2.DlpServiceClient()
    parent = f"projects/{project_id}"
    item = {"value": text_to_redact}
    info_types = [{"name": "PERSON_NAME"}, {"name": "PHONE_NUMBER"}, {"name": "STREET_ADDRESS"}, {"name": "EMAIL_ADDRESS"}]
    inspect_config = {"info_types": info_types}
    deidentify_config = {"info_type_transformations": {"transformations": [{"primitive_transformation": {"replace_with_info_type_config": {}}}]}}
    request = dlp_v2.DeidentifyContentRequest(parent=parent, inspect_config=inspect_config, deidentify_config=deidentify_config, item=item)
    
    try:
        response = dlp_client.deidentify_content(request=request)
        print("Step 2: DLP sanitization successful.")
        return response.item.value
    except Exception as e:
        print(f"Error during DLP processing: {e}")
        raise https_fn.HttpsError(code="internal", message="Failed to sanitize document with Cloud DLP.")

def analyze_document_with_gemini(project_id, location, sanitized_text):
    """Generates insights using the Gemini 1.5 Pro model."""
    print("Step 3: Starting Gemini analysis.")
    vertexai.init(project=project_id, location=location) # Initialize Vertex AI here
    gemini_model = GenerativeModel("gemini-1.5-pro-preview-0409")
    
    prompt = f"""
    You are an expert legal assistant. Your task is to simplify the following legal document.
    Provide a clear, structured analysis.

    Your analysis MUST include the following sections using Markdown:
    *   **## Document Purpose:** What is this document for in one sentence?
    *   **## Key Parties:** Who are the main people or companies involved?
    *   **## Core Obligations:** What are the 3-4 most important things the user MUST do?
    *   **## Key Rights:** What are the 3-4 most important rights or protections the user receives?
    *   **## 🚨 Red Flags (Potential Risks):** Identify 2-3 clauses that could be risky or unfavorable and explain them simply.

    Here is the document text:
    ---
    {sanitized_text}
    ---
    """
    
    try:
        response = gemini_model.generate_content(prompt)
        print("Step 3: Gemini analysis successful.")
        return response.text
    except Exception as e:
        print(f"Error during Gemini analysis: {e}")
        raise https_fn.HttpsError(code="internal", message="Failed to generate insights with Gemini AI.")


# ===================================================================
# === The Main Cloud Function (With ROBUST Initialization) ===
# ===================================================================

@https_fn.on_request(cors=options.CorsOptions(cors_origins="*", cors_methods=["post"]))
def analyze_legal_document(req: https_fn.Request) -> https_fn.Response:
    """
    This is the main entry point. It handles the incoming file from the website,
    runs the full AI pipeline, and returns the final analysis.
    """
    
    # --- LAZY INITIALIZATION ---
    # This block ensures that Firebase and Vertex AI are only initialized ONCE.
    global _initialized
    if not _initialized:
        initialize_app()
        _initialized = True
        print("Firebase Admin SDK initialized.")
    # --- END INITIALIZATION ---
    
    PROJECT_ID = os.environ.get("GCLOUD_PROJECT")
    LOCATION = "us-central1"

    print("New request received for document analysis.")
    
    if 'file' not in req.files:
        print("Error: No file found in the request.")
        raise https_fn.HttpsError(code="invalid-argument", message="No file uploaded.")
        
    uploaded_file = req.files['file']
    file_content = uploaded_file.read()
    mime_type = uploaded_file.content_type
    
    DOCAI_PROCESSOR_ID = "c42849c05c8c73d9" 
    DOCAI_LOCATION = "us" 
    
    try:
        extracted_text = extract_text_with_docai(PROJECT_ID, DOCAI_LOCATION, DOCAI_PROCESSOR_ID, file_content, mime_type)
        sanitized_text = sanitize_text_with_dlp(PROJECT_ID, extracted_text)
        final_analysis = analyze_document_with_gemini(PROJECT_ID, LOCATION, sanitized_text)
        
        print("Pipeline complete. Returning successful response.")
        
        return https_fn.Response(
            {"analysis": final_analysis},
            status=200,
            headers={"Content-Type": "application/json"}
        )

    except Exception as e:
        print(f"An unexpected error occurred in the pipeline: {e}")
        raise https_fn.HttpsError(code="internal", message="An unexpected error occurred.")