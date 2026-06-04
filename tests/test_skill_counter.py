import csv

from src.skill_counter import detect_skills, count_skills_from_csv

def test_detect_python():
    assert "python" in detect_skills("We need Python experience")


def test_javascript_does_not_detect_java():
    result = detect_skills("We need JavaScript experience")
    assert "javascript" in result
    assert "java" not in result

def testing_detect_skill_function():
    result = detect_skills("     ")
    assert len(result) == 0

    result = detect_skills("ml is the same as machine learning")
    assert len(result) == 1
    assert "machine learning" in result

    result = detect_skills("node.js, fast api and c++ are part of cs")
    assert len(result) == 3
    assert "node.js", "c++" in result
    assert "fastapi" in result

def test_standalone_js_detects_javascript():
    result = detect_skills("We need js and react")

    assert "javascript", "react" in result

def test_react_js_does_not_detect_javascript():
    result = detect_skills("We need react.js experience")

    assert "react" in result
    assert "javascript" not in result

def test_detect_python():
    result = detect_skills("We need Python experience")

    assert "python" in result


def test_py_alias_detects_python():
    result = detect_skills("Looking for py and sql")

    assert "python" in result
    assert "sql" in result


def test_javascript_does_not_detect_java():
    result = detect_skills("We need JavaScript experience")

    assert "javascript" in result
    assert "java" not in result


def test_java_detected_as_java():
    result = detect_skills("We need Java experience")

    assert "java" in result
    assert "javascript" not in result


def test_c_plus_plus_detected():
    result = detect_skills("C++ is required for this role")

    assert "c++" in result


def test_nodejs_does_not_detect_javascript():
    result = detect_skills("node.js, fast api and c++ are part of cs")

    assert "node.js" in result
    assert "fastapi" in result
    assert "c++" in result
    assert "javascript" not in result
    assert len(result) == 3


def test_reactjs_does_not_detect_javascript():
    result = detect_skills("We need react.js experience")

    assert "react" in result
    assert "javascript" not in result


def test_standalone_js_detects_javascript():
    result = detect_skills("We need js and react")

    assert "javascript" in result
    assert "react" in result


def test_machine_learning_phrase_detected():
    result = detect_skills("This role requires machine learning experience")

    assert "machine learning" in result


def test_random_text_returns_empty_list():
    result = detect_skills("yyyyyyyyyyyyyyyy")

    assert result == []


def test_repeated_skill_counts_once_in_detect_skills():
    result = detect_skills("python python python sql")

    assert "python" in result
    assert "sql" in result
    assert result.count("python") == 1


def test_count_skills_from_csv_counts_correctly(tmp_path):
    csv_path = tmp_path / "jobs.csv"

    rows = [
        {
            "job_title": "Job 1",
            "description": "Python Python SQL"
        },
        {
            "job_title": "Job 2",
            "description": "py and js"
        },
        {
            "job_title": "Job 3",
            "description": "node.js and react.js"
        },
        {
            "job_title": "Job 4",
            "description": "yyyyyyyyyyyy"
        }
    ]

    with open(csv_path, "w", encoding="utf-8", newline="") as file:
        fieldnames = ["job_title", "description"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for row in rows:
            writer.writerow(row)

    result = count_skills_from_csv(csv_path)

    assert result["python"] == 2
    assert result["sql"] == 1
    assert result["javascript"] == 1
    assert result["node.js"] == 1
    assert result["react"] == 1
    assert "java" not in result