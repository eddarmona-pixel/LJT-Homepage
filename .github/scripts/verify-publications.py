from html.parser import HTMLParser
from pathlib import Path


class Publications(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active = False
        self.in_entry = False
        self.entries = []

    def handle_starttag(self, tag, attrs):
        if tag == 'div' and dict(attrs).get('class') == 'personal-publications':
            self.active = True
        if self.active and tag == 'p':
            self.in_entry = True
            self.entries.append('')

    def handle_endtag(self, tag):
        if tag == 'div':
            self.active = False
        if tag == 'p':
            self.in_entry = False

    def handle_data(self, data):
        if self.active and self.in_entry:
            self.entries[-1] += data


def entries(path):
    parser = Publications()
    parser.feed(Path(path).read_text())
    return parser.entries


home = entries('_site/index.html')
publications = entries('_site/publications/index.html')
assert len(home) == 7, 'Expected six publications and a Scholar link'
assert home == publications, 'Publication lists differ between pages'
print('All six publication entries match on both pages.')
