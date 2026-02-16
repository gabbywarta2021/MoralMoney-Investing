import json

SPEC_JSON = """
{ "openapi": "3.0.3", "info": {"title": "MoralMoney Investing API", "version": "0.1.0"}, "paths": {} }
"""


def main():
    # Load the full spec template and write it as the canonical openapi.json
    import os
    here = os.path.dirname(__file__)
    template_path = os.path.join(here, '..', 'openapi_full.json')
    with open(template_path, 'r') as tf:
        spec = json.load(tf)
    with open(os.path.join(here, '..', 'openapi.json'), 'w') as f:
        json.dump(spec, f, indent=2, ensure_ascii=False)
    # validate
    with open('openapi.json') as f:
        json.load(f)
    print('WROTE and validated openapi.json')


if __name__ == '__main__':
    main()

