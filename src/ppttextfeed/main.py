'''
Main routine
'''

import argparse
import asyncio
import json
import sys

from . import ppttext
from . import obsws


def _list_texts(obj):
    if isinstance(obj, str):
        return [obj, ]
    if isinstance(obj, (int, float, bool)):
        return []
    if isinstance(obj, dict):
        for key in ('text', 'text_range', 'text_frame'):
            if key in obj:
                return _list_texts(obj[key])
        return []
    return [_list_texts(x) for x in obj if x]


def _get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--jmespath-filter', action='store', default=None)
    parser.add_argument('--obsws-connect', action='store', default='localhost:4455')
    parser.add_argument('--obsws-password', action='store', default=None)
    parser.add_argument('--obsws-source-name', action='store', default=None)
    parser.add_argument('--print-raw', action='store_true', default=False)
    parser.add_argument('--shape-delimiter', action='store', default='\n')
    parser.add_argument('--poll-wait-time', action='store', default=1.0, type=float)
    return parser.parse_args()

def main():
    'The main routine'
    args = _get_args()

    try:
        asyncio.run(_loop(args))
    except KeyboardInterrupt:
        pass


def _filter_text(p, slide, args, jmespath_filter):
    obj = p.slide_dicts(slide)
    if jmespath_filter:
        obj = jmespath_filter.search(obj)
        texts = _list_texts(obj)
    else:
        texts = p.slide_texts(slide)
    text = args.shape_delimiter.join(texts)
    return (text.replace('\r', ' ').strip(), obj)


async def _loop(args):

    if args.jmespath_filter:
        # pylint: disable=C0415
        import jmespath
        jmespath_filter = jmespath.compile(args.jmespath_filter)
    else:
        jmespath_filter = None

    p = ppttext.PPTText()

    # Prepare the sink
    if args.obsws_connect:
        (host, port) = args.obsws_connect.rsplit(':', 2)
        sink = obsws.Text2Obs(host=host, port=int(port), password=args.obsws_password)
    else:
        sink = None

    while True:
        try:
            slide = p.get_slide(check_outdated=True)
        except ppttext.NoUpdate:
            await asyncio.sleep(args.poll_wait_time)
            continue

        if slide:
            (text, obj) = _filter_text(p, slide, args, jmespath_filter=jmespath_filter)
        else:
            (text, obj) = ('', None)

        if args.print_raw:
            print(json.dumps(obj, ensure_ascii=False, indent=2))
        else:
            print(text)
        try:
            await sink.send(text, args.obsws_source_name)
        except Exception as e: # pylint: disable=W0718
            sys.stderr.write(f'Error: Failed to send text to {args.obsws_connect}: {e}\n')
        await asyncio.sleep(args.poll_wait_time)


if __name__ == '__main__':
    main()
