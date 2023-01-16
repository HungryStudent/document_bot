import datetime

from docxtpl import DocxTemplate
from docx2pdf import convert



def convert_to_pdf(data):
    convert("documents/шаблон-fial.docx", "documents/output.pdf")


def get_docx(context):
    pass
    print(context)
    doc = DocxTemplate("documents/template.docx")
    doc.render(context)
    today = datetime.datetime.now()
    name = today.strftime('%d-%m-%y_%H-%M') + ".docx"
    doc.save(name)
    return name

