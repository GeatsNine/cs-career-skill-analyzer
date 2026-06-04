import csv
import re

RULES = {
    "Machine Learning": [
        "machine learning", 
        "ml", 
        "ai", 
        "artificial intelligence", 
        "pytorch", 
        "scikit-learn", 
        "sklearn"
    ],

    "Data Engineering": [
        "data engineer",
        "pipeline",
        "etl",
        "data pipeline"
    ],

    "Data / Analytics": [
        "data analyst",
        "data analytics",
        "analytics",
        "dashboard",
        "excel"
    ],

    "Full Stack": [
        "full stack",
        "full-stack",
        "frontend and backend",
        "react node"
    ],

    "Frontend": [
        "frontend",
        "front-end",
        "react",
        "javascript",
        "typescript",
        "html",
        "css"
    ],

    "Backend": [
        "backend",
        "back-end",
        "server",
        "api",
        "fastapi",
        "django",
        "spring boot",
        "java"
    ],

    "Cloud / DevOps": [
        "cloud",
        "aws",
        "docker",
        "linux",
        "devops",
        "infrastructure"
    ],

    "Mobile": [
        "mobile",
        "android",
        "kotlin",
        "ios",
        "app developer"
    ],

    "Software Engineering": [
        "software engineer",
        "software developer",
        "developer",
        "programming",
        "git"
    ]
}

def contains_keyword(text, keyword):
    pattern = r"(?<!\w)" + re.escape(keyword) + r"(?!\w)"
    return re.search(pattern, text) is not None

def classify_role(job_title: str, description: str):
    job_title = job_title or ""
    description = description or ""

    text = job_title + " " + description
    text = text.lower()

    for role, keywords in RULES.items():
        for keyword in keywords:
            if contains_keyword(text, keyword):
                return role

    return "Other"

def classify_jobs(input_path):
    updated_job_role = []

    with open(input_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            role = classify_role(row.get("job_title"), row.get("description"))
            
            row["role_category"] = role
            updated_job_role.append(row)

    return updated_job_role

def save_classified_jobs(output_path, job_role):
    with open(output_path, "w", encoding="utf-8", newline="") as file:
        fieldnames = ["job_title", "company", "location", "description", "role_category"]

        writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction="ignore")

        writer.writeheader()

        for job in job_role:
            writer.writerow(job)


def count_roles(classified_jobs):
    role_count = {}

    for job in classified_jobs:
        role = job["role_category"]
        role_count[role] = role_count.get(role, 0) + 1

    return role_count

def save_role_counts(output_path, role_counts):
    with open(output_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["role_category", "count"])

        for role_category, count in role_counts:
            writer.writerow([role_category, count])


def main():
    updated_job_role = classify_jobs("output/cleaned_job_posts.csv")
    save_classified_jobs("output/classified_job_posts.csv", updated_job_role)

    role_count = count_roles(updated_job_role)
    sorted_role_count = sorted(role_count.items(), key=lambda item: item[1], reverse=True)

    save_role_counts("output/role_counts.csv", sorted_role_count)

if __name__ == "__main__":
    main()