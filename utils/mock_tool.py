import csv
import os
import sys
from time import strftime, gmtime
from reportlab.pdfgen import canvas
from utils.common import send_results
from utils.config import get_dir


directory_path = get_dir() + os.sep + 'input_files_dir' + os.sep

def run_tool(run_id):
    out_path = get_dir() + os.sep + 'Output.pdf'
    pdf_file = canvas.Canvas(out_path)
    pdf_file.drawString(0, 0, "hello whats up?")
    os.chmod(directory_path+run_id+'_design.csv',755)
    with open(directory_path+run_id+'_design.csv', 'r') as csv_file_obj:
        reader = csv.reader(csv_file_obj)
        x = 25
        y = 25
        for row in reader:
            str_row = str(row)
            pdf_file.drawString(x, y, str_row)
            pdf_file.drawString(x + 3, y + 3, 'NEXT')
            y = y + 25
            if y % 100 == 0:
                pdf_file.showPage()
        pdf_file.save()
        return pdf_file


if __name__ == '__main__':
    run_tool(sys.argv[1])
