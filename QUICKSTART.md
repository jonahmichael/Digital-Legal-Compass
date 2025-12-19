# Digital Legal Compass - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

This guide will help you get the Digital Legal Compass up and running quickly.

### Step 1: Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.8+ installed (`python --version`)
- ✅ Node.js 18+ installed (`node --version`)
- ✅ npm installed (`npm --version`)
- ✅ Google API Key ([Get one here](https://makersuite.google.com/app/apikey))

### Step 2: Clone or Extract Project

```bash
cd digitallegalcompass
```

### Step 3: Backend Setup (5 steps)

```bash
# 1. Navigate to backend
cd backend

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
.\venv\Scripts\Activate  # Windows PowerShell
# source venv/bin/activate  # macOS/Linux

# 4. Install dependencies (takes 1-2 minutes)
pip install -r requirements.txt

# 5. Create .env file
# Copy .env.example to .env and add your Google API key
# GOOGLE_API_KEY=your_actual_api_key_here
```

**Create `.env` file:**
```env
GOOGLE_API_KEY=your_google_api_key_here
```

**Start the backend:**
```bash
python main.py
```

✅ Backend running at http://localhost:8000

### Step 4: Frontend Setup (3 steps)

Open a **NEW terminal** window:

```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies (takes 1-2 minutes)
npm install

# 3. Start development server
npm run dev
```

✅ Frontend running at http://localhost:3000

### Step 5: Test the Application

1. **Open Browser**: Navigate to http://localhost:3000
2. **Upload a Document**: Click "Select legal documents" and upload a PDF, TXT, or MD file
3. **Wait for Confirmation**: You'll see "Successfully uploaded X document(s)"
4. **Ask a Question**: Type a question in the chat box like "What is this document about?"
5. **Get Answer**: The AI will respond with an answer based on your document

## 🎯 Quick Test

Use this test document to verify everything works:

**Create `test.txt`:**
```
This is a test legal agreement between Party A and Party B.
The payment terms are $1000 per month.
The contract duration is 12 months.
Either party can terminate with 30 days notice.
```

**Upload it and ask:**
- "What are the payment terms?"
- "How long is the contract?"
- "What is the termination notice period?"

## 🔧 Troubleshooting Quick Fixes

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install -r requirements.txt

# Check if .env exists and has API key
type .env  # Windows
cat .env   # macOS/Linux
```

### Frontend won't start
```bash
# Check Node version
node --version  # Should be 18+

# Clear and reinstall
rm -rf node_modules package-lock.json
npm install

# Try different port
npm run dev -- -p 3001
```

### Can't connect frontend to backend
1. Verify backend is running on port 8000
2. Check `frontend/next.config.js` has correct rewrite rules
3. Try accessing http://localhost:8000 directly

### Documents won't upload
1. Check file size (keep under 10MB for testing)
2. Verify file type (PDF, TXT, or MD only)
3. Check backend console for errors
4. Ensure backend `temp_data/` directory exists

## 📚 Next Steps

- Read [README.md](README.md) for full documentation
- Check [backend/README.md](backend/README.md) for API details
- See [frontend/README.md](frontend/README.md) for UI customization
- Visit http://localhost:8000/docs for interactive API documentation

## 🆘 Need Help?

Common questions:
- **Where do I get a Google API key?** → https://makersuite.google.com/app/apikey
- **What Python version?** → 3.8 or higher
- **What Node version?** → 18 or higher
- **Is this free?** → Google API has a free tier
- **Can I use OpenAI instead?** → Code modifications needed

## ✅ Success Checklist

- [ ] Backend starts without errors
- [ ] Frontend loads at http://localhost:3000
- [ ] Can upload a test document
- [ ] Can ask questions and get answers
- [ ] Answers include source attribution

Congratulations! 🎉 Your Digital Legal Compass is now running!
