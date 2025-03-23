from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import random
from selenium.webdriver.chrome.options import Options
import time
from utils import news_categories, sports_category


class BBCNewsScrapper():
    def __init__(self):
        """Initialize the driver"""
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(options=options)
        self.timeout = 30


    def scroll_to_bottom(self):
        """
        Scroll to the bottom of page because of lazy loading images. 
        A timeout of 30 seconds is used to handle infinite loading. 
        """
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        start_time = time.time()  # Record the start time

        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randint(1, 3)) 

            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break  # Stop scrolling if no more content loads

            # Check if timeout has been reached
            if time.time() - start_time > self.timeout:
                print("Timeout reached while scrolling!")
                break  

            last_height = new_height

    
    def get_news(self, category=""):
        """
        Scrapes news data from the BBC website based on the provided category.

        This function will navigate to the appropriate section of the BBC website (home, news, business, etc.)
        and extract the headline, description, image URL, news link, last updated time, and tag for each news card
        on the page. The extracted data is returned as a list of dictionaries.

        Args:
            category (str): The category of news to scrape. Possible values include:
                        "news", "business", "innovation", "culture", "arts", "travel", "future-planet".

        Returns:
            list: A list of dictionaries containing the extracted data for each news card.
                Each dictionary contains the keys: "headline", "description", "image_url", "news_link", 
                "last_updated", and "tag".
        """
        if category not in news_categories:
            return

        url = f"https://www.bbc.com/{category}"
        self.driver.get(url)

        # scroll to the bottom of page
        self.scroll_to_bottom()

        wait = WebDriverWait(self.driver, random.randint(15, 18))
        cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="dundee-card"]')))

        card_data = []

        # Loop through each card and extract relevant data
        for card in cards:
            # If headline is not present then its not a news
            headline = self.get_element_text(card, './/h2[@data-testid="card-headline"]')
            print(category, headline)
            if not headline:
                continue
            description = self.get_element_text(card, './/p[@data-testid="card-description"]')  # Use correct XPath for description
            image_url = self.get_element_attribute(card, './/div[@data-testid="card-image-wrapper"]//img', 'src')
            news_link = self.get_element_attribute(card, './/a[@data-testid="internal-link"]', 'href')
            last_updated = self.get_element_text(card, './/span[@data-testid="card-metadata-lastupdated"]')
            tag = self.get_element_text(card, './/span[@data-testid="card-metadata-tag"]')
            
            card_data.append({
                "headline": headline,
                "description": description,
                "image_url": image_url,
                "news_link": news_link,
                "last_updated": last_updated,
                "tag": tag
            })

        return card_data


    def get_sports_news(self, category=""):
        """
        Scrapes sports news from BBC Sport based on the given category.

        This method navigates to the BBC Sport page corresponding to the provided category (e.g., football, cricket) 
        and extracts headlines, news links, and image URLs from promotional elements on the page.

        Args:
        category (str): The category of sports news to fetch. Available options are:
                    "", "football", "cricket", "formula1", "rugby-union", "tennis", 
                    "golf", "athletics", "cycling". Defaults to an empty string, which fetches the general sports page.

        Returns:
        list: A list of dictionaries containing extracted data for each sports card on the page. Each dictionary contains:
            - "headline" (str): The headline of the sports news article.
            - "news_link" (str): The URL of the news article.
            - "image_url" (str, optional): The URL of the image associated with the article (if available).
            - "tag" (str, optional): The tag of the news associated with the article (if available).
            - "last_updated" (str): date on which the news was posted
        """
        if category not in sports_category:
            return

        url = f"https://www.bbc.com/sport/{category}"  
        self.driver.get(url)

        wait = WebDriverWait(self.driver, random.randint(9, 12))
        # Wait until promo elements are present
        sports_cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.ssrcss-1va2pun-UncontainedPromoWrapper')))

        # Initialize a list to store the extracted data
        sports_data = []

        for card in sports_cards:
            # If we dont get the headline, then its not a news 
            headline = self.get_element_text(card, ".//*[contains(@class, 'PromoHeadline')]")
            if not headline:
                continue

            news_link = self.get_element_attribute(card, ".//*[contains(@class, 'PromoLink')]", 'href')
            image_url = self.get_element_attribute(card, ".//*[contains(@class, 'ImageWrapper')]//img", 'src')
            tag = self.get_element_text(card, ".//ul[contains(@class, 'MetadataStripContainer')]//li[1]//a//span")
            last_updated = self.get_element_text(card, ".//ul[contains(@class, 'MetadataStripContainer')]//div[contains(@class, 'GroupChildrenForWrapping')]//li//span[@aria-hidden='true']")
            
            sports_data.append({
                "headline": headline,
                "news_link": news_link,
                "image_url": image_url,
                "tag": tag,
                "last_updated": last_updated
            })

        return sports_data
    
    def get_element_text(self, element, xpath):
        """Helper method to get text from an element safely."""
        try:
            return element.find_element(By.XPATH, xpath).text
        except NoSuchElementException:
            return None

    def get_element_attribute(self, element, xpath, attribute):
        """Helper method to get an attribute value from an element safely."""
        try:
            return element.find_element(By.XPATH, xpath).get_attribute(attribute)
        except NoSuchElementException:
            return None

    

    def close_driver(self):
        """Close the WebDriver."""
        if self.driver:
            self.driver.quit()

