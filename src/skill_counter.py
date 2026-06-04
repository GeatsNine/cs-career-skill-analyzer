import csv
import re
from src.skill_config import SKILL_ALIASES

def contains_keyword(text, keyword):
    pattern = r"(?<![\w.])" + re.escape(keyword) + r"(?![\w.])"
    return re.search(pattern, text) is not None

def detect_skills(description: str):
    seen = set()
    description = description.lower()

    for canonical_skill, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            if contains_keyword(description, alias):
                seen.add(canonical_skill)

    return sorted(seen)

def count_skills_from_csv(csv_path):
    skill_count = {}

    with open(csv_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            skill_mentioned = detect_skills(row.get("description", ""))
            
            for skill in skill_mentioned:
                skill_count[skill] = skill_count.get(skill, 0) + 1
    
    return skill_count  

def save_skill_counts(output_path, sorted_skills):
    with open(output_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["skill", "count"])

        for skill, count in sorted_skills:
            writer.writerow([skill, count])

def main():
    skill_count = count_skills_from_csv("output/cleaned_job_posts.csv")
    sorted_skills = sorted(skill_count.items(), key=lambda item: item[1], reverse=True)
    save_skill_counts("output/top_skills.csv", sorted_skills)
    print(detect_skills("We need C++, JavaScript, React.js and machine learning."))

if __name__ == "__main__":
    main()