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
    google_api_key = os.getenv("GOOGLE_API_KEY")
    #google_api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    index_html_content = """<!DOCTYPE html>\n<html lang='en'>\n<head>\n<meta charset='UTF-8'>\n<title>{app_name}</title>\n<link rel='stylesheet' href='styles.css'>\n</head>\n<body>\n<h1>Welcome to {app_name}</h1>\n</body>\n</html>""".format(app_name=app_name)
    styles_css_content = """body {\n  font-family: Arial, sans-serif;\n  background-color: #f0f0f0;\n}"""
    app_py_content = "# Main Python file for the project"
    utils_py_content = "# Utility functions for common tasks"
    config_json_content = "{}"
    requirements_txt_content = "# List of Python dependencies\nflask==2.0.1\n"
    setup_py_content = "from setuptools import setup, find_packages\n\nsetup(\n    name='{app_name}',\n    version='0.1',\n    packages=find_packages(),\n    install_requires=['flask'],\n)".format(app_name=app_name)


    prompt = f"""
I need to create a  PYTHON project {app_name}.Create file structure and add the file content inside it to make it a full fledged PYTHON basedweb app.
Add every files necessary to create a project such that i have to just install the packages and then run it by pip install and python run.
 Return  a JSON in the format given ahead of a PYTHON Project:

    example_dict = {{
        "src":{{
            "templates" : {{
                  "index.html": "{index_html_content}",
          "styles.css": "{styles_css_content}",
            }}
        "index.html": "{index_html_content}",
        "styles.css": "{styles_css_content}",
        "app.py": "{app_py_content}",
        "utils.py": "{utils_py_content}",
        "requirements.txt": "{requirements_txt_content}",
        }}
        
    }}

Please provide only file names  along with contents which is necessary to build {app_name}PYTHON  Project. Limit the number of files to 10. Avoid providing additional explanations or descriptions.
"""
    print(prompt)

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
        zip_directory("src", zip_name)
        st.success("File structure generated successfully!")
        st.download_button(
            label="Download Project",
            data=open(zip_name, "rb").read(),
            file_name=zip_name,
            mime="application/zip"
        )

if __name__ == "__main__":
    main()
