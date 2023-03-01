import datetime
import requests
import json
from docxtpl import DocxTemplate


def convert_to_pdf(name, is_bill=False):
    instructions = {
        'parts': [
            {
                'file': 'document'
            }
        ]
    }

    full_name = name + ".docx"
    if is_bill:
        full_name = name + "_bill.docx"

    response = requests.request(
        'POST',
        'https://api.pspdfkit.com/build',
        headers={
            'Authorization': 'Bearer pdf_live_Y49xidbW78c9hozks6zNbnQcS8VS9OW4ScNXoDOhv7p'
        },
        files={
            'document': open(full_name, 'rb')
        },
        data={
            'instructions': json.dumps(instructions)
        },
        stream=True
    )
    save_name = name + ".pdf"
    if is_bill:
        save_name = name + "_bill.pdf"
    if response.ok:
        with open(save_name, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=8096):
                fd.write(chunk)
    else:
        print(response.text)
        exit()


def get_docx(context):
    doc = DocxTemplate("documents/template.docx")
    doc.render(context)
    today = datetime.datetime.now()
    name = "documents/" + today.strftime('%d-%m-%y_%H-%M')
    doc.save(name + ".docx")
    convert_to_pdf(name)
    doc = DocxTemplate("documents/template_bill.docx")
    doc.render(context)
    doc.save("documents/" + today.strftime('%d-%m-%y_%H-%M') + "_bill.docx")
    convert_to_pdf(name)
    return name
