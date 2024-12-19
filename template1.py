from jinja2 import Environment, FileSystemLoader
from os import path, makedirs
import subprocess

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

Pre_A1 = '60px'
A1_1 = '190px'
A1_2 = '315px'
A1_3 = '445px'
A2_1 = '565px'
A2_2 = '695px'
B1 = '825px'

LOREM = """• Lorem ipsum dolor sit amet, consectetur adipiscing elit. In semper lacus non feugiat rhoncus.\n• Lorem ipsum dolor sit amet, consectetur adipiscing elit. In semper lacus non feugiat rhoncus.\n• Lorem ipsum dolor sit amet, consectetur adipiscing elit. In semper lacus non feugiat rhoncus.\n"""

# END OF HARD CODED VARIABLES


def get_template(template_name):
    env = Environment(loader=FileSystemLoader('templates/template1'), comment_start_string='{=',
  comment_end_string='=}')
    template = env.get_template(template_name)
    return template

def get_avalible_filename(filename):
    if not path.exists('./template1-output'): makedirs("./template1-output")
    if path.exists(f"./template1-output/{filename}"):
        counter = 2
        baseName = filename.rsplit('.', 1)[0]
        extension = filename.rsplit('.', 1)[-1]
        while path.exists(f"./template1-output/{baseName}-{counter}.{extension}"):
            counter += 1
        return f"{baseName}-{counter}.{extension}"
    else:
        return filename

def insertProgressbar(width, type):
    progressBarHTML = f"<style type='text/css'>.progress-bar-{type}{{width: {width};}}</style>"
    return progressBarHTML


def render(template_name, context, isPage1=False):
    template = get_template(template_name)
    if isPage1:
        listeningLevel = context["listening_level"]
        readingLevel = context["reading_level"]
        speakingLevel = context["speaking_level"]
        writingLevel = context["writing_level"]
        result = template.render({
            "listening_progress": insertProgressbar(getProgressWidth(listeningLevel), "listening"),
            "reading_progress": insertProgressbar(getProgressWidth(readingLevel), "reading"),
            "speaking_progress": insertProgressbar(getProgressWidth(speakingLevel), "speaking"),
            "writing_progress": insertProgressbar(getProgressWidth(writingLevel), "writing"),
            **context
        })
        return result, {"name": context["name"], "test_center": context["test_center"], "school": context["school"]}
    else:
        result = template.render(**context)
        return result, {"name": context["name"], "test_center": context["test_center"], "school": context["school"]}


def write_file(output, content):
    with open(f"./template1-output/{output}", "w", encoding="utf-8") as f:
        return f.write(content)


def getProgressWidth(level):
    match level:
        case "Pre-A1":
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


def page1(context):
    result, studentInfo = render('page1.html', {
        "exam": context["exam"],
        "examtype": context["examtype"],
        "name": context["name"],
        "securecode": context["securecode"],
        "date": context["date"], 
        "school": context["school"],
        "test_center": context["test_center"],
        "administration": context["administration"],
        "level": context["level"],
        "listening_level": context["listening_level"],
        "reading_level": context["reading_level"],
        "speaking_level": context["speaking_level"],
        "writing_level": context["writing_level"],
    }, True)
    output = get_avalible_filename(f"{studentInfo["name"].upper()}-page1.html")
    write_file(output, result)
    return output

def page2(context):
    result, studentInfo = render('page2.html', {
        "exam": context["exam"],
        "examtype": context["examtype"],
        "name": context["name"],
        "securecode": context["securecode"],
        "date": context["date"], 
        "school": context["school"],
        "test_center": context["test_center"],
        "administration": context["administration"],
        "listening_level": context["listening_level"],
        "listening_means": context["listening_means"],
        "listening_improve": context["listening_improve"]
    })
    output = get_avalible_filename(f"{studentInfo["name"].upper()}-page2.html")
    write_file(output, result)
    return output

def page3(context):
    result, studentInfo = render('page3.html', {
        "exam": context["exam"],
        "examtype": context["examtype"],
        "name": context["name"],
        "securecode": context["securecode"],
        "date": context["date"], 
        "school": context["school"],
        "test_center": context["test_center"],
        "administration": context["administration"],
        "reading_level": context["reading_level"],
        "reading_means": context["reading_means"],
        "reading_improve": context["reading_improve"]
    })
    output = get_avalible_filename(f"{studentInfo["name"].upper()}-page3.html")
    write_file(output, result)
    return output

def page4(context):
    result, studentInfo = render('page4.html', {
        "exam": context["exam"],
        "examtype": context["examtype"],
        "name": context["name"],
        "securecode": context["securecode"],
        "date": context["date"], 
        "school": context["school"],
        "test_center": context["test_center"],
        "administration": context["administration"],
        "speaking_level": context["speaking_level"],
        "speaking_means": context["speaking_means"],
        "speaking_improve": context["speaking_improve"]
    })
    output = get_avalible_filename(f"{studentInfo["name"].upper()}-page4.html")
    write_file(output, result)
    return output

def page5(context):
    result, studentInfo = render('page5.html', {
        "exam": context["exam"],
        "examtype": context["examtype"],
        "name": context["name"],
        "securecode": context["securecode"],
        "date": context["date"], 
        "school": context["school"],
        "test_center": context["test_center"],
        "administration": context["administration"],
        "writing_level": context["writing_level"],
        "writing_means": context["writing_means"],
        "writing_improve": context["writing_improve"]
    })
    output = get_avalible_filename(f"{studentInfo["name"].upper()}-page5.html")
    write_file(output, result)
    return output, list(studentInfo.values())

def getAllPages(context):
    files = [page1(context), page2(context), page3(context), page4(context), *page5(context)]
    return files

if __name__ == "__main__":
    context = {
        "exam": "VTest English for Schools",
        "examtype": "AGES 7–10 | 4 SKILLS",
        "name": "EMİNE BERRA ESKİLİ",
        "securecode": "57H33859Z",
        "date": "04 May 2024",
        "school": "PINAR KOLEJİ",
        "test_center": "PINAR KOLEJİ",
        "administration": "Online standard",
        "level": "Pre-A1",
        "listening_level": "A1.1",
        "reading_level": "Pre-A1",
        "speaking_level": "Pre-A1",
        "writing_level": "Pre-A1",
        "listening_means": LOREM,
        "listening_improve": LOREM,
        "reading_means": LOREM,
        "reading_improve": LOREM,
        "speaking_means": LOREM,
        "speaking_improve": LOREM,
        "writing_means": LOREM,
        "writing_improve": LOREM,
    }

    files = getAllPages(context)
    result = subprocess.run(['node', 'template1Parser.js'] + [str(arg) for arg in files], capture_output=True, text=True)
    print('STDOUT:', result.stdout)
    print('STDERR:', result.stderr)

    
