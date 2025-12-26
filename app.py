#app.py 
import streamlit as st
import pandas as pd
from fpdf import FPDF
from engine.recommendation_engine import (
    get_streams_by_board,
    get_subject_combinations,
    get_course_categories,
    recommend_courses,
    courses as COURSE_DATA
)

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="Career Guidance System",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ======================================================
# STYLES (TECH + PROFESSIONAL)
# ======================================================
st.markdown("""
<style>
body { background-color:#F6F8FB; }

.hero {
    background: linear-gradient(135deg, #0F2027, #203A43, #2C5364);
    padding: 42px;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-bottom: 34px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.25);
}

.hero h1 {
    font-size: 44px;
    font-weight: 900;
}

.hero p {
    font-size: 15px;
    opacity: 0.9;
}

.card {
    background: #FFFFFF;
    padding: 28px;
    border-radius: 18px;
    box-shadow: 0 10px 26px rgba(0,0,0,0.08);
    margin-bottom: 30px;
}

.section-title {
    font-size: 22px;
    font-weight: 800;
    color: #0B5ED7;
    margin-bottom: 16px;
}

.kpi-card {
    background: linear-gradient(135deg, #FFFFFF, #F1F4F9);
    padding: 24px;
    border-radius: 16px;
    text-align: center;
    box-shadow: inset 0 0 0 1px #E0E6ED;
}

.kpi-value {
    font-size: 30px;
    font-weight: 900;
    color: #0B5ED7;
}

.kpi-label {
    font-size: 12px;
    color: #555;
    letter-spacing: 0.6px;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# HERO
# ======================================================
st.markdown("""
<div class="hero">
    <h1>🎓 Career Recommendation System</h1>
    <p>Professional, data-driven academic guidance after 12th</p>
</div>
""", unsafe_allow_html=True)

# ======================================================
# STUDENT PROFILE
# ======================================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>👤 Student Profile</div>", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    name = st.text_input("Student Name", placeholder="Enter full name")
with c2:
    board = st.selectbox("Education Board", ["CBSE", "ICSE", "State Board"])

st.markdown("</div>", unsafe_allow_html=True)

if not name:
    st.info("Please enter student name to proceed.")
    st.stop()

# ======================================================
# ACADEMIC BACKGROUND
# ======================================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>📘 Academic Background</div>", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    stream = st.selectbox("Stream", get_streams_by_board(board))
with c2:
    subject_combo = st.selectbox("Subject Combination", get_subject_combinations(stream))

st.markdown("</div>", unsafe_allow_html=True)

# ======================================================
# AVAILABLE COURSES
# ======================================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>📚 Eligible Course Landscape</div>", unsafe_allow_html=True)

categories = get_course_categories(subject_combo)
available_rows = [
    {"Category": cat, "Course Name": c}
    for cat in categories
    for c in COURSE_DATA.get(cat, [])
]

st.dataframe(
    pd.DataFrame(available_rows),
    hide_index=True,
    width="stretch"
)
st.markdown("</div>", unsafe_allow_html=True)

# ======================================================
# EXPECTED MARKS
# ======================================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>📊 Expected Performance</div>", unsafe_allow_html=True)

marks = st.slider("Expected Percentage", 40, 100, step=5)
st.markdown("</div>", unsafe_allow_html=True)

# ======================================================
# RESULTS
# ======================================================
if st.button("🎯 Generate Career Insights", width="stretch"):

    results = recommend_courses(subject_combo, marks)
    alternate = list(set(results["safe_options"] + results["backup_options"]))

    # ---------------- KPI CARDS ----------------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)

    k1.markdown(f"<div class='kpi-card'><div class='kpi-value'>{marks}%</div><div class='kpi-label'>EXPECTED SCORE</div></div>", unsafe_allow_html=True)
    k2.markdown(f"<div class='kpi-card'><div class='kpi-value'>{stream}</div><div class='kpi-label'>STREAM</div></div>", unsafe_allow_html=True)
    k3.markdown(f"<div class='kpi-card'><div class='kpi-value'>{len(categories)}</div><div class='kpi-label'>CAREER DOMAINS</div></div>", unsafe_allow_html=True)
    k4.markdown(f"<div class='kpi-card'><div class='kpi-value'>{len(results['best_fit'])}</div><div class='kpi-label'>BEST FIT COURSES</div></div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- INSIGHT ----------------
    st.success(
        f"Based on your academic profile and an expected score of {marks}%, "
        f"you are strongly aligned with career paths in {', '.join(categories)}."
    )

    # ---------------- RESULT TABLES ----------------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>✅ Recommended Courses</div>", unsafe_allow_html=True)

        rec_df = pd.DataFrame({
            "S.No": range(1, len(results["best_fit"]) + 1),
            "Course Name": results["best_fit"]
        })

        st.dataframe(
            rec_df,
            hide_index=True,
            width="stretch",
            column_config={
                "S.No": st.column_config.NumberColumn("S.No", width="small"),
                "Course Name": st.column_config.TextColumn("Course Name", width="large")
            }
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>🔁 Alternate Career Options</div>", unsafe_allow_html=True)

        alt_df = pd.DataFrame({
            "S.No": range(1, len(alternate) + 1),
            "Course Name": alternate
        })

        st.dataframe(
            alt_df,
            hide_index=True,
            width="stretch",
            column_config={
                "S.No": st.column_config.NumberColumn("S.No", width="small"),
                "Course Name": st.column_config.TextColumn("Course Name", width="large")
            }
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # ======================================================
    # PROFESSIONAL PDF REPORT (TABLE-BASED)
    # ======================================================
    def clean(txt):
        return txt.encode("latin-1", "ignore").decode("latin-1")

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 12, clean("Career Recommendation Report"), ln=True, align="C")
    pdf.ln(6)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, clean("Student Profile"), ln=True)

    pdf.set_font("Arial", size=11)
    profile = [
        ("Student Name", name),
        ("Board", board),
        ("Stream", stream),
        ("Subject Combination", subject_combo),
        ("Expected Marks", f"{marks}%")
    ]

    for label, value in profile:
        pdf.cell(60, 8, clean(label), border=1)
        pdf.cell(120, 8, clean(value), border=1, ln=True)

    pdf.ln(6)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, clean("Recommended Courses"), ln=True)

    pdf.set_font("Arial", "B", 11)
    pdf.cell(20, 8, "S.No", border=1)
    pdf.cell(160, 8, "Course Name", border=1, ln=True)

    pdf.set_font("Arial", size=11)
    for i, c in enumerate(results["best_fit"], start=1):
        pdf.cell(20, 8, str(i), border=1)
        pdf.cell(160, 8, clean(c), border=1, ln=True)

    pdf.ln(6)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, clean("Alternate Career Options"), ln=True)

    pdf.set_font("Arial", "B", 11)
    pdf.cell(20, 8, "S.No", border=1)
    pdf.cell(160, 8, "Course Name", border=1, ln=True)

    pdf.set_font("Arial", size=11)
    if alternate:
        for i, c in enumerate(alternate, start=1):
            pdf.cell(20, 8, str(i), border=1)
            pdf.cell(160, 8, clean(c), border=1, ln=True)
    else:
        pdf.cell(180, 8, clean("No alternate options available"), border=1, ln=True)

    file_name = f"{name}_Career_Recommendation_Report.pdf"
    pdf.output(file_name)

    st.download_button(
        "📄 Download Professional Career Report (PDF)",
        data=open(file_name, "rb").read(),
        file_name=file_name,
        mime="application/pdf"
    )
