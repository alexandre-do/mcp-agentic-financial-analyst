import streamlit as st

st.title("Agentic Data Analyst")
st.write("This is the starter Streamlit front end for your agentic analytics workflow.")

question = st.text_area("Ask a data question", "What are the top trends in my dataset?")

if st.button("Analyze"):
    st.info("The application is scaffolded. Connect your agent and data tools here.")
    st.write(question)
