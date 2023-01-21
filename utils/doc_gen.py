import datetime

from docxtpl import DocxTemplate
from docx2pdf import convert


def convert_to_pdf(name):
    convert(name, name[:-4]+".pdf")
    return name[:-4]+".pdf"


def get_docx(context):
    doc = DocxTemplate("documents/template.docx")
    doc.render(context)
    today = datetime.datetime.now()
    name = "documents/" + today.strftime('%d-%m-%y_%H-%M') + ".docx"
    doc.save(name)
    return name
