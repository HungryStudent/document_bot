from docxtpl import DocxTemplate
from docx2pdf import convert

convert("documents/шаблон-fial.docx", "documents/output.pdf")

doc = DocxTemplate("documents/шаблон-fin2al.docx")
context = {}
doc.replace_media("photo1.jpg", "photo2.jpg")
doc.render(context)
doc.save("шаблон-fial.docx")

