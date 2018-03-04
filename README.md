# About
For every 5 minutes, scrape products from jdsports.co.uk according to the specified search criteria. Compare with previous scraped products, send email whenever there is difference (new product found, product removed from website, product detail changed, etc).

# Programming Framework
- python 3

# Python dependencies
- urllib
- pyquery
- mailer

# How to install
1. make sure python 3 is installed
1. install dependencies
    ~~~
    pip install urllib pyquery mailer
    ~~~
1. create config.json with this format:
    ~~~
    {
        "query": [ "<product1>", "<product2>", "<product3>" ],
        "sender":
        {
            "id": "<gmail user name of sender>",
            "password": "<gmail password of sender>"
        },
        "recipient": [ "<email of recipient 1>", "<email of recipient 2>" ]
    }
    ~~~

    For example. If ultraboost and pureboost are the products you want to monitor. And you want the notification messages to be sent from kmbear603@gmail.com to larry@google.com and tcook.apple.com. Password of kmbear603@gmail.com is "kmbear603s-secret-password". Your config.json should look like this:
    ~~~
    {
        "query": [ "ultraboost", "pureboost" ],
        "sender":
        {
            "id": "kmbear603",
            "password": "kmbear603s-secret-password"
        },
        "recipient": [ "larry@google.com", "tcook@apple.com" ]
    }
    ~~~

# How to run
1. make sure config.json is in correct format and exists in the same directory as Main.py
2. execute
    ~~~
    python Main.py
    ~~~

# Contributor
kmbear603@gmail.com
