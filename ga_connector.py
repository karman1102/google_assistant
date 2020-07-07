import logging
import json
from sanic import Blueprint, response
from sanic.request import Request
from typing import Text, Optional, List, Dict, Any

from rasa.core.channels.channel import UserMessage, OutputChannel
from rasa.core.channels.channel import InputChannel
from rasa.core.channels.channel import CollectingOutputChannel

logger = logging.getLogger(__name__)


class GoogleAssistant(InputChannel):
    # inherits rasa core InputChannel
    @classmethod
    def name(cls):
        #   this function will define our webhook url prefix
        return 'google_assistant'

    def blueprint(self, on_new_message):
        # this will define the webhook that assistant will use to pass thw inputs to Rasa Core, collect and send back
        google_webhook = Blueprint('google_webhook', __name__)

        @google_webhook.route("/", methods=['GET'])
        async def health(request):
            return response.json({"status": "ok"})

        # implementation of a health route - it will receive GET requests sent by Google Assistant and will return
        # 200 OK message confirming that the connection works well.

        @google_webhook.route("/webhook", methods=['POST'])
        async def receive(request):
            payload = request.json
            print(payload)
            intent = payload['inputs'][0]['intent']
            text = payload['inputs'][0]['rawInputs'][0]['query']

            template = {
                "expectUserResponse": 'true',
                "expectedInputs": [
                    {
                        "possibleIntents": [
                            {
                                "intent": "actions.intent.TEXT"
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
            value = template['expectedInputs'][0]['inputPrompt']['richInitialPrompt']['items']
            if intent == 'actions.intent.MAIN':
                message = "Hello! Welcome to the Rasa-powered Google Assistant skill. You can start by saying hi."
                item = {"simpleResponse": {"textToSpeech": message}}
                value.append(item)
            else:
                out = CollectingOutputChannel()
                await on_new_message(UserMessage(text, out))
                output = out.messages
                print(output)
                for i in range(len(output)):
                    if "text" in output[i]:
                        # text responses passed as utter messages or under 'text' in domain file
                        message = output[i]['text']
                        item = {"simpleResponse": {"textToSpeech": message}}
                        value.append(item)
                    elif "custom" in output[i]:
                        # handles all custom output (e.g json messages)
                        r = output[i]['custom']
                        value.append(r)
                    elif "image" in output[i]:
                        # for all messages under 'images' in domain file
                        image_url = output[i]['image']
                        value.append({"basicCard": {
                            "image": {"url": image_url, "accessibilityText": "Image alternate text"},
                            "imageDisplayOptions": "CROPPED"}})

            return response.json(template)

        return google_webhook
