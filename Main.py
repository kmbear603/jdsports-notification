#!/usr/bin/env python3

from JDSports import JDSports
from Gmail import Gmail
from datetime import datetime
from time import sleep, strftime
import os.path
import json

class Engine:
    def __init__(self):
        self._read_config()
        self.jdsports = JDSports()

    def _read_config(self):
        """ read properties from config.json """
        
        config_file_name = "config.json"
        
        if not os.path.isfile(config_file_name):
            raise FileNotFoundError(config_file_name + " is not found")

        try:
            data = json.load(open(config_file_name))
        except:
            raise ValueError(config_file_name + " is not a valid json")

        self.queries = self._read_config_value(data, "query")
        self.sender = self._read_config_value(data, "sender")
        self.recipients = self._read_config_value(data, "recipient")

    @classmethod
    def _read_config_value(cls, obj, prop_name):
        if not prop_name in obj:
            raise ValueError(prop_name + " is not defined in config")
        return obj[prop_name]

    def _update_product_list(self):
        """ get products of all queries and return as a list """
        lst = []
        for query in self.queries:
            return_val = self.jdsports.fetch(query)
            if not return_val["success"]:
                continue
            for item in return_val["list"]:
                lst.append(item)
        return lst

    @classmethod
    def _products_to_html(cls, title, products):
        """ convert products into html for sending email """

        html = "<h1>" + title + "</h1>"

        html += "<ul>"
        for product in products:
            html += "<li>"
            html += "<a href='" + product["url"] + "'>"
            html += "<img src='" + product["img"] + "'>"
            #html += product["title"]
            if "original-price" in product and product["original-price"] != product["price"]:
                html += "<strike>$" + str(product["original-price"]) + "</strike> "
            html += "$" + str(product["price"])
            html += "</a>"
            html += "</li>"
        html += "</ul>"

        html += "<hr>"

        return html

    def _send_email(self, compare_result):
        """ send the compare result to recipients """
        subject = "JDSports update - " + datetime.now().strftime("%m/%d %H:%M")
        html = ""

        if len(compare_result["new"]) > 0:
            html += self._products_to_html("New", compare_result["new"])

        if len(compare_result["removed"]) > 0:
            html += self._products_to_html("Removed", compare_result["removed"])

        if len(compare_result["changed"]) > 0:
            html += self._products_to_html("Changed", compare_result["changed"])

        #if len(compare_result["identical"]) > 0:
        #    html += self._products_to_html("Identical", compare_result["identical"])

        Gmail(self.sender["id"], self.sender["password"], self.recipients, subject, html).send()

    @classmethod
    def _compare_products(cls, products, reference_products):
        """ return new items, removed items, changed items and identical items """

        reference_product_table = {}
        for p in reference_products:
            reference_product_table[p["id"]] = p

        new = []
        removed = []
        changed = []
        identical = []

        for product in products:
            try:
                ref_product = reference_product_table[product["id"]]
            except KeyError:
                ref_product = None

            if ref_product is None:
                new.append(product)
            else:
                if not cls._are_objects_equal(product, ref_product):
                    changed.append(product)
                else:
                    identical.append(product)
                del reference_product_table[product["id"]]

        for id_ in reference_product_table:
            removed.append(reference_product_table[id_])

        return { "new": new, "removed": removed, "changed": changed, "identical": identical }

    @classmethod
    def _are_objects_equal(cls, obj1, obj2):
        """ compare two objects """
        if not type(obj1) == type(obj2):
            return False

        elif type(obj1) is list:
            if len(obj1) != len(obj2):
                return False

            for i in range(0, len(obj1)):
                if not cls._are_objects_equal(obj1[i], obj2[i]):
                    return False

        elif type(obj1) is dict:
            for prop in obj1:
                if obj2[prop] is None:
                    return False
                elif not cls._are_objects_equal(obj1[prop], obj2[prop]):
                    return False

            for prop in obj2:
                if obj1[prop] is None:
                    return False
                elif not cls._are_objects_equal(obj1[prop], obj2[prop]):
                    return False

        elif not obj1 == obj2:
            return False

        return True

    @classmethod
    def _is_changed(cls, compare_result):
        return len(compare_result["new"]) > 0 or len(compare_result["removed"]) > 0 or len(compare_result["changed"]) > 0

    @classmethod
    def _show_status(cls, msg):
        print(datetime.now().strftime("%H:%M:%S") + " " + msg)

    def run(self):
        last_products = None

        while True:
            self._show_status("downloading products")
            products = self._update_product_list()
            self._show_status("found " + str(len(products)) + " products")

            if not last_products is None:
                compare_result = self._compare_products(products, last_products)
                if self._is_changed(compare_result):
                    self._show_status("changed, sending email")
                    try:
                        self._send_email(compare_result)
                        self._show_status("sent email")
                    except:
                        self._show_status("failed to send email")
                else:
                    self._show_status("no change")

            last_products = products
            
            self._show_status("sleep 5 minutes")
            sleep(300)

if __name__ == "__main__":
    engine = Engine()
    engine.run()
