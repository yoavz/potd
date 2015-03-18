import requests
import pprint
import time

BASE_URL = 'https://api.instagram.com/v1/users/'
CLIENT_ID = '3641224112654af7b0cc37d58b60b6ce'
PIZZA_ID = '264145867'

def fetch(user_id, client_id, url=None):

    params = {
        "client_id": client_id
    }

    if not url:
        url = BASE_URL + user_id + '/media/recent/'

    r = requests.get(url, params=params)
    return r.json()


def organize(payload, log=True):

    data = payload.get('data')
    if not data:
        print 'No data field'
        return {}


    def prune(o):
        wanted = [ "filter", "tags", "id", "location", "created_time", "link", "caption", "likes", "images" ]
        return { k: o.get(k) for k in wanted }

    images = [ prune(o) for o in data if o.get("type") == "image" ]
    if log:
        print 'organized images: ' + str(len(images))

    return images

def fetch_all(user_id, client_id):

    data = []
    url = None

    while (True):
        raw = fetch(user_id, client_id, url)
        data += organize(raw)

        if raw.get("pagination") and raw.get("pagination").get("next_url"):
            url = raw.get("pagination").get("next_url")
            print "next url: " + url
            time.sleep(1)
        else:
            break

    return data

    

if __name__ == '__main__':

    data = fetch_all(PIZZA_ID, CLIENT_ID)
    data = sorted(data, key=lambda p: p.get("created_time"), reverse=True)

    import json
    with open('pizzas.json', 'w') as outfile:
        json.dump(data, outfile, encoding="utf-8")

    print "Got " + str(len(data)) + " pizza data"
    print "Most recent pizza: " + data[0]["created_time"]
    print "Oldest pizza: " + data[-1]["created_time"]


