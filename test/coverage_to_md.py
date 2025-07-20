'''
Convert coverage.json to summary table for GitHub Actions
'''
import argparse
import json

_HEADER_KEY_PAIRS = (
        ('File', None),
        ('Stmts', 'num_statements'),
        ('Miss', 'missing_lines'),
        ('Branch', 'num_branches'),
        ('BrPart', 'num_partial_branches'),
        ('Cover', 'percent_covered', '{:.0f}%'),
)

def _value(p, summary, file):
    v = summary[p[1]] if p[1] else file
    if len(p) == 2:
        return f'{v}'
    if len(p) == 3:
        return p[2].format(v)
    raise ValueError(f'Unsupported size of p = {p}')

def _pad_cell(t, w):
    if t == '---':
        return '-' * w
    if t.removesuffix('%').replace('.', '').isdigit():
        return f'{t:>{w}}'
    return f'{t:<{w}}'

def create_md_table(data) -> str:
    '''
    Convert the data to table in markdown
    :param data: data read from coverage.json
    :return: table in markdown
    '''
    table = [
            [p[0] for p in _HEADER_KEY_PAIRS],
            ['---' for _ in _HEADER_KEY_PAIRS],
    ]
    for file, stats in data["files"].items():
        summary = stats['summary']
        table.append([_value(p, summary, f'`{file}`') for p in _HEADER_KEY_PAIRS])

    totals = data['totals']
    table.append([_value(p, totals, '*Total*') for p in _HEADER_KEY_PAIRS])

    widths = [max(len(v) for v in x) for x in zip(*table)]

    lines = ['| ' + ' | '.join(_pad_cell(v, widths[i]) for i, v in enumerate(line)) + ' |' for line in table]

    return '\n'.join(lines)

def main():
    'The main routine'
    parser = argparse.ArgumentParser()
    parser.add_argument('coverage_json', action='store', default='coverage.json')
    args = parser.parse_args()

    with open(args.coverage_json, encoding='utf-8') as fr:
        data = json.load(fr)

    print(create_md_table(data))

if __name__ == '__main__':
    main()
