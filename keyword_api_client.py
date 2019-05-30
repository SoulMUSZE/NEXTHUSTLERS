from http.client import HTTPSConnection
from base64 import b64encode
from json import loads
from json import dumps

from credentials import SEO_LOGIN, SEO_PASSWORD

class RestClient:
    domain = "api.dataforseo.com"

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def request(self, path, method, data=None):
        connection = HTTPSConnection(self.domain)
        try:
            base64_bytes = b64encode(
                ("%s:%s" % (self.username, self.password)).encode("ascii")
                ).decode("ascii")
            headers = {'Authorization' : 'Basic %s' %  base64_bytes}
            connection.request(method, path, headers=headers, body=data)
            response = connection.getresponse()
            return loads(response.read().decode())
        finally:
            connection.close()

    def get(self, path):
        return self.request(path, 'GET')

    def post(self, path, data):
        if isinstance(data, str):
            data_str = data
        else:
            data_str = dumps(data)
        return self.request(path, 'POST', data_str)


def get_related_keywords(seed_word, depth=2, limit=15, country='US'):

    client = RestClient(SEO_LOGIN, SEO_PASSWORD)

    post_data = dict()
    # you can set as "index of post_data" your ID, string, etc. we will return it with all results.
    # post_data[random.randint(1, 30000000)] = dict(
    post_data['NEXTHUSTLERS'] = dict(
        keyword=seed_word,
        country_code=country,
        language="en",
        depth=depth,
        limit=limit,
        offset=0,
        orderby="search_volume,desc",
        filters=[
            ["cpc", ">", 0],
            "or",
            [
                ["search_volume", ">", 0],
                "and",
                ["search_volume", "<=", 10000]
            ]
        ]
    )

    response = client.post("/v2/kwrd_finder_related_keywords_get", dict(data=post_data))

    if response["status"] == "error":
        # print("error. Code: %d Message: %s" %(response["error"]["code"], response["error"]["message"]))
        # return render_template('keywords.html', keywords="API Error")
        return False
    else:
        keywords = response['results']['NEXTHUSTLERS']['related']

        if keywords == "No data":
            # return render_template('keywords.html', keywords=response['results'])
            return False
        else:
            key_list = []

            for keyword in keywords:
                key_list.append({k: keyword[k] for k in ('key', 'search_volume')})

            key_list = [pair for pair in key_list if pair['key'] != seed_word]

            return key_list