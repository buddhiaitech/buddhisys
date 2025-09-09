# AGENTS.md - RPA Workflow Project

## Build/Test Commands
- Run main workflow: `python run_rpa.py`
- Direct execution: `python rpa_workflow.py` or `python complete_website_workflow.py`
- Install dependencies: `pip install -r requirements.txt`
- No unit tests found - system tests via full workflow execution

## Architecture & Structure
- **Main Scripts**: `complete_website_workflow.py`, `rpa_workflow.py`
- **Modules**: `/modules/` contains `browser_automation.py`, `pdf_processor.py`, `email_automation.py`
- **Configuration**: `config.json` for all settings including URLs, email, and timeouts
- **Logging**: Comprehensive logging to `/logs/` directory with timestamps

## Code Style & Conventions
- **Language**: Python 3.7+
- **Imports**: Standard library first, then third-party (selenium, webdriver-manager, etc.)
- **Classes**: PascalCase (e.g., `CompleteWebsiteWorkflow`, `RPAWorkflow`)
- **Methods**: snake_case with descriptive names (e.g., `step1_launch_browser`)
- **Docstrings**: Triple quotes with Args/Returns documentation
- **Error Handling**: Try/except blocks with logging, graceful fallbacks
- **File Paths**: Windows-style paths with backslashes, absolute paths preferred
- **Constants**: Chrome paths, selectors, timeouts defined as class attributes
