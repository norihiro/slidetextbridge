'''
Base class definition
'''

import re

def set_config_arguments(cfg, has_src=True):
    '''
    Set the standard config arguments
    :param cfg:  Instance of ConfigBase
    '''
    cfg.add_argment('type', type=str)
    cfg.add_argment('name', type=str, default=None)
    if has_src:
        cfg.add_argment('src', type=str, default=None)


class PluginBase:
    '''
    The base class for text sources, filters, and sinks.
    '''

    @classmethod
    def type_name(cls):
        'Return the name of the type'
        return 'base'

    def __init__(self, ctx, cfg=None):
        self.ctx = ctx
        self.name = cfg.name
        self.sinks = []

    def connect_to(self, name=None, args=None):
        '''
        Connect this instance to the source of the text.
        :param name:  The name of the source
        :param args:  The argument that will be passed to `update` callback
        '''
        src = self.ctx.get_instance(name=name)
        return src.add_sink(self, args=args)

    def add_sink(self, sink, args=None):
        '''
        Connect a sink, that will receive the contents of this plugin.
        :param sink:  The instance of PluginBase
        :param args:  Any object
        '''
        self.sinks.append((sink, args))

    async def initialize(self):
        '''
        Callback when the system is started.
        '''

    async def emit(self, slide):
        '''
        Send the new slide to all sinks.
        :param slide:  The new slide.
        '''
        for sink, args in self.sinks:
            await sink.update(slide, args)

    async def update(self, slide, args):
        '''
        The callback function when updating the new slide.
        '''
        pass


class SlideBase():
    def __init__(slide=None, data=None):
        pass

    def to_texts(self):
        '''
        List all texts
        :return:  List of strings
        '''
        return []

    def __str__(self):
        return '\n'.join(self.to_texts())

    @staticmethod
    def convert_object(obj, params=()):
        d = {}
        def _f(attrname, f_conv=None):
            dest = re.sub('(.)([A-Z])', r'\1_\2', attrname).lower()
            try:
                v = getattr(obj, attrname)
            except:
                return
            if f_conv:
                v = f_conv(v)
            d[dest] = v
        for p in params:
            if isinstance(p, tuple):
                _f(p[0], p[1])
            else:
                _f(p)
        return d

