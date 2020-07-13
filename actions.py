from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction

'''
All these steps have been implemented in order to append to the existing payload, 
The generic approach of sending the whole request as is would have required modifications and won't work for responses 
sent from the domain.yml file.
While writing actions here, there are a few points to remember:
- Implementing buttons and pictures happens in the 'Basic Card' template
- Carousel, basic card, table format rich responses can be passed together in one payload 
- Not more than two text responses can occur together
- NOTE : 'Suggestion Chips' require a separate payload/json response DO NOT send it in same response
        Payload for suggestion chips is same as title 
        
'''


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_test"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Hello World!")
        dispatcher.utter_message(text="Hello World!")
        # '''         --------------------- Example for Carousel Template  -------------------------------------    '''
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
        # dispatcher.utter_message(json_message=r)

        # '''       ----------------- Example for Quick Reply/Suggestion Chips Template  -----------------------    '''
        r2 = {
            "suggestions": [
                {
                    "title": "Suggestion 1"
                },
                {
                    "title": "Suggestion 2"
                },
                {
                    "title": "Test"
                }
            ],
            "linkOutSuggestion": {
                "destinationName": "Suggestion Link",
                "url": "https://assistant.google.com/"
            }
        }
        # dispatcher.utter_message(json_message=r2)
        # '''         --------------------- Example for Helper Intent  -------------------------------------    '''
        r3 = {
            "expectUserResponse": 'true',
            "expectedInputs": [
                {
                    "possibleIntents": [
                        {
                            "intent": "actions.intent.PERMISSION",
                            "inputValueData": {
                                "@type": "type.googleapis.com/google.actions.v2.PermissionValueSpec",
                                "optContext": "To address you by name and know your location",
                                "permissions": [
                                    "NAME",
                                    "DEVICE_PRECISE_LOCATION"
                                ]
                            }
                        }
                    ]
                }
            ]
        }
        # dispatcher.utter_message(json_message=r3)
        #               --------------- helper intent option  ----------------------
        r4 = {
            "expectUserResponse": 'true',
            "expectedInputs": [
                {
                    "possibleIntents": [
                        {
                            "intent": "actions.intent.OPTION",
                            "inputValueData": {
                                "@type": "type.googleapis.com/google.actions.v2.OptionValueSpec",
                                "listSelect": {
                                    "title": "List Title",
                                    "items": [
                                        {
                                            "optionInfo": {
                                                "key": "SELECTION_KEY_ONE",
                                                "synonyms": [
                                                    "synonym 1",
                                                    "synonym 2",
                                                    "synonym 3"
                                                ]
                                            },
                                            "description": "This is a description of a list item.",
                                            "image": {
                                                "url": "https://storage.googleapis.com/actionsresources/logo_assistant_2x_64dp.png",
                                                "accessibilityText": "Image alternate text"
                                            },
                                            "title": "Title of First List Item"
                                        },
                                        {
                                            "optionInfo": {
                                                "key": "SELECTION_KEY_GOOGLE_HOME",
                                                "synonyms": [
                                                    "Google Home Assistant",
                                                    "Assistant on the Google Home"
                                                ]
                                            },
                                            "description": "Google Home is a voice-activated speaker powered by the Google Assistant.",
                                            "image": {
                                                "url": "https://storage.googleapis.com/actionsresources/logo_assistant_2x_64dp.png",
                                                "accessibilityText": "Google Home"
                                            },
                                            "title": "Google Home"
                                        },
                                        {
                                            "optionInfo": {
                                                "key": "SELECTION_KEY_GOOGLE_PIXEL",
                                                "synonyms": [
                                                    "Google Pixel XL",
                                                    "Pixel",
                                                    "Pixel XL"
                                                ]
                                            },
                                            "description": "Pixel. Phone by Google.",
                                            "image": {
                                                "url": "https://storage.googleapis.com/actionsresources/logo_assistant_2x_64dp.png",
                                                "accessibilityText": "Google Pixel"
                                            },
                                            "title": "Google Pixel"
                                        }
                                    ]
                                }
                            }
                        }
                    ],
                    "inputPrompt": {
                        "richInitialPrompt": {
                            "items": [
                                {
                                    "simpleResponse": {
                                        "textToSpeech": "This is a list example."
                                    }
                                }
                            ]
                        }
                    }
                }
            ]
        }
        dispatcher.utter_message(json_message=r4)
        return []


class ActionHello(Action):

    def name(self) -> Text:
        return "action_confirm"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        text2 = 'rasa story works with location'
        dispatcher.utter_message(text=text2)
        return []


class ActionForm(FormAction):

    def name(self) -> Text:
        return "form_json"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ['json']

    def slot_mappings(self):
        return {'json': self.from_text()}

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any], ) -> List[Dict]:
        load = tracker.get_slot('json')
        channel = tracker.get_latest_input_channel()
        print(channel)
        print(load)
        if load:
            message = "Please provide details on the issue that you are facing."
        else:
            message = "shit"
        dispatcher.utter_message(text=message)
        return []


class ActionGreet(Action):

    def name(self) -> Text:
        return "action_greet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("What would you like to do today?")
        r2 = {
            "suggestions": [
                {
                    "title": "Report an issue"
                },
                {
                    "title": "Submit feedback"
                },
            ]
        }
        dispatcher.utter_message(json_message=r2)
        return []


from rasa_sdk.events import FollowupAction


class ActionReport(Action):

    def name(self) -> Text:
        return "action_report"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        load = tracker.get_slot('json')
        if load:
            dispatcher.utter_message('By reporting through Civilcops, you agree to our terms of use.')
        else:
            return [FollowupAction('action_fetch')]
        return []


class ActionRetrieve(Action):

    def name(self) -> Text:
        return "action_fetch"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        r3 = {
            "expectUserResponse": 'true',
            "expectedInputs": [
                {
                    "possibleIntents": [
                        {
                            "intent": "actions.intent.PERMISSION",
                            "inputValueData": {
                                "@type": "type.googleapis.com/google.actions.v2.PermissionValueSpec",
                                "optContext": "To address you by your name and location",
                                "permissions": [
                                    "NAME",
                                    "DEVICE_PRECISE_LOCATION"
                                ]
                            }
                        }
                    ]
                }
            ]
        }
        dispatcher.utter_message(json_message=r3)
        return [FollowupAction('form_json')]
