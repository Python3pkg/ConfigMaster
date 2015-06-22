class ConfigKey(object):
    def __init__(self):
        self.parsed = False

    def dump(self):
        d = {}
        for item in self.__dict__:
            if item in ['parsed', 'dump', 'parse_data']:
                continue
            if isinstance(self.__dict__[item], ConfigKey):
                d[item] = self.__dict__[item].dump()
            else:
                d[item] = self.__dict__[item]
        return d

    @classmethod
    def iter_list(cls, data: list):
        l = []
        for item in data:
            if isinstance(item, list):
                l.append(cls.iter_list(item))
            elif isinstance(item, dict):
                ncfg = ConfigKey.parse_data(item)
                l.append(ncfg)
            else:
                l.append(item)
        return l


    @classmethod
    def parse_data(cls, data: dict):
        """
        Create a Config Key entity.
        :param data: The dict to create the entity from.
        :return: A new ConfigKey object.
        """
        cfg = ConfigKey()
        if data is None:
            return cfg
        for key, item in data.items():
            if isinstance(item, dict):
                # Create a new ConfigKey object with the dict.
                ncfg = ConfigKey.parse_data(item)
                # Set our new ConfigKey as an attribute of ourselves.
                setattr(cfg, key, ncfg)
            elif isinstance(item, list):
                # Iterate over the list, creating ConfigKey items as appropriate.
                nlst = ConfigKey.iter_list(item)
                # Set our new list as an attribute of ourselves.
                setattr(cfg, key, nlst)
            else:
                # Set the item as an attribute of ourselves.
                setattr(cfg, key, item)
        # Flip the parsed flag,
        cfg.parsed = True
        return cfg

