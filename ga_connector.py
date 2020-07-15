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

        def parse_message(output=None, payload=None):
            richInitialPrompt = payload['expectedInputs'][0]['inputPrompt']['richInitialPrompt']
            value = payload['expectedInputs'][0]['inputPrompt']['richInitialPrompt']['items']
            print("IN PARSE ", output)
            for i in range(len(output)):
                print(output[i])
                if "text" in output[i]:
                    # text responses passed as utter messages or under 'text' in domain file
                    message = output[i]['text']
                    item = {"simpleResponse": {"textToSpeech": message}}
                    value.append(item)
                elif "custom" in output[i]:
                    r = output[i]['custom']
                    # handles all custom output (e.g json messages)
                    if "suggestions" in r:
                        richInitialPrompt['suggestions'] = r['suggestions']
                        if 'linkOutSuggestion' in r:
                            richInitialPrompt['linkOutSuggestion'] = r['linkOutSuggestion']

                    if 'expectedInputs' in r:
                        return output[i]['custom']

                    else:
                        value.append(r)
                elif "image" in output[i]:
                    # for all messages under 'images' in domain file
                    image_url = output[i]['image']
                    value.append({"basicCard": {
                        "image": {"url": image_url, "accessibilityText": "Image alternate text"},
                        "imageDisplayOptions": "CROPPED"}})
            return payload

        @google_webhook.route("/webhook", methods=['POST'])
        async def receive(request):
            out = CollectingOutputChannel()
            payload = request.json
            convId = payload['conversation']['conversationId']
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
            print("PAYLOAD : ", payload)

            if intent == 'actions.intent.MAIN':
                # message = "Hello! Welcome to the Rasa-powered Google Assistant skill. You can start by saying hi."
                # item = {"simpleResponse": {"textToSpeech": message}}
                # value.append(item)
                message = "Hello"
                await on_new_message(UserMessage(message, out, input_channel='GoogleAssistant', sender_id=convId))
                output = out.messages
                print(output)
                template = parse_message(output=output, payload=template)
            #     helper intents payload receive
            elif intent != 'actions.intent.TEXT':
                if intent == 'actions.intent.OPTION':
                    await on_new_message(UserMessage(text, out, input_channel='GoogleAssistant', sender_id=convId))
                    output = out.messages
                    template = parse_message(output=output, payload=template)
                elif intent == 'actions.intent.PERMISSION':
                    data = json.dumps(payload)
                    await on_new_message(UserMessage(data, out, input_channel='GoogleAssistant', sender_id=convId))
                    output = out.messages
                    template = parse_message(output=output, payload=template)
                else:
                    message = "option payload, configure for this intent"
                    item = {"simpleResponse": {"textToSpeech": message}}
                    value.append(item)
            else:
                await on_new_message(UserMessage(text, out, input_channel='GoogleAssistant', sender_id=convId))
                output = out.messages
                template = parse_message(output=output, payload=template)

            print("TEMPLATE : ", template)
            return response.json(template)

        return google_webhook
