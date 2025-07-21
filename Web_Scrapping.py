from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# ✅ Twitter Login Credentials (Replace with your details)
TWITTER_USERNAME = #########
TWITTER_PASSWORD = ##########

# ✅ Setup Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")  
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)  # Explicit wait

def login_twitter():
    """Logs into Twitter using Selenium."""
    driver.get("https://twitter.com/login")
    time.sleep(5)

    # ✅ Step 1: Enter Username
    try:
        username_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@autocomplete='username']")))
        username_input.send_keys(TWITTER_USERNAME)
        username_input.send_keys(Keys.RETURN)
    except Exception as e:
        print("❌ Error entering username:", e)
        driver.quit()

    time.sleep(3)  # Wait for next step

    # ✅ Step 2: Enter Password
    try:
        password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        password_input.send_keys(TWITTER_PASSWORD)
        password_input.send_keys(Keys.RETURN)
    except Exception as e:
        print("❌ Error entering password:", e)
        driver.quit()

    time.sleep(5)  # Allow login

def scrape_tweets(query, label, num_tweets=300):
    """
    Scrapes tweets for a given search query and assigns a label.
    
    Parameters:
    - query: Search keyword
    - label: 1 for suicidal, 0 for non-suicidal
    - num_tweets: Number of tweets to scrape
    
    Returns:
    - A list of (User ID, Tweet, Label) tuples.
    """
    driver.get(f"https://twitter.com/search?q={query}&f=live")
    time.sleep(5)

    tweets_data = []

    for _ in range(10):  # Scroll 10 times
        tweet_elements = driver.find_elements(By.XPATH, '//div[@data-testid="tweetText"]')
        user_handles = driver.find_elements(By.XPATH, '//div[@data-testid="User-Name"]//span')

        for tweet, user in zip(tweet_elements, user_handles):
            tweets_data.append((user.text, tweet.text, label))  # Store (User ID, Tweet, Label)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        if len(tweets_data) >= num_tweets:
            break

    return tweets_data

if __name__ == "__main__":
    login_twitter()

    # ✅ Scrape Suicidal Tweets (Label: 1)
    suicidal_keywords = "suicidal OR depression OR feeling hopeless OR I want to die"
    suicidal_tweets = scrape_tweets(suicidal_keywords, label="Suicidal", num_tweets=300)

    # ✅ Scrape Non-Suicidal Tweets (Label: 0)
    non_suicidal_keywords = "happy OR excited OR feeling great OR life is amazing"
    non_suicidal_tweets = scrape_tweets(non_suicidal_keywords, label="Non-Suicidal", num_tweets=300)

    # ✅ Merge Data & Save to CSV
    all_tweets = suicidal_tweets + non_suicidal_tweets
    df = pd.DataFrame(all_tweets, columns=["User ID", "Tweet", "Label"])
    df.to_csv("labeled_tweets.csv", index=False)
    print("✅ Scraped & Labeled tweets saved as 'labeled_tweets.csv'")

    driver.quit()
