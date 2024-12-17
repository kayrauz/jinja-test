from jinja2 import Environment, FileSystemLoader
from os import path

"""
Variables

{{ exam }} = the exam e.g. VTEST English for Schools
{{ examtype }} = the type of exam e.g. AGES 7–10 | 4 SKILLS
{{ securecode }} = the secure code for the exam e.g. 8M6T42844
{{ date }} = the date of the exam e.g. 04 May 2024
{{ school }} = the name of the school e.g. PINAR KOLEJI
{{ administration }} = administration of the exam e.g. Online standard
{{ name }} = name of the student e.g. kayra uz
{{ level }} = overall level e.g. A1.1
{{ listening_level }} = listening level 
{{ reading_level }} = reading level
{{ speaking_level }} = speaking level
{{ writing_level }} = writing level

"""

def get_template(template_name):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(template_name)
    return template

def get_avalible_filename(filename):
    if path.exists(filename):
        counter = 2
        baseName = filename.rsplit('.', 1)[0]
        extension = filename.rsplit('.', 1)[-1]
        while path.exists(f"{baseName}-{counter}.{extension}"):
            counter+=1
        return f"{baseName}-{counter}.{extension}"
    else:
        return filename

def render(template_name,context):
    template = get_template(template_name)
    result = template.render(**context)
    output = get_avalible_filename(output)
    return result

def write_file(output,content):
    with open(output, "w") as f:
        return f.write(content)




if __name__ == "__main__":
    result = render('index.html',"output.html", {"name":"<b>Kayra</b>"})
    write_file(result)






