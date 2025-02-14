import time
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from flask_socketio import SocketIO

start_time = time.time()
# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])  # Enable CORS for frontend requests
socketio = SocketIO(app, cors_allowed_origins="*")  # Enable WebSockets (optional)

# OpenAI API Key
openai.api_base = "https://openrouter.ai/api/v1"
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

# Subject categories
SUBJECTS_JSS = ["Math", "Science", "Social Studies"]
SUBJECTS_SSS = ["Mathematics", "Physics", "Biology", "Chemistry", "computer studies", "geography", "business education"]


def generate_prompt(subject, grade, user_query):
    """Creates a structured prompt to keep AI responses relevant to the subject, ensuring alignment with the Kenyan
    CBC syllabus."""

    return f"""
    You are an AI tutor specializing in the Kenyan CBC syllabus.
    Your sole focus is tutoring {subject} for students at the {grade} level.

    Instructions: - Before answering, consult relevant sources (such as the current Kenyan CBC syllabus for the 
    specified {grade}) to ensure accuracy and alignment with the curriculum. 
    - Only provide answers based on the 
    content that is present in the Kenyan CBC syllabus for the specified {grade} and {subject} level. - If the answer requires more 
    in-depth information, search for syllabus-based content from reliable sources, ensuring that the information is 
    factual and aligns with the curriculum. - Responses should be focused and directly answer the user's query 
    without irrelevant content or straying from the syllabus. - If the question is unrelated to {subject}, 
    politely inform the user and suggest examples of related topics. For example: [Insert CBC topics for the subject 
    here].
    - strictly don't include irrelevant content in the answer, just give the answer directly.
    - Provide clear, concise, and structured explanations tailored for students at the {grade} level but don't have 
    to mentioned the grade. - For Math, present step-by-step solutions without using unnecessary words. Show the 
    formula first (if applicable) and proceed with step-by-step calculations. - If multiple methods are available to 
    solve a Math problem, provide each method with detailed steps.
    - NB:Do not mention the words 'Kenyan CBC syllabus' in responses, just give the answer directly.
    
    Now, please answer this question: {user_query}
    """


@app.route('/api/ai-tutor', methods=['POST'])
def ai_tutor():
    data = request.json
    category = data.get('category', '')
    subject = data.get('subject', '')
    query = data.get('query', '')

    # Validate category
    if category not in ["JSS", "SSS"]:
        return jsonify({"error": "Invalid category. Choose JSS or SSS"}), 400

    # Validate subject
    valid_subjects = SUBJECTS_JSS if category == "JSS" else SUBJECTS_SSS
    if subject not in valid_subjects or query == '':
        return jsonify({"error": f"Invalid subject for {category}. Available subjects: {valid_subjects} or invalid "
                                 f"question"}), 400

    prompt = generate_prompt(subject, category, query)
    try:
        response = openai.ChatCompletion.create(
            model="mistralai/mistral-7b-instruct",  # Use free-tier model
            messages=[{"role": "system", "content": prompt}],
            max_token=200,
            temperature=0
        )
        answer = response['choices'][0]['message']['content']
        elapsed_time = time.time() - start_time
        print(f"OpenRouter call took {elapsed_time} seconds")
        print('answer', answer)
        return jsonify(
            {"result": answer, "explanation": f"This explanation follows the Kenyan CBC syllabus for {subject}."}
        )
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": f"OpenAI Error: {str(e)}"}), 500


# WebSocket Test Route (Optional)
@socketio.on('connect')
def handle_connect():
    print("Client connected")
    socketio.emit('message', {'data': 'Connected to AI Tutor WebSocket'})


if __name__ == '__main__':
    socketio.run(app, debug=True)
