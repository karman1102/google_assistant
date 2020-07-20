from copy import deepcopy as copy

template = {
    "basicCard": {
        "title": "",
        "subtitle": "",
        "formattedText": "",
        "image": {
            "url": "",
            "accessibilityText": ""
        }
    }
}


class Card:
    def __init__(self):
        self.template = copy(template)

    def add(self, title='', subtitle='', description=' ', image='', acc_text=' '):
        self.template['basicCard']['title'] = title
        self.template['basicCard']['subtitle'] = subtitle
        self.template['basicCard']['formattedText'] = description
        self.template['basicCard']['image']['url'] = image
        self.template['basicCard']['image']['accessibilityText'] = acc_text

    def add_button(self, title, url):
        dict1 = {"title": title, "openUrlAction": {"url": url}}
        self.template['basicCard']['buttons'] = [dict1]

    def get_card(self):
        return self.template
