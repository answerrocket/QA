# AnswerRocket Skill Builder Starter Repository

A ready-to-use starter repository for building AnswerRocket skills with Claude Code. This repository comes pre-configured with development tools, testing utilities, and deployment scripts to accelerate your skill development.

## 🚀 Quick Start

### Prerequisites

Before getting started, ensure you have:

- **Python 3.11+** - Check with `python --version`
- **Claude Code** installed and configured
- **AnswerRocket instance** with API access
- **Git** for version control

### Verify Prerequisites

```bash
# Check Python version (should be 3.11+)
python --version

# Check if you can access your AnswerRocket instance
curl -I https://your-answerrocket-instance.com

# Verify Git is installed
git --version
```

### Setup

1. **Create Virtual Environment**

   ```bash
   # Create virtual environment
   python -m venv .venv

   # Activate virtual environment
   # On macOS/Linux:
   source .venv/bin/activate
   # On Windows:
   # .venv\Scripts\activate
   ```

2. **Install Dependencies**

   ```bash
   pip install -e .
   ```

3. **Configure Environment**

   Create a `.env` file in the root directory with your AnswerRocket credentials:

   ```env
   # AnswerRocket Instance Configuration
   AR_URL=https://your-answerrocket-instance.com
   AR_TOKEN=your_api_token_here

   # Project Configuration
   COPILOT_ID=your_copilot_id
   DATASET_ID=your_default_dataset_id
   DATABASE_ID=your_default_database_id
   REPO_ID=your_repository_id
   ```

   **Where to find these values:**

   - `AR_URL`: Your AnswerRocket instance URL
   - `AR_TOKEN`: Generate in AnswerRocket → User Panel → SDK key
   - `COPILOT_ID`: Found in your AnswerRocket → Studio → Copilots
   - `DATASET_ID`: Available in AnswerRocket → Studio → Datasets
   - `DATABASE_ID`: Found in AnswerRocket → Studio → Databases
   - `REPO_ID`: Your skill repository ID in AnswerRocket

4. **Verify Setup**

   ```bash
   ./builder_utils/scripts/run-all-tests
   ```

   You should see all tests pass with green checkmarks ✅

## 📁 What's Included

```
├── builder_utils/              # Pre-built development tools
│   ├── scripts/               # Ready-to-use command utilities
│   └── tests/                 # Environment validation
├── skills.txt                  # Skill registry
├── CLAUDE.md                   # Claude Code configuration
└── pyproject.toml              # Dependencies and project config
```

## 🛠️ Built-in Development Tools

This repository comes with pre-built command-line utilities to speed up your development:

| Tool                   | Purpose                                                 | Example Usage                                                          |
| ---------------------- | ------------------------------------------------------- | ---------------------------------------------------------------------- |
| `run-python`           | Execute Python code or files                            | `./builder_utils/scripts/run-python "print('test')"`                   |
| `get-dataset-metadata` | Retrieve your dataset schema and information            | `./builder_utils/scripts/get-dataset-metadata`                         |
| `execute-sql`          | Run SQL queries against your AnswerRocket database      | `./builder_utils/scripts/execute-sql`                                  |
| `run-skill`            | Test skills locally with parameters                     | `./builder_utils/scripts/run-skill my_skill --parameters '{}'`         |
| `test-visualization`   | Test skill visualizations for errors and console issues | `./builder_utils/scripts/test-visualization skill.py func --json-only` |
| `package-skill`        | Validate and package a specific skill for deployment    | `./builder_utils/scripts/package-skill my_skill.py`                    |
| `sync-repo`            | Deploy skills to AnswerRocket                           | `./builder_utils/scripts/sync-repo`                                    |
| `run-all-tests`        | Validate your development environment                   | `./builder_utils/scripts/run-all-tests`                                |

### Detailed Tool Examples

```bash
# Test your environment
./builder_utils/scripts/run-all-tests

# Explore your data
./builder_utils/scripts/get-dataset-metadata
./builder_utils/scripts/execute-sql

# Execute Python code directly
./builder_utils/scripts/run-python "import pandas as pd; print(pd.__version__)"

# Test a skill with specific parameters
./builder_utils/scripts/run-skill my_skill --parameters '{"param1": "value1"}'

# Test skill visualizations for errors
./builder_utils/scripts/test-visualization my_skill.py my_skill_function --json-only
./builder_utils/scripts/test-visualization my_skill.py my_skill_function --full-test

# Package and validate a skill
./builder_utils/scripts/package-skill my_skill.py

# Deploy all registered skills
./builder_utils/scripts/sync-repo
```

## 💡 Key Features

### Pre-configured Environment

- **AnswerRocket SDK integration** - Ready-to-use client setup
- **Skill framework** - Latest skill-framework package with UI components
- **Testing utilities** - Pytest and Playwright for comprehensive testing
- **Data tools** - Pandas, NumPy for data manipulation

### Development Workflow Support

- **Environment validation** - Automated checks for proper setup
- **Data exploration** - Built-in tools to understand your datasets
- **Skill testing** - Local and remote testing capabilities
- **Deployment automation** - One-command deployment to AnswerRocket

### Best Practices Built-in

- **Organized file structure** - Clear separation of skills and helper files
- **Testing framework** - Comprehensive test coverage requirements
- **Version control ready** - Git integration with proper .gitignore

## 🧪 Testing Framework

This repository includes a comprehensive testing framework to validate your development environment:

### Test Categories

The testing suite covers:

- **Package imports and connections** - Validates all required packages are installed
- **AnswerRocket client functionality** - Tests API connectivity and authentication
- **Skill framework components** - Verifies skill-framework package integration
- **Visualization framework** - Tests UI component rendering capabilities
- **Helper utilities** - Validates all builder tools are working correctly

