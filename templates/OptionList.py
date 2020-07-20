import json
from copy import deepcopy as copy

template = {
    "expectUserResponse": "true",
    "expectedInputs": [
        {
            "possibleIntents": [
                {
                    "intent": "actions.intent.OPTION",
                    "inputValueData": {
                        "@type": "type.googleapis.com/google.actions.v2.OptionValueSpec",
                        "listSelect": {
                            "title": '',
                            "items": []
                        }
                    }
                }
            ],
            "inputPrompt": {
                "richInitialPrompt": {
                    "items": []
                }
            }

        }
    ]
}


class ListChoice:
    def __init__(self):
        self.template = copy(template)

    def add(self, key, synonyms=None, description='', image_url='', image_text='', title=''):
        r2 = {
            "optionInfo": {
                "key": "SELECTION_KEY_{}".format(key),
                "synonyms": []
            },
            "description": description,
            "image": {
                "url": image_url,
                "accessibilityText": image_text
            },
            "title": title
        }
        for i in synonyms:
            r2['optionInfo']['synonyms'].append(i)
        self.template['expectedInputs'][0]['possibleIntents'][0]['inputValueData']['listSelect']['items'].append(r2)

    def get_message(self):
        return self.template

    def __str__(self):
        return self.template

    def add_message(self, text, title):
        message = {
            "simpleResponse": {
                "textToSpeech": text
            }
        }
        self.template['expectedInputs'][0]['inputPrompt']['richInitialPrompt']['items'].append(message)
        self.template['expectedInputs'][0]['possibleIntents'][0]['inputValueData']['listSelect']['title'] = title
