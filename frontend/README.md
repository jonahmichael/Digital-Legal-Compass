# Digital Legal Compass - Frontend

> Modern Next.js frontend for the Digital Legal Compass RAG-powered legal document assistant.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup](#setup)
- [Project Structure](#project-structure)
- [Components](#components)
- [Configuration](#configuration)
- [Development](#development)
- [Building for Production](#building-for-production)

## Overview

The frontend provides an intuitive, responsive interface for uploading legal documents and querying them using natural language. Built with Next.js 14 and styled with Tailwind CSS, it offers a modern user experience with real-time chat capabilities.

## Features

✨ **Key Features:**
- 📁 **Drag & Drop Upload**: Easy document upload interface
- 💬 **Real-time Chat**: Interactive conversation with AI
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile
- 🎨 **Modern UI**: Clean, professional design with Tailwind CSS
- ⚡ **Fast Performance**: Next.js optimization and SSR
- 🔄 **Live Updates**: Real-time response streaming
- 📊 **Source Attribution**: Display relevant document sources
- 🎯 **Smart State Management**: Tracks upload and chat state

## Tech Stack

| Component | Technology | Version | Purpose |
|-----------|------------|---------|----------|
| **Framework** | Next.js | 14.x | React framework with SSR |
| **UI Library** | React | 18.x | Component-based UI |
| **Styling** | Tailwind CSS | 3.x | Utility-first CSS |
| **HTTP Client** | Axios | Latest | API requests |
| **Build Tool** | Turbopack | Built-in | Fast bundling |

## Setup

### Prerequisites

- Node.js 18 or higher
- npm or yarn
- Backend server running on port 8000

### Installation

1. **Install dependencies:**
```bash
npm install
```

### Installation

1. **Install dependencies:**
```bash
npm install
# or
yarn install
```

2. **Configure environment (optional):**

The `.env.local` file is already configured:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Modify if your backend runs on a different URL.

3. **Run the development server:**
```bash
npm run dev
# or
yarn dev
```

The UI will be available at: **http://localhost:3000**

## Project Structure

```
frontend/
├── app/
│   ├── components/
│   │   ├── DocumentUpload.js      # Document upload component
│   │   └── Chat.js                # Chat interface component
│   ├── layout.js                  # Root layout with metadata
│   ├── page.js                    # Home page (main UI)
│   └── globals.css                # Global styles & Tailwind
├── public/                        # Static assets
├── .env.local                     # Environment variables
├── next.config.js                 # Next.js configuration
├── tailwind.config.js             # Tailwind CSS configuration
├── postcss.config.js              # PostCSS configuration
├── package.json                   # Dependencies & scripts
└── README.md                      # This file
```

## Components

### DocumentUpload Component

**Location**: `app/components/DocumentUpload.js`

**Purpose**: Handles document upload functionality

**Features:**
- Multi-file selection
- File type validation (PDF, TXT, MD)
- Upload progress indication
- Success/error messaging
- Triggers callback on successful upload

**Props:**
```javascript
{
  onUploadSuccess: () => void  // Callback when upload completes
}
```

**Usage:**
```jsx
<DocumentUpload onUploadSuccess={() => setDocumentsUploaded(true)} />
```

**Key Functions:**
- `handleFileChange(e)`: Updates selected files state
- `handleUpload()`: Sends files to backend API

### Chat Component

**Location**: `app/components/Chat.js`

**Purpose**: Interactive chat interface for querying documents

**Features:**
- Message history display
- Real-time response rendering
- Auto-scroll to latest message
- Loading indicator
- Error handling
- Disabled state before document upload

**Props:**
```javascript
{
  disabled: boolean  // Disables chat until documents uploaded
}
```

**Usage:**
```jsx
<Chat disabled={!documentsUploaded} />
```

**Key Functions:**
- `handleSubmit(e)`: Sends query to backend
- `scrollToBottom()`: Auto-scrolls to latest message

**Message Format:**
```javascript
{
  role: 'user' | 'assistant',
  content: string
}
```

### Home Page

**Location**: `app/page.js`

**Purpose**: Main application layout

**Features:**
- Two-column responsive layout
- State management for upload status
- Conditional chat enabling

**Layout:**
- Left panel: Document Upload
- Right panel: Chat Interface

### Root Layout

**Location**: `app/layout.js`

**Purpose**: Application-wide layout and metadata

**Features:**
- HTML structure
- Metadata configuration
- Global styling imports

## Configuration

### Environment Variables

**File**: `.env.local`

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Note**: Variables prefixed with `NEXT_PUBLIC_` are exposed to the browser.

### Next.js Configuration

**File**: `next.config.js`

```javascript
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
    ];
  },
}
```

**Key Features:**
- **React Strict Mode**: Enhanced development checks
- **API Rewrites**: Proxies `/api/*` to backend (avoids CORS)

### Tailwind Configuration

**File**: `tailwind.config.js`

```javascript
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

**Customization:**
- Add custom colors in `theme.extend.colors`
- Add custom fonts in `theme.extend.fontFamily`
- Add plugins for additional features

## Development

### Available Scripts

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linter
npm run lint
```

### Development Server

```bash
npm run dev
```

Opens at: http://localhost:3000

**Features:**
- Hot module replacement
- Fast refresh
- Error overlay
- Development tools

### Adding New Components

1. Create component file in `app/components/`:
```javascript
// app/components/NewComponent.js
'use client'

export default function NewComponent() {
  return <div>New Component</div>
}
```

2. Import in page or other component:
```javascript
import NewComponent from './components/NewComponent'
```

### Styling Guidelines

**Using Tailwind Classes:**
```jsx
<div className="flex items-center justify-between p-4 bg-blue-500 rounded-lg">
  <h1 className="text-2xl font-bold text-white">Title</h1>
</div>
```

**Custom CSS (when needed):**
```css
/* app/globals.css */
.custom-class {
  @apply flex items-center gap-4;
}
```

### API Integration

**Upload Documents:**
```javascript
const formData = new FormData()
files.forEach(file => formData.append('files', file))

const response = await axios.post('/api/documents/upload', formData, {
  headers: { 'Content-Type': 'multipart/form-data' }
})
```

**Chat:**
```javascript
const response = await axios.post('/api/documents/chat', {
  message: userInput
})
```

## Building for Production

### Build Command

```bash
npm run build
```

**Output:**
- Optimized JavaScript bundles
- Static HTML pages
- CSS minification
- Image optimization

### Start Production Server

```bash
npm start
```

Runs on http://localhost:3000

### Performance Optimizations

**Automatic:**
- Code splitting
- Tree shaking
- Image optimization
- Font optimization
- CSS minification

**Manual Optimizations:**
```javascript
// Use dynamic imports for large components
const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <p>Loading...</p>
})
```

### Deployment

**Vercel (Recommended):**
```bash
npm i -g vercel
vercel
```

**Other Platforms:**
- Build: `npm run build`
- Start: `npm start`
- Set environment variables
- Configure reverse proxy to backend

**Environment Variables for Production:**
```env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

## Troubleshooting

### Common Issues

**Issue: "Cannot connect to backend"**
- Check backend is running on port 8000
- Verify `next.config.js` rewrite rules
- Check CORS settings in backend

**Issue: "Module not found"**
```bash
rm -rf node_modules package-lock.json
npm install
```

**Issue: "Tailwind styles not applying"**
- Check `tailwind.config.js` content paths
- Verify `globals.css` imports Tailwind directives
- Restart dev server

**Issue: "Upload not working"**
- Check file size limits
- Verify file types (PDF, TXT, MD only)
- Check backend logs
- Test with smaller files

**Issue: "Chat responses not appearing"**
- Upload documents first
- Check browser console for errors
- Verify backend API responses
- Check network tab in DevTools

### Debug Mode

```bash
# Enable Next.js debug logging
NODE_OPTIONS='--inspect' npm run dev

# Check build analysis
npm run build -- --debug
```

### Browser DevTools

- **Console**: Check for JavaScript errors
- **Network**: Monitor API requests/responses
- **React DevTools**: Inspect component state

## Best Practices

### Code Organization
- Keep components small and focused
- Use client components (`'use client'`) only when needed
- Separate business logic from presentation

### Performance
- Use `loading.js` for loading states
- Implement error boundaries
- Optimize images with Next.js Image component

### Accessibility
- Use semantic HTML
- Add ARIA labels
- Test with keyboard navigation
- Ensure color contrast

### Security
- Never expose secrets in client-side code
- Validate user inputs
- Sanitize data before rendering
- Use HTTPS in production

---

For backend setup and API documentation, see [backend/README.md](../backend/README.md)
