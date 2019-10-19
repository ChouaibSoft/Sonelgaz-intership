import datetime

from django.http import FileResponse
from django.shortcuts import redirect
from reportlab.rl_config import defaultPageSize
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.pagesizes import portrait
from reportlab.lib.pagesizes import A4
from billingManager import models
from reportlab.pdfgen import canvas

#INV_LOGO = getattr(settings, 'INV_LOGO', path.join(settings.MEDIA_ROOT, 'static/images/

page_width = defaultPageSize[0]
page_hight = defaultPageSize[1]


def create_pdf(pk):
    slip = models.Slip.objects.get(slip_id=pk)
    title = 'Bordereau numéro :' + str(slip.slip_num) + '-' + str(slip.service.service_abv) + '-' + \
            str(datetime.datetime.now().year)
    pdf_file_name = 'Bordereau numéro :' + str(slip.slip_num) + '-' + str(slip.service.service_abv) + '-' + \
                    str(datetime.datetime.now().year) + '.pdf'
    
    pdf_file = canvas.Canvas(pdf_file_name, pagesize=portrait(A4))
    create_header(pdf_file, title)
    create_content(pdf_file, slip)
    #create_footer()
    pdf_file.showPage()
    pdf_file.save()
    slip.closed = True


def create_header(pdf_file, title):
    page_width = defaultPageSize[0]
    page_hight = defaultPageSize[1]

    pdf_file.setStrokeColorRGB(0.9, 0.5, 0.2)
    pdf_file.setFillColorRGB(0.2, 0.2, 0.2)
    pdf_file.setFont('Helvetica-Bold', 16)
    string_size = stringWidth(title, 'Helvetica-Bold', 16)
    pdf_file.drawString((page_width - string_size)/2.0, page_hight-100, title)
    pdf_file.setFont('Helvetica', 18)
    pdf_file.setLineWidth(4)

def create_content(pdf_file, slip):
    bills = models.Bill.objects.filter(slip=slip)
    pdf_file.setFont('Helvetica-Bold', 14)
    string_size = 50
    pdf_file.drawString(string_size, page_hight-200, 'N° Facture')
    string_size += stringWidth('N° Facture', 'Helvetica-Bold', 14) + 50
    pdf_file.drawString(string_size, page_hight-200, 'Type')
    string_size += stringWidth('Type', 'Helvetica-Bold', 14) + 50
    pdf_file.drawString(string_size, page_hight-200, 'Fournisseur')
    string_size += stringWidth('Fournisseur', 'Helvetica-Bold', 14) + 50
    pdf_file.drawString(string_size, page_hight-200, 'Objet')
    string_size += stringWidth('Objet', 'Helvetica-Bold', 14) + 50
    pdf_file.drawString(string_size, page_hight-200, 'Date Facturation')
    pdf_file.setFont('Helvetica', 12)
    i = 250
    for bill in bills:
        string_size = 50
        pdf_file.drawString(string_size, page_hight-i, bill.bill_num)
        string_size += stringWidth(bill.bill_num, 'Helvetica', 12) + 50
        pdf_file.drawString(string_size, page_hight-i, bill.bill_type)
        string_size += stringWidth(bill.bill_type, 'Helvetica', 12) + 50
        pdf_file.drawString(string_size, page_hight-i, str(bill.provider))
        string_size += stringWidth(str(bill.provider), 'Helvetica', 12) + 50
        pdf_file.drawString(string_size, page_hight-i, bill.object)
        string_size += stringWidth(bill.object, 'Helvetica', 12) + 50
        pdf_file.drawString(string_size, page_hight-i, str(bill.billing_date))
        i += 50


def create_footer():
        return




