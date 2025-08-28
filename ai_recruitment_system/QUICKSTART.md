# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Setup Environment
```bash
cd ai_recruitment_system
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API Key
```bash
cp env.example .env
# Edit .env and add your OpenAI API key
```

### 3. Run the Application
```bash
python run.py
```

### 4. Open in Browser
Navigate to `http://localhost:8501`

## 🎯 What You Can Do

1. **Select a Job**: Choose from 3 sample positions
2. **Upload CV**: Upload PDF, DOCX, or TXT files
3. **Get Instant Results**: AI evaluation with scores and feedback

## 🔧 Troubleshooting

**API Key Error**: Make sure your `.env` file contains a valid OpenAI API key
**Import Errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`
**Port Issues**: Streamlit will automatically find an available port

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check out the code structure in the `app/` directory
- Run tests with `pytest` to verify everything works
