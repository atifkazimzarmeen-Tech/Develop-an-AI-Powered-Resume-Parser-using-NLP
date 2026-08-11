# 🤖 AI-Powered Resume Parser

An AI-powered Resume Parser built using Python, NLP, Machine Learning, and Flask.

🔗 **Live Demo:** http://127.0.0.1:5000/

---

## 📌 Project Overview

The AI Resume Parser extracts structured information from resumes uploaded in PDF, DOCX, or TXT format using Natural Language Processing, Regular Expressions, and Machine Learning.

## ✨ Features

- 📄 Upload PDF, DOCX, and TXT resumes
- 👤 Extract candidate name
- 📧 Extract email address
- 📱 Extract phone number
- 🛠️ Extract skills
- 💼 Extract work experience
- 🎓 Extract education
- 🤖 Predict resume category
- 📋 Generate structured JSON output
- ⬇️ Download parsed JSON
- 🌐 Flask-based web application
- 🌙 Modern dark-themed UI

## 🧠 Technologies Used

- Python
- Flask
- NLP
- spaCy
- Scikit-learn
- TF-IDF Vectorization
- Regular Expressions
- PDFMiner
- python-docx
- Pandas
- HTML5
- CSS3
- JavaScript

## 🤖 Machine Learning

The model was trained using the `UpdatedResumeDataSet.csv` dataset.

TF-IDF Vectorization was used to convert resume text into numerical features, followed by machine learning classification.

### Model Performance

| Model | Accuracy | Precision | Recall | F1 Score |
|---|---:|---:|---:|---:|
| Logistic Regression | 85.29% | 81.13% | 85.29% | 81.58% |
| Linear SVM | 85.29% | 81.13% | 85.29% | 81.58% |
| Naive Bayes | 64.71% | 51.96% | 64.71% | 55.69% |

## 📊 Output

The system extracts structured information such as:

- Name
- Email
- Phone
- Skills
- Experience
- Education
- Resume Category
- 
## 📁 Project Structure
AI_Resume_Parser/
│
├── app.py
├── resume_parser.py
├── resume_classifier.pkl
├── tfidf_vectorizer.pkl
├── model_info.pkl
├── sample_output.json
├── requirements.txt
├── README.md
│
├── templates/
│   ├── index.html
│   └── result.html
│
├── static/
│   └── style.css
│
└── uploads/

## ⚙️ Run Locally

git clone YOUR_GITHUB_REPOSITORY_URL
cd AI_Resume_Parser

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python app.py

## 📋 Sample JSON Output

```json
{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "skills": [
        "Python",
        "Machine Learning",
        "AWS"
    ],
    "experience": [
        {
            "title": "Data Scientist",
            "company": "TechCorp",
            "years": 2
        }
    ]
}

