import PyPDF2
import streamlit as st
from openai import OpenAI
st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

st.title("📄 AI Resume Analyzer")
st.markdown("Get instant AI-powered resume feedback 🚀")
st.divider()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)

st.title("📄 AI Resume Analyzer")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

resume_text = ""

if uploaded_file:
    reader = PyPDF2.PdfReader(uploaded_file)
    for page in reader.pages:
        resume_text += page.extract_text()
job_role = st.text_input("💼 Enter Job Role (e.g., Data Analyst)")

st.divider()
if st.button("🚀 Analyze Resume"):
    if resume_text and job_role:
        with st.spinner("Analyzing..."):
            try:
                prompt = f"""
                Analyze the resume for {job_role}.

                Return in this format:

                Score: (out of 100)

                Strengths:
                - 

                Weaknesses:
                - 

                Missing Skills:
                - 

                Suggestions:
                - 

                Resume:
                {resume_text}
                """

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}]
                )

                result = response.choices[0].message.content

                st.subheader("📊 Analysis Result")
                st.write(result)

                st.success("Analysis completed successfully!")

                st.download_button(
                    label="📥 Download Report",
                    data=result,
                    file_name="resume_analysis.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error("API Error: Please check your API key or quota.")
    else:
        st.warning("Please upload resume and enter job role")