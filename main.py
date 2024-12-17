from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
from os import path
from weasyprint.text.fonts import FontConfiguration

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
{{ listening_progress }} = listening progress bar
{{ reading_progress }} = reading progress bar
{{ speaking_progress }} = speaking progress bar
{{ writing_progress }} = writing progress bar

"""

# HARD CODED VARIABLES DO NOT TOUCH

Pre_A1 = '50px'
A1_1 = '150px'
A1_2 = '240px'
A1_3 = '340px'
A2_1 = '440px'
A2_2 = '540px'
B1 = '620px'

# END OF HARD CODED VARIABLES


def get_template(template_name):
    env = Environment(loader=FileSystemLoader('templates'), comment_start_string='{=',
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

def insertProgressbar(width, type):
    progressBarHTML = f"<style type='text/css'>.progress-bar-{type}{{width: {width}}}</style>"
    print(progressBarHTML)
    return progressBarHTML


def render(template_name, context):
    listeningProgress = context["listening_level"]
    readingLevel = context["reading_level"]
    speakingLevel = context["speaking_level"]
    writingLevel = context["writing_level"]
    template = get_template(template_name)
    result = template.render({
        "name": context["name"].upper(),
        "listening_progress": insertProgressbar(getProgressWidth(listeningProgress), "listening"),
        "reading_progress": insertProgressbar(getProgressWidth(readingLevel), "reading"),
        "speaking_progress": insertProgressbar(getProgressWidth(speakingLevel), "speaking"),
        "writing_progress": insertProgressbar(getProgressWidth(writingLevel), "writing"),
        "exam": context["exam"],
        "securecode": context["securecode"],
        "date": context["date"],
        "school": context["school"],
        "school": context["school"],
        "administration": context["administration"],
        "level": context["level"],
        "listening_level": context["listening_level"],
        "reading_level": context["reading_level"],
        "reading_level": context["reading_level"],
        "writing_level": context["writing_level"],
        "examtype": context["examtype"]
    })
    return result


def write_file(output, content):
    with open(output, "w", encoding="utf-8") as f:
        return f.write(content)


def getProgressWidth(level):
    match level:
        case "Pre A1":
            return Pre_A1
        case "A1":
            return A1_1
        case "A1.1":
            return A1_1
        case "A1.2":
            return A1_2
        case "A1.3":
            return A1_3
        case "A2":
            return A2_1
        case "A2.1":
            return A2_1
        case "A2.2":
            return A2_2
        case "B1":
            return B1
        case default:
            raise ValueError("No valid level given")


def convertToPdf(filename):
    return HTML(filename=filename).write_pdf(get_avalible_filename("pdfRapor.pdf"))

if __name__ == "__main__":

    result = render('report.html', {
    "name": "Kayra UZ",
    "exam": "testExam", 
    "securecode": "HGJH234", 
    "date": "23 asd 3034", 
    "school": "radno", 
    "administration": "asdasdasd",
    "level": "A1.1",
    "listening_level": "A1.2",
    "reading_level": "A1.3",
    "speaking_level": "A1.1",
    "writing_level": "A1.2",
    "examtype": "random"
    })
    output = get_avalible_filename("output.html")
    write_file(output, result)
    convertToPdf(output)
