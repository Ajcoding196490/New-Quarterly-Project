import os
import requests
import annasAPIkeys

# Get the key from your custom python file
newsAPIKey = annasAPIkeys.NEWS_API_KEY
print ("Using NewsAPI Key:", newsAPIKey)


def fetch_top_articles(api_key, topic, article_count=5):
    """
    Fetches the top articles for a given topic from the NewsAPI.
    """
    
    # --- THIS IS THE FIX ---
    # We are using the /top-headlines endpoint, which is allowed on the free plan.
    # We also removed the "sortBy" parameter, which is not supported by this endpoint.
    url = (f"https://newsapi.org/v2/top-headlines?"
           f"q={topic}&"
           f"pageSize={article_count}&"
           f"apiKey={api_key}")

    print(f"Fetching articles for '{topic}'...")

    try:
        # Make the request to the API
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            
            # Check if the API status is 'ok' and articles were found
            if data.get("status") == "ok":
                articles = data.get("articles", [])
                
                if not articles:
                    print("No articles found for this topic.")
                    return []
                
                # Return the list of article objects
                return articles
            else:
                # Handle API-level errors (e.g, 'apiKeyInvalid')
                print(f"API Error: {data.get('message')}")
                return []
        else:
            # Handle HTTP errors (e.g., 404 Not Found, 401 Unauthorized)
            print(f"HTTP Error: Received status code {response.status_code}")
            
            # This part prints the specific error message from the server
            try:
                error_data = response.json()
                print(f"Server says: {error_data.get('message')}")
            except requests.exceptions.JSONDecodeError:
                print(f"Server says: {response.text}")
            return []

    except requests.exceptions.RequestException as e:
        # Handle network-level errors (e.g., connection timed out)
        print(f"Error connecting to NewsAPI: {e}")
        return []

# --- Main part of the script ---
if __name__ == "__main__":
    
    # Get the API key from the variable defined at the top
    API_KEY = newsAPIKey

    if not API_KEY:
        print("Error: NEWS_API_KEY not found.")
        print("Please make sure your annasAPIkeys.py file is correct.")
    else:
        # Define the topic you want to search for
        TOPIC_TO_SEARCH = "artificial intelligence"
        
        # Fetch the articles
        articles_list = fetch_top_articles(API_KEY, TOPIC_TO_SEARCH)
        
        if articles_list:
            print(f"\nSuccessfully fetched {len(articles_list)} articles:")
            print("-----------------------------------------------")
            
            # Loop through the articles and print their title and URL
            for i, article in enumerate(articles_list):
                print(f"\nArticle {i + 1}:")
                print(f"  Title: {article.get('title')}")
                print(f"  URL: {article.get('url')}")
                # We'll use the 'content' or 'description' for summarization later
                # print(f"  Description: {article.get('description')}")
        else:
            print("Failed to fetch articles.")