# import requests module
import requests

username = 'Altec92'
page = "https://api.discogs.com/users/{}/inventory?page=1&per_page=50".format(username)


# парсим все пластинки юзера
while page != None:
    print(page)
    # Making a get request
    response = requests.get(page)
    listings = response.json()['listings']
    for listing in listings:
        id = listing['id']
        condition = listing['condition']
        sleeve_condition = listing['sleeve_condition']
        comments = listing['comments']
        price = listing['price']['value']
        # release
        thumbnail = listing['release']['thumbnail']
        description = listing['release']['description']
        images = listing['release']['images']
        artist = listing['release']['artist']
        realese_format = listing['release']['format']
        resource_url = listing['release']['resource_url']
        title = listing['release']['title']
        year = listing['release']['year']
        release_id = listing['release']['id']
        print(id)
    try:
        page = response.json()['pagination']['urls']['next']
    except:
        page = None
