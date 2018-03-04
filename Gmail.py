from mailer import Mailer
from mailer import Message

class Gmail:
    """ for sending gmail """

    def __init__(self, id_, password, recipient, subject, body_html):
        self.message = Message(From=id_ + "@gmail.com", To=recipient, charset="utf-8")
        self.message.Subject = subject
        self.message.Html = body_html

        self.sender = Mailer("smtp.gmail.com", port=587, usr=id_ + "@gmail.com", pwd=password, use_tls=True)

    def send(self):
        """ send out """
        self.sender.send(self.message)
