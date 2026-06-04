import csv

def clean_text(text: str, lower: bool):
    words = text.split()

    updated_words_list = []
    updated_text = ""

    for word in words:
        word = word.strip(".!,?")

        if lower: word = word.lower()

        updated_words_list.append(word)

    updated_text = " ".join(updated_words_list)

    return updated_text.strip()

# def is_valid_job(job):
#     if not job["job_title"].strip():
#         return False
    
#     if not job["company"].strip():
#         return False
    
#     if not job["location"].strip():
#         return False
    
#     if not job["description"].strip():
#         return False
    
#     return True

# Example: if CSV has title instead of job_title, your code breaks.

# Better code style:
def is_valid_job(job):
    required_fields = ["job_title", "company", "location", "description"]

    for field in required_fields:
        if not job.get(field, "").strip():
            return False

    return True

# Get job_title if it exists. If it does not exist, use empty string.

def remove_duplicate_jobs(jobs):
    seen = set()
    unique_job_list = []

    for job in jobs:
        key = (
            job["job_title"].lower(),
            job["company"].lower(),
            job["location"].lower(),
            job["description"]
        )

        if key not in seen:
            seen.add(key)
            unique_job_list.append(job)

    return unique_job_list

def clean_job_record(job: dict):
    cur = job.copy()

    cur["job_title"] = clean_text(cur["job_title"], False)
    cur["company"] = clean_text(cur["company"], False)
    cur["location"] = clean_text(cur["location"], False)
    cur["description"] = clean_text(cur["description"], True)

    return cur

def main():
    with open("data/dirty_job_posts.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        
        valid_job_list = []
        read = 0

        for row in reader:
            read += 1
            row = clean_job_record(row)
            
            if (is_valid_job(row)):
                valid_job_list.append(row)
    
        unique_job_list = remove_duplicate_jobs(valid_job_list)
        
        print("Total rows read:", read)
        print("Valid rows:", len(valid_job_list))
        print("Invalid rows removed:", read - len(valid_job_list))
        print("Duplicates removed:", len(valid_job_list) - len(unique_job_list))
        print("Cleaned rows saved:", len(unique_job_list))

    with open("output/cleaned_job_posts.csv", "w", encoding="utf-8", newline="") as file:
        # writer = csv.writer(file)

        # writer.writerow(["job_title", "company", "location", "description"])
        
        # for job in unique_job_list:
        #     writer.writerow([job["job_title"], job["company"], job["location"], job["description"]])

        fieldnames = ["job_title", "company", "location", "description"]

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for job in unique_job_list:
            writer.writerow(job)

        # Because each job is already a dictionary, DictWriter is cleaner:

if __name__ == "__main__":
    main()