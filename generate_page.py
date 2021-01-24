"""
Generate page with date using jinja
"""

from jinja2 import Template

import datetime as dt

for template in ["index.template.html", "comments.template.html", "comments.template.js" ]:


    with open(template) as f:
        template_text = f.read()

    my_template = Template(template_text)


    if "index" in template:
        new_page = my_template.render(date=dt.datetime.today())
    else:
        new_page = my_template.render(date=dt.date.today())

    outfile_name = template.split(".")
    outfile_name.remove("template")
    outfile_name = (".").join(outfile_name)

    with open(outfile_name, 'w+') as f:
        f.write(new_page)
        print(f"Wrote {outfile_name}")