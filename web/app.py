import streamlit as st
import pandas as pd
import json
import google.generativeai as ai
from paddleocr import PaddleOCR
import cv2
import numpy as np
import io
import os
import random
import string
from hackathon1 import perform_ocr
# Use the correct path to the students_results.json file on your system
file_path = "C:/Users/Nowshinfarhana/Desktop/STREAM_LIT/students_results.json"

# Check if the file exists
if os.path.exists(file_path):
    with open(file_path, "r") as file:
        student_data = json.load(file)
else:
    st.error("Student data file not found. Please upload the correct file.")

# Configure the API key for Google Generative AI
API_KEY = 'AIzaSyAUSSO25YP1c-ETuiQaUSiVomYlezDuLqc'
ai.configure(api_key=API_KEY)

# Set up PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# Set up the title and header
st.title("RGUKT File Converter & Chatbot")
st.header("Hello RGUKT!")

# --------------------- Section 1: File Upload and Conversion -------------------------
st.subheader("Image OCR")

# File upload section
uploaded_file = st.file_uploader("Upload Your Image File", type=["jpg", "jpeg", "png"])

# Initialize variables for extracted data
extracted_data = None
json_data = None

# Step 1: Perform OCR and convert to JSON
# Step 1: Perform OCR and convert to JSON
if st.button("Extract Text to JSON"):
    if uploaded_file is not None:
        image_path = uploaded_file.name

        with st.spinner("Extracting text from the image..."):
            output_img, output = perform_ocr(uploaded_file)  # Pass the uploaded file directly
            
            # Convert to JSON
            json_data = json.dumps(output, indent=4)
            st.success("Text successfully extracted and converted to JSON!")

        # Show preview of JSON content
        st.subheader("Preview of Extracted JSON Data:")
        st.json(json_data)
        
        # Display the uploaded image
        st.subheader("Uploaded Image Preview:")
        st.image(output_img, caption="Uploaded Image", use_column_width=True)
    else:
        st.warning("Please upload an image file first.")

# --------------------- Download JSON Section -------------------------
if json_data is not None:
    st.download_button(
        label="Download JSON",
        data=json_data,
        file_name="extracted_data.json",
        mime="application/json",
        key="download_json"  # Unique key to prevent conflicts
    )

# --------------------- Section 2: Chatbot -------------------------
st.markdown("<br><br>", unsafe_allow_html=True)

st.subheader("Chat with the Bot")

# Chatbot section integrated with student results
if st.button("Start Chat"):
    st.session_state.chat_active = True

if 'chat_active' in st.session_state and st.session_state.chat_active:
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    if 'chat_session' not in st.session_state:
        st.session_state.chat_session = ai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            }
        ).start_chat(history=st.session_state.chat_history)

    # Chat Interface with Student Data Access
    st.subheader("Ask about student results")

    user_input = st.text_input("You:", "")

    # Function to get all student names
    def get_all_student_names():
        names = [student['student_name'] for student in student_data['students']]
        return names

    # Function to get highest and lowest marks across all students
    def get_highest_lowest_marks():
        highest_marks = 0
        lowest_marks = 100
        for student in student_data["students"]:
            for subject in student["subjects"]:
                marks = int(subject["marks"])
                if marks > highest_marks:
                    highest_marks = marks
                if marks < lowest_marks:
                    lowest_marks = marks
        return highest_marks, lowest_marks

    # Function to get average marks across all students
    def get_average_marks():
        total_marks = 0
        total_subjects = 0
        for student in student_data["students"]:
            for subject in student["subjects"]:
                total_marks += int(subject["marks"])
                total_subjects += 1
        return total_marks / total_subjects if total_subjects > 0 else 0

    # Function to get the highest marks for a specific student
    def get_student_highest_marks(student_name):
        for student in student_data["students"]:
            if student_name.lower() in student["student_name"].lower():
                highest_marks = max(int(subject["marks"]) for subject in student["subjects"])
                return highest_marks
        return None

    if user_input:
        response = ""

        # Handle queries related to highest marks
        if "highest marks" in user_input.lower():
            highest_marks, _ = get_highest_lowest_marks()
            response = f"The highest marks across all students is {highest_marks}."

        # Handle queries related to lowest marks
        elif "lowest marks" in user_input.lower():
            _, lowest_marks = get_highest_lowest_marks()
            response = f"The lowest marks across all students is {lowest_marks}."

        # Handle queries related to average marks
        elif "average marks" in user_input.lower():
            average_marks = get_average_marks()
            response = f"The average marks across all students is {average_marks:.2f}."

        # Handle queries for highest marks of a specific student
        elif "highest marks got by" in user_input.lower():
            for name in get_all_student_names():
                if name.lower() in user_input.lower():
                    highest_marks = get_student_highest_marks(name)
                    response = f"The highest marks got by {name} is {highest_marks}."
                    break
            if not response:
                response = "Sorry, I couldn't find that student."

        # Handle queries to list all student names
        elif "names of all students" in user_input.lower():
            names = get_all_student_names()
            response = "The names of all students are: " + ", ".join(names)

        # Handle queries related to a specific student's details
        else:
            for student in student_data["students"]:
                if student["student_name"].lower() in user_input.lower() or student["registration_number"] in user_input:
                    response += f"Student: {student['student_name']}, Registration Number: {student['registration_number']}\n"
                    for subject in student['subjects']:
                        response += f"{subject['subject']}: {subject['marks']} marks\n"
                    response += f"Total Marks: {student['total_marks']}, Grade: {student['grade']}\n"
                    response += f"Exam Center: {student['exam_center']}\n\n"
        
        # If no specific student data is found, forward the query to the generative AI model
        if not response:
            response = st.session_state.chat_session.send_message(user_input).text

        st.session_state.chat_history.append({"user": user_input, "bot": response})

        for chat in st.session_state.chat_history:
            st.write(f"You: {chat['user']}")
            st.write(f"Bot: {chat['bot']}")

    if st.button("End Chat"):
        st.session_state.chat_active = False

