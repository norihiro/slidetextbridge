'''
Main routine
'''

import argparse
import asyncio
import logging

from slidetextbridge.core.context import Context
from slidetextbridge.core import configtop

def _get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', action='store', default='config.yaml')
    parser.add_argument('--strict', action='store_true')
    return parser.parse_args()

def _setup_ctx(cfgs):
    ctx = Context()
    from slidetextbridge.plugins import accumulate # pylint: disable=C0415
    for step in cfgs.steps:
        cls = accumulate.plugins[step.type]
        inst = cls(ctx=ctx, cfg=step)
        ctx.add_instance(inst)
    return ctx

async def _loop(ctx):
    await ctx.initialize_all()
    while True:
        await asyncio.sleep(1)

def main():
    'The entry point'
    logging.basicConfig(level=logging.INFO)
    args = _get_args()
    cfgs = configtop.load(args.config)
    ctx = _setup_ctx(cfgs)

    try:
        asyncio.run(_loop(ctx))
    except KeyboardInterrupt:
        logging.getLogger(__name__).info('Interrupted')

if __name__ == '__main__':
    main()
