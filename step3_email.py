import smtplib
import ssl
import annasAPIkeys

def send_test_email():
    """
    Connects to Gmail's SMTP server and sends a simple test email.
    """

    # --- Get credentials from your keys file ---
    sender_email = annasAPIkeys.SENDER_EMAIL
    receiver_email = annasAPIkeys.RECEIVER_EMAIL
    password = annasAPIkeys.SENDER_APP_PASSWORD

    if not sender_email or not receiver_email or not password:
        print("Error: Email credentials not found in annasAPIkeys.py")
        return

    # --- Email settings ---
    smtp_server = "smtp.gmail.com"
    port = 465  # For SSL connection

    # --- Create the email message ---
    subject = "Test Email from Python"
    body = "Hello! This is a test email from the AI Newsletter script."

    # The 'f' string formats the email correctly with headers
    message = f"Subject: {subject}\n\n{body}"

    # Create a secure SSL context
    context = ssl.create_default_context()

    print(f"Connecting to Gmail server to send test email to {receiver_email}...")

    try:
        # Connect to the server and send the email
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            print("Login successful.")
            server.sendmail(sender_email, receiver_email, message)
            print("✅ Success! Email sent.")

    except smtplib.SMTPAuthenticationError:
        print("❌ Authentication Error: Invalid email or App Password.")
        print("   Please check your SENDER_EMAIL and SENDER_APP_PASSWORD.")
    except Exception as e:
        print(f"\n❌ An error occurred:")
        print(e)

# --- Main part of the script ---
if __name__ == "__main__":
    send_test_email()