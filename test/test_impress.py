import sys
import types
import unittest
from unittest.mock import MagicMock, patch, AsyncMock

try:
    import uno
except ImportError:
    mock_uno = types.SimpleNamespace(getComponentContext=lambda: None)
    sys.modules['uno'] = mock_uno

from slidetextbridge.plugins import impress


class TestImpressCapture(unittest.IsolatedAsyncioTestCase):
    def test_type_name(self):
        self.assertEqual(impress.ImpressCapture.type_name(), 'impress')

    async def _test_loop_once(self, uno_shapes):
        ctx = MagicMock()

        uno_ctx = MagicMock()

        resolver = MagicMock()
        uno_ctx.ServiceManager.createInstanceWithContext.return_value = resolver

        uno_inst = MagicMock()
        resolver.resolve.return_value = uno_inst

        desktop = MagicMock()
        uno_inst.ServiceManager.createInstanceWithContext.return_value = desktop

        component = MagicMock()
        desktop.getCurrentComponent.return_value = component

        presentation = MagicMock()
        component.getPresentation.return_value = presentation

        controller = MagicMock()
        presentation.getController.return_value = controller

        uno_slide = MagicMock()
        controller.getCurrentSlide.return_value = uno_slide

        cfg = impress.ImpressCapture.config({})
        obj = impress.ImpressCapture(ctx=ctx, cfg=cfg)

        with (patch('asyncio.sleep') as mock_sleep,
              patch('uno.getComponentContext') as MockGetComponentContext):
            mock_sleep.return_value = None
            MockGetComponentContext.return_value = uno_ctx

            obj.emit = AsyncMock()
            uno_slide.__iter__.return_value = uno_shapes

            await obj._loop_once()

            slide = obj.emit.call_args[0][0]

            mock_sleep.assert_called_once()

        uno_ctx.ServiceManager.createInstanceWithContext.assert_called_once_with(
                'com.sun.star.bridge.UnoUrlResolver', uno_ctx)
        resolver.resolve.assert_called_once_with(
                'uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext')
        uno_inst.ServiceManager.createInstanceWithContext.assert_called_once_with(
                'com.sun.star.frame.Desktop', uno_inst)

        return slide

    async def test_texts(self):
        shape1 = MagicMock()
        shape1.Text.getString.return_value = 'text1'
        shape2 = MagicMock()
        shape2.Text.getString.return_value = 'text2'
        uno_shapes = [shape1, shape2]

        slide = await self._test_loop_once(uno_shapes = uno_shapes)
        uno_slide = MagicMock()
        uno_slide.__iter__.return_value = uno_shapes

        self.assertEqual(slide.to_dict(), impress._dict_from_slide(uno_slide))
        self.assertEqual(slide.to_texts(), ['text1', 'text2'])

    async def test_texts_heights(self):
        shape1 = MagicMock()
        shape1.Text.getString.return_value = 'text1'
        shape1.CharHeight = 16
        shape2 = MagicMock()
        shape2.Text.getString.return_value = 'text2'
        shape2.CharHeight = 16
        uno_shapes = [shape1, shape2]

        slide = await self._test_loop_once(uno_shapes = uno_shapes)

        d = slide.to_dict()
        self.assertEqual(len(d['shapes']), 2)
        self.assertEqual(d['shapes'][0]['text'], 'text1')
        self.assertEqual(d['shapes'][0]['char_height'], 16)
        self.assertEqual(d['shapes'][1]['text'], 'text2')
        self.assertEqual(d['shapes'][1]['char_height'], 16)

        # cover to_texts()
        self.assertEqual(str(slide), 'text1\ntext2')

if __name__ == "__main__":
    unittest.main()
