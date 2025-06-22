'''
Configuration file reader
'''

import yaml
from ppttextfeed.plugins import plugins
from .config import ConfigBase

class ConfigTop(ConfigBase):
    # pylint: disable=R0903
    '''
    The class to hold every configuration
    '''
    def __init__(self):
        super().__init__()
        self.add_argment('steps', conversion=ConfigTop._steps_converter, default=[])

    @staticmethod
    def _steps_converter(data):
        ret = []
        for d in data:
            cls = plugins[d['type']]
            cfg = cls.config(d)
            ret.append(cfg)
        return ret


def load(filename):
    '''
    Load the config file in YAML
    :param filename: The file name to read
    '''
    with open(filename, 'r', encoding='utf8') as fr:
        d = yaml.safe_load(fr)

    cfgs = ConfigTop()
    cfgs.parse(d)
    return cfgs
