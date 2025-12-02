# Flask Application

A simple Python Flask web application. Production env of fuzzy

## Project Structure

```
.
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .venv/                 # Virtual environment (not in git)
└── README.md             # This file
```

## Setup Instructions

### 1. Create Virtual Environment

```powershell
python -m venv .venv
```

### 2. Activate Virtual Environment

**On Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
.venv\Scripts\activate.bat
```

**On macOS/Linux:**
```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

## Running the Application

Once the virtual environment is activated and dependencies are installed:

```powershell
python app.py
```

The application will start on `http://localhost:5000`

## API Endpoints

- `GET /` - Returns a welcome message
- `GET /health` - Health check endpoint

## Deactivating Virtual Environment

To deactivate the virtual environment:

```powershell
deactivate
```

## Dependencies

- **Flask** - Web framework
- **Werkzeug** - WSGI utilities library (Flask dependency)
