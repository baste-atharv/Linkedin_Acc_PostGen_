from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv
import pickle
import os
import re

# --- CONFIG ---
LINKEDIN_PROFILE_URL = "https://www.linkedin.com/in/aarongolbin/recent-activity/all/"
SCROLL_DURATION = 5 * 60  # in seconds
COOKIES_FILE = "linkedin_cookies.pkl"
CSV_FILE = "user_posts.csv"

def launch_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def load_cookies(driver):
    if os.path.exists(COOKIES_FILE):
        print("🍪 Loading cookies...")
        cookies = pickle.load(open(COOKIES_FILE, "rb"))
        driver.get("https://www.linkedin.com")
        for cookie in cookies:
            if 'sameSite' in cookie:
                del cookie['sameSite']
            driver.add_cookie(cookie)
        driver.get("https://www.linkedin.com/feed/")
        time.sleep(3)
        print("✅ Cookies applied.")
    else:
        print("⚠️ No cookies found. Please log in manually and save them.")

def scroll_down(driver, duration=SCROLL_DURATION):
    print(f"⏬ Starting scroll for {duration // 60} minutes...")
    start = time.time()
    end = start + duration
    last_height = driver.execute_script("return document.body.scrollHeight")

    while time.time() < end:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    print("✅ Scrolling complete.")

def extract_posts(driver):
    print("📦 Extracting posts using Selenium...")
    
    # Target the scaffold-finite-scroll__content which contains all posts
    posts_container = driver.find_element(By.CSS_SELECTOR, "div.scaffold-finite-scroll__content")
    posts = posts_container.find_elements(By.CSS_SELECTOR, "li.HzDsNelEKxZBQWYVWlrFPdmLIqMRsWNDSrSdE > div")
    
    print(f"🔍 Found {len(posts)} posts")

    posts_data = []
    for idx, post in enumerate(posts):
        try:
            print(f"Processing post {idx + 1}...")
            post_data = {
                "author": "Unknown",
                "timestamp": "Unknown",
                "text": "",
                "reactions": "0",
                "comments": "0",
                "reposts": "0",
                "media_type": "",
                "has_image": False,
                "has_article": False,
                "post_url": ""
            }

            # Extract Author Information
            try:
                # Check if it's a repost first
                try:
                    repost_header = post.find_element(By.CSS_SELECTOR, "span.update-components-header__text-view")
                    if "reposted this" in repost_header.text:
                        original_poster = post.find_element(By.CSS_SELECTOR, "span.uAnjjQbIsfvUekXwiikOVdvawtVaconjnwL")
                        post_data["author"] = original_poster.text.strip()
                        post_data["reposted_by"] = repost_header.text.split(" reposted")[0].strip()
                except:
                    # Direct post
                    author_element = post.find_element(By.CSS_SELECTOR, "span.uAnjjQbIsfvUekXwiikOVdvawtVaconjnwL")
                    post_data["author"] = author_element.text.strip()
            except Exception as e:
                print(f"⚠️ Author extraction error: {e}")

            # Extract Timestamp
            try:
                timestamp_element = post.find_element(By.CSS_SELECTOR, "span.update-components-actor__sub-description")
                post_data["timestamp"] = timestamp_element.text.strip()
            except Exception as e:
                print(f"⚠️ Timestamp extraction error: {e}")

            # Extract Post Text
            try:
                text_element = post.find_element(By.CSS_SELECTOR, "div.feed-shared-inline-show-more-text")
                post_data["text"] = text_element.text.strip()
            except Exception as e:
                print(f"⚠️ Text extraction error: {e}")

            # Extract Reactions
            try:
                reactions_element = post.find_element(By.CSS_SELECTOR, "span.social-details-social-counts__reactions-count")
                post_data["reactions"] = reactions_element.text.strip()
            except Exception as e:
                print(f"⚠️ Reactions extraction error: {e}")

            # Extract Comments Count
            try:
                comments_element = post.find_element(By.CSS_SELECTOR, "li.social-details-social-counts__comments button")
                comments_text = comments_element.text.strip()
                comments_count = re.search(r'(\d+(?:,\d+)*)', comments_text)
                if comments_count:
                    post_data["comments"] = comments_count.group(1)
            except Exception as e:
                print(f"⚠️ Comments extraction error: {e}")

            # Extract Reposts Count
            try:
                reposts_element = post.find_element(By.CSS_SELECTOR, "button[aria-label*='reposts']")
                reposts_text = reposts_element.text.strip()
                reposts_count = re.search(r'(\d+(?:,\d+)*)', reposts_text)
                if reposts_count:
                    post_data["reposts"] = reposts_count.group(1)
            except Exception as e:
                print(f"⚠️ Reposts extraction error: {e}")

            # Check for images
            try:
                images = post.find_elements(By.CSS_SELECTOR, "div.update-components-image")
                if images:
                    post_data["has_image"] = True
                    post_data["media_type"] = "image"
            except Exception as e:
                print(f"⚠️ Image detection error: {e}")

            # Check for articles
            try:
                articles = post.find_elements(By.CSS_SELECTOR, "article.update-components-article")
                if articles:
                    post_data["has_article"] = True
                    post_data["media_type"] = "article"
                    
                    # Try to get article URL
                    try:
                        article_link = articles[0].find_element(By.CSS_SELECTOR, "a.update-components-article__meta")
                        post_data["post_url"] = article_link.get_attribute("href")
                    except:
                        pass
            except Exception as e:
                print(f"⚠️ Article detection error: {e}")

            posts_data.append(post_data)
            print(f"✅ Post {idx + 1} processed")

        except Exception as e:
            print(f"⚠️ Post {idx + 1} extraction error: {e}")
            continue

    print(f"✅ Extracted {len(posts_data)} structured posts.")
    return posts_data

def extract_post_full_html(driver):
    """Extract the full HTML of posts for debugging"""
    posts_container = driver.find_element(By.CSS_SELECTOR, "div.scaffold-finite-scroll__content")
    return posts_container.get_attribute('innerHTML')

def save_to_csv(posts, file_path=CSV_FILE):
    if not posts:
        print("⚠️ No posts to save.")
        return

    fieldnames = ["author", "reposted_by", "timestamp", "text", "reactions", 
                  "comments", "reposts", "media_type", "has_image", "has_article", "post_url"]
    
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(posts)
    print(f"📝 {len(posts)} posts saved to {file_path}")

def save_debug_html(html_content, file_path="linkedin_posts_debug.html"):
    """Save the HTML content for debugging purposes"""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"💾 Debug HTML saved to {file_path}")

def main():
    driver = launch_driver()
    driver.get("https://www.linkedin.com")
    time.sleep(2)

    # Load cookies and navigate
    load_cookies(driver)
    time.sleep(2)

    print(f"🔗 Navigating to profile: {LINKEDIN_PROFILE_URL}")
    driver.get(LINKEDIN_PROFILE_URL)
    time.sleep(5)

    # Scroll and extract posts
    scroll_down(driver)
    
    # Save the HTML for debugging if needed
    debug_html = extract_post_full_html(driver)
    save_debug_html(debug_html)
    
    # Extract and save post data
    posts = extract_posts(driver)
    save_to_csv(posts)
    
    driver.quit()

if __name__ == "__main__":
    main()
