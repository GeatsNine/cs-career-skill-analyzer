from src.data_cleaner import (
    clean_text,
    is_valid_job,
    remove_duplicate_jobs,
    clean_job_record,
)

def test_clean_text_lowercase():
    assert clean_text(" PYTHON!!! ", True) == "python"
    assert clean_text("     !!!   .....", True) == ""
    assert clean_text("I love  MineCraft      and coding!!! ", True) == "i love minecraft and coding"
    assert clean_text("Handsome Guyyy!!! good", False) == "Handsome Guyyy good"


def test_invalid_job_missing_title():
    job_one = {
        "job_title": "",
        "company": "ABC",
        "location": "Sydney",
        "description": "Python role"
    }

    job_two = {
        "job_title": "Software Engineer",
        "company": "",
        "location": "Sydney",
        "description": "Python role"
    }

    job_three = {
        "job_title": "Software Engineer",
        "company": "ABC",
        "location": "",
        "description": "Python role"
    }

    job_four = {
        "job_title": "Software Engineer",
        "company": "ABC",
        "location": "Sydney",
        "description": ""
    }

    assert is_valid_job(job_one) == False
    assert is_valid_job(job_two) == False
    assert is_valid_job(job_three) == False
    assert is_valid_job(job_four) == False

def test_valid_job_missing_title():
    job = {
        "job_title": "Software Engineer",
        "company": "ABC",
        "location": "Sydney",
        "description": "Python role"
    }

    assert is_valid_job(job) == True

def test_clean_job_record():
    job = {
        "job_title": "Software!!!    Engineer...",
        "company": "   ABC  ",
        "location": "...Sydney    ....",
        "description": "Python     role"
    }
    
    result = {
        "job_title": "Software Engineer",
        "company": "ABC",
        "location": "Sydney",
        "description": "python role"
    }

    print(clean_job_record(job))
    assert clean_job_record(job) == result

def test_remove_duplicate_jobs():
    job_one = {
        "job_title": "Master Software Engineer",
        "company": "ABC",
        "location": "Sydney",
        "description": "Python role"
    }

    job_two = {
        "job_title": "Graduate Backend",
        "company": "ABC",
        "location": "Sydney",
        "description": "Python role"
    }

    job_three = {
        "job_title": "Master Software Engineer",
        "company": "ABC",
        "location": "Sydney",
        "description": "Python role"
    }

    job_four = {
        "job_title": "Degree CS",
        "company": "ABC",
        "location": "Sydney",
        "description": "Python role"
    }

    jobs = [job_one, job_two, job_three, job_four]

    result = remove_duplicate_jobs(jobs)
    print(result)
    assert len(result) == 3

    assert result == [job_one, job_two, job_four]

def test_clean_text_lowercase_and_punctuation():
    result = clean_text("  PYTHON!!! SQL???  ", True)

    assert result == "python sql"


def test_clean_text_keeps_capitalisation_when_lower_false():
    result = clean_text("  ABC Tech!!!  ", False)

    assert result == "ABC Tech"


def test_clean_text_extra_spaces():
    result = clean_text("  Data     Science     Course  ", True)

    assert result == "data science course"


def test_clean_text_empty_string():
    result = clean_text("", True)

    assert result == ""


def test_clean_text_spaces_only():
    result = clean_text("     ", True)

    assert result == ""


def test_valid_job_returns_true():
    job = {
        "job_title": "Graduate Software Engineer",
        "company": "ABC Tech",
        "location": "Sydney",
        "description": "Python role"
    }

    assert is_valid_job(job) is True


def test_invalid_job_missing_title():
    job = {
        "job_title": "",
        "company": "ABC Tech",
        "location": "Sydney",
        "description": "Python role"
    }

    assert is_valid_job(job) is False


def test_invalid_job_missing_company():
    job = {
        "job_title": "Graduate Software Engineer",
        "company": "",
        "location": "Sydney",
        "description": "Python role"
    }

    assert is_valid_job(job) is False


def test_invalid_job_missing_location():
    job = {
        "job_title": "Graduate Software Engineer",
        "company": "ABC Tech",
        "location": "",
        "description": "Python role"
    }

    assert is_valid_job(job) is False


def test_invalid_job_missing_description():
    job = {
        "job_title": "Graduate Software Engineer",
        "company": "ABC Tech",
        "location": "Sydney",
        "description": ""
    }

    assert is_valid_job(job) is False


def test_invalid_job_spaces_only_field():
    job = {
        "job_title": "   ",
        "company": "ABC Tech",
        "location": "Sydney",
        "description": "Python role"
    }

    assert is_valid_job(job) is False


def test_remove_duplicate_jobs_removes_exact_duplicates():
    jobs = [
        {
            "job_title": "Frontend Developer",
            "company": "WebStudio",
            "location": "Melbourne",
            "description": "React and CSS"
        },
        {
            "job_title": "Frontend Developer",
            "company": "WebStudio",
            "location": "Melbourne",
            "description": "React and CSS"
        },
        {
            "job_title": "Backend Developer",
            "company": "CloudApp",
            "location": "Brisbane",
            "description": "Java and SQL"
        }
    ]

    result = remove_duplicate_jobs(jobs)

    assert len(result) == 2


def test_clean_job_record_cleans_fields():
    job = {
        "job_title": " Graduate Software Engineer ",
        "company": " ABC Tech ",
        "location": " Sydney ",
        "description": " We need PYTHON, SQL and Git!!! "
    }

    result = clean_job_record(job)

    assert result["job_title"] == "Graduate Software Engineer"
    assert result["company"] == "ABC Tech"
    assert result["location"] == "Sydney"
    assert result["description"] == "we need python sql and git"