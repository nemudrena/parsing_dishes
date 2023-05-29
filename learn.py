import requests
from bs4 import BeautifulSoup
import re
import csv

# Завтрак
url = [['https://1000.menu/catalog/salaty/', 'salads'], ['https://1000.menu/catalog/desert/', 'deserts'],
       ['https://1000.menu/catalog/vtoroe-bludo/', 'goryachee'], ['https://1000.menu/catalog/supj/', 'soup'],
       ['https://1000.menu/catalog/vjpechka/', 'vypechka'], ['https://1000.menu/catalog/kasha-recipes/', 'kasha'],
       ['https://1000.menu/catalog/tvorog/', 'tvorog']]
url0 = 'https://1000.menu'

list_of_ingredients = []
ingredients_of_dishes = []
name_of_dishes = []
href_of_dishes = []
kbgu_dishes = []
anons_dishes = []
type_of_dish = []
for j in url:
    for b in range(1, 3):
        print(j[1], str(b))
        site = j[0] + str(b)
        response = requests.get(site)
        bf = BeautifulSoup(response.text, 'lxml')
        catalog = bf.find_all('div', class_='info-preview')
        for i in range(len(catalog)):
            href_dish = catalog[i].find('a', class_='h5')
            site_catalog = url0 + href_dish['href']
            response = requests.get(site_catalog)
            site_of_dish = BeautifulSoup(response.text, 'lxml')

            dish_name = site_of_dish.find('h1')

            ingredients = site_of_dish.find_all('div', class_='list-column align-top')
            if ingredients:
                href_of_dishes.append(site_catalog)
                name_of_dishes.append(dish_name.text)
                for k in range(len(ingredients)):
                    ing = ingredients[k].find('a', class_='name')
                    list_of_ingredients.append(ing.text)
                info_weight = site_of_dish.find('select', id='nutr_port_calc_switch')
                weight_dish = info_weight.find('option')
                weight_dish = weight_dish.text
                weight_dish = re.findall("\d+", weight_dish)[0]
                kbgu_dish = []
                kallor_dish = site_of_dish.find('span', id='nutr_kcal')
                kbgu_dish.append(round(int(kallor_dish.text) / 100 * int(weight_dish)))
                b_dish = site_of_dish.find('span', id='nutr_ratio_p')
                kbgu_dish.append(round(int(b_dish.text) / 100 * int(weight_dish)))
                g_dish = site_of_dish.find('span', id='nutr_ratio_f')
                kbgu_dish.append(round(int(g_dish.text) / 100 * int(weight_dish)))
                u_dish = site_of_dish.find('span', id='nutr_ratio_c')
                kbgu_dish.append(round(int(u_dish.text) / 100 * int(weight_dish)))
                kbgu_dishes.append(kbgu_dish)

                type_of_dish.append(j[1])

                ingredients_of_dishes.append(list_of_ingredients)

                list_of_ingredients = []
                kbgu_dish = []

with open("info_test_salad_3.csv", mode="w", encoding='utf-8') as w_file:
    file_writer = csv.writer(w_file, delimiter="\\", lineterminator="\r")
    for i in range(len(name_of_dishes)):
        for j in range(len(ingredients_of_dishes[i])):
            print(name_of_dishes[i], ingredients_of_dishes[i][j])
            file_writer.writerow([name_of_dishes[i], ingredients_of_dishes[i][j]])

temp = ['type']
for i in range(len(ingredients_of_dishes)):
    for j in range(len(ingredients_of_dishes[i])):
        if ingredients_of_dishes[i][j] not in temp:
            temp.append(ingredients_of_dishes[i][j])

list_of_rows = []
for i in range(len(name_of_dishes)):
    list_of_points = [type_of_dish[i]]
    for mark_ingredient in temp[1:]:
        if mark_ingredient in ingredients_of_dishes[i]:
            list_of_points.append(1)
        else:
            list_of_points.append(0)
    list_of_rows.append(list_of_points)

with open("test_salad_3.csv", mode="w", encoding='utf-8') as w_file:
    file_writer = csv.writer(w_file, delimiter="\\", lineterminator="\r")
    file_writer.writerow(temp)
    for i in range(len(list_of_rows)):
        file_writer.writerow(list_of_rows[i])
