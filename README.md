# AI Recruitment System

A professional AI-powered recruitment platform that automates CV screening and candidate evaluation using advanced LangGraph workflows and OpenAI models.

## 🚀 Features

- **Intelligent CV Processing**: Extract and analyze text from PDF, DOCX, and TXT files
- **AI-Powered Evaluation**: Automated candidate assessment using OpenAI GPT models
- **Workflow Automation**: LangGraph-based decision trees for recruitment processes
- **Professional UI**: Clean, modern Streamlit interface
- **Modular Architecture**: Well-structured, maintainable codebase
- **Real-time Processing**: Instant application evaluation and feedback

## 🏗️ Architecture

The system follows a professional multi-layered architecture:

```
ai_recruitment_system/
├── app/
│   ├── core/           # Configuration and utilities
│   ├── models/         # Data models and schemas
│   ├── services/       # Business logic services
│   ├── agents/         # AI workflow and nodes
│   ├── ui/            # User interface components
│   └── main.py        # Main application entry point
├── tests/             # Unit and integration tests
├── docs/              # Documentation
├── requirements.txt   # Python dependencies
└── run.py            # Application runner
```

### Core Components

- **Models**: Data structures for job postings and application states
- **Services**: CV parsing, job management, and recruitment agent orchestration
- **Agents**: LangGraph workflow nodes for AI-powered decision making
- **UI Components**: Modular Streamlit components for better maintainability

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai_recruitment_system
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment configuration**
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-4o-mini
   ```

## 🚀 Usage

### Running the Application

```bash
# Using the entry point script
python run.py

# Or directly with Streamlit
streamlit run app/main.py
```

The application will be available at `http://localhost:8501`

### How to Use

1. **Select a Job Position**: Choose from available positions in the sidebar
2. **Upload CV**: Upload your CV in PDF, DOCX, or TXT format
3. **Submit Application**: Click "Submit Application" to process your CV
4. **View Results**: Get instant feedback including:
   - Experience level assessment
   - Skill match evaluation
   - Technical competency score
   - Interview scheduling or feedback

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-4o-mini` |

### Application Settings

Modify `app/core/config.py` to customize:
- File upload limits
- Supported file types
- UI configuration
- Model parameters

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_services.py
```

## 📊 Workflow

The recruitment process follows this AI-powered workflow:

1. **CV Text Extraction**: Parse uploaded documents
2. **Candidate Information Extraction**: Extract name and basic info
3. **Experience Categorization**: Classify as Entry/Mid/Senior level
4. **Skill Assessment**: Evaluate match with job requirements
5. **Technical Evaluation**: Score technical competency (1-10)
6. **Decision Routing**: 
   - Score ≥ 7: Schedule interview
   - Senior level + Score ≥ 6: Escalate to recruiter
   - Otherwise: Reject with feedback

## 🔒 Security & Privacy

- All file processing is done locally
- No CV data is stored permanently
- OpenAI API calls are made securely
- Environment variables protect API keys

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add type hints to all functions
- Write comprehensive docstrings
- Include unit tests for new features
- Update documentation as needed


## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation in the `docs/` folder
- Review the code comments for implementation details

## 🔮 Roadmap

- [ ] Database integration for job postings
- [ ] User authentication and profiles
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] API endpoints for external integration
- [ ] Batch processing capabilities
- [ ] Custom workflow configuration

## 🙏 Acknowledgments

- OpenAI for providing the GPT models
- LangChain and LangGraph for workflow orchestration
- Streamlit for the web interface framework
- The open-source community for various dependencies


