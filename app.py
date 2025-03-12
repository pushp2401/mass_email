import streamlit as st
import pandas as pd
import yagmail
import re 
import time
import os 
from dotenv import load_dotenv
load_dotenv()
sender_email = os.getenv('SENDER_EMAIL')
app_password = os.getenv('APP_PASSWORD')#soonju

# Initialize yagmail
yag = yagmail.SMTP(sender_email, app_password, host="smtp.gmail.com")  # Change host if not Gmail 



def extract_name(email):
    match = re.match(r"([a-zA-Z0-9._%+-]+)@", email)
    if match:
        name_part = match.group(1).replace(".", " ").replace("_", " ").title()
        first_name = name_part.split()[0]
        return first_name
    return None

def show_success_message(user):
    success_placeholder = st.empty()  # Create a placeholder
    success_placeholder.success(f"✅ Email sent successfully to {user}!")  # Show success message
    time.sleep(3)  # Wait for 3 seconds
    success_placeholder.empty() 
st.title("Mass cold email sender")

uploaded_file = st.file_uploader( "Upload you client list as csv here" ,type=["csv"])
if uploaded_file is not None : 
    subject_input = st.text_area("Enter mail subject:" , placeholder = "Followup regarding data science budget")
    body_input = st.text_area("Enter mail body:" , placeholder = "This mail is regarding...\nBest regards,\n Barbara Daniels")
    uploaded_pictures = st.file_uploader("Optional : Upload Images to attach : ", type=["png", "jpg", "jpeg"] , accept_multiple_files = True)
    signature_input = st.text_area("Enter email signature : " , placeholder = "\n Barbara daniels\n VP, XYZ Ltd\n +91-1234567890\nAtlanta, USA ")
    if st.button("Send mail") :
        if subject_input and body_input:
            if uploaded_file :
                file_type = uploaded_file.type
                if file_type == "text/csv" :
                    df = pd.read_csv(uploaded_file)
                    for one_mail in df['mail'] :
                        name = extract_name(one_mail)
                        full_mail_content = "Hello " + name + ",\n" + body_input + "\n" + "---------------" +  "\n\n"
                        if signature_input is not None : 
                            signature_bold = f"""
                            <html>
                                <body style="font-family: Arial, sans-serif;">
                                    <p><strong style="color: black;">{signature_input}</strong></p>
                                </body>
                            </html>
                            """
                        full_mail_content = full_mail_content + signature_bold
                        if uploaded_pictures is not None : 
                            yag.send(to = one_mail , subject = subject_input , contents = full_mail_content , attachments = uploaded_pictures)
                            show_success_message(one_mail) 
                        else :
                            yag.send(to = one_mail , subject = subject_input , contents = full_mail_content) 
                            show_success_message(one_mail) 

        else :
            st.write("Please provide mail subject and body")
