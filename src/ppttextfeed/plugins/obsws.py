'''
Send text to OBS Studio
'''

import simpleobsws
from . import base
from ppttextfeed.core import config


class ObsWsEmitterConfig(config.ConfigBase):
    def __init__(self):
        super().__init__()
        self.add_argment('url', type=str, default='ws://localhost:4455/')
        self.add_argment('password', type=str, default=None)
        self.add_argment('source_name', type=str, default=None)
        base.set_config_arguments(self)


class ObsWsEmitter(base.PluginBase):
    '''
    Emit text to OBS Studio
    '''
    @classmethod
    def type_name(cls):
        'Return the name of the type'
        return 'obsws'

    @staticmethod
    def config(data):
        cfg = ObsWsEmitterConfig()
        cfg.parse(data)
        return cfg

    def __init__(self, ctx, cfg=None):
        super().__init__(ctx=ctx, cfg=cfg)
        self.ws = None
        self.cfg = cfg
        self.connect_to(cfg.src)

    async def _ws_connect(self):
        self.ws = simpleobsws.WebSocketClient(url=self.cfg.url, password=self.cfg.password)
        await self.ws.connect()
        if not await self.ws.wait_until_identified():
            self.ws.disconnect()
            self.ws = None

    async def update(self, text, args):
        if not text:
            text = ''
        elif not isinstance(text, str):
            text = str(text)

        try:
            if not self.ws:
                await self._ws_connect()

            await self._send_request('SetInputSettings', {
                'inputName': self.cfg.source_name,
                'inputSettings': {'text': text}
            })
        except Exception as e:
            print(f'Error: {e}')

    async def _send_request(self, req, data, retry=2):
        while retry > 0:
            retry -= 1
            try:
                res = await self.ws.call(simpleobsws.Request(req, data))
                if res.ok():
                    return res.responseData
            except Exception as e: # pylint: disable=W0718
                try:
                    await self.ws.disconnect()
                except: # pylint: disable=W0702
                    pass
                if retry == 0:
                    raise e
                try: # pylint: disable=W0702
                    await self._ws_connect()
                except:
                    self.ws = None
