import csv
import os
import sys
from time import strftime, gmtime
from reportlab.pdfgen import canvas
from utils.common import send_results
from utils.config import get_dir


def run_tool(user_design_file, analyzes, user_email):
    for a in analyzes:
        print(a)
    dest = get_dir() + os.sep + 'Output.pdf'
    pdf_file = canvas.Canvas(dest)
    pdf_file.drawString(0, 0, "hello whats up?")
    os.chmod(design, 755)
    with open(user_design_file, 'r') as csv_file_obj:
        reader = csv.reader(csv_file_obj)
        x = 25
        y = 25
        for row in reader:
            print(str(row))
            str_row = str(row)
            pdf_file.drawString(x, y, str_row)
            pdf_file.drawString(x + 3, y + 3, 'NEXT')
            y = y + 25
            if y % 100 == 0:
                pdf_file.showPage()
        pdf_file.save()
        send_results(user_email, strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        return pdf_file


if __name__ == '__main__':
    design = sys.argv[1]
    alignment = sys.argv[2]
    analyzes = sys.argv[3]
    email = sys.argv[4]
    run_tool(design, analyzes, email)
