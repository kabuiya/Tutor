[![CircleCI](https://dl.circleci.com/status-badge/img/gh/kabuiya/Tutor/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/kabuiya/Tutor/tree/main)
[![Coverage Status](https://coveralls.io/repos/github/kabuiya/tutor/badge.svg?branch=circleci-project-setup)](https://coveralls.io/github/kabuiya/tutor?branch=circleci-project-setup)
# `AI Tutor - CBC Curriculum Assistant`

```markdown
## `📚 AI Tutor - A Chatbot for Kenyan CBC Syllabus`

`AI Tutor is an AI-powered chatbot designed to help students in Kenya by providing subject-specific tutoring based on the **Competency-Based Curriculum (CBC)**. It integrates OpenRouter AI models for intelligent responses and includes **voice synthesis** for auditory learning.`

## `🚀 Features`

- `📖 CBC Syllabus-Based Answers: AI generates responses strictly based on the Kenyan curriculum.`
- `🔄 WebSockets for Instant Responses: Faster communication with the AI.`
- `🔊 Voice Output: Users can listen to the AI-generated answers.`
- `✅ Automated Testing & Coverage: Integrated with CircleCI and pytest-cov.`
- `🏗️ Continuous Integration: Ensures stable builds before deployment.`

## `🛠️ Installation & Setup`

Follow these steps to set up the AI Tutor application.

### `1️⃣ Clone the Repository`

git clone https://github.com/your-username/ai-tutor.git
cd ai-tutor

### `2️⃣ Create a Virtual Environment`

python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows

### `3️⃣ Install Dependencies`
pip install -r requirements.txt
### `4️⃣ Set Environment Variables`
echo "OPENAI_API_KEY=your_openrouter_api_key" > .env


## `🔥 Running the Application`

### `1️⃣ Start the Flask Backend`

python app.py
## `🧪 Running Tests & Generating Coverage Reports`

Run automated tests and check code coverage.

 ### `1️⃣ Run Unit Tests`
pytest
## `📈 Continuous Integration (CI) with CircleCI`

### `1️⃣ Create a .circleci/config.yml File`
version: 2.1
jobs:
  test:
    docker:
      - image: python:3.10
    steps:
      - checkout
      - run:
          name: Install Dependencies
          command: pip install -r requirements.txt
      - run:
          name: Run Tests
          command: pytest --cov=app --cov-report=xml
      - run:
          name: Upload Coverage
          command: bash <(curl -s https://codecov.io/bash)
workflows:
  version: 2
  test:
    jobs:
      - test








