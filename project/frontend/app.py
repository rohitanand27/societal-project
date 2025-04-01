import streamlit as st
import requests
import pandas as pd
import json

st.set_page_config(page_title="AI Career Guidance", layout="wide")

st.title("🚀 AI-Powered Career Guidance System")
st.markdown("### Upload your resume and get AI-powered **career insights, job recommendations, and skill gap analysis!**")

st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Career Insights", "AI Chatbot"])

if page == "Home":
    st.write("### 📄 Upload Your Resume")
    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])

    if uploaded_file is not None:
        with st.spinner("🔍 Analyzing your resume..."):
            files = {"file": uploaded_file.getvalue()}
            response = requests.post("http://127.0.0.1:5000/upload", files=files)

        if response.status_code == 200:
            st.success("✅ Resume processed successfully!")
            st.session_state["resume_data"] = response.json()
            st.experimental_rerun()
        else:
            st.error("❌ Error processing resume. Please try again.")

elif page == "Career Insights":
    if "resume_data" not in st.session_state:
        st.warning("⚠ Please upload a resume first!")
    else:
        resume_data = st.session_state["resume_data"]

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("👤 Personal Details")
            st.write(f"**Name:** {resume_data.get('name', 'N/A')}")
            st.write(f"**Email:** {resume_data.get('email', 'N/A')}")
            st.write(f"**Phone:** {resume_data.get('phone', 'N/A')}")

        with col2:
            st.subheader("📚 Education & Experience")
            st.write(f"**Degree:** {resume_data.get('degree', 'N/A')}")
            st.write(f"**Experience:** {resume_data.get('total_experience', 'N/A')} years")

        st.subheader("💡 Skills Extracted")
        skills = resume_data.get("skills", [])
        st.write(", ".join(skills) if skills else "No skills detected.")

        st.subheader("🚀 Career Recommendations")
        recommended_jobs = resume_data.get("recommended_jobs", [])
        for job in recommended_jobs:
            st.markdown(f"✅ **{job}**")

        # Job Recommendation Chart
        st.subheader("📊 Job Market Trends")
        job_df = pd.DataFrame({
            "Job Roles": recommended_jobs,
            "Demand Score": [80, 70, 85, 60, 75][:len(recommended_jobs)]
        })
        st.bar_chart(job_df.set_index("Job Roles"))

        st.success("🔗 Want to improve your skills? Check out **Coursera, Udemy, or LinkedIn Learning**!")

elif page == "AI Chatbot":
    st.write("## 💬 AI Career Guidance Chatbot")
    st.markdown("Ask any career-related question!")

    user_input = st.text_input("Type your question...")
    if st.button("Ask AI"):
        if user_input:
            with st.spinner("🔍 Thinking..."):
                response = requests.post("http://127.0.0.1:5000/chatbot", json={"query": user_input})
            
            if response.status_code == 200:
                st.success("🤖 AI Response:")
                st.write(response.json()["response"])
            else:
                st.error("❌ Error connecting to AI chatbot.")
