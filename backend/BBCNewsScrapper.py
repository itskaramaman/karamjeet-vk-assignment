from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import random
from selenium.webdriver.chrome.options import Options


class BBCNewsScrapper():
    def __init__(self):
        """Initialize the driver"""
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(options=options)

    
    def get_news(self, filter=""):
        """
        Scrapes news data from the BBC website based on the provided filter.

        This function will navigate to the appropriate section of the BBC website (home, news, business, etc.)
        and extract the headline, description, image URL, news link, last updated time, and tag for each news card
        on the page. The extracted data is returned as a list of dictionaries.

        Args:
            filter (str): The category of news to scrape. Possible values include:
                        "news", "business", "innovation", "culture", "arts", "travel", "future-planet".
                        If the filter is not one of these, the function will exit without scraping.

        Returns:
            list: A list of dictionaries containing the extracted data for each news card.
                Each dictionary contains the keys: "headline", "description", "image_url", "news_link", "last_updated", and "tag".
        """

        # These are the valid urls
        valid_filters = ["", "news", "business", "innovation", "culture", "arts", "travel", "future-planet"]

        if filter not in valid_filters:
            filter = ""

        url = f"https://www.bbc.com/{filter}"
        self.driver.get(url)

        wait = WebDriverWait(self.driver, random.randint(10, 12))
        cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="dundee-card"]')))

        # Initialize a list to store extracted data
        card_data = []

        # Loop through each card and extract relevant data
        for card in cards:
            headline = card.find_element(By.CSS_SELECTOR, '[data-testid="card-headline"]').text
            description = card.find_element(By.CSS_SELECTOR, '[data-testid="card-description"]').text
            image_url = card.find_element(By.CSS_SELECTOR, '[data-testid="card-image-wrapper"] img').get_attribute('src')

            try:
                news_link = card.find_element(By.XPATH, './/a[@data-testid="internal-link"]').get_attribute('href')
            except Exception as e:
                news_link = None
            
            # Use XPath to locate the last updated time
            try:
                last_updated = card.find_element(By.XPATH, './/span[@data-testid="card-metadata-lastupdated"]').text
            except Exception as e:
                last_updated = None
            
            # Use XPath to locate the tag
            try:
                tag = card.find_element(By.XPATH, './/span[@data-testid="card-metadata-tag"]').text
            except Exception as e:
                tag = None
            
            # Append the extracted data to the list
            if headline and description:
                card_data.append({
                    "headline": headline,
                    "description": description,
                    "image_url": image_url,
                    "news_link": news_link,
                    "last_updated": last_updated,
                    "tag": tag
                })

        return card_data


    def get_sports_news(self, filter=""):
        """
        Scrapes sports news from BBC Sport based on the given filter.

        This method navigates to the BBC Sport page corresponding to the provided filter (e.g., football, cricket) 
        and extracts headlines, news links, and image URLs from promotional elements on the page.

        Args:
        filter (str): The category of sports news to fetch. Available options are:
                    "", "football", "cricket", "formula1", "rugby-union", "tennis", 
                    "golf", "athletics", "cycling". Defaults to an empty string, which fetches the general sports page.

        Returns:
        list: A list of dictionaries containing extracted data for each promo element on the page. Each dictionary contains:
            - "headline" (str): The headline of the sports news article.
            - "news_link" (str): The URL of the news article.
            - "image_url" (str, optional): The URL of the image associated with the article (if available).
        """

        valid_filters = ["", "football", "cricket", "formula1", "rugby-union", "tennis", "golf", "athletics", "cycling"]
        if filter not in valid_filters:
            filter = ""

        url = f"https://www.bbc.com/sport/{filter}"  
        self.driver.get(url)

        wait = WebDriverWait(self.driver, random.randint(9, 12))
        # Wait until promo elements are present
        promos = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.ssrcss-1va2pun-UncontainedPromoWrapper')))

        # Initialize a list to store the extracted data
        promo_data = []

        for promo in promos:
            try:
                headline = promo.find_element(By.XPATH, ".//*[contains(@class, 'PromoHeadline')]").text
            except Exception as e:
                headline = None

            try:
                news_link = promo.find_element(By.XPATH, ".//*[contains(@class, 'PromoLink')]").get_attribute('href')
            except Exception as e:
                news_link = None

            try:
                image_url = promo.find_element(By.XPATH, ".//*[contains(@class, 'ImageWrapper')]//img").get_attribute('src')
            except Exception as e:
                image_url = None
            

            if headline and news_link:
                promo_data.append({
                    "headline": headline,
                    "news_link": news_link,
                    "image_url": image_url
                })

        return promo_data
    

    def close_driver(self):
        """Close the WebDriver."""
        if self.driver:
            self.driver.quit()

