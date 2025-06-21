'''
Filter with JMESPath
'''

import jmespath
from . import base
from ppttextfeed.core import config


class JMESPathFilter(base.PluginBase):
    '''
    Filter shapes with JMESPath
    '''
    @classmethod
    def type_name(cls):
        'Return the name of the type'
        return 'jmespath'

    @staticmethod
    def config(data):
        cfg = config.ConfigBase()
        base.set_config_arguments(cfg)
        cfg.add_argment('filter', type=str)
        cfg.parse(data)
        return cfg

    def __init__(self, ctx, cfg=None):
        super().__init__(ctx=ctx, cfg=cfg)
        self.cfg = cfg
        self.connect_to(cfg.src)
        self.jmespath_filter = jmespath.compile(cfg.filter)

    async def update(self, slide, args):
        obj = slide.to_dict()
        obj = self.jmespath_filter.search(obj)
        slide = slide.__class__(data=obj)
        await self.emit(slide)
