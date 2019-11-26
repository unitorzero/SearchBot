import json


class Translate:
    def __init__(self, sources, default_locale):
        self.sources = sources
        self.default_locale = default_locale
        self.locales = []
        self.translates = {}
        self._init_sources()

    def _init_sources(self):
        for source_key, source_value in self.sources.items():
            if isinstance(source_value, dict):
                self.translates[source_key] = source_value
            if isinstance(source_value, str):
                file = open(source_value, 'r')
                self.translates[source_key] = json.loads(''.join(file.readlines()))

            self.locales.append(source_key)

    def __call__(self, locale=''):
        locale = locale or self.default_locale
        if locale not in self.locales:
            raise KeyError('local not find')
        translates = self.translates[locale]

        def translate(key=''):
            if isinstance(key, str):
                key = key.split('.')
            key_gen = iter(key)

            def get_value_by_chain(obj, key):
                if isinstance(obj, str):
                    return obj

                return get_value_by_chain(obj.get(next(key)), key)

            return get_value_by_chain(translates, key_gen)

        return translate

    def all(self, key):
        values = []
        for locale in self.locales:
            values.append(self(locale)(key))
        return values
