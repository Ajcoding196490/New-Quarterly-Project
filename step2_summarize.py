import annasAPIkeys
from openai import OpenAI

# Set your API key from your keys file
# This is a different way than using .env, but just as good.
client = OpenAI(
    api_key=annasAPIkeys.OPENAI_API_KEY
)

# --- This is our sample text to test with ---
# We use triple-quotes (""") for a string that spans multiple lines
SAMPLE_ARTICLE_TEXT = """
Large language models (LLMs) are a type of artificial intelligence (AI) 
that can mimic human intelligence. They are trained on massive amounts of
text data to understand and generate language. This allows them to perform
a wide range of tasks, including translation, summarization, and writing
creative content. However, they also raise concerns about misinformation,
job displacement, and potential misuse. As the technology continues to
evolve, it is crucial for developers and policymakers to address these
ethical challenges and ensure that LLMs are used responsibly. The models
work by predicting the next word in a sequence, a simple-sounding but
computationally intensive process.
"""

# This is the prompt we send to the AI.
# We are "prompt engineering" by telling it *exactly* what we want.
PROMPT = f"""
Please summarize the following article for a newsletter in 3 concise bullet points:

---
{SAMPLE_ARTICLE_TEXT}
---
"""

print("Sending sample article to OpenAI for summarization...")

try:
    # This is the API call you mentioned
    # Note: 'gpt-5' does not exist yet. The best model to use is 'gpt-4o'
    # or 'gpt-3.5-turbo' which is cheaper and faster.
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # You can change this to "gpt-4o" if you prefer
        messages=[
            {"role": "user", "content": PROMPT}
        ]
    )
    
    # Extract the summary text from the response
    summary = response.choices[0].message.content
    
    print("\n✅ Success! Here is the summary:")
    print("---------------------------------")
    print(summary)

except Exception as e:
    print(f"\n❌ Error connecting to OpenAI:")
    print(e)