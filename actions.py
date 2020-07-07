from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_test"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Hello World!")
        dispatcher.utter_message(text="Hello World!")
        r = {
              "carouselBrowse": {
                "items": [
                  {
                    "description": "Description of item 1",
                    "footer": "Item 1 footer",
                    "image": {
                      "accessibilityText": "Image alternate text",
                      "url": "https://storage.googleapis.com/actionsresources/logo_assistant_2x_64dp.png"
                    },
                    "openUrlAction": {
                      "url": "https://example.com"
                    },
                    "title": "Title of item 1"
                  },
                  {
                    "description": "Description of item 2",
                    "footer": "Item 2 footer",
                    "image": {
                      "accessibilityText": "Image alternate text",
                      "url": "https://storage.googleapis.com/actionsresources/logo_assistant_2x_64dp.png"
                    },
                    "openUrlAction": {
                      "url": "https://example.com"
                    },
                    "title": "Title of item 2"
                  }
                    ]
              }
        }

        dispatcher.utter_message(json_message=r)
        return []

