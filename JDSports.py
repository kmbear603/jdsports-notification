""" class file for JD Sports """

import urllib.request
import urllib.parse
import pyquery
import requests

class JDSports:
    """ JD Sports UK """

    def __init__(self):
        pass

    def log(self, msg):
        #print(msg)
        pass

    def fetch(self, query):
        """ get search results from JD Sports """

        self.log("start")

        items = []

        self.log("searching " + query + " on JD Sports")

        start_index = 0
        domain = "https://www.jdsports.co.uk"
        base_url = domain + "/search/" + query.replace(" ", "+") + "/?sort=price-low-high"

        hdrs = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "Connection": "keep-alive",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "accept-encoding": "gzip, deflate, br",
            'Accept-Language': 'en-US,en;q=0.5',
            "upgrade-insecure-requests": "1",
        }

        session = requests.Session()

        while True:
            if start_index > 0:
                url = base_url + "&from=" + str(start_index)
            else:
                url = base_url

            try:
                res = session.get(url=url, headers=hdrs)
                html = res.text
            except urllib.request.HTTPError as e:
                if e.code == 404:
                    break
                raise e

            dom = pyquery.PyQuery(html)

            product_element_list = dom(".productListItem")

            if product_element_list is None or len(product_element_list) == 0:
                break
            
            for product_element in product_element_list:
                item = {}

                item_title_anchor_element = dom(".itemTitle a", product_element)
                url = urllib.parse.urljoin(base_url, item_title_anchor_element.attr("href"))
                item["url"] = url
                item["title"] = item_title_anchor_element.text()

                item["id"] = url
                if item["id"][len(item["id"]) - 1] == '/':
                    item["id"] = item["id"][:len(item["id"]) - 1]
                item["id"] = item["id"][item["id"].rfind('/') + 1:]

                item_price_element_list = dom("[data-oi-price]", product_element)
                # if item is in sales, item_price_element_list will contain two elements -[0]: original price, [1]: current price
                if len(item_price_element_list) == 1:
                    # no discount
                    item["price"] = item["original-price"] = float(item_price_element_list[0].text[1:])
                elif len(item_price_element_list) == 2:
                    # no discount
                    item["original-price"] = float(item_price_element_list[0].text[1:])
                    item["price"] = float(item_price_element_list[1].text[1:])
                else:
                    raise "more than two span[@data-oi-price] are found"

                img_element = dom(".thumbnail", product_element)
                item["img"] = urllib.parse.urljoin(base_url, img_element.attr("data-src"))

                duplicated = False
                for i in items:
                    if i["id"] == item["id"]:
                        duplicated = True
                        break

                if not duplicated:
                    items.append(item)

            start_index = start_index + len(product_element_list)

        items.sort(key=lambda i: i["price"])

        self.log("found " + str(len(items)) + " items")

        self.log("end")

        return {"success": True, "list": items}
