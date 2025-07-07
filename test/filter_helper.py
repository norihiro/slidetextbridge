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

    filter_obj = cls(ctx=ctx, cfg=cfg)
    filter_obj.emit = AsyncMock()

    if (slide and slides) or (not slide and not slides):
        raise ValueError('Either slide or slides should be specified.')

    if slide:
        await filter_obj.update(slide, args=None)
        filter_obj.emit.assert_awaited_once()
        return filter_obj.emit.await_args[0][0]

    ret = []
    for slide in slides:
        slide_text_orig = '\n'.join(slide.to_texts())
        await filter_obj.update(slide, args=None)
        ret.append(filter_obj.emit.await_args[0][0])
        slide_text_new = '\n'.join(slide.to_texts())
        if slide_text_orig != slide_text_new:
            raise ValueError('The original slide has changed: ' +\
                    f'"{slide_text_orig}" -> "{slide_text_new}"')

    return ret
