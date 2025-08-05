import streamlit as st
import PyPDF2
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from io import BytesIO


predefined_skills = [
    'python', 'java', 'sql', 'excel', 'machine learning',
    'django', 'html', 'css', 'flask', 'pandas', 'numpy', 'communication'
]

job_roles = {
    "Python Developer": ['python', 'flask', 'django', 'pandas'],
    "Data Analyst": ['python', 'sql', 'excel', 'pandas', 'communication'],
    "Web Developer": ['html', 'css', 'javascript', 'django'],
}

learning_links = {
    'flask': 'https://www.youtube.com/watch?v=Z1RJmh_OqeA',
    'django': 'https://www.youtube.com/watch?v=F5mRW0jo-U4',
    'sql': 'https://www.youtube.com/watch?v=27axs9dO7AE',
    'excel': 'https://www.youtube.com/watch?v=8v9efx8f3tY',
    'communication': 'https://www.youtube.com/watch?v=3vC5TsSyNjU',
    'html': 'https://www.youtube.com/watch?v=UB1O30fR-EE',
    'css': 'https://www.youtube.com/watch?v=yfoY53QXEnI',
    'pandas': 'https://www.youtube.com/watch?v=vmEHCJofslg',
}



def extract_text_from_pdf(uploaded_file):
    text = ""
    pdf = PyPDF2.PdfReader(uploaded_file)
    for page in pdf.pages:
        text += page.extract_text()
    return text

def extract_skills(text):
    text = text.lower()
    return [skill for skill in predefined_skills if skill in text]

def suggest_job_role(user_skills):
    best_match = ""
    highest_match_count = 0
    missing_skills = []

    for role, required_skills in job_roles.items():
        match_count = len(set(user_skills) & set(required_skills))
        if match_count > highest_match_count:
            highest_match_count = match_count
            best_match = role
            missing_skills = list(set(required_skills) - set(user_skills))

    return best_match, highest_match_count, missing_skills

def generate_pdf(result_text):
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    text_object = c.beginText(40, 800)
    text_object.setFont("Helvetica", 12)
    for line in result_text.split('\n'):
        text_object.textLine(line)
    c.drawText(text_object)
    c.save()
    buffer.seek(0)
    return buffer


st.set_page_config(page_title="Smart Resume Analyzer", layout="centered")
st.title("📄 Smart Resume Analyzer")
st.write("Upload your resume (PDF), and we'll analyze your skills and suggest a job role.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    with st.spinner("Analyzing your resume..."):
        try:
            resume_text = extract_text_from_pdf(uploaded_file)
            skills = extract_skills(resume_text)
            suggested_role, match_score, missing_skills = suggest_job_role(skills)

            st.success("✅ Resume Analyzed Successfully!")
            st.subheader("🎯 Skills Found:")
            st.write(", ".join(skills))

            st.subheader("💼 Suggested Job Role:")
            st.write(f"**{suggested_role}**")

            st.subheader("⭐ Skill Match Score:")
            st.write(f"{match_score} matched skills")

            st.subheader("❌ Missing Skills:")
            if missing_skills:
                for skill in missing_skills:
                    link = learning_links.get(skill, "Search on YouTube")
                    st.markdown(f"- {skill.title()}: [Learn here]({link})")
            else:
                st.write("None! Great job!")

           
            st.subheader("📊 Skill Match Chart")
            fig, ax = plt.subplots()
            ax.bar(["Matched", "Missing"], [match_score, len(missing_skills)], color=["green", "red"])
            ax.set_ylabel("Number of Skills")
            ax.set_title("Skill Match Overview")
            st.pyplot(fig)

          
            st.subheader("📥 Download Analysis Report")

            full_report = f"""
Resume Analyzed Successfully!

Skills Found: {skills}
Best Job Match: {suggested_role}
Skill Match Score: {match_score}
Missing Skills: {missing_skills}
"""

            pdf_file = generate_pdf(full_report)
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_file,
                file_name="resume_analysis_report.pdf",
                mime="application/pdf"
            )

        except Exception as e:
            st.error(f"Something went wrong: {e}")
