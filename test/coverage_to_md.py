'''
Convert coverage.json to summary table for GitHub Actions
'''
import argparse
import json

_HEADER_KEY_PAIRS = (
        ('File', None, '`{}`'),
        ('Stmts', 'num_statements'),
        ('Cover', 'percent_covered', '{:.0f}%'),
)

def _list_to_row(v):
    return '| ' + ' | '.join(v) + ' |'

def create_md_table(data) -> str:
    '''
    Convert the data to table in markdown
    :param data: data read from coverage.json
    :return: table in markdown
    '''
    lines = [
            _list_to_row([p[0] for p in _HEADER_KEY_PAIRS]),
            _list_to_row(['-----' for p in _HEADER_KEY_PAIRS]),
    ]

    for file, stats in data["files"].items():
        summary = stats['summary']
        # pylint: disable=W0640,R1710
        def _value(p):
            v = summary[p[1]] if p[1] else file
            if len(p) == 2:
                return f'{v}'
            if len(p) == 3:
                return p[2].format(v)
        lines.append(_list_to_row([_value(p) for p in _HEADER_KEY_PAIRS]))

    return '\n'.join(lines)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('coverage_json', action='store', default='coverage.json')
    args = parser.parse_args()

    with open(args.coverage_json, encoding='utf-8') as fr:
        data = json.load(fr)

    print(create_md_table(data))
