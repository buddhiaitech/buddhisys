# 🤖 PDF-AGENT: Intelligent RPA Automation System

<div align="center">

![PDF-AGENT Logo](https://img.shields.io/badge/PDF--AGENT-Intelligent%20RPA-blue?style=for-the-badge&logo=robot)
![Python](https://img.shields.io/badge/Python-3.7+-green?style=for-the-badge&logo=python)
![React](https://img.shields.io/badge/React-18+-blue?style=for-the-badge&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green?style=for-the-badge&logo=fastapi)

**Automated PDF Form Filling with AI-Powered Data Generation and Web Interface Control**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/buddhiaitech/buddhisys.svg)](https://github.com/buddhiaitech/buddhisys/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/buddhiaitech/buddhisys.svg)](https://github.com/buddhiaitech/buddhisys/network)

</div>

## 🎯 Overview

PDF-AGENT is a comprehensive Robotic Process Automation (RPA) system that intelligently fills PDF forms using AI-generated data and provides a modern web interface for monitoring and control. The system combines Python automation scripts with a React-based dashboard for seamless workflow management.

## ✨ Key Features

- 🤖 **AI-Powered Data Generation** - Uses Google Gemini AI to generate realistic form data
- 📄 **Intelligent PDF Processing** - Automatically detects and fills all form fields
- 🌐 **Web Interface** - Modern React dashboard for workflow control and monitoring
- 🔄 **Real-time Monitoring** - Live progress tracking and log streaming
- 🖥️ **Remote Desktop Integration** - NoVNC support for visual automation monitoring
- 📧 **Email Automation** - Automatic email sending with filled PDF attachments
- 🔧 **Modular Architecture** - Extensible Python modules for different automation tasks
- ⚡ **API-First Design** - FastAPI backend for scalable automation management

## 🏗️ System Architecture

<svg width="800" height="600" xmlns="http://www.w3.org/2000/svg">
  <!-- Background -->
  <rect width="800" height="600" fill="#f8fafc" stroke="#e2e8f0" stroke-width="2"/>
  
  <!-- Title -->
  <text x="400" y="30" text-anchor="middle" font-family="Arial, sans-serif" font-size="24" font-weight="bold" fill="#1e293b">PDF-AGENT System Architecture</text>
  
  <!-- Frontend Layer -->
  <rect x="50" y="60" width="700" height="80" fill="#dbeafe" stroke="#3b82f6" stroke-width="2" rx="10"/>
  <text x="400" y="85" text-anchor="middle" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#1e40af">Frontend Layer (React)</text>
  <text x="100" y="110" font-family="Arial, sans-serif" font-size="12" fill="#1e40af">• Control Panel - Start/Stop Workflows</text>
  <text x="100" y="125" font-family="Arial, sans-serif" font-size="12" fill="#1e40af">• Console - NoVNC Remote Desktop</text>
  <text x="400" y="110" font-family="Arial, sans-serif" font-size="12" fill="#1e40af">• Real-time Progress Tracking</text>
  <text x="400" y="125" font-family="Arial, sans-serif" font-size="12" fill="#1e40af">• Live Log Streaming</text>
  
  <!-- API Layer -->
  <rect x="50" y="160" width="700" height="80" fill="#dcfce7" stroke="#22c55e" stroke-width="2" rx="10"/>
  <text x="400" y="185" text-anchor="middle" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#166534">API Layer (FastAPI)</text>
  <text x="100" y="210" font-family="Arial, sans-serif" font-size="12" fill="#166534">• /workflows/start - Launch Python Scripts</text>
  <text x="100" y="225" font-family="Arial, sans-serif" font-size="12" fill="#166534">• /workflows/stop - Terminate Processes</text>
  <text x="400" y="210" font-family="Arial, sans-serif" font-size="12" fill="#166534">• /workflows/status - Process Monitoring</text>
  <text x="400" y="225" font-family="Arial, sans-serif" font-size="12" fill="#166534">• CORS-enabled for Web Integration</text>
  
  <!-- Python Automation Layer -->
  <rect x="50" y="260" width="700" height="120" fill="#fef3c7" stroke="#f59e0b" stroke-width="2" rx="10"/>
  <text x="400" y="285" text-anchor="middle" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#92400e">Python Automation Layer</text>
  
  <!-- Workflow Boxes -->
  <rect x="80" y="300" width="180" height="60" fill="#fbbf24" stroke="#f59e0b" stroke-width="1" rx="5"/>
  <text x="170" y="320" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#92400e">Final Complete</text>
  <text x="170" y="335" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#92400e">Website → PDF → Email</text>
  <text x="170" y="350" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#92400e">All Fields Filled</text>
  
  <rect x="280" y="300" width="180" height="60" fill="#fbbf24" stroke="#f59e0b" stroke-width="1" rx="5"/>
  <text x="370" y="320" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#92400e">Fill & Send</text>
  <text x="370" y="335" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#92400e">PDF Focused</text>
  <text x="370" y="350" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#92400e">TREC Form</text>
  
  <rect x="480" y="300" width="180" height="60" fill="#fbbf24" stroke="#f59e0b" stroke-width="1" rx="5"/>
  <text x="570" y="320" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#92400e">Partial Run</text>
  <text x="570" y="335" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#92400e">Testing Only</text>
  <text x="570" y="350" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="#92400e">No Email</text>
  
  <!-- Core Modules -->
  <rect x="50" y="400" width="700" height="100" fill="#fce7f3" stroke="#ec4899" stroke-width="2" rx="10"/>
  <text x="400" y="425" text-anchor="middle" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#be185d">Core Python Modules</text>
  
  <rect x="80" y="440" width="150" height="50" fill="#f9a8d4" stroke="#ec4899" stroke-width="1" rx="5"/>
  <text x="155" y="460" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#be185d">Browser Automation</text>
  <text x="155" y="475" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" fill="#be185d">Selenium WebDriver</text>
  
  <rect x="250" y="440" width="150" height="50" fill="#f9a8d4" stroke="#ec4899" stroke-width="1" rx="5"/>
  <text x="325" y="460" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#be185d">PDF Processor</text>
  <text x="325" y="475" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" fill="#be185d">AI Data Generation</text>
  
  <rect x="420" y="440" width="150" height="50" fill="#f9a8d4" stroke="#ec4899" stroke-width="1" rx="5"/>
  <text x="495" y="460" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#be185d">Email Automation</text>
  <text x="495" y="475" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" fill="#be185d">SMTP Integration</text>
  
  <rect x="590" y="440" width="150" height="50" fill="#f9a8d4" stroke="#ec4899" stroke-width="1" rx="5"/>
  <text x="665" y="460" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#be185d">Gemini AI</text>
  <text x="665" y="475" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" fill="#be185d">Data Generation</text>
  
  <!-- Arrows -->
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#64748b"/>
    </marker>
  </defs>
  
  <!-- Frontend to API -->
  <line x1="400" y1="140" x2="400" y2="160" stroke="#64748b" stroke-width="2" marker-end="url(#arrowhead)"/>
  
  <!-- API to Python -->
  <line x1="400" y1="240" x2="400" y2="260" stroke="#64748b" stroke-width="2" marker-end="url(#arrowhead)"/>
  
  <!-- Python to Modules -->
  <line x1="400" y1="380" x2="400" y2="400" stroke="#64748b" stroke-width="2" marker-end="url(#arrowhead)"/>
  
  <!-- External Services -->
  <rect x="650" y="520" width="120" height="60" fill="#e0e7ff" stroke="#6366f1" stroke-width="2" rx="5"/>
  <text x="710" y="540" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="#4338ca">External Services</text>
  <text x="710" y="555" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" fill="#4338ca">• TREC Website</text>
  <text x="710" y="570" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" fill="#4338ca">• Gmail SMTP</text>
  
  <!-- Arrow to External Services -->
  <line x1="400" y1="500" x2="710" y2="520" stroke="#6366f1" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- Node.js 16+
- Google Chrome browser
- Google Gemini AI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/buddhiaitech/buddhisys.git
   cd buddhisys
   ```

2. **Set up Python environment**
   ```bash
   # Create virtual environment
   python -m venv .venv
   
   # Activate virtual environment
   # Windows:
   .venv\Scripts\activate
   # Linux/Mac:
   source .venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file
   echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
   echo "GMAIL_EMAIL=your_email@gmail.com" >> .env
   echo "GMAIL_PASSWORD=your_app_password" >> .env
   ```

4. **Set up React frontend**
   ```bash
   cd web
   npm install
   ```

### Running the Application

1. **Start the FastAPI backend**
   ```bash
   python -m uvicorn server:app --host 127.0.0.1 --port 8000 --reload
   ```

2. **Start the React frontend**
   ```bash
   cd web
   npm run dev
   ```

3. **Access the application**
   - Web Interface: http://localhost:5173
   - API Documentation: http://localhost:8000/docs

## 📋 Available Workflows

### 1. Final Complete Workflow
- **Purpose**: End-to-end automation with email sending
- **Process**: Visit TREC website → Fill PDF with AI data → Send email
- **Features**: Fills ALL form fields, generates realistic data, sends completed PDF

### 2. Fill and Send Workflow
- **Purpose**: PDF-focused automation
- **Process**: Fill actual TREC form → Visit website → Send email
- **Features**: Uses real PDF file, AI-powered field mapping

### 3. Partial Workflow
- **Purpose**: Testing and development
- **Process**: Visit website → Fill PDF (no email)
- **Features**: Quick testing without email sending

## 🎛️ Web Interface Features

### Control Panel
- **Workflow Management**: Start, stop, and reset automation workflows
- **Real-time Monitoring**: Live progress bars and status updates
- **Log Streaming**: Real-time log display with filtering
- **Process Control**: View running processes and their PIDs

### Console
- **Linux Monitor**: NoVNC connection to Linux VPS
- **Windows VPS**: NoVNC connection to Windows server
- **Remote Desktop**: Visual monitoring of automation execution
- **Scalable Interface**: Adjustable viewport size and zoom

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/workflows` | GET | List all running workflows |
| `/workflows/start` | POST | Start a new workflow |
| `/workflows/stop` | POST | Stop a running workflow |
| `/workflows/status/{pid}` | GET | Get workflow status and logs |

### Example API Usage

```bash
# Start a workflow
curl -X POST "http://localhost:8000/workflows/start" \
  -H "Content-Type: application/json" \
  -d '{"workflow_id": "final-complete", "script_path": "final_complete_workflow.py"}'

# Check status
curl "http://localhost:8000/workflows/status/12345"

# Stop workflow
curl -X POST "http://localhost:8000/workflows/stop" \
  -H "Content-Type: application/json" \
  -d '{"pid": 12345}'
```

## 🏗️ Project Structure

```
buddhisys/
├── web/                          # React frontend
│   ├── src/
│   │   ├── components/          # Reusable UI components
│   │   ├── pages/              # Main application pages
│   │   │   ├── ControlPanel.tsx # Workflow management
│   │   │   └── Console.tsx     # NoVNC monitoring
│   │   └── services/           # API service layer
│   └── package.json
├── modules/                     # Python automation modules
│   ├── browser_automation.py   # Selenium WebDriver wrapper
│   ├── pdf_processor.py        # PDF form filling with AI
│   └── email_automation.py     # Email sending functionality
├── logs/                       # Execution logs
├── server.py                   # FastAPI backend server
├── final_complete_workflow.py  # Complete automation workflow
├── fill_and_send_workflow.py   # PDF-focused workflow
├── run_partial.py             # Testing workflow
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🤖 AI Integration

The system uses Google Gemini AI for intelligent data generation:

- **Realistic Data**: Generates contextually appropriate form data
- **Field Mapping**: Automatically maps AI data to PDF form fields
- **Type Detection**: Handles different field types (text, signatures, dates)
- **Fallback Logic**: Graceful handling of AI API failures

## 🔒 Security Features

- **Environment Variables**: Sensitive data stored in environment variables
- **CORS Protection**: Configured CORS for secure API access
- **Process Isolation**: Each workflow runs in isolated subprocess
- **Log Sanitization**: Sensitive data filtered from logs

## 🚀 Deployment

### Local Development
```bash
# Terminal 1: Backend
python -m uvicorn server:app --host 127.0.0.1 --port 8000 --reload

# Terminal 2: Frontend
cd web && npm run dev
```

### Production Deployment
```bash
# Build React app
cd web && npm run build

# Serve with production server
pip install gunicorn
gunicorn server:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 📊 Monitoring and Logging

- **Structured Logging**: JSON-formatted logs with timestamps
- **Process Tracking**: Real-time process status monitoring
- **Error Handling**: Comprehensive error logging and recovery
- **Performance Metrics**: Execution time and resource usage tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini AI** for intelligent data generation
- **Selenium** for web automation capabilities
- **React** for the modern web interface
- **FastAPI** for the robust API backend
- **PyMuPDF** for PDF processing

## 📞 Support

For support, email support@buddhiaitech.com or create an issue in the GitHub repository.

---

<div align="center">

**Made with ❤️ by [BuddhiAI Tech](https://github.com/buddhiaitech)**

[![GitHub](https://img.shields.io/badge/GitHub-buddhiaitech-black?style=for-the-badge&logo=github)](https://github.com/buddhiaitech)
[![Website](https://img.shields.io/badge/Website-buddhiaitech.com-blue?style=for-the-badge)](https://buddhiaitech.com)

</div>
