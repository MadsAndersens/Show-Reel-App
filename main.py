import streamlit as st

st.set_page_config(
    page_title="Welcome to my showreel! 👋",
    page_icon="👋",
)

st.write("# Welcome to my showreel! 👋")
st.write("This is a collection of my work, showcasing some of my skills and experience.")

st.header("Contact Information")
st.write("Email: [madsa2398@gmail.com](mailto:madsa2398@gmail.com)")
st.write("Phone: +45 93 97 92 87")

# Create two columns for LinkedIn
col1, col2 = st.columns([1, 20])
with col1:
    # Display LinkedIn logo
    st.image("images/linkedin-48.png", width=30)
with col2:
    # Display LinkedIn link
    st.markdown("[LinkedIn](https://www.linkedin.com/in/mads-andersen-102732149/)")

# Create two columns for GitHub
col1, col2 = st.columns([1, 20])
with col1:
    # Display GitHub logo
    st.image("images/github-50.png", width=30)
with col2:
    # Display GitHub link
    st.markdown("[GitHub](https://github.com/MadsAndersens)")


# Redirection to other pages
st.header("Showreel Contents")
st.write("Click on the links below to see the contents of this showreel.")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("👀 About Me",use_container_width=True):
        st.switch_page('pages/1_👀_about_me.py')
with col2:
    if st.button("🤖 ML",use_container_width=True):
        st.switch_page('pages/2_🤖_Auto_ML.py')
with col3:
    if st.button("👟 Active ML",use_container_width=True):
        st.switch_page('pages/3_👟_active_learning.py')
with col4:
    if st.button("👔 BI Dashboard",use_container_width=True):
        st.switch_page('pages/4_👔_BI_dashboard.py')
