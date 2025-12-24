#engine/recommendation_engine.py

from utils.data_loader import load_json

boards = load_json("boards.json")
streams = load_json("streams.json")
course_categories = load_json("course_categories.json")
courses = load_json("courses.json")
eligibility = load_json("eligibility_rules.json")


def get_streams_by_board(board):
    return boards.get(board, [])


def get_subject_combinations(stream):
    return streams.get(stream, [])


def get_course_categories(subject_combo):
    return course_categories.get(subject_combo, [])


def recommend_courses(subject_combo, marks):
    result = {
        "best_fit": [],
        "safe_options": [],
        "backup_options": []
    }

    for category in course_categories.get(subject_combo, []):
        for course in courses.get(category, []):
            min_marks = eligibility.get(course, 50)

            if marks >= min_marks + 10:
                result["best_fit"].append(course)
            elif marks >= min_marks:
                result["safe_options"].append(course)
            else:
                result["backup_options"].append(course)

    return result
