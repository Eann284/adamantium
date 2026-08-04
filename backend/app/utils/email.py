import os
import yagmail
from dotenv import load_dotenv, find_dotenv

# ✅ Load .env from the correct location
load_dotenv(find_dotenv())

def send_release_email(technician_email, technician_name, mrf_id, release_by, items):
    
    username = os.getenv("MAIL_USERNAME")
    password = os.getenv("MAIL_PASSWORD")
    print(f"MAIL_USERNAME: {username}")
    print(f"MAIL_PASSWORD: {'*' * len(password) if password else 'NOT SET'}")

    if not username or not password:
        print("Email credentials missing. Check your .env file.")
        return

    items_list = "\n".join([
        f"Product ID: {item['product_id']} | Quantity: {item['quantity']}"
        for item in items
    ])
    
    subject = f"Material Request {mrf_id} has been Released!"
    
    body = f"""
Dear {technician_name},

Your material request has been released by {release_by}.

MRF ID: {mrf_id}
Released by: {release_by}

Items Released:
{items_list}

Please proceed to the warehouse to collect your items.

Thank you,
Inventory Management System
    """
    try:
        yag = yagmail.SMTP(
            user=username,
            password=password,
            host="smtp.gmail.com",
            port=587,
            smtp_starttls=True,
            smtp_ssl=False
        )
        yag.send(to=technician_email, subject=subject, contents=body)
        print(f"Email sent to {technician_email}")
    except Exception as e:
        print(f"Email error: {e}")