import streamlit as st

# Page Configuration
st.set_page_config(page_title="Mads Andersen - Data Scientist", layout="wide")

# Header and Introduction
st.title("About Mads Andersen")
st.image("images/face.png", width=150)
st.markdown("""
    Welcome! I am Mads Andersen, a passionate Data Scientist with a keen interest in AI, 
    boasting international experience and adaptability in the tech world.
""")

# Contact Information
st.header("Contact Information")
st.write("Email: [madsa2398@gmail.com](mailto:madsa2398@gmail.com)")
st.write("Phone: +45 93 97 92 87")

# About Me Section
st.header("About Me")
st.markdown("""
    As a Data Scientist, I specialize in Python and machine learning, applying these skills 
    to solve real-world problems. With my education and experience across different cultures, 
    I bring a unique perspective to data science projects.
""")

# Skills Overview
st.header("Skills Overview")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Hard Skills")
    st.markdown("""
        - Python
        - SQL
        - Tableau
        - Git
    """)
with col2:
    st.subheader("Soft Skills")
    st.markdown("""
        - Communication
        - Teamwork
        - Flexibility
    """)

# Education
st.header("Education")
st.markdown("""
    - MSc in Economics and Business Administration, Copenhagen Business School
    - BSc in Mathematics and Technology, Technical University of Denmark
    - Exchange Program, University of Maryland (Honors awarded)
""")

# Publications and Projects
st.header("Publications and Projects")
st.markdown("""
    - NeurIPS 2022 Workshop Publication - SolarDK: A high-resolution urban solar panel image classification and localization dataset
    - Solar Panel Fault Detection Project
    - Chest X-Ray Image Classification Project
""")

# Relevant Courses
st.header("Relevant Courses")
st.markdown("""
    - Machine Learning and Data Mining
    - Active Machine Learning and Agency
    - Computer Vision
    - Reinforcement Learning and control
""")

# Work Experience
st.header("Work Experience")
st.markdown("""
    - Student Data Scientist, Legal Desk (nov. 2023 - present)   
""")

# Other Experiences
st.header("Other Experiences")
st.markdown("""
    - Enlisted - Slesvigske Fodregiment Fall 2019
    - Ollerup Højskole - Spring 2019
""")

# Footer
st.markdown("""
    Thank you for visiting my profile. Feel free to reach out for professional inquiries or opportunities!
""")

# To run the app, save this code in a Python file and run `streamlit run filename.py` in your terminal.
