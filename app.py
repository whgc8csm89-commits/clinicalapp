import streamlit as st
from openai import OpenAI

# 1. Setup OpenAI Client
# The API Key must be stored in Replit Secrets as OPENAI_API_KEY
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 2. Page Configuration
st.set_page_config(page_title="AI Clinical Scribe", layout="wide")

# Custom CSS for a professional medical look
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; background-color: #004d99; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_value=True)

# 3. App Interface
st.title("🩺 Professional Clinical Scribe")
st.subheader("Automated Medical Documentation")

# Layout: Two columns
left_col, right_col = st.columns([1, 1])

with left_col:
    st.markdown("### Patient Information")
    patient_name = st.text_input("Patient Full Name:")
    
    col_a, col_b = st.columns(2)
    with col_a:
        dob = st.text_input("Date of Birth (YYYY-MM-DD):")
    with col_b:
        sex = st.selectbox("Sex:", ["Male", "Female", "Other"])
    
    st.markdown("### Clinical Dictation")
    dictation = st.text_area("Enter provider notes or transcript:", height=350, 
                             placeholder="Example: Patient presents with uncontrolled Type 2 Diabetes...")
    
    generate_btn = st.button("GENERATE CLINICAL NOTE")

# 4. Processing Logic
if generate_btn:
    if not dictation or not patient_name:
        st.error("Error: Please provide at least the Patient Name and Dictation.")
    else:
        with right_col:
            with st.spinner("Generating professional note..."):
                try:
                    # The instructions for the AI are in English to ensure professional terminology
                    system_prompt = """You are a professional Medical Scribe. 
                    Create a formal, billable clinical note (SOAP format) based on the input.
                    Include:
                    - Chief Complaint
                    - HPI (detailed)
                    - ROS
                    - Physical Exam
                    - Assessment & Plan (with ICD-10 codes and HCC status)
                    - Suggested CPT code.
                    All output must be in professional medical English."""

                    user_input = f"Patient: {patient_name}, DOB: {dob}, Sex: {sex}. Input: {dictation}"

                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_input}
                        ],
                        temperature=0.2
                    )

                    final_note = response.choices[0].message.content
                    
                    st.markdown("### Generated Note")
                    # Display the note in a text area so it's easy to edit and copy
                    st.text_area("Copy and paste to EMR:", value=final_note, height=550)
                    st.success("Note generated successfully!")
                
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
