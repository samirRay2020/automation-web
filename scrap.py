import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

# Get email credentials and recipient from environment
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")

def extract_text_by_css_selector(url, css_selector):
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, "html.parser")
    elements = soup.select(css_selector)

    results = []
    for elem in elements:
        text = elem.get_text(strip=True)
        if text:
            results.append(text)

    return results

def send_email(subject, body, to_email):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER       # 👈 your Gmail
    msg["To"] = to_email                         # 👈 recipient email

    # Use Gmail SMTP with your actual Gmail and App Password
    smtp_user = EMAIL_USER
    app_password = "abwa cptv swwl qasz"  # 🔒 Replace with your Gmail App Password

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_APP_PASSWORD)
        smtp.send_message(msg)

def date_is_after(text, target_date_str="4 June 2025"):
    try:
        date_obj = datetime.strptime(text.strip(), "%d %B %Y")
        target_date = datetime.strptime(target_date_str, "%d %B %Y")
        return date_obj > target_date
    except Exception as e:
        return False

if __name__ == "__main__":
    url = "https://www.business-humanrights.org/en/latest-news/mexico-labour-rights-petitions-submitted-under-the-united-states-mexico-canada-agreement-usmca/"
    
    # First CSS: count items
    css_selector1 = "div.block.richtext-block li"
    extracted_texts1 = extract_text_by_css_selector(url, css_selector1)
    c1 = len(extracted_texts1)
    print("\nList Items:\n")
    for item in extracted_texts1:
        print("-", item)
    print("Total:", c1)
    c1 = 35
    # Second CSS: check date
    css_selector2 = "dl.timeline-item__meta dd:not([class])"
    extracted_texts2 = extract_text_by_css_selector(url, css_selector2)
    c2_valid_date = False

    for text in extracted_texts2:
        if date_is_after(text, "4 June 2025"):
            c2_valid_date = True
            print("\nDate found after 4 June 2025:", text)
            break
  
    # Trigger email alert
    if c1 > 33 or c2_valid_date:
        subject = "⚠️ USMCA Alert: Condition Met"
        body = f"Triggered because:\n- Items count: {c1}\n- Recent date found: {c2_valid_date}"
        send_email(subject, body, EMAIL_TO)  # 👈 Change to recipient email
        print("\n📧 Email sent!")

    else:
        print("\nNo alert triggered.")
