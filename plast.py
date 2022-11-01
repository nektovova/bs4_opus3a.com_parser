from cgi import print_exception
import requests
from bs4 import BeautifulSoup
import re
import dop_functions

# вызовем функцию получения списка url
urls = dop_functions.get_url_list()


# итерируем по списку и парсим все категории

index = 1
for url in urls:
    print('===')
    print('new_category: ' + str(index) + ' from ' + str(len(urls)))
    dop_functions.parse_all_items_in_category(url, False)
    index=index+1


# dop_functions.parse_all_items_in_category('mtu/klasik-muzik-vihuela/2cbbd6340abed0563c1a1dd2d53e7f3a', False)

# Надо решить с этим проблему
# Rachmaninoff Preludes - tudes-Tableaux - Moments Musicaux

# и решить:
# запись в бд тех кого уже спарсили, категория если полностью закачана. И задавать в параметры, парсить с ноля или нет.Чистить бд или нет.
'''
    что нужно еще сделать:
- Все собрать страницы по которым мы будем ходить - ГОТОВО
- Перебирать их для старта скрипта. Может тут уже получится в функцию завернуть всю конструкцию - ГОТОВО
- Добавление в бд и проверка на дубли 
- Если что-то пропало, то мы должны это удалять из своей бд
- Если что-то изменило цену, то мы должны поменять цену
'''

