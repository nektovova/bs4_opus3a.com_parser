from cgi import print_exception
import requests
from bs4 import BeautifulSoup
import re
import db
from urllib.error import HTTPError


# функция для получения актуального списка категорий
def get_url_list():
    url = "https://www.opus3a.com/muzik-turleri"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # соберем все ссылки на странице
    links_with_text = []
    for a in soup.find_all('a', href=True): 
        if a.text:
            links_with_text.append(a['href'])

    # отфильтруем список ссылок, оставим только те что содержат mtu
    r = re.compile("\/mtu\/")
    filtered_list = list(filter(r.match, links_with_text))

    # удалим дубликаты в списке методом set
    filtered_list = list(set(filtered_list))

    # print списка
    # print(filtered_list)

    # возврат списка из функции
    return filtered_list



# функция для парсинга всех товаров в категории
def parse_all_items_in_category(category_url, need_we_check_item):
    page_number = 1
    finish_page = 1000000
    # print(need_we_check_item)

    # пока номер страницы не равен финальной страницу
    while page_number != finish_page:

        # url собирается из базы и номера страницы
        url = "https://www.opus3a.com/" + category_url + "?sayfa=" + str(page_number)
        print(url)

        page = requests.get(url)
        if page.status_code != 200:
            print('Error 403 or 404')
            return
        
        soup = BeautifulSoup(page.content, "html.parser")
        
        # чекаем случился ли редирект
        title = soup.find('title').text
        if title == 'Opus3a - Plak, LP, CD, DVD - Müzik Market':
            print('Redirected, finish')
            return

        # чекаем, может нет товаров
        no_items_in_category = soup.find('div', attrs={'style': 'font-size: 15px;'}).text.strip()
        if no_items_in_category == 'Ürün bulunmamaktadır.':
            print('Embpty category, finish')
            return

        # найдем все div товаров и положим их в список mydivs
        mydivs = soup.find_all("div", {"class": "plak-box-large"})

        # собираем из каждого div данные
        for div_element in mydivs:
            # используем блок try-exept
            try: 
                name = re.sub('\"', '', div_element.find("div", class_="plak-name wordwrap").text.strip())
                name = re.sub("\'", "''", name)
                # name = "Rachmaninoff Preludes - tudes-Tableaux - Moments Musicaux"
                # get url of item
                item_url = re.sub('.*\/', '', div_element.find_all('a', href=True)[0]['href'])

                # use lambda function (one line small function), можно объеденить эти две строки но я не буду, иначе упадет читаемость
                singer_name = div_element.find("div", class_="singer-name wordwrap")
                if singer_name == None:
                    singer_name = '-'
                else:
                    singer_name = re.sub('\"', '', singer_name.text.strip())
                    singer_name = re.sub('\'', "''", singer_name)
                
                item_format = re.sub('\"', ' inch', div_element.find("div", class_="format").text.strip())
                image = re.sub('\/MID2\/', '/max/', div_element.find('img')['src'])
                price = div_element.find("div", class_="price").text.strip()
            # если выявлена ошибка, то пока пропускаем поле
            except:
                print("Something went wrong")
                print(url)
                name = name.encode('utf-8')
                print(name)
                
            # если с данными все в порядке, то продолжаем
            else:
                # print('ok')
                '''
                print("= = = = =\n= = = = =\n= = = = =\n= = = = =\n= = = = =\n")
                print('category url:')
                print(url)
                print("= = = = =\n= = = = =\n= = = = =\n= = = = =\n= = = = =\n")
                print('item url:')
                print(item_url)
                '''
    
                if price in ('Tükendi', 'Yakında'): # останавливаем парсинг если цен больше нет.
                    # print('finish, exit loop')
                    # финиш пейдж это текущий номер страницы плюс один. То есть в следующем цикле они сравняются.
                    # если не попадается цена отсутствующая, то мы попадаем в бесконечный парсинг
                    # print(name)
                    finish_page = page_number + 1
                    break
                else:
                    # пока отключил конвертацию price в int
                    # price = int(re.sub('\..*', '', price))
                    '''
                    print(price)
                    print(name)
                    # в качестве аргумента передаем в lambda функцию наш singer_name объект
                    print(singer_name)
                    print(item_format)
                    print(image)
                    print(item_url)
                    '''

                    # если параметр нужно ли чекать = True, то
                    if need_we_check_item == True:
                        print(parse_item(item_url))
                    
                    release_year = 1000
                    barcode = '1h2h3h'

                    # добавление в базу данных
                    db.create_table()
                    try:
                        db.add_data(name, singer_name, category_url, item_format, release_year, barcode, price, item_url)
                    except:
                        print('error adding to DB')
                        print(url)
                        name = name.encode('utf-8')
                        print(name)

                    
                    #db.get_data()

                    # print('===========')
                    # функция проверки есть ли такая пластинка в бд, если есть то
                
                

        # после действий всех добавляем номеру страницы единицу
        page_number += 1



def parse_item(url):
    url = "https://www.opus3a.com" + url
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    
    description_div = soup.find("div", {"class": "product-description-properties"})
    barcode_div = description_div.find_all("div")

    # parse firma
    firma = barcode_div[0].find_all('a')[0].text.strip()
    print("firma: " + firma)

    # parse barcode and year or realese
    for item in barcode_div[0].find_all():
        if item.name=='b' and item.text=='Barkod: ':
            if item.next_element.next_element.strip()!='':
                barcode = item.next_element.next_element.strip()
                print(barcode)
        elif item.name=='b' and item.text=='Yayınlanma Tarihi: ':
            if item.next_element.next_element.strip()!='':
                release_date = item.next_element.next_element.strip()
                print(release_date)


    return

