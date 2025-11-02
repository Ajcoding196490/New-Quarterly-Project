import os
import requests
import annasAPIkeys
import smtplib
import ssl
from openai import OpenAI

# --- Setup OpenAI Client ---
# Load the key and initialize the client once
try:
    openai_client = OpenAI(
        api_key=annasAPIkeys.OPENAI_API_KEY
    )
    print("OpenAI client initialized.")
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    openai_client = None

# ======================================================================
#  PHASE 1: FETCH ARTICLES
# ======================================================================

def fetch_top_articles(api_key, topic, article_count=3):
    """
    Fetches the top articles for a given topic from the NewsAPI.
    (Using the /top-headlines endpoint for the free plan)
    """
    url = (f"https://newsapi.org/v2/top-headlines?"
           f"q={topic}&"
           f"pageSize={article_count}&"
           f"apiKey={api_key}")

    print(f"Fetching articles for '{topic}'...")
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                articles = data.get("articles", [])
                print(f"Successfully fetched {len(articles)} articles.")
                return articles
            else:
                print(f"NewsAPI Error: {data.get('message')}")
                return []
        else:
            print(f"HTTP Error: Received status code {response.status_code}")
            return []
    except Exception as e:
        print(f"Error connecting to NewsAPI: {e}")
        return []

# ======================================================================
#  PHASE 2: SUMMARIZE ARTICLE
# ======================================================================

def summarize_article(article_content):
    """
    Sends article content to OpenAI for summarization.
    """
    if not openai_client:
        print("OpenAI client is not initialized. Skipping summary.")
        return "Could not summarize."

    # Use the article description or content provided by NewsAPI
    # We ask for a "one-sentence" summary to keep the email clean
    PROMPT = f"""
    Please summarize the following news article snippet in one concise sentence:
    ---
    {article_content}
    ---
    """
    
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": PROMPT}
            ]
        )
        summary = response.choices[0].message.content
        return summary
    except Exception as e:
        print(f"Error during summarization: {e}")
        return "Could not summarize article."

# ======================================================================
#  PHASE 3: SEND EMAIL
# ======================================================================

def send_email(subject, email_body):
    """
    Connects to Gmail's SMTP server and sends the email.
    """
    sender_email = annasAPIkeys.SENDER_EMAIL
    receiver_email = annasAPIkeys.RECEIVER_EMAIL
    password = annasAPIkeys.SENDER_APP_PASSWORD

    smtp_server = "smtp.gmail.com"
    port = 465  # For SSL

    # Format the email message with headers (important for it to work!)
    # We must use .encode('utf-8') to handle any special characters
    message = f"Subject: {subject}\n\n{email_body}".encode('utf-8')

    context = ssl.create_default_context()

    print(f"Connecting to email server to send to {receiver_email}...")
    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
            print("✅✅✅ Email sent successfully!")
            
    except Exception as e:
        print(f"❌ Error sending email: {e}")


# ======================================================================
#  MAIN SCRIPT EXECUTION
# ======================================================================

def main():
    TOPIC = "artificial intelligence"
    
    # --- Step 1: Fetch ---
    articles = fetch_top_articles(annasAPIkeys.NEWS_API_KEY, TOPIC)
    
    if not articles:
        print("No articles found. Exiting.")
        return

    # --- Step 2 & 3: Summarize & Format ---
    
    # Start building the email body
    email_content = f"Here is your AI News update for {TOPIC}:\n"
    email_content += "=========================================\n\n"
    
    for i, article in enumerate(articles):
        print(f"Summarizing article {i+1}...")
        
        # Get the title, URL, and description
        title = article.get('title')
        url = article.get('url')
        
        # Use 'description' or 'content' for the summary.
        # Fallback to a blank string if both are missing.
        content_to_summarize = article.get('description') or article.get('content') or ""

        if not content_to_summarize:
            summary = "No content available to summarize."
        else:
            summary = summarize_article(content_to_summarize)
        
        # Add this article to our email body
        email_content += f"ARTICLE {i+1}: {title}\n"
        email_content += f"SUMMARY: {summary}\n"
        email_content += f"LINK: {url}\n\n"
        email_content += "-----------------------------------------\n\n"

    print("\n--- Final Email Content ---")
    print(email_content)
    print("---------------------------")

    # --- Step 4: Send ---
    email_subject = f"Your Daily AI News Report - {TOPIC}"
    send_email(email_subject, email_content)

if __name__ == "__main__":
    main()