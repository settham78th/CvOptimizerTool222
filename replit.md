# CV Generator Application

## Overview
This is an AI-powered CV Generator application built with Flask. The application allows users to input their personal information, education, experience, and skills, and then generates a professional CV using AI language models via OpenRouter API. The application focuses on ethical CV generation that avoids fabricating information.

## User Preferences
Preferred communication style: Simple, everyday language.

## System Architecture
The application follows a simple web application architecture with the following components:

1. **Frontend**: HTML templates using Bootstrap for responsive UI design
2. **Backend**: Flask web framework for routing and request handling
3. **AI Integration**: OpenAI/OpenRouter API for generating CV content
4. **PDF Handling**: Utilities for extracting text from uploaded PDF files

The application doesn't currently use a database but has placeholder files for future database implementation. The architecture prioritizes simplicity and focuses on the core functionality of CV generation using prompt engineering.

## Key Components

### 1. Web Server
- **Flask Application** (`app.py`, `main.py`): Handles HTTP requests, form submissions, and renders templates
- **Gunicorn**: Production WSGI server for deployment

### 2. CV Generation
- **CV Generator** (`cv_generator.py`): Core component that interfaces with AI models to generate CV content
- **OpenRouter Integration** (`utils/openrouter_api.py`): Handles communication with the OpenRouter API

### 3. Data Processing
- **PDF Extraction** (`utils/pdf_extraction.py`): Extracts text from uploaded PDF files using PDFMiner

### 4. User Interface
- **Templates** (`templates/`): HTML templates for the application's pages
  - `base.html`: Base template with common layout elements
  - `index.html`: Main form for CV generation
  - `cv.html`: Display template for the generated CV
- **Static Assets** (`static/`): CSS and JavaScript files for frontend functionality

## Data Flow

1. **User Input**: Users enter personal information through the web form (`index.html`)
2. **Form Submission**: Data is sent to the `/generate` endpoint
3. **AI Processing**: The application sends user data to the CV generator, which uses OpenRouter API to create professional CV content
4. **Result Display**: The generated CV is stored in the session and rendered using the `cv.html` template

For PDF processing:
1. User uploads a PDF file
2. The application extracts text using PDFMiner
3. The extracted text is used as input for AI processing

## External Dependencies

### Primary Dependencies
- **Flask**: Web framework for the application
- **OpenAI/OpenRouter**: AI service for generating CV content
- **PDFMiner**: For PDF text extraction
- **Bootstrap**: Frontend framework for responsive design
- **Gunicorn**: WSGI server for deployment

### API Dependencies
- **OpenRouter API**: Requires an API key stored in the `OPENROUTER_API_KEY` environment variable

## Deployment Strategy

The application is configured for deployment on Replit with the following characteristics:

1. **Environment**: Python 3.11 with required dependencies installed via pip
2. **Server**: Gunicorn WSGI server binding to port 5000
3. **Port Configuration**: Local port 5000 mapped to external port 80
4. **Dependencies Management**: Dependencies are defined in `pyproject.toml`

### Runtime Configuration
- The application uses Gunicorn as the WSGI server with live-reloading enabled
- Environment variables (particularly `OPENROUTER_API_KEY` and `SESSION_SECRET`) should be configured in the Replit environment

### Future Expansion
- The codebase includes placeholders for database models (`models.py`) which could be implemented for saving CVs and user accounts
- The application could be expanded to include user authentication, saved CV templates, and more advanced CV editing features