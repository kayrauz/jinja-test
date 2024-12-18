from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
from os import path
from weasyprint.text.fonts import FontConfiguration

"""
Variables

{{ exam }} = the exam e.g. VTEST English for Schools
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
{{ listening_progress }} = listening progress bar
{{ reading_progress }} = reading progress bar
{{ speaking_progress }} = speaking progress bar
{{ writing_progress }} = writing progress bar
{{ estimate }}
{{ descriptors }}
{{ points_to_work_on }}
{{ grammer_level }}
{{ conversation_level }}
{{ expression_level }}

"""

LEVELS = ["A1","A2.1","A2.2","B1.1","B1.2","B2.1","B2.2","C1.1","C1.2","C2"]

def get_template(template_name):
    env = Environment(loader=FileSystemLoader('templates/template2'), comment_start_string='{=',
  comment_end_string='=}')
    template = env.get_template(template_name)
    return template


def get_avalible_filename(filename):
    if path.exists(filename):
        counter = 2
        baseName = filename.rsplit('.', 1)[0]
        extension = filename.rsplit('.', 1)[-1]
        while path.exists(f"{baseName}-{counter}.{extension}"):
            counter += 1
        return f"{baseName}-{counter}.{extension}"
    else:
        return filename

def insertProgressbar(studentLevel, levelType, LEVELS=LEVELS):
    global finalScript
    finalScript = ""
    student = LEVELS.index(studentLevel)
    for level in LEVELS:
        current = LEVELS.index(level)
        if current <= student:
            finalScript += f"{levelType}_{level.replace('.', '_').lower()},"
    return finalScript

def getAllProgressbars(context):
    global text
    text = []
    if "listening_level" in context:
        listeningProgress = insertProgressbar(context["listening_level"], "listening")
        readingProgress = insertProgressbar(context["reading_level"], "reading")
        speakingProgress = insertProgressbar(context["speaking_level"], "speaking")
        writingProgress = insertProgressbar(context["writing_level"], "writing")
        overallProgres = insertProgressbar(context["level"], 'overall')
        text = f"{listeningProgress}{readingProgress}{speakingProgress}{writingProgress}{overallProgres}".split(',')
        return True, text
    else:
        grammerProgress = insertProgressbar(context["grammer_level"], "grammer")
        expressionProgress = insertProgressbar(context["expression_level"], "expression")
        conversationProgress = insertProgressbar(context["conversation_level"], "conversation")
        text = f"{grammerProgress}{expressionProgress}{conversationProgress}".split(',')
        return False, text
    
    




def render(template_name, context):
    isPage1, ids = getAllProgressbars(context)
    template = get_template(template_name)
    if isPage1:
        result = template.render({
            "name": context["name"].upper(),
            "script": ids,
            "exam": context["exam"],
            "securecode": context["securecode"],
            "date": context["date"],
            "school": context["school"],
            "administration": context["administration"],
            "level": context["level"],
            "listening_level": context["listening_level"],
            "reading_level": context["reading_level"],
            "speaking_level": context["speaking_level"],
            "writing_level": context["writing_level"],
            "test_center": context["test_center"],
            "estimate": context["estimate"],
            "descriptors": context["descriptors"]
        })
        return result
    else:
        result = template.render({
            "name": context["name"].upper(),
            "script": ids,
            "exam": context["exam"],
            "securecode": context["securecode"],
            "date": context["date"],
            "school": context["school"],
            "administration": context["administration"],
            "points_to_work_on": context["points_to_work_on"],
            "test_center": context["test_center"],
            "grammer_level": context["grammer_level"],
            "expression_level": context["expression_level"],
            "conversation_level": context["conversation_level"]
        })
        return result


def write_file(output, content):
    with open(output, "w", encoding="utf-8") as f:
        return f.write(content)

def convertToPdf(filename):
    return HTML(filename=filename).write_pdf(get_avalible_filename("pdfRapor.pdf"))

def page1():
    result = render('page1.html', {
    "name": "Kayra UZ", # TRUE
    "exam": "testExam", # TRUE
    "securecode": "HGJH234", # TRUE
    "date": "23 asd 3034",  # TRUE
    "school": "radno",  # TRUE
    "administration": "asdasdasd", # TRUE
    "test_center": "random test", # TRUE
    "level": "A2.1", # TRUE
    "listening_level": "A2.2", # TRUE
    "reading_level": "B1.1", # TRUE
    "speaking_level": "B1.2", # TRUE
    "writing_level": "B2.1", # TRUE
    "estimate": "estimateee", # TRUE
    "descriptors": "dasdasdasdasd" # TRUE
    })
    output = get_avalible_filename("output-page1-1.html")
    return write_file(output, result)

def page2():
    result = render('page2.html', {
    "name": "Kayra UZ", # TRUE
    "exam": "testExam", # TRUE
    "securecode": "HGJH234", # TRUE
    "date": "23 asd 3034",  # TRUE
    "school": "radno",  # TRUE
    "administration": "asdasdasd", # TRUE
    "test_center": "random test", # TRUE
    "grammer_level": "A2.1",
    "expression_level": "A2.1",
    "conversation_level": "A2.1",
    "points_to_work_on": "asdasd"
    })
    output = get_avalible_filename("output-page2-1.html")
    return write_file(output, result)

if __name__ == "__main__":
    page1()
    page2()
    
    #convertToPdf(output)