### Running Tests

```bash
# Run all environment tests
./builder_utils/scripts/run-all-tests

# Run specific test categories
python -m pytest builder_utils/tests/test_packages_and_connections.py -v
python -m pytest builder_utils/tests/test_skill_preview_example.py -v
python -m pytest builder_utils/tests/test_visualization_framework.py -v
python -m pytest builder_utils/tests/test_helper_utilities.py -v
python -m pytest builder_utils/tests/test_executor_integration.py -v
```

### Testing Skill Visualizations

The `test-visualization` tool helps debug and validate skill visualizations before deployment:

```bash
# Quick JSON validation (recommended for development)
./builder_utils/scripts/test-visualization my_skill.py my_skill_function --json-only

# Full browser test with console error detection
./builder_utils/scripts/test-visualization my_skill.py my_skill_function --full-test

# Test with parameters
./builder_utils/scripts/test-visualization dashboard.py create_dashboard --json-only --parameters '{"region": "US"}'

# Debug mode (visible browser for troubleshooting)
./builder_utils/scripts/test-visualization chart_skill.py my_chart --full-test --visible
```

**Key Features:**

- ⚡ **Fast JSON validation**: Detects JavaScript functions in JSON, missing properties, invalid structure
- 🌐 **Browser testing**: Uses skill-framework preview server to render charts and detect console errors
- 🔍 **Error detection**: Catches common visualization errors like Highcharts configuration issues
- 🧹 **Clean testing**: Uses temporary files with automatic cleanup
- 📊 **Performance metrics**: Reports page load times and response status
- ✅ **CLI compatible**: Returns proper exit codes for automated workflows

## 🤖 Claude Code Integration

This repository is specifically designed to work with Claude Code, providing an AI-powered development experience:

### How It Works

1. **CLAUDE.md Configuration** - Contains detailed instructions for Claude Code on how to:

   - Build skills using the skill-framework
   - Use the helper tools effectively
   - Follow best practices for skill development
   - Interact with specialized sub-agents

2. **Sub-Agent System** - Claude Code has access to specialized research agents:

   - `skill-framework-specialist` - Expert on skill-framework package
   - `visualization-specialist` - Expert on creating visualizations
   - `ar-sdk-specialist` - Expert on AnswerRocket SDK

3. **Automated Workflow** - Claude Code follows a structured process for skill development

### Working with Claude Code

Claude Code will automatically use the appropriate tools and follow best practices for skill development, testing, and deployment.

## 🚨 Troubleshooting

### Common Setup Issues

#### Virtual Environment Problems

```bash
# If activation fails
python -m venv --clear .venv
source .venv/bin/activate
pip install -e .
```

#### Environment Variable Issues

```bash
# Check if .env file exists and has correct values
cat .env

# Test AnswerRocket connection
./builder_utils/scripts/run-python "
from answerrocket_client import AnswerRocketClient
import os
client = AnswerRocketClient()
print('✅ Connection successful')
"
```

#### Tool Execution Issues

```bash
# Make sure scripts are executable
chmod +x builder_utils/scripts/*

# If tools fail, check virtual environment
which python
pip list | grep skill-framework
```

### Common Skill Development Issues

#### Skill Not Found Error

- Ensure skill file is in the root directory
- Check that `@skill` decorator is present
- Verify skill name matches function name

#### Parameter Errors

```bash
# Always pass parameters as JSON string
./builder_utils/scripts/run-skill skill_name --parameters '{"param1": "value1"}'

# Not like this:
./builder_utils/scripts/run-skill skill_name --parameters param1=value1
```

#### Packaging Failures

- Ensure all imports are available
- Check that skill returns `SkillOutput` object
- Verify all required parameters are defined

#### Database Connection Issues

```bash
# Test database connection
./builder_utils/scripts/execute-sql
# Follow prompts to test SQL queries
```

### Getting Help

1. **Check Test Results**: `./builder_utils/scripts/run-all-tests`
2. **Validate Environment**: Ensure all environment variables are set correctly
3. **Review Logs**: Check error messages for specific issues
4. **Ask Claude Code**: Describe your issue for automated troubleshooting

## 📚 Architecture Overview

### Repository Structure

```
├── builder_utils/           # Development tools and utilities
│   ├── scripts/            # Command-line tools
│   ├── tests/              # Environment validation tests
│   └── *.py                # Core utility modules
├── .claude/                # Claude Code research cache
├── skills.txt              # Skill registry for deployment
├── CLAUDE.md               # Claude Code configuration
├── .env.example            # Environment template
└── your_skills.py          # Your skill files go here
```

### Data Flow

1. **Development**: Create skills using skill-framework
2. **Testing**: Validate locally with run-skill tool
3. **Packaging**: Validate deployment readiness
4. **Registration**: Add to skills.txt
5. **Deployment**: Sync to AnswerRocket via Git

### Key Components

- **skill-framework**: Core skill development package
- **answerrocket-client**: API integration for data access
- **Builder Utils**: Custom tools for development workflow
- **Testing Suite**: Comprehensive validation framework

## 🔧 Dependencies Included

- **skill-framework[ui]** - Core AnswerRocket skill development with UI components
- **answerrocket-client** - API integration for data access and deployment
- **pandas & numpy** - Data manipulation and analysis
- **pytest & playwright** - Testing frameworks for comprehensive validation
- **python-dotenv** - Environment variable management

---

**Ready to build?** Run `./builder_utils/scripts/run-all-tests` to get started!
