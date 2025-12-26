#pages/1_Master_Admin.py
import streamlit as st
import pandas as pd
from utils.data_loader import load_json, save_json

st.set_page_config(page_title="Master Admin Dashboard", layout="wide")

# ==================================================
# STYLES
# ==================================================
st.markdown("""
<style>
body { background:#F4F6F9; }

.title {
    font-size:38px;
    font-weight:900;
    color:#0B5ED7;
    margin-bottom:30px;
}

.hero {
    background:linear-gradient(135deg,#0B5ED7,#1F3C88);
    padding:28px;
    border-radius:20px;
    color:white;
    margin-bottom:35px;
    box-shadow:0 14px 30px rgba(0,0,0,0.25);
}

.card {
    background:#FFFFFF;
    padding:26px;
    border-radius:18px;
    box-shadow:0 12px 26px rgba(0,0,0,0.08);
    margin-bottom:28px;
}

.kpi {
    padding:22px;
    border-radius:18px;
    color:white;
    text-align:center;
    box-shadow:0 10px 22px rgba(0,0,0,0.18);
}

.kpi h2 { font-size:34px; margin-bottom:6px; }
.kpi p { font-size:14px; opacity:0.9; }

.kpi-blue { background:linear-gradient(135deg,#4FACFE,#00C6FF); }
.kpi-green { background:linear-gradient(135deg,#43E97B,#38F9D7); }
.kpi-purple { background:linear-gradient(135deg,#667EEA,#764BA2); }
.kpi-orange { background:linear-gradient(135deg,#F7971E,#FFD200); }
.kpi-red { background:linear-gradient(135deg,#FF416C,#FF4B2B); }

.section-title {
    font-size:22px;
    font-weight:800;
    color:#1F618D;
    margin-bottom:6px;
}

.desc {
    font-size:14px;
    color:#555;
    margin-bottom:18px;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# HERO
# ==================================================
st.markdown("""
<div class="hero">
    <h1>🔐 Master Admin Dashboard</h1>
    <p>Central control panel for academic structure, eligibility & career logic</p>
</div>
""", unsafe_allow_html=True)

# ==================================================
# LOGIN
# ==================================================
if "admin" not in st.session_state:
    st.session_state.admin = False

if not st.session_state.admin:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Admin Login")
    st.caption("Use admin credentials to access system controls")

    u = st.text_input("Username", help="Default: admin")
    p = st.text_input("Password", type="password", help="Default: admin123")

    if st.button("Login", width="stretch"):
        if u == "admin" and p == "admin123":
            st.session_state.admin = True
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ==================================================
# LOAD DATA
# ==================================================
boards = load_json("boards.json")
streams = load_json("streams.json")
categories = load_json("course_categories.json")
courses = load_json("courses.json")
eligibility = load_json("eligibility_rules.json")

# ==================================================
# SIDEBAR
# ==================================================
section = st.sidebar.radio(
    "Admin Sections",
    [
        "📊 Dashboard",
        "📘 Streams & Subjects",
        "🧩 Course Categories",
        "🎓 Courses",
        "📏 Eligibility Rules"
    ]
)

# ==================================================
# 📊 DASHBOARD
# ==================================================
if section == "📊 Dashboard":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>System Overview</div>", unsafe_allow_html=True)
    st.markdown("<div class='desc'>Live snapshot of the data powering student recommendations.</div>", unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.markdown(f"<div class='kpi kpi-blue'><h2>{len(boards)}</h2><p>Boards</p></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='kpi kpi-green'><h2>{len(streams)}</h2><p>Streams</p></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='kpi kpi-purple'><h2>{sum(len(v) for v in streams.values())}</h2><p>Subject Combos</p></div>", unsafe_allow_html=True)
    c4.markdown(f"<div class='kpi kpi-orange'><h2>{sum(len(v) for v in categories.values())}</h2><p>Categories</p></div>", unsafe_allow_html=True)
    c5.markdown(f"<div class='kpi kpi-red'><h2>{sum(len(v) for v in courses.values())}</h2><p>Courses</p></div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# 📘 STREAMS & SUBJECTS
# ==================================================
elif section == "📘 Streams & Subjects":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Streams & Subject Combinations</div>", unsafe_allow_html=True)
    st.markdown("<div class='desc'>Controls what subject options students see after choosing a stream.</div>", unsafe_allow_html=True)

    stream = st.selectbox("Select Stream", list(streams.keys()))
    st.caption("Example: Science → Mathematics + Computer Science")

    st.write("### Existing Subject Combinations")
    st.table(pd.DataFrame({"Subject Combination": streams[stream]}))

    st.divider()

    st.subheader("➕ Add Subject Combination")
    new_subject = st.text_input("Subject Name", placeholder="Mathematics + Computer Science")

    if st.button("Add Subject Combination"):
        if new_subject and new_subject not in streams[stream]:
            streams[stream].append(new_subject)
            save_json("streams.json", streams)
            st.success("Subject combination added")
            st.rerun()

    st.divider()

    st.subheader("🗑 Delete Subject Combination")
    st.caption("⚠ This removes linked categories & courses")

    del_subject = st.selectbox("Select Subject", streams[stream])
    confirm = st.checkbox("I understand the impact")

    if st.button("Delete Subject") and confirm:
        streams[stream].remove(del_subject)
        categories.pop(del_subject, None)
        save_json("streams.json", streams)
        save_json("course_categories.json", categories)
        st.warning("Subject deleted")
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# 🧩 COURSE CATEGORIES
# ==================================================
elif section == "🧩 Course Categories":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Course Categories</div>", unsafe_allow_html=True)
    st.markdown("<div class='desc'>Broad career domains mapped to subject combinations.</div>", unsafe_allow_html=True)

    subject = st.selectbox("Subject Combination", list(categories.keys()))
    st.table(pd.DataFrame({"Category": categories.get(subject, [])}))

    new_category = st.text_input("New Category", placeholder="Data & IT")

    if st.button("Add Category"):
        categories.setdefault(subject, []).append(new_category)
        save_json("course_categories.json", categories)
        st.success("Category added")
        st.rerun()

    st.divider()

    del_category = st.selectbox("Delete Category", categories.get(subject, []))
    confirm = st.checkbox("Confirm deletion")

    if st.button("Delete Category") and confirm:
        categories[subject].remove(del_category)
        save_json("course_categories.json", categories)
        st.warning("Category deleted")
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# 🎓 COURSES
# ==================================================
elif section == "🎓 Courses":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Courses</div>", unsafe_allow_html=True)
    st.markdown("<div class='desc'>Exact degrees and programs recommended to students.</div>", unsafe_allow_html=True)

    category = st.selectbox("Category", list(courses.keys()))
    st.table(pd.DataFrame({"Course": courses[category]}))

    new_course = st.text_input("New Course", placeholder="B.Tech (AI & ML)")

    if st.button("Add Course"):
        courses.setdefault(category, []).append(new_course)
        save_json("courses.json", courses)
        st.success("Course added")
        st.rerun()

    st.divider()

    del_course = st.selectbox("Delete Course", courses[category])
    confirm = st.checkbox("Remove eligibility rules also")

    if st.button("Delete Course") and confirm:
        courses[category].remove(del_course)
        eligibility.pop(del_course, None)
        save_json("courses.json", courses)
        save_json("eligibility_rules.json", eligibility)
        st.warning("Course deleted")
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# 📏 ELIGIBILITY
# ==================================================
elif section == "📏 Eligibility Rules":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Eligibility Rules</div>", unsafe_allow_html=True)
    st.markdown("<div class='desc'>Controls minimum score required for course recommendation.</div>", unsafe_allow_html=True)

    course = st.selectbox("Course", list(eligibility.keys()))
    marks = st.number_input("Minimum Percentage", 40, 100, value=eligibility.get(course, 50))

    if st.button("Save Eligibility"):
        eligibility[course] = marks
        save_json("eligibility_rules.json", eligibility)
        st.success("Eligibility updated")
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
