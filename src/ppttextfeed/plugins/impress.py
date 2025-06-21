'''
Get text from LibreOffice Impress
'''

import asyncio
import uno
from . import base
from ppttextfeed.core import config


class ImpressCaptureConfig(config.ConfigBase):
    def __init__(self):
        super().__init__()
        base.set_config_arguments(self, has_src=False)


class ImpressCapture(base.PluginBase):
    '''
    Get text from LibreOffice Impress
    '''
    @classmethod
    def type_name(cls):
        'Return the name of the type'
        return 'impress'

    @staticmethod
    def config(data):
        cfg = ImpressCaptureConfig()
        cfg.parse(data)
        return cfg

    def __init__(self, ctx, cfg=None):
        super().__init__(ctx=ctx, cfg=cfg)
        self._last_slide = self
        self._desktop = None

    async def initialize(self):
        asyncio.create_task(self._loop())

    async def _loop(self):
        while True:
            if not self._desktop:
                self._connect()

            slide = self._get_slide()
            if slide != self._last_slide:
                self._last_slide = slide
                await self.emit(ImpressSlide(slide))

            await asyncio.sleep(1)

    def _connect(self):
        context = uno.getComponentContext()
        resolver = context.ServiceManager.createInstanceWithContext(
                'com.sun.star.bridge.UnoUrlResolver', context)
        uno_inst = resolver.resolve(
                'uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext')
        self._desktop = uno_inst.ServiceManager.createInstanceWithContext(
                'com.sun.star.frame.Desktop', uno_inst)

    def _get_slide(self):
        c = self._desktop.getCurrentComponent()
        presentation = c.getPresentation()
        controller = presentation.getController()
        return controller.getCurrentSlide()


class ImpressSlide(base.SlideBase):
    def __init__(self, slide=None, data=None):
        self._slide = slide
        if isinstance(data, list):
            self._dict = {'shapes': data}
        else:
            self._dict = data

    def to_texts(self):
        '''
        List all texts
        :return:  List of strings
        '''
        if self._dict:
            return _list_texts(self._dict)
        else:
            texts = []
            for shape in self._slide:
                texts.append(shape.Text.getString())
            return texts

    def to_dict(self):
        if not self._dict:
            shapes = []
            for shape in self._slide:
                s = base.SlideBase.convert_object(shape, params=(
                    ('Text', lambda v: v.getString()),
                    'CharColor',
                    'CharHeight',
                    'CharFontName',
                ))
                s['text'] = shape.Text.getString()
                shapes.append(s)
            self._dict = {'shapes': shapes}
        return self._dict


def _list_texts(obj):
    if isinstance(obj, str):
        return [obj, ]
    if isinstance(obj, (int, float, bool)):
        return []
    if isinstance(obj, dict):
        for key in ('shapes', 'text'):
            if key in obj:
                return _list_texts(obj[key])
        return []
    ret = []
    for x in obj:
        if x:
            ret += _list_texts(x)
    return ret
