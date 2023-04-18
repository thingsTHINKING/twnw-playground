import configparser
import os.path


def read_config(name):
    config = configparser.ConfigParser()
    config.read(os.path.join("data", name))
    return config
