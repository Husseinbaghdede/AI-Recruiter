import os

project_structure = {
    "ai_recruitment_system": {
        "app": {
            "__init__.py": "",
            "main.py": "# Main Streamlit application\n",
            "core": {
                "__init__.py": "",
                "config.py": "# Configuration management\n",
                "exceptions.py": "# Custom exceptions\n",
            },
            "models": {
                "__init__.py": "",
                "job_posting.py": "# Job posting data model\n",
                "application_state.py": "# Agent state model\n",
            },
            "services": {
                "__init__.py": "",
                "cv_parser.py": "# CV parsing service\n",
                "recruitment_agent.py": "# Main agent service\n",
                "job_service.py": "# Job management service\n",
            },
            "agents": {
                "__init__.py": "",
                "nodes.py": "# Workflow nodes\n",
                "workflow.py": "# LangGraph workflow\n",
            },
            "ui": {
                "__init__.py": "",
                "components": {
                    "__init__.py": "",
                    "job_display.py": "# Job display components\n",
                    "file_upload.py": "# CV upload components\n",
                    "results_display.py": "# Results display\n",
                },
            },
        },
        "requirements.txt": "",
        ".env": "",
        "README.md": "# AI Recruitment System\n",
    }
}


def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)


if __name__ == "__main__":
    create_structure(".", project_structure)
    print("✅ Project structure created successfully.")
