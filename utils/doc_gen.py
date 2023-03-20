import datetime
import requests
import json
from docxtpl import DocxTemplate

from docx2pdf import convert


def convert_to_pdf(name):
    convert(name + ".docx", name + ".pdf")


def get_docx(context, is_ip=False):
    doc = DocxTemplate("documents/template.docx")
    if is_ip:
        doc = DocxTemplate("documents/template_ip.docx")
    doc.render(context)
    today = datetime.datetime.now()
    doc_name = "documents/" + f'Договор {context["number"]} {today.strftime("%d-%m-%y")}'
    doc.save(doc_name + ".docx")
    convert_to_pdf(doc_name)

    doc = DocxTemplate("documents/template_bill.docx")
    if is_ip:
        doc = DocxTemplate("documents/template_bill_ip.docx")
    doc.render(context)
    bill_name = "documents/" + f'Счет {context["number"]} {today.strftime("%d-%m-%y")}'
    doc.save(bill_name + ".docx")
    convert_to_pdf(bill_name)
    return doc_name, bill_name


def get_kp(context):
    doc = DocxTemplate("documents/template_kp.docx")
    doc.render(context)
    today = datetime.datetime.now()
    doc_name = "documents/" + f'КП {context["number"]} {today.strftime("%d-%m-%y")}'
    doc.save(doc_name + ".docx")
    convert_to_pdf(doc_name)
    return doc_name
