import os
import shutil
import zipfile
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

def create_folders_and_files(dictionary, current_path=""):
    for key, value in dictionary.items():
        if isinstance(value, dict):
            folder_path = os.path.join(current_path, key)
            os.makedirs(folder_path, exist_ok=True)
            create_folders_and_files(value, folder_path)
        elif isinstance(value, str):  # Check if the value is a string (file content)
            file_path = os.path.join(current_path, key)
            with open(file_path, 'w') as f:
                f.write(value)

def zip_directory(directory, zip_name):
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, directory))

def generate_file_structure(app_name):
    #google_api_key = os.getenv("GOOGLE_API_KEY")
    google_api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    app_js_content = """import React from 'react';function App(){return(<div><h1>Welcome to My App</h1><p>This is a sample content for the main App component.</p></div>);}export default App;"""
    header_js_content = """import React from 'react';function Header(){return(<header><h2>This is the Header</h2></header>);}export default Header;"""


    prompt = f"""
Create a file structure for a {app_name} project with the necessary files and content. 
The output should be in JSON format, adhering to the structure provided below:

example_dict = {{
    "src": {{
        "public": {{
            "index.html": "Base HTML file with necessary structure and content.",
            "styles.css": "body  font-family: Arial, sans-serif; background-color: #f0f0f0; "
        }},
        "components": {{
            "App.js": "{app_js_content}",
            "Header.js": "{header_js_content}",
            "Footer.js": "Component file for the footer section."
        }},
        "utils": {{
            "api.js": "Utility file for making API calls.",
            "helpers.js": "Utility functions for common tasks."
        }},
        "config": {{
            "config.json": "Configuration file for application settings."
        }},
        "index.js": "Main entry point for the React application."
        "package.json": "File containing metadata and dependencies for the project."
    }}
}}

Ensure that the file structure includes at least the following files:
- index.html
- styles.css
- App.js
- api.js
- helpers.js
- config.json

Please provide only file names  along with contents which is necessary to build {app_name} Project. Limit the number of files to 10. Avoid providing additional explanations or descriptions.
"""

    response = model.generate_content(prompt)
    res = response.candidates[0].content.parts[0].text
    
    # Extracting the text part from the response
    start_index = res.find("```")+ 7 # Index of the start of the text part
    end_index = res.rfind("```")  # Index of the end of the text part
    file_structure_text = res[start_index:end_index]
    
    return eval(file_structure_text)

def main():
    st.title("App File Generator")
    app_name = st.text_input("Enter the name of the application")
    if st.button("Generate File Structure"):
        file_structure = generate_file_structure(app_name)
        create_folders_and_files(file_structure)
        zip_name = f"{app_name}_project.zip"
        zip_directory("/project", zip_name)
        st.success("File structure generated successfully!")
        st.download_button(
            label="Download Project",
            data=open(zip_name, "rb").read(),
            file_name=zip_name,
            mime="application/zip"
        )

if __name__ == "__main__":
    main()
