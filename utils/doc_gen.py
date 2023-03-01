import datetime
import requests
import json
from docxtpl import DocxTemplate


def convert_to_pdf(name):
    instructions = {
        'parts': [
            {
                'file': 'document'
            }
        ]
    }

    response = requests.request(
        'POST',
        'https://api.pspdfkit.com/build',
        headers={
            'Authorization': 'Bearer pdf_live_Y49xidbW78c9hozks6zNbnQcS8VS9OW4ScNXoDOhv7p'
        },
        files={
            'document': open(name + ".docx", 'rb')
        },
        data={
            'instructions': json.dumps(instructions)
        },
        stream=True
    )

    if response.ok:
        with open(name + ".pdf", 'wb') as fd:
            for chunk in response.iter_content(chunk_size=8096):
                fd.write(chunk)
    else:
        print(response.text)
        exit()


def get_docx(context):
    doc = DocxTemplate("documents/template.docx")
    doc.render(context)
    today = datetime.datetime.now()
    doc_name = "documents/" + f'Договор {context["number"]} {today.strftime("%d-%m-%y")}'
    doc.save(doc_name + ".docx")
    convert_to_pdf(doc_name)

    doc = DocxTemplate("documents/template_bill.docx")
    doc.render(context)
    bill_name = "documents/" + f'Счет {context["number"]} {today.strftime("%d-%m-%y")}'
    doc.save(bill_name + ".docx")
    convert_to_pdf(bill_name)
    return doc_name, bill_name
