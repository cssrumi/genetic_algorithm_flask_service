from data.data import Data


class DataMapper:

    def __init__(self, mapping: dict):
        self.mapping = mapping

    def set_mapping(self, mapping):
        self.mapping = mapping

    def get_data_object(self, obj):
        data_dict = {}
        if not isinstance(obj, dict):
            for key in self.mapping.keys():
                try:
                    value = obj.__dict__.get(self.mapping.get(key))
                    if isinstance(value, str):
                        value = value.replace(',', '.')
                    data_dict[key] = float(value)
                except ValueError:
                    pass
        else:
            for key in self.mapping.keys():
                try:
                    value = obj.get(self.mapping.get(key))
                    if isinstance(value, str):
                        value = value.replace(',', '.')
                    data_dict[key] = float(value)
                except ValueError:
                    pass
        return Data(*data_dict.values())

    @staticmethod
    def get_default_mapping():
        from inspect import signature
        d_map = {}
        args = str(signature(Data.__init__)).strip('(').strip(')').split(', ')
        args.remove('self')
        for k in args:
            d_map[k] = k
        return d_map
