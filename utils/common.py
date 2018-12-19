import datetime
import os
import subprocess
import sys
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename

from utils.config import get_mail, get_dir


def debug_print(message):
    cur_time = datetime.datetime.now().time()
    print("\n*****DEBUG: " + str(cur_time) + " - " + str(message) + " ****************\n")


def run_dna_tool(tool_path, alignment_path, design_path):
    cmd = sys.executable + ' ' + tool_path + ' ' + alignment_path + ' ' + design_path
    debug_print('b4 process')
    process_output = subprocess.check_output(cmd)
    debug_print('after process. output is :')
    debug_print(process_output)
    if os.path.exists(process_output):
        debug_print('file is existing')
    else:
        debug_print('file is none')


def send_results(email, time):
    msg = MIMEMultipart()
    msg['Subject'] = 'DNA-STORAGE-TOOL results'
    msg['To'] = ','.join([email])
    msg['From'] = os.environ.get('email')
    file = get_dir() + os.sep + 'Output.pdf'
    msg.attach(
        MIMEText(' your DNA-STORAGE-TOOL results of run that started on: ' + time + ', are now available to Download'))
    with open(file, "rb") as fil:
        part = MIMEApplication(
            fil.read(),
            Name=basename(file)
        )
    # After the file is closed
    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(file)
    msg.attach(part)
    try:
        get_mail().send_message(msg)
    except:
        print("COULDN'T SEND EMAIL")
