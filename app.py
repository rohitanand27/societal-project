from flask import Flask, request, jsonify
from pyresparser import ResumeParser
import os
import openai

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# OpenAI API Key (Replace with your own)
openai.api_key = "YOUR_OPENAI_API_KEY"

# Job Recommendations based on extracted skills
def get_job_recommendations(skills):
    job_roles = {
        "Python": ["Software Engineer", "Data Scientist", "AI Engineer"],
        "Machine Learning": ["ML Engineer", "AI Researcher", "Data Scientist"],
        "Project Management": ["Product Manager", "Business Analyst"],
        "JavaScript": ["Frontend Developer", "Full Stack Developer"]
    }
    
    recommended_jobs = set()
    for skill in skills:
        if skill in job_roles:
            recommended_jobs.update(job_roles[skill])
    
    return list(recommended_jobs) if recommended_jobs else ["General IT Jobs"]

# AI Chatbot for Career Guidance
def chat_with_ai(user_query):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_query}]
    )
    return response["choices"][0]["message"]["content"]

@app.route('/upload', methods=['POST'])
def upload_resume():
    file = request.files['file']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        data = ResumeParser(file_path).get_extracted_data()
        data["recommended_jobs"] = get_job_recommendations(data.get("skills", []))
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = request.json.get("query")
    if not user_input:
        return jsonify({"error": "Empty query"}), 400
    
    response = chat_with_ai(user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
