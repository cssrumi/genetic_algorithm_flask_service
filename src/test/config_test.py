import config


def instance_test():
    cfg1 = config.Config()
    cfg2 = config.Config.get_instance()

    assert cfg1 is cfg2


def env_test():
    pass


def enum_test():
    from enums import TimeUnitTypes, SaveIntervalTypes
    cfg = config.Config()
    loaded_time_unit = cfg.time_unit
    loaded_save_interval_type = cfg.save_interval_type

    assert TimeUnitTypes.SEC is loaded_time_unit
    assert SaveIntervalTypes.TIME is loaded_save_interval_type


def int_test():
    pass


def float_test():
    pass


def str_test():
    pass


def boolean_test():
    pass


if __name__ == '__main__':
    instance_test()
    enum_test()
