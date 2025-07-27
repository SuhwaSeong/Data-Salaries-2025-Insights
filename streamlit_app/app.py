import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="2025 Data Salaries Dashboard", layout="wide")
st.title("💼 Data Science, AI & ML Job Salaries – 2025")

@st.cache_data
def load_data():
    return pd.read_csv("streamlit_app/salaries.csv")

df = load_data()

# ------------------------
# 🔍 Sidebar Filter Options
# ------------------------
st.sidebar.header("🧭 Filter Options")

# Location Filter
location_filter = st.sidebar.selectbox("🌍 Company Location", ["All"] + sorted(df["company_location"].unique()))
if location_filter != "All":
    df = df[df["company_location"] == location_filter]

# Experience Level Filter
experience_filter = st.sidebar.multiselect(
    "🎓 Experience Level", df["experience_level"].unique(), default=df["experience_level"].unique()
)
df = df[df["experience_level"].isin(experience_filter)]

# Remote Ratio Filter
remote_filter = st.sidebar.multiselect(
    "💻 Remote Ratio", df["remote_ratio"].unique(), default=df["remote_ratio"].unique()
)
df = df[df["remote_ratio"].isin(remote_filter)]

# Company Size Filter
company_size_filter = st.sidebar.multiselect(
    "🏢 Company Size", df["company_size"].unique(), default=df["company_size"].unique()
)
df = df[df["company_size"].isin(company_size_filter)]

# ------------------------
# 📊 Visualizations
# ------------------------
st.subheader("📊 Summary Statistics")
st.write(df.describe())

# Top 15 Job Titles by Average Salary
st.subheader("💵 Average Salary by Job Title (Top 15)")
top_jobs = df.groupby("job_title")["salary_in_usd"].mean().sort_values(ascending=False).head(15).reset_index()
fig1 = px.bar(top_jobs, x="salary_in_usd", y="job_title", orientation="h",
              title="Top 15 Average Salaries by Job Title", color="salary_in_usd")
fig1.update_layout(yaxis=dict(autorange="reversed"))
st.plotly_chart(fig1, use_container_width=True)

# Average Salary by Experience Level
st.subheader("🧠 Average Salary by Experience Level")
exp_salary = df.groupby("experience_level")["salary_in_usd"].mean().reset_index()
fig2 = px.bar(exp_salary, x="experience_level", y="salary_in_usd",
              title="Average Salary by Experience Level", color="salary_in_usd")
st.plotly_chart(fig2, use_container_width=True)
