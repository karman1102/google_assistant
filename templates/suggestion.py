from copy import deepcopy

template = {
    "suggestions": []
}


class SuggestionText:
    def __init__(self):
        self.template = deepcopy(template)

    def add_text(self, text=None):
        payload = {"title": text}
        self.template['suggestions'].append(payload)

    def add_link(self, text, link):
        self.template['linkOutSuggestion'] = {'destinationName': text}
        self.template['linkOutSuggestion']['url'] = link

    def __str__(self):
        return self.template

    def get_suggestion(self):
        return self.template
