# App File Generator

## Overview

The **App File Generator** is a Streamlit-based web application designed to streamline the process of creating a structured Python project for web applications. By inputting the desired name of your application, this tool automatically generates the necessary file structure and content required to set up a basic web app. The generated files are then packaged into a downloadable zip file, simplifying the initial setup process for developers.

## Features

- **User Input for App Name:**
  - Users can enter the name of their application, which is used to customize the generated files.
- **Automatic File Structure Generation:**
  - The application uses the Google Generative AI API to create a JSON structure that outlines the necessary files and their contents for a Python-based web app.
- **File Creation and Organization:**
  - The app creates directories and files based on the generated JSON structure, including:
    - `index.html` and `styles.css` for the frontend.
    - `app.py` and `utils.py` for backend functionality.
    - `requirements.txt` for dependency management.
    - `setup.py` for packaging the application.
- **Zipping the Project:**
  - Once the file structure is created, the app compresses the directory into a zip file for easy download.
- **Downloadable Zip File:**
  - Users can download the generated project as a zip file directly from the web interface.

## Technical Details

- **Streamlit:** The app is built using Streamlit, a framework for creating interactive web applications in Python.
- **Google Generative AI API:** Utilized to generate the content and structure of the project files based on user input.
- **File Handling:** Python's `os`, `shutil`, and `zipfile` libraries are used to create directories, files, and compress the project into a zip file.
- **Environment Variables:** API keys and other sensitive information are managed using the `dotenv` library.

## Sample:


https://github.com/irfan-iiitr/CodeBundle-AI/assets/123577873/c911a022-fdda-482b-af4f-ac6a280bcf45



https://github.com/irfan-iiitr/CodeBundle-AI/assets/123577873/82a26804-f874-49ff-9130-4eec40c886b5


