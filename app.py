#app.py

import streamlit as st
import pandas as pd
from engine.recommendation_engine import (
    get_streams_by_board,
    get_subject_combinations,
    get_course_categories,
    recommend_courses,
    courses as COURSE_DATA
)
from fpdf import FPDF

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Career Guidance System", layout="centered")

st.markdown("""
<style>
.title { font-size:32px; font-weight:bold; color:#1F618D; text-align:center; }
.section { font-size:22px; font-weight:bold; margin-top:25px; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>Career Recommendation System</div>", unsafe_allow_html=True)

# ---------------- COURSE DESCRIPTION MAP ----------------
COURSE_DETAILS = {
    "MBBS": "Professional medical degree to become a licensed doctor.",
    "BDS": "Dental science program focused on oral health and dentistry.",
    "BAMS": "Medical degree based on Ayurvedic treatment and traditional medicine.",
    "BHMS": "Medical program focused on homeopathic systems of treatment.",
    "B.Sc Nursing": "Healthcare program focused on patient care and clinical practice.",
    "B.Pharm": "Pharmacy degree dealing with medicines and drug development.",

    "B.Sc Biotechnology": "Study of biological processes used in healthcare, agriculture, and research.",
    "B.Sc Microbiology": "Focuses on microorganisms and their role in health, environment, and industry.",
    "B.Sc Research": "Research-oriented science program preparing for higher studies and innovation.",

    "B.Tech": "Engineering degree covering applied technology and problem-solving skills.",
    "BE": "Engineering program focused on core technical and practical skills.",

    "BCA": "Computer applications program focused on software development and IT systems.",
    "B.Sc Computer Science": "Core computer science degree covering programming and system design.",
    "Data Science": "Focuses on data analysis, statistics, and machine learning.",
    "AI & ML": "Specialization in artificial intelligence and machine learning technologies.",
    "Cyber Security": "Focuses on protecting systems, networks, and digital information.",

    "B.Com": "Commerce degree covering accounting, finance, and business fundamentals.",
    "CA": "Professional course in accounting, taxation, and auditing.",
    "CMA": "Cost and management accounting program for financial decision-making.",
    "BBA": "Business administration program focusing on management and leadership skills.",
    "BBM": "Business management degree with practical business exposure.",
    "BMS": "Management program focused on organizational and business operations.",

    "BA Economics": "Study of economic systems, markets, and financial policies.",
    "B.Sc Statistics": "Program focused on data analysis, probability, and statistical methods.",

    "Fashion Design": "Creative program focused on clothing, textiles, and fashion industry.",
    "Graphic Design": "Design program focusing on visual communication and digital creativity.",
    "Journalism": "Program focused on media, reporting, and communication skills.",
    "Mass Communication": "Study of media platforms, advertising, and public communication.",
    "BFA": "Fine arts program focusing on creative and visual art forms."
}

def get_course_detail(course_name):
    return COURSE_DETAILS.get(
        course_name,
        "Undergraduate program offering strong career opportunities in this field."
    )

# ---------------- STUDENT NAME ----------------
name = st.text_input("Enter your name")
if not name:
    st.stop()

# ---------------- EDUCATION BOARD ----------------
board = st.selectbox("Select Education Board", ["CBSE", "ICSE", "State Board"])

# ---------------- STREAM ----------------
stream = st.selectbox("Select Stream", get_streams_by_board(board))

# ---------------- SUBJECT COMBINATION ----------------
st.markdown("<div class='section'>Select Subject Combination</div>", unsafe_allow_html=True)
subject_combo = st.radio(
    "Available subject combinations",
    get_subject_combinations(stream)
)

# ---------------- AVAILABLE COURSES ----------------
st.markdown("<div class='section'>Available Courses</div>", unsafe_allow_html=True)

categories = get_course_categories(subject_combo)
rows = []

for category in categories:
    for course in COURSE_DATA.get(category, []):
        rows.append({
            "Course Category": category,
            "Course Name": course
        })

st.table(pd.DataFrame(rows))

# ---------------- EXPECTED MARKS ----------------
marks = st.slider("Expected Percentage", 40, 100, step=5)

# ---------------- RESULTS ----------------
if st.button("Show Career Results"):

    results = recommend_courses(subject_combo, marks)
    alternate = list(set(results["safe_options"] + results["backup_options"]))

    st.markdown("<div class='section'>Career Recommendation</div>", unsafe_allow_html=True)
    st.write(
        f"Based on your academic profile, you are well suited for "
        f"{', '.join(categories)}-related courses."
    )

    # ---------------- RECOMMENDED COURSES TABLE ----------------
    st.subheader("Recommended Courses")

    if results["best_fit"]:
        df_rec = pd.DataFrame([
            {
                "S.No": i + 1,
                "Course Name": c,
                "Course Details": get_course_detail(c)
            }
            for i, c in enumerate(results["best_fit"])
        ])
        st.table(df_rec)
    else:
        st.info("No courses meet this score range.")

    # ---------------- ALTERNATE CAREER OPTIONS TABLE ----------------
    st.subheader("Alternate Career Options")

    if alternate:
        df_alt = pd.DataFrame([
            {
                "S.No": i + 1,
                "Course Name": c,
                "Course Details": get_course_detail(c)
            }
            for i, c in enumerate(alternate)
        ])
        st.table(df_alt)
    else:
        st.info("No alternate career options available.")

    # ---------------- PDF GENERATION ----------------
    def clean(text):
        return text.encode("latin-1", "ignore").decode("latin-1")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, clean("Career Recommendation Report"), ln=True, align="C")
    pdf.ln(5)

    pdf.cell(0, 8, clean(f"Name: {name}"), ln=True)
    pdf.cell(0, 8, clean(f"Board: {board}"), ln=True)
    pdf.cell(0, 8, clean(f"Stream: {stream}"), ln=True)
    pdf.cell(0, 8, clean(f"Subject Combination: {subject_combo}"), ln=True)
    pdf.cell(0, 8, clean(f"Expected Marks: {marks}%"), ln=True)
    pdf.ln(5)

    pdf.cell(0, 8, clean("Recommended Courses"), ln=True)
    for c in results["best_fit"]:
        pdf.cell(0, 8, clean(f"- {c}: {get_course_detail(c)}"), ln=True)

    pdf.ln(3)
    pdf.cell(0, 8, clean("Alternate Career Options"), ln=True)
    for c in alternate:
        pdf.cell(0, 8, clean(f"- {c}: {get_course_detail(c)}"), ln=True)

    file_name = f"{name}_Career_Recommendation_Report.pdf"
    pdf.output(file_name)

    st.download_button(
        "Download Career Recommendation Report (PDF)",
        data=open(file_name, "rb").read(),
        file_name=file_name,
        mime="application/pdf"
    )
