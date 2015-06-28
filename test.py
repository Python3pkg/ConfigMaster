import os
import pytest

# Import our modules.

from configmaster.ConfigKey import ConfigKey

from configmaster.JSONConfigFile import JSONConfigFile
from configmaster.YAMLConfigFile import YAMLConfigFile
from configmaster.JSONConfigFile import NetworkedJSONConfigFile

from configmaster import exc

def test_loading_valid_json():
    cfg = JSONConfigFile("test_data/test.json")
    assert isinstance(cfg.config, ConfigKey)
    assert cfg.config.parsed

def test_loading_valid_yml():
    cfg = YAMLConfigFile("test_data/test.yml")
    assert isinstance(cfg.config, ConfigKey)
    assert cfg.config.parsed

def test_created_config_file():
    if os.path.exists("test_data/no_such_file.yml"):
        os.remove("test_data/no_such_file.yml")
    try:
        cfg = YAMLConfigFile("test_data/no_such_file.yml")
        # next line should happen
        parsed = True
    except:
        parsed = False
    assert parsed
    assert not cfg.config.parsed

def test_loaded_config_item():
    cfg = YAMLConfigFile("test_data/test.yml")
    assert cfg.config.hello == "goodbye"

def test_embedded_dict():
    cfg = YAMLConfigFile("test_data/test.yml")
    assert isinstance(cfg.config.edc, ConfigKey)
    assert cfg.config.edc.op == 4
    assert cfg.config.edc.po == 6

def test_embedded_list():
    cfg = YAMLConfigFile("test_data/test.yml")
    assert isinstance(cfg.config.fruit, list)
    assert cfg.config.fruit[0] == "apples"
    assert cfg.config.fruit[1] == "oranges"
    assert cfg.config.fruit[2] == "bananas"

def test_embedded_dict_inside_list():
    cfg = YAMLConfigFile("test_data/test.yml")
    assert isinstance(cfg.config.houses, list)
    assert isinstance(cfg.config.houses[0], ConfigKey)
    assert cfg.config.houses[0].red is False
    assert cfg.config.houses[0].blue is True
    assert cfg.config.houses[1].red is True
    assert cfg.config.houses[1].blue is False

@pytest.mark.xfail(raises=exc.LoaderException)
def test_invalid_yaml_data():
    cfg = YAMLConfigFile("test_data/invalid.data")

@pytest.mark.xfail(raises=exc.LoaderException)
def test_invalid_json_data():
    cfg = JSONConfigFile("test_data/invalid.data")

@pytest.mark.xfail(raises=AttributeError)
def test_invalid_key_get():
    cfg = YAMLConfigFile("test_data/test.yml")
    assert cfg.config.q == "w"

def test_configkey_dump():
    cfg = YAMLConfigFile("test_data/test.yml")
    assert cfg.config.dump() == {"hello": "goodbye", "qaz": 1, "wsx": 2, "edc": {"op": 4, "po": 6},
                                        "fruit": ["apples", "oranges", "bananas"],
                                        "houses": [{"red": False, "blue": True}, {"red": True, "blue": False}]}

def test_configkey_iter():
    cfg = YAMLConfigFile("test_data/test.yml")
    assert set(x for x in cfg.config) == {"hello", "qaz", "wsx", "edc", "fruit", "houses"}

