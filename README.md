# Agent Support System

## Setup Instructions

### Prerequisites

- Python 3.8 or higher installed on your system
- Git (optional, for version control)

### Step 1: Create a Virtual Environment

A virtual environment isolates your project dependencies from your system Python.

**On Windows (Command Prompt):**

```bash
python -m venv venv
```

**On Windows (Git Bash / PowerShell):**

```bash
python -m venv venv
```

**On macOS / Linux:**

```bash
python3 -m venv venv
```

### Step 2: Activate the Virtual Environment

**On Windows (Command Prompt):**

```bash
venv\Scripts\activate
```

**On Windows (PowerShell):**

```bash
venv\Scripts\Activate.ps1
```

**On Windows (Git Bash) / macOS / Linux:**

```bash
source venv/Scripts/activate
```

After activation, you should see `(venv)` at the beginning of your terminal prompt.

### Step 3: Install Dependencies

With the virtual environment activated, install all required packages:

```bash
pip install -r requirements.txt
```

This will install all dependencies listed in `requirements.txt`, including:

- Data processing (pandas, numpy)
- Email processing (beautifulsoup4, lxml)
- Database (psycopg2, sqlalchemy)
- ML/NLP (torch, transformers, spacy)
- LLM integration (langchain, google-genai)
- And more...

### Step 4: Configure Environment Variables

Create a `.env` file with your configuration:

```bash
cp .env.example .env
```

Edit the `.env` file and fill in your actual values:

- EMAIL: Your Gmail email address
- APP_PASSWORD: Your Gmail app password
- POSTGRESQL_CONNECTION: Your database connection string
- Other configuration as needed

**Important:** Never commit the `.env` file to version control. It's already in `.gitignore`.

### Step 5: Run the Application

Once everything is set up, you can run your application:

```bash
python main.py
```

## Deactivating the Virtual Environment

When you're done working, deactivate the virtual environment:

```bash
deactivate
```

## Troubleshooting

**Issue: `python` command not found**

- Try using `python3` instead on macOS/Linux
- Ensure Python is installed and added to your PATH

**Issue: Permission denied on activation script**

- On PowerShell: You may need to enable script execution: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

**Issue: Module not found errors**

- Make sure the virtual environment is activated (you should see `(venv)` in your prompt)
- Reinstall dependencies: `pip install -r requirements.txt`

## Project Structure

```
agent_support_system/
├── venv/                 # Virtual environment (ignored in git)
├── .env                  # Environment variables (ignored in git)
├── .env.example          # Template for environment variables
├── requirements.txt      # Python dependencies
├── settings.py           # Configuration loaded from .env
└── README.md            # This file
```
