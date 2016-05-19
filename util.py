import json
import logging
__author__ = 'tantran'
config = None
with open('data.json') as data_file:
    config = json.loads(data_file.read())


def get_config(key):
    try:
        result = {}
        for i in str(key).split('__'):
            result = result.get(i, config.get(i, None))
            if (result is None) or (type(result) is not dict):
                break
        return True, result
    except Exception as e:
        logging.exception(e)
        return False, None


def reload_config():
    global config
    with open('data.json') as data_file:
        config = json.loads(data_file.read())
    return True, {"message": "Reloaded config file"}


def call_cmd(cmd="", params=""):
    switcher = {
        'get_config': get_config(params),
        'reload_config': reload_config()
    }
    return switcher[cmd]