# --------------------- Conversion Section After Chat -------------------------
# --------------------- Conversion Section After Chat -------------------------
# Streamlit app title
st.title("Convert Extracted JSON to CSV/Excel")

# Store the extracted JSON data in session state to persist across interactions
if json_data is not None and "json_data" not in st.session_state:
    st.session_state.json_data = json_data  # Save extracted JSON data in session state

# Ensure json_data is retrieved from session state
if "json_data" in st.session_state:
    json_data = st.session_state.json_data
    
    # Step 1: Convert JSON to DataFrame
    try:
        # Convert JSON data (from OCR) to a Python object
        json_dict = json.loads(json_data)  # Parse the JSON string into a Python dictionary
        
        # Normalize JSON data to a flat table (DataFrame)
        df = pd.json_normalize(json_dict)

        st.success("JSON data loaded successfully!")

        # Display the DataFrame in the app
        st.subheader("Preview of the DataFrame:")
        st.dataframe(df)

        # Step 2: User selects the output format
        conversion_format = st.selectbox("Choose the format for conversion:", ["Select", "CSV", "Excel"])

        # Step 3: Convert and provide download button
        if conversion_format == "CSV":
            # Convert DataFrame to CSV
            csv = df.to_csv(index=False)
            
            # Create a download button for the CSV file
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="converted_file.csv",
                mime="text/csv"
            )

        elif conversion_format == "Excel":
            # Convert DataFrame to Excel
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
            
            # Create a download button for the Excel file
            st.download_button(
                label="Download Excel",
                data=output.getvalue(),
                file_name="converted_file.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"Error converting JSON data: {e}")
else:
    st.info("Please extract text to JSON first before converting.")


# --------------------- API Key Management Section -------------------------
st.markdown("<br><br>", unsafe_allow_html=True)

st.sidebar.header("API Key Management & Access")

# Sample storage for API keys (you can replace this with a database)
api_keys_db = "api_keys.json"

# Load existing API keys from a JSON file
def load_api_keys():
    if not os.path.exists(api_keys_db):
        return {}
    with open(api_keys_db, "r") as f:
        return json.load(f)

# Save API keys to a JSON file
def save_api_keys(api_keys):
    with open(api_keys_db, "w") as f:
        json.dump(api_keys, f)

# Generate a unique API key
def generate_api_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

# Load the API keys database
api_keys = load_api_keys()

# Sidebar navigation for different sections
app_mode = st.sidebar.selectbox("Choose the mode", ["Generate API Key", "Access via API Key"])

# 1. API Key Generation Section
if app_mode == "Generate API Key":
    st.header("API Key Management")
    user_id = st.text_input("Enter your username to manage API keys:")
    
    if st.button("Generate API Key"):
        if user_id:
            api_keys = load_api_keys()
            if user_id not in api_keys:
                # Generate a new API key for the user
                new_api_key = generate_api_key()
                api_keys[user_id] = new_api_key
                save_api_keys(api_keys)
                st.success(f"API Key generated for {user_id}: {new_api_key}")
            else:
                st.warning(f"API Key already exists for {user_id}: {api_keys[user_id]}")
        else:
            st.warning("Please enter a valid username.")
    
    # Option to display existing keys for the user
    if st.button("Show Existing API Key"):
        api_keys = load_api_keys()
        if user_id:
            if user_id in api_keys:
                st.info(f"Your existing API key is: {api_keys[user_id]}")
            else:
                st.warning(f"No API key found for {user_id}. Please generate one first.")
        else:
            st.warning("Please enter a valid username.")

# 2. API Key Validation and Access Section
elif app_mode == "Access via API Key":
    st.header("Access Functionality Using API Key")
    
    # Step 1: Prompt user to enter their API key for validation
    api_key_input = st.text_input("Enter your API Key:")
    
    # Step 2: Check if the entered API key is valid
    if api_key_input:
        if api_key_input in api_keys.values():
            st.success("API Key validated!")
            # Store the valid API key in session state
            st.session_state["api_key"] = api_key_input
            
            # Proceed with the file upload or chatbot functionality
            st.write("Proceed with file upload or chatbot interactions below.")
            
            # Example of file upload
            uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "csv"])
            if uploaded_file is not None:
                st.write(f"File {uploaded_file.name} uploaded successfully!")
                
                # Further processing based on uploaded file can go here...
            
            # Example of chatbot interaction (just a placeholder)
            chatbot_input = st.text_input("Chat with the bot:")
            if chatbot_input:
                st.write(f"Bot response: You said '{chatbot_input}'")
        
        else:
            st.error("Invalid API Key. Please enter a valid one.")
            if "api_key" in st.session_state:
                del st.session_state["api_key"]  # Clear session key if validation fails
    else:
        st.warning("Please enter an API Key to continue.")

# CSS for customizing button colors
st.markdown("""
<style>
div.stButton > button {
    background-color: #4CAF50; /* Green */
    color: white;
    border: none;
    padding: 10px 20px;
    margin-top: 20px;
    cursor: pointer;
    border-radius: 5px;
}
div.stButton > button:hover {
    background-color: #45a049; /* Darker green */
}
</style>
""", unsafe_allow_html=True)
