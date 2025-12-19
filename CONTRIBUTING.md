# Contributing to Digital Legal Compass

Thank you for your interest in contributing to Digital Legal Compass! This document provides guidelines and instructions for contributing.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Testing Guidelines](#testing-guidelines)

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect differing viewpoints and experiences

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 18+
- Git
- Google API Key
- Familiarity with FastAPI, Next.js, LangChain

### Development Setup

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/digitallegalcompass.git
   cd digitallegalcompass
   ```

3. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/digitallegalcompass.git
   ```

4. **Set up backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # or .\venv\Scripts\Activate on Windows
   pip install -r requirements.txt
   cp .env.example .env
   # Add your GOOGLE_API_KEY to .env
   ```

5. **Set up frontend**
   ```bash
   cd frontend
   npm install
   ```

6. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## How to Contribute

### Types of Contributions

**🐛 Bug Reports**
- Use GitHub Issues
- Include clear title and description
- Provide steps to reproduce
- Include system info (OS, Python/Node version)
- Add screenshots if relevant

**✨ Feature Requests**
- Open a GitHub Issue first
- Explain the problem it solves
- Describe proposed solution
- Discuss implementation approach

**📝 Documentation**
- Fix typos or unclear explanations
- Add examples or tutorials
- Improve API documentation
- Update README files

**💻 Code Contributions**
- Bug fixes
- New features
- Performance improvements
- Code refactoring

### Finding Issues to Work On

- Look for `good first issue` label
- Check `help wanted` label
- Ask in discussions for guidance

## Coding Standards

### Python (Backend)

**Style Guide:** PEP 8

```python
# Good
def process_documents(file_paths: List[str]) -> List[Document]:
    """
    Process documents and return chunks.
    
    Args:
        file_paths: List of file paths to process
        
    Returns:
        List of document chunks
    """
    documents = []
    for path in file_paths:
        # Process file
        pass
    return documents
```

**Key Points:**
- Use type hints
- Write docstrings for functions
- Keep functions small and focused
- Use meaningful variable names
- Max line length: 88 characters (Black formatter)

**Imports:**
```python
# Standard library
import os
from typing import List, Optional

# Third-party
from fastapi import APIRouter
from langchain_core.documents import Document

# Local
from app.services import process_documents
```

### JavaScript/React (Frontend)

**Style Guide:** Airbnb JavaScript Style Guide

```javascript
// Good
export default function DocumentUpload({ onUploadSuccess }) {
  const [files, setFiles] = useState([])
  const [loading, setLoading] = useState(false)

  const handleUpload = async () => {
    // Upload logic
  }

  return (
    <div className="container">
      {/* Component content */}
    </div>
  )
}
```

**Key Points:**
- Use functional components with hooks
- Use meaningful component and variable names
- Keep components small and focused
- Use Tailwind CSS classes
- Add PropTypes or TypeScript types

**File Structure:**
```javascript
// Imports
import { useState } from 'react'
import axios from 'axios'

// Component
export default function Component() {
  // State
  const [state, setState] = useState(initial)

  // Effects
  useEffect(() => {
    // Effect logic
  }, [dependencies])

  // Handlers
  const handleAction = () => {
    // Handler logic
  }

  // Render
  return (
    <div>
      {/* JSX */}
    </div>
  )
}
```

### Documentation

- Use Markdown for documentation
- Keep line length under 100 characters
- Use code blocks with syntax highlighting
- Include examples for complex features
- Update relevant docs with code changes

## Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```bash
feat(upload): add support for DOCX files

Add functionality to process Microsoft Word documents
in addition to PDF, TXT, and MD files.

Closes #123
```

```bash
fix(chat): resolve message duplication issue

Fixed bug where messages were appearing twice
in the chat interface due to state update race condition.

Fixes #456
```

```bash
docs(readme): update installation instructions

Clarified Python version requirements and added
troubleshooting section for common setup issues.
```

### Commit Best Practices

- Write clear, descriptive messages
- Use present tense ("add" not "added")
- Keep subject line under 50 characters
- Separate subject from body with blank line
- Reference issues and PRs in footer

## Pull Request Process

### Before Submitting

1. **Update your branch**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Test your changes**
   ```bash
   # Backend tests
   cd backend
   pytest

   # Frontend tests
   cd frontend
   npm test
   ```

3. **Lint your code**
   ```bash
   # Backend
   black .
   flake8 .

   # Frontend
   npm run lint
   ```

4. **Update documentation**
   - Update README if needed
   - Add docstrings/comments
   - Update API docs if applicable

### Submitting Pull Request

1. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request on GitHub**
   - Use a clear title
   - Fill out the PR template
   - Link related issues
   - Add screenshots for UI changes

3. **PR Template**
   ```markdown
   ## Description
   Brief description of changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Code refactoring

   ## Testing
   - [ ] Tested locally
   - [ ] Added/updated tests
   - [ ] All tests pass

   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Documentation updated
   - [ ] No new warnings
   - [ ] Linked related issues

   ## Screenshots (if applicable)
   Add screenshots here
   ```

### Review Process

- Maintainers will review your PR
- Address feedback and comments
- Update PR with requested changes
- Once approved, it will be merged

### After Merge

```bash
# Update your local main
git checkout main
git pull upstream main

# Delete feature branch
git branch -d feature/your-feature-name
git push origin --delete feature/your-feature-name
```

## Testing Guidelines

### Backend Tests

**Location:** `backend/tests/`

```python
# tests/test_document_processor.py
import pytest
from app.services.document_processor import process_documents

def test_process_pdf():
    """Test PDF processing"""
    result = process_documents(['test.pdf'])
    assert len(result) > 0
    assert result[0].page_content

def test_unsupported_file():
    """Test unsupported file type"""
    with pytest.raises(ValueError):
        process_documents(['test.docx'])
```

**Run tests:**
```bash
cd backend
pytest
pytest --cov  # With coverage
```

### Frontend Tests

**Location:** `frontend/__tests__/`

```javascript
// __tests__/DocumentUpload.test.js
import { render, screen, fireEvent } from '@testing-library/react'
import DocumentUpload from '../app/components/DocumentUpload'

test('renders upload button', () => {
  render(<DocumentUpload />)
  const button = screen.getByText(/upload documents/i)
  expect(button).toBeInTheDocument()
})

test('handles file selection', () => {
  render(<DocumentUpload />)
  const input = screen.getByLabelText(/select files/i)
  const file = new File(['test'], 'test.pdf', { type: 'application/pdf' })
  
  fireEvent.change(input, { target: { files: [file] } })
  expect(screen.getByText('test.pdf')).toBeInTheDocument()
})
```

**Run tests:**
```bash
cd frontend
npm test
npm test -- --coverage  # With coverage
```

### Manual Testing Checklist

**Backend:**
- [ ] Server starts without errors
- [ ] Can upload PDF file
- [ ] Can upload TXT file
- [ ] Can upload MD file
- [ ] Rejects unsupported file types
- [ ] Chat returns valid responses
- [ ] Sources are correct
- [ ] Error handling works

**Frontend:**
- [ ] Page loads correctly
- [ ] Can select files
- [ ] Upload progress shown
- [ ] Success message displayed
- [ ] Chat input enabled after upload
- [ ] Messages display correctly
- [ ] Loading indicator works
- [ ] Responsive on mobile
- [ ] Error messages shown

## Questions?

- Open a discussion on GitHub
- Ask in existing issues
- Check documentation
- Review closed PRs for examples

## Recognition

Contributors will be:
- Added to CONTRIBUTORS.md
- Mentioned in release notes
- Appreciated in project documentation

---

Thank you for contributing to Digital Legal Compass! 🎉
