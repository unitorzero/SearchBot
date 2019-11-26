class ValueKeyValue:
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def get_keys(self, value_for_key):
        return [key for key, value in self.dictionary.items() if value_for_key in value]

    def get_value(self, key):
        return self.dictionary.get(key, None)
