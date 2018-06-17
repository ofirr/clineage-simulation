from nose.tools import *

# make code in ../src/* importable
import os
import sys
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../src')))
from utils import handle_config_args


def test_handle_config_args_01():
    "should correctly load config-test.list"

    configs = [
        'config-test.list'
    ]

    config_jsons = handle_config_args('.', configs)

    assert_equals(len(config_jsons), 2)

    assert_equals(config_jsons[0], 'config-01.json')
    assert_equals(config_jsons[1], 'config-02.json')


def test_handle_config_args_02():
    "should correctly load individual config json files"

    configs = [
        'config-01.json',
        'config-03.json'
    ]

    config_jsons = handle_config_args('.', configs)

    assert_equals(len(config_jsons), 2)

    assert_equals(config_jsons[0], configs[0])
    assert_equals(config_jsons[1], configs[1])


def test_handle_config_args_03():
    "should correctly load config-test.list and individual config json files"

    configs = [
        'config-test.list',
        'config-03.json'
    ]

    config_jsons = handle_config_args('.', configs)

    assert_equals(len(config_jsons), 3)

    assert_equals(config_jsons[0], 'config-01.json')
    assert_equals(config_jsons[1], 'config-02.json')
    assert_equals(config_jsons[2], 'config-03.json')


def test_handle_config_args_04():
    "should correctly load config-test.list and individual config json files"
    
    configs = [
        'config-04.json',
        'config-test.list',
        'config-03.json'
    ]

    config_jsons = handle_config_args('.', configs)

    assert_equals(len(config_jsons), 4)

    assert_equals(config_jsons[0], 'config-04.json')
    assert_equals(config_jsons[1], 'config-01.json')
    assert_equals(config_jsons[2], 'config-02.json')
    assert_equals(config_jsons[3], 'config-03.json')
