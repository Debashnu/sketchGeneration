import streamlit as st
from model import GenerativeModel

# Initialize the GenerativeModel
model = GenerativeModel('gemini-pro')

st.title("Welcome to Arduino Code Generator")

# Input fields for project details and components using columns
col1, col2 = st.columns(2)

with col1:
    project_details = st.text_area('Project Details', 'Please enter your project details or requirements')

with col2:
    components = st.text_area('Components', 'Enter the components you are using')

# Button to generate code
if st.button("Generate Code"):
    if len(project_details.strip()) == 0:
        st.warning('Please enter your project details or requirements')
    else:
        # Generate Arduino code using model.py
        generated_code = model.generate_arduino_code(project_details, components)
        
        # Display generated code
        st.success("Generated Arduino code:")
        st.code(generated_code, language='cpp')
        
        # Offer download button for the generated .ino file
        st.download_button(
            label="Download .ino file",
            data=generated_code,
            file_name="generate_code.ino",
            mime="text/plain"
        )
        