'''
Configuration file reader
'''

import yaml
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
        from slidetextbridge.plugins import accumulate # pylint: disable=C0415
        ret = []
        for d in data:
            cls = accumulate.plugins[d['type']]
            cfg = cls.config(d)
            ret.append(cfg)
        return ret


def load(filename):
    '''
    Load the config file in YAML
    :param filename: The file name to read
    '''

    class _LoaderWithLineNumber(yaml.SafeLoader): # pylint: disable=R0901
        _filename = filename
        def construct_mapping(self, node, deep=False):
            mapping = super().construct_mapping(node, deep=deep)
            location = f'{self._filename}:{node.start_mark.line+1}'
            if node.start_mark.line != node.end_mark.line:
                location += f'-{node.end_mark.line+1}'
            mapping['_location'] = location
            return mapping

    with open(filename, 'r', encoding='utf8') as fr:
        d = yaml.load(fr, Loader=_LoaderWithLineNumber)

    cfgs = ConfigTop()
    cfgs.parse(d)
    return cfgs
