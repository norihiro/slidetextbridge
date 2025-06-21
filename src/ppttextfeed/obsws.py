'''
Send text to OBS Studio
'''
# -*- coding: utf-8 -*-

import simpleobsws


class Text2Obs:
    '''
    Send text to OBS Studio
    '''
    def __init__(self, host, port, password=None):
        self.host = host
        self.port = port
        self.password = password
        self.ws = None

    async def connect(self):
        'Connect to obs-websocket server'
        if not self.ws:
            self.ws = simpleobsws.WebSocketClient(
                    url=f'ws://{self.host}:{self.port}',
                    password=self.password
            )
        await self.ws.connect()
        if not await self.ws.wait_until_identified():
            self.ws.disconnect()
            self.ws = None

    async def send(self, text, source_name):
        '''
        Set text

        :param text:         Text to be set
        :param source_name:  Name of the text source
        '''
        if not self.ws:
            await self.connect()
        if not text:
            text = ''
        await self._send_request('SetInputSettings', {
            'inputName': source_name,
            'inputSettings': {'text': text}
        })

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
                    await self.connect()
                except:
                    self.ws = None
