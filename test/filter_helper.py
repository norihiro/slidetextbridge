import unittest
from unittest.mock import MagicMock, AsyncMock

def make_slide(texts, cls=None):
    if not cls:
        from slidetextbridge.plugins import text_filters
        cls = text_filters.TextFilteredSlide
    return cls({'shapes': [{'text': t} for t in texts]})

async def run_filter(cls, cfg, slide=None, slides=None):
    ctx = MagicMock()
    if isinstance(cfg, dict):
        cfg = cls.config(cfg)

    from slidetextbridge.plugins import base
    src = base.PluginBase(ctx=ctx, cfg=MagicMock())
    ctx.get_instance.return_value = src

    filter_obj = cls(ctx=ctx, cfg=cfg)

    mock_sink = AsyncMock()
    filter_obj.add_sink(mock_sink, None)

    if (slide and slides) or (not slide and not slides):
        raise ValueError('Either slide or slides should be specified.')

    if slide:
        await src.emit(slide)
        mock_sink.update.assert_awaited_once()
        return mock_sink.update.await_args[0][0]

    ret = []
    for slide in slides:
        slide_text_orig = '\n'.join(slide.to_texts())
        await filter_obj.update(slide, args=None)
        ret.append(mock_sink.update.await_args[0][0])
        slide_text_new = '\n'.join(slide.to_texts())
        if slide_text_orig != slide_text_new:
            raise ValueError('The original slide has changed: ' +\
                    f'"{slide_text_orig}" -> "{slide_text_new}"')

    return ret
