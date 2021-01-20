"""
Generate page with date using jinja
"""

from jinja2 import Template

import datetime as dt

with open('template.html') as f:
    template_text = f.read()

template = Template(template_text)

new_page = template.render(date=dt.datetime.today())

with open('index.html', 'w+') as f:
    f.write(new_page)