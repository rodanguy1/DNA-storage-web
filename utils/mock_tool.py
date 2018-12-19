import csv
import os
import sys
from datetime import time

from reportlab.pdfgen import canvas

# def GetParser():
#     parser = argparse.ArgumentParser(description='Demo for eitans project')
#     parser.add_argument('-csv_path' , required=True)
#     parser.add_argument('-analyze_level' , required=True,type=list)
#     return parser.parse_args()
from utils.common import send_results
from utils.config import get_dir


def run_tool(design):
    dest = get_dir() + os.sep + 'Output.pdf'
    # if (os.path.exists(dest)):
    #     print('path existed')
    #     os.remove(dest)
    pdf_file = canvas.Canvas(dest)
    pdf_file.drawString(0, 0, "hello whats up?")
    os.chmod(design, 755)
    with open(design, 'r') as csv_file_obj:
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
        # print("****")
        pdf_file.save()
        # print('****after')
        send_results('rodanguy@gmail.com', time)
        return pdf_file


# def ValidateArgs(args_valid):
#     if not os.path.exists(args.csv_path):
#         args_valid = False
#         return "Path to Csv doesnt exist." , args_valid
#     if args.analyze_level > 10 or args.analyze_level < 1:
#         print(args.analyze_level)
#         args_valid = False
#         return "Your Analyzation Level is invalid." , args_valid
#     return "", args_valid

if __name__ == '__main__':
    design = sys.argv[1]
    alignment = sys.argv[2]
    run_tool(design)
