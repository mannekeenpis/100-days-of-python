from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from urllib.request import urlopen, Request
from selenium.webdriver.chrome.options import Options
import time
import os


class TwitterBot:
    def __init__(self, driver_path):
        self.driver = webdriver.Chrome(executable_path=driver_path)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

    def find_by_hashtag(self, hashtag, no_of_images=10):
        url = f"https://twitter.com/hashtag/{hashtag}"
        self.__find_images_by_url(url, no_of_images)

    def find_by_username(self, username, no_of_images=10):
        url = f"https://twitter.com/{username}"
        self.__find_images_by_url(url, no_of_images)

    def find_by_search(self, query, no_of_images=10):
        url = f"https://twitter.com/search?q={query}"
        self.__find_images_by_url(url, no_of_images)

    def __find_images_by_url(self, url, no_of_images):
        self.driver.get(url)
        time.sleep(16)
        image_links = set()
        while no_of_images > len(image_links):
            # Select img tags
            img_tags = self.driver.find_elements_by_css_selector(
                '[aria-label="Image"] img')

            # Extract image links
            for element in img_tags:
                link = element.get_attribute('src').split('&name')[0]
                image_links.add(link)

            # Scroll
            self.driver.execute_script(
                'window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(3)
            print(f"{len(image_links)} images found.")

        # Create Directory and download the image
        print("Downloading Started.")
        self.__create_directory()
        for link in image_links:
            self.__download_image(link)

    def __create_directory(self, dir_name='Images'):
        if not os.path.isdir('Images'):
            os.mkdir("Images")

    def __download_image(self, url):
        file_name = os.path.basename(url).replace('?format=', '.')
        local_file = open(os.path.join("Images", file_name), 'wb')
        req = Request(url=url, headers=self.headers)
        with urlopen(req) as response:
            local_file.write(response.read())
        print(f"{file_name} is downloaded.")

    def close(self):
        self.driver.close()
