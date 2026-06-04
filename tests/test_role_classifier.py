import csv

from src.role_classifier import classify_role, count_roles, classify_jobs


def test_classify_machine_learning_role():
    result = classify_role(
        "Machine Learning Intern",
        "Python ML pandas and pytorch"
    )

    assert result == "Machine Learning"


def test_classify_data_engineering_role():
    result = classify_role(
        "Data Engineer",
        "Build data pipelines and ETL workflows"
    )

    assert result == "Data Engineering"


def test_classify_data_analytics_role():
    result = classify_role(
        "Data Analyst",
        "Create dashboards using Excel and analytics"
    )

    assert result == "Data / Analytics"


def test_classify_full_stack_priority():
    result = classify_role(
        "Full Stack Developer",
        "Need React Node JavaScript and backend experience"
    )

    assert result == "Full Stack"


def test_classify_frontend_role():
    result = classify_role(
        "Junior Frontend Developer",
        "React HTML CSS and JavaScript"
    )

    assert result == "Frontend"


def test_classify_backend_role():
    result = classify_role(
        "Backend Developer",
        "Build APIs using FastAPI and Java"
    )

    assert result == "Backend"


def test_classify_cloud_devops_role():
    result = classify_role(
        "Cloud Graduate Engineer",
        "AWS Docker Linux and cloud infrastructure"
    )

    assert result == "Cloud / DevOps"


def test_classify_mobile_role():
    result = classify_role(
        "Mobile Developer Intern",
        "Android Kotlin app developer"
    )

    assert result == "Mobile"


def test_classify_software_engineering_role():
    result = classify_role(
        "Graduate Software Engineer",
        "Programming and Git experience"
    )

    assert result == "Software Engineering"


def test_classify_other_role():
    result = classify_role(
        "Office Assistant",
        "Answer calls and organise files"
    )

    assert result == "Other"


def test_count_roles_counts_correctly():
    classified_jobs = [
        {"role_category": "Frontend"},
        {"role_category": "Frontend"},
        {"role_category": "Backend"},
        {"role_category": "Machine Learning"},
    ]

    result = count_roles(classified_jobs)

    assert result["Frontend"] == 2
    assert result["Backend"] == 1
    assert result["Machine Learning"] == 1


def test_count_roles_empty_list():
    result = count_roles([])

    assert result == {}


def test_classify_jobs_adds_role_category(tmp_path):
    csv_path = tmp_path / "cleaned_jobs.csv"

    rows = [
        {
            "job_title": "Junior Frontend Developer",
            "company": "WebStudio",
            "location": "Melbourne",
            "description": "React HTML CSS"
        },
        {
            "job_title": "Backend Developer",
            "company": "CloudApp",
            "location": "Brisbane",
            "description": "FastAPI Java server"
        }
    ]

    with open(csv_path, "w", encoding="utf-8", newline="") as file:
        fieldnames = ["job_title", "company", "location", "description"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for row in rows:
            writer.writerow(row)

    result = classify_jobs(csv_path)

    assert len(result) == 2
    assert result[0]["role_category"] == "Frontend"
    assert result[1]["role_category"] == "Backend"