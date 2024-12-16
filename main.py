from jinja2 import Environment, FileSystemLoader
from os import path

fileExists = False
outputName = "output.html"

if path.exists(outputName):
    fileExists = True

NAME = "Kayra"

env = Environment(loader=FileSystemLoader('templates'))

output = env.get_template('index.html').render(name=NAME)

def writeFile(filename):
    with open(filename, "w") as f:
        return f.write(output)

if fileExists:
    counter = 2
    baseName = outputName.rsplit('.', 1)[0]
    extension = outputName.rsplit('.', 1)[-1]
    
    while path.exists(f"{baseName}-{counter}.{extension}"):
        counter+=1
    writeFile(f"{baseName}-{counter}.{extension}")
else:
    writeFile(outputName)


