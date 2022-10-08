from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as BS
import json
import time


class VkusnoITochka_parser:
	def __init__(self):
		chrome_options = Options()
		chrome_options.add_argument("--headless")
		chrome_options.add_argument("--log-level=3")
		self.url = "https://vkusnoitochka.ru/menu"
		self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
		self.driver.set_window_size(1920, 1080)
		self.get_page()

	
	def get_page(self):
		self.driver.get(self.url)
		time.sleep(1)
		html = self.driver.page_source
		self.soup = BS(html, 'lxml')


	def get_menu(self):
		menu = self.soup.find_all(class_='catalog-product')
		menu_items = self.soup.find_all(class_='menu-categories__item')
		driver_menu_items = self.driver.find_elements(By.CLASS_NAME, 'menu-categories__item')
		

		menu_items_titles = [item.text for item in menu_items]
		menu_json = dict()

		i=0
		for item in menu_items_titles:
			menu_json[item] = list()
			menu_json[item].append(i)
			i+=1

		for menu_item in driver_menu_items:
			try:
				menu_item.click()
				time.sleep(1/3)

				self.soup = BS(self.driver.page_source, 'lxml')
				menu = self.soup.find_all(class_='catalog-product')

				selected_item = self.soup.find(class_='menu-categories__item_selected').text
				id_category = 0
				for item in menu:
					text = str(item.find(class_='catalog-product-title').text)
					price = ' '.join([str(i.strip()) for i in item.find(class_='catalog-product__price').text.split('\n')])
					menu_json[selected_item].append([[id_category, text], price])
					id_category += 1
			except:
				pass

			with open('menu.json', 'w', encoding='utf-8') as f:
				json.dump(menu_json, f, ensure_ascii=False)

