class Sorting:
    def __init__(self):
        self.dict = {}

    def slovar(self, category, name, message_id, chat_id):
        if category not in self.dict:
            self.dict[category] = {}
        self.dict[category].update({name: {"chat": chat_id, "message": message_id}})
        return self.dict

    def keyses(self, slova):
        for categories in self.dict:
            slova += f"{categories} \n"
        return slova

    def valueses(self, slova, categor):
        for values in self.dict[categor]:
            slova += f"{values} \n"
        return slova
