import re
import spacy


# Load SpaCy model
nlp = spacy.load("en_core_web_sm")


# =========================================================
# SKILLS DATABASE
# =========================================================

SKILLS = [
    "Python",
    "Java",
    "C++",
    "C",
    "JavaScript",
    "TypeScript",
    "SQL",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "Natural Language Processing",
    "NLP",
    "Computer Vision",
    "TensorFlow",
    "Keras",
    "PyTorch",
    "Scikit-learn",
    "Pandas",
    "NumPy",
    "Matplotlib",
    "Seaborn",
    "OpenCV",
    "Flask",
    "Django",
    "FastAPI",
    "Streamlit",
    "AWS",
    "Azure",
    "Google Cloud",
    "Docker",
    "Kubernetes",
    "Git",
    "GitHub",
    "Power BI",
    "Tableau",
    "Excel",
    "HTML",
    "CSS",
    "React",
    "Node.js",
    "Data Science",
    "Data Analysis",
    "Data Visualization",
    "R",
    "MATLAB"
]


# =========================================================
# EMAIL
# =========================================================

def extract_email(text):

    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'

    match = re.search(pattern, text)

    if match:
        return match.group(0)

    return None


# =========================================================
# PHONE
# =========================================================

def extract_phone(text):

    pattern = r'(?:(?:\+92|0092|0)?[\s-]?)?(?:3\d{2})[\s-]?\d{3}[\s-]?\d{4}'

    match = re.search(pattern, text)

    if match:
        return match.group(0)

    # General international/phone pattern
    pattern2 = r'\+?\d[\d\s().-]{8,}\d'

    match = re.search(pattern2, text)

    if match:
        return match.group(0).strip()

    return None


# =========================================================
# NAME
# =========================================================

def extract_name(text):

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    # Try SpaCy PERSON entities
    doc = nlp(text[:5000])

    for ent in doc.ents:

        if ent.label_ == "PERSON":

            name = ent.text.strip()

            # Avoid very long entity
            if 2 <= len(name.split()) <= 4:
                return name

    # Fallback: first reasonable line
    for line in lines[:10]:

        if (
            len(line.split()) <= 4
            and not re.search(
                r'email|phone|mobile|resume|curriculum|linkedin|github',
                line,
                re.IGNORECASE
            )
            and not any(char.isdigit() for char in line)
        ):

            return line

    return None


# =========================================================
# SKILLS
# =========================================================

def extract_skills(text):

    found_skills = []

    text_lower = text.lower()

    for skill in SKILLS:

        pattern = r'(?<!\w)' + re.escape(skill.lower()) + r'(?!\w)'

        if re.search(pattern, text_lower):

            found_skills.append(skill)

    return sorted(
        list(set(found_skills))
    )


# =========================================================
# EDUCATION
# =========================================================

def extract_education(text):

    education_keywords = [
        "Bachelor",
        "Bachelors",
        "B.Tech",
        "B.E",
        "BS",
        "B.Sc",
        "Master",
        "Masters",
        "M.Tech",
        "M.E",
        "MS",
        "M.Sc",
        "MBA",
        "PhD",
        "Ph.D",
        "Diploma",
        "Intermediate",
        "Matric"
    ]

    education = []

    lines = text.split("\n")

    for line in lines:

        line = line.strip()

        if not line:
            continue

        for keyword in education_keywords:

            if re.search(
                r'\b' + re.escape(keyword) + r'\b',
                line,
                re.IGNORECASE
            ):

                if line not in education:
                    education.append(line)

                break

    return education[:10]


# =========================================================
# EXPERIENCE
# =========================================================

def extract_experience(text):

    experience = []

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    job_titles = [
        "Data Scientist",
        "Data Analyst",
        "Machine Learning Engineer",
        "AI Engineer",
        "AI Developer",
        "Software Engineer",
        "Software Developer",
        "Python Developer",
        "Web Developer",
        "Frontend Developer",
        "Backend Developer",
        "Full Stack Developer",
        "Project Manager",
        "Business Analyst",
        "HR Manager",
        "Marketing Manager",
        "Intern",
        "Research Assistant"
    ]

    for i, line in enumerate(lines):

        for title in job_titles:

            if title.lower() in line.lower():

                company = None
                years = None

                # Look at next few lines for company/year
                nearby_text = " ".join(
                    lines[i:i + 4]
                )

                year_match = re.search(
                    r'(\d+(?:\.\d+)?)\s*(?:years?|yrs?)',
                    nearby_text,
                    re.IGNORECASE
                )

                if year_match:
                    years = float(
                        year_match.group(1)
                    )

                    if years.is_integer():
                        years = int(years)

                # Company extraction
                if i + 1 < len(lines):

                    possible_company = lines[i + 1]

                    if (
                        len(possible_company.split()) <= 8
                        and possible_company.lower()
                        != title.lower()
                    ):

                        company = possible_company

                experience.append({
                    "title": title,
                    "company": company,
                    "years": years
                })

                break

    return experience


# =========================================================
# COMPLETE PARSER
# =========================================================

def parse_resume(text):

    result = {

        "name": extract_name(text),

        "email": extract_email(text),

        "phone": extract_phone(text),

        "skills": extract_skills(text),

        "education": extract_education(text),

        "experience": extract_experience(text)

    }

    return result