from fastapi.testclient import TestClient

from src.api import app

client = TestClient(app)


def test_home_route():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "CS Career Skill Analyzer API is running"
    }


def test_health_route():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_detect_skills_api():
    response = client.post(
        "/detect-skills",
        json={
            "description": "We need Python and SQL"
        }
    )

    data = response.json()

    assert response.status_code == 200
    assert "python" in data["skills_detected"]
    assert "sql" in data["skills_detected"]
    assert data["total_skills_detected"] == 2


def test_detect_skills_api_aliases():
    response = client.post(
        "/detect-skills",
        json={
            "description": "We need py, js, react.js and machine learning"
        }
    )

    data = response.json()

    assert response.status_code == 200
    assert "python" in data["skills_detected"]
    assert "javascript" in data["skills_detected"]
    assert "react" in data["skills_detected"]
    assert "machine learning" in data["skills_detected"]


def test_detect_skills_api_random_text():
    response = client.post(
        "/detect-skills",
        json={
            "description": "yyyyyyyyyyyyyyyy"
        }
    )

    data = response.json()

    assert response.status_code == 200
    assert data["skills_detected"] == []
    assert data["total_skills_detected"] == 0


def test_detect_skills_missing_description_returns_422():
    response = client.post(
        "/detect-skills",
        json={}
    )

    assert response.status_code == 422


def test_analyze_jobs_api():
    response = client.post(
        "/analyze-jobs",
        json={
            "jobs": [
                {
                    "job_title": "Frontend Developer",
                    "description": "React and JS"
                },
                {
                    "job_title": "Backend Developer",
                    "description": "Python and SQL"
                },
                {
                    "job_title": "ML Intern",
                    "description": "Machine learning and PyTorch"
                }
            ]
        }
    )

    data = response.json()

    assert response.status_code == 200
    assert data["total_jobs"] == 3
    assert data["skill_count"]["react"] == 1
    assert data["skill_count"]["javascript"] == 1
    assert data["skill_count"]["python"] == 1
    assert data["skill_count"]["sql"] == 1
    assert data["skill_count"]["machine learning"] == 1
    assert data["skill_count"]["pytorch"] == 1