import config


def instance_test():
    cfg1 = config.Config()
    cfg2 = config.Config.get_instance()

    assert cfg1 is cfg2

    print('instance_test passed')


def env_test():
    cfg = config.Config()
    print(vars(cfg))

    print('env_test passed')


def load_from_yaml_test():
    cfg = config.Config()
    cfg._load_from_yaml()


def enum_test():
    from enums import TimeUnitTypes, SaveIntervalTypes
    cfg = config.Config()
    loaded_time_unit = cfg.time_unit
    loaded_save_interval_type = cfg.save_interval_type

    assert TimeUnitTypes.SEC is loaded_time_unit
    assert SaveIntervalTypes.TIME is loaded_save_interval_type

    print('enum_test passed')


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
    env_test()
    enum_test()
    load_from_yaml_test()
