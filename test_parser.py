import json
import time

from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class VkusnoITochka_parser:
	def __init__(self):
		self.yandex_base_url = "https://eda.yandex.ru"
		self.yandex_url = "https://eda.yandex.ru/Dubna?shippingType=delivery"
		self.vit_url = "https://vkusnoitochka.ru"
		
		

	def get_page(self, url):
		chrome_options = Options()
		chrome_options.add_argument("--headless")
		chrome_options.add_argument("--log-level=3")
		self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
		self.driver.set_window_size(1920, 20000)
		self.driver.get(url)
		time.sleep(1)
		html = self.driver.page_source
		self.soup = BS(html, 'lxml')

	def get_vit_menu(self):
		self.get_page(self.vit_url)
		time.sleep(1)
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
				temp_list = []
				for item in menu:
					text = str(item.find(class_='catalog-product-title').text)
					price = ' '.join([str(i.strip()) for i in item.find(class_='catalog-product__price').text.split('\n')])
					if len(temp_list) > 9:
						menu_json[selected_item].append(temp_list)
						temp_list = []
					temp_list.append([[id_category, text], price])
					id_category += 1
				menu_json[selected_item].append(temp_list)


			except:
				pass

		with open('Вкусно и точка.json', 'w', encoding='utf-8') as f:
			f.write(json.dumps(menu_json, ensure_ascii=False))


	def get_yandex_restaurants(self):
		self.get_page(self.yandex_url)
		all_restaurants = self.soup.find(class_='PlaceList_lg').find_all(class_='PlaceListBduItem_lg')
		return all_restaurants


	def get_restaurants_links_and_titles(self):
		return [[restaurant.find('a')['href'], restaurant.find(class_='NewPlaceItem_title').text] for restaurant in self.get_yandex_restaurants()]


	def parse_online_restaurants(self):
		restaurants_titles = {"restaurants": [restaurant[1] for restaurant in self.get_restaurants_links_and_titles()]}
		restaurants_titles["restaurants"].append('Вкусно и точка')
		with open("restaurants.json", "w", encoding='utf-8') as f:
			f.write(json.dumps(restaurants_titles, ensure_ascii=False))


	def get_restaurant_menu(self):
		restaurants = self.get_restaurants_links_and_titles()
		self.parse_online_restaurants()
		for restaurant in restaurants:
			self.get_page(self.yandex_base_url + restaurant[0])
			time.sleep(1)
			all_menu = dict()
			restaurant_menu = []
			i = 0
			for menu in self.soup.find_all(class_='RestaurantMenu_category'):
				catergory = menu.find('h2').text
				all_menu[catergory] = list()
				all_menu[catergory].append(i)
				i += 1
				id_category = 0
				temp_list = []
				for food in menu.find_all(class_='RestaurantMenu_item'):
					food_name = food.find(class_='UiKitDesktopProductCard_name').text
					food_price = ''.join(food.find(class_='UiKitDesktopProductCard_price').text.split()[:-1])

					if len(temp_list) > 9:
						all_menu[catergory].append(temp_list)
						temp_list = []
					temp_list.append([[id_category, food_name], food_price])
					id_category += 1
				all_menu[catergory].append(temp_list)

			with open(f"{restaurant[1].strip()}.json", "w", encoding='utf-8') as f:
				f.write(json.dumps(all_menu, ensure_ascii=False))
		
		

if __name__ == '__main__':
	p = VkusnoITochka_parser()
	p.get_vit_menu()
	p.get_restaurant_menu()
	p.driver.close()
	p.driver.quit()
	