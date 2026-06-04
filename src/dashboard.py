import streamlit as st
import pandas as pd
import requests

# Section 1: Header
st.header("CS Career Skill Analyzer Dashboard")

st.write("Analyze junior and graduate CS job posts to identify commonly requested technical skills.")

# Section 2: Summary Metrics
df_jobs = pd.read_csv("output/classified_job_posts.csv")
df_skills = pd.read_csv("output/top_skills.csv")

df_skills["count"] = pd.to_numeric(df_skills["count"]) # change the data type of count from str to int
df_skills = df_skills.sort_values(by="count", ascending=False)
top_skill = "N/A"

if len(df_skills) > 0:
    top_skill = df_skills.iloc[0]["skill"] # Get the first row, then get the value in the skill column.

st.subheader("Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Total Jobs", len(df_jobs))
col2.metric("Unique Skills", len(df_skills))
col3.metric("Top Skill", top_skill)

# Section 3: Top Skills Chart
top_n = st.slider("Number of top skills to show", 1, len(df_skills), min(10, len(df_skills)))

top_skills_df = df_skills.head(top_n)

if len(top_skills_df) > 0:
    chart_skills = top_skills_df.set_index("skill")["count"] 
    st.bar_chart(chart_skills)
else:
    st.warning("No skills match this filter.")

# Section 4: Skill Table
st.subheader("Number of top skills in Table")

display_skills_df = df_skills.copy()
top_display_skills_df = display_skills_df.head(top_n)
top_display_skills_df.index = range(1, len(top_display_skills_df) + 1)

st.dataframe(top_display_skills_df)

# Section 5: Job Post Explorer
st.subheader("Job Post Explorer")

location_option = ["All"] + sorted(df_jobs["location"].unique().tolist())
selected_location = st.selectbox("Filter by location", location_option)

if selected_location == "All":
    filtered_df_jobs = df_jobs
else:
    filtered_df_jobs = df_jobs[df_jobs["location"] == selected_location]

search_keyword = st.text_input("Search job title", "")

if search_keyword:
    filtered_df_jobs = filtered_df_jobs[
        filtered_df_jobs["job_title"].str.contains(search_keyword, case=False, na=False)
    ]
# na=False prevents errors if some row is missing a title.

display_jobs_df = filtered_df_jobs.copy()
display_jobs_df.index = range(1, len(display_jobs_df) + 1)

st.dataframe(display_jobs_df)

# Week 6 assignment
# Section 6: Live Skill Detector
def call_detect_skills_api(job_description):
    API_URL = "http://127.0.0.1:8000"

    try:
        response = requests.post(
            f"{API_URL}/detect-skills", 
            json={
                "description": job_description
            },
            timeout=5)

        if response.status_code == 200:
            data = response.json()

            skills_detected = data["skills_detected"]
            total_skills_detected = data["total_skills_detected"]

            if total_skills_detected == 0:
                st.warning("No technical skills were detected in this text.")
            else:
                st.write("Detected skills:")
                st.write(skills_detected)
                st.metric("Total Skills Detected", total_skills_detected)

        elif response.status_code == 422:
            st.error("Invalid request. Description is missing or has the wrong format.")

        else:
            st.error(f"API error: {response.status_code}")   

    except requests.exceptions.RequestException:
        st.error("API server is not running. Start FastAPI first.")

st.header("Live Skill Detector")

job_description = st.text_area("Type your job description:")

if st.button("Analyze Skills"):
    if job_description.strip() == "":
        st.warning("Please enter a job description.")
    else:
        call_detect_skills_api(job_description)

# Week 7 assignment
st.subheader("Role Category Summary")

df_role = pd.read_csv("output/role_counts.csv")

df_role["count"] = pd.to_numeric(df_role["count"])
df_role = df_role.sort_values(by="count", ascending=False)

if len(df_role) > 0:
    top_n = st.slider(
        "Number of top roles to show",
        1,
        len(df_role),
        min(10, len(df_role))
    )

    top_roles_df = df_role.head(top_n)

    chart_roles = top_roles_df.set_index("role_category")["count"]
    st.bar_chart(chart_roles)

    display_role_df = top_roles_df.copy()
    display_role_df.index = range(1, len(display_role_df) + 1)

    st.dataframe(display_role_df)
else:
    st.warning("No role data available.")