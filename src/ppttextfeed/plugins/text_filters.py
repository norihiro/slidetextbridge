'''
Filters to modify texts
'''

import re
from . import base
from ppttextfeed.core import config

class TextLinebreakFilter(base.PluginBase):
    '''
    Filter line breaks in texts
    '''

    @classmethod
    def type_name(cls):
        'Return the name of the type'
        return 'linebreak'

    @staticmethod
    def config(data):
        cfg = config.ConfigBase()
        base.set_config_arguments(cfg)
        cfg.add_argment('shape_delimiter', type=str, default='\n')
        cfg.add_argment('line_delimiter', type=str, default='\n')
        cfg.add_argment('strip', type=bool, default=True)
        cfg.parse(data)
        return cfg

    def __init__(self, ctx, cfg=None):
        super().__init__(ctx=ctx, cfg=cfg)
        self.cfg = cfg
        self.connect_to(cfg.src)

    def _filter_shape_text(self, text):
        lines = text.split('\n')
        if self.cfg.strip:
            stripped = []
            for t in lines:
                t = t.strip()
                if t:
                    stripped.append(t)
            lines = stripped
        return self.cfg.line_delimiter.join(lines)

    async def update(self, slide, args):
        texts = slide.to_texts()
        shapes = [{
            'text': self._filter_shape_text(t),
            'shape_delimiter': self.cfg.shape_delimiter
            } for t in texts]
        slide = TextFilteredSlide(data={'shapes': shapes})
        await self.emit(slide)


class RegexFilter(base.PluginBase):
    '''
    Filter lines with regex
    '''

    @classmethod
    def type_name(cls):
        'Return the name of the type'
        return 'regex'

    @staticmethod
    def config(data):
        cfg = config.ConfigBase()
        base.set_config_arguments(cfg)
        cfg.add_argment('pattern', type=str)
        cfg.add_argment('repl', type=str)
        cfg.parse(data)
        return cfg

    def __init__(self, ctx, cfg=None):
        super().__init__(ctx=ctx, cfg=cfg)
        self.pattern_re = re.compile(cfg.pattern)
        self.cfg = cfg
        self.connect_to(cfg.src)

    def _filter_shape_text(self, text):
        lines = [self.pattern_re.sub(self.cfg.repl, t) for t in text.split('\n')]
        return '\n'.join(lines)

    async def update(self, slide, args):
        if isinstance(slide, TextFilteredSlide):
            d = slide.to_dict()
            for shape in d['shapes']:
                shape['text'] = self._filter_shape_text(shape['text'])
        else:
            texts = slide.to_texts()
            shapes = [{
                'text': self._filter_shape_text(t),
                } for t in texts]
            slide = TextFilteredSlide(data={'shapes': shapes})
        await self.emit(slide)


class TextFilteredSlide(base.SlideBase):
    def __init__(self, data=None):
        if isinstance(data, list):
            self._dict = {'shapes': data}
        else:
            self._dict = data

    def to_texts(self):
        try:
            if self._dict:
                return [shape['text'] for shape in self._dict['shapes']]
        except (TypeError, KeyError):
            return []

    def __str__(self):
        ret = ''
        shape_delimiter = ''
        for shape in self._dict['shapes']:
            ret += shape_delimiter
            ret += shape['text']
            shape_delimiter = shape['shape_delimiter'] if 'shape_delimiter' in shape else '\n'
        return ret

    def to_dict(self):
        return self._dict
