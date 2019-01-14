import datetime
import json
import os
import subprocess
import sys
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
from utils.config import get_mail, get_dir


def debug_print(message):
    cur_time = datetime.datetime.now().time()
    print("\n*****DEBUG: " + str(cur_time) + " - " + str(message) + " ****************\n")


def run_dna_tool(tool_path, alignment_path, design_path, analyzes, email):
    cmd = sys.executable + ' ' + tool_path + ' ' + alignment_path + ' ' + design_path + ' ' + analyzes + ' ' + email
    cmd2 = [sys.executable, tool_path, alignment_path, design_path, analyzes, email]
    debug_print('b4 process')
    process_output = subprocess.check_output(cmd2)
    debug_print('after process. output is :')
    debug_print(process_output)
    if os.path.exists(process_output):
        debug_print('file is existing')
    else:
        debug_print('file is none')


def contains_non_ascii_characters(str):
    return not all(ord(c) < 128 for c in str)


def add_header(message, header_name, header_value):
    if contains_non_ascii_characters(header_value):
        h = Header(header_value, 'utf-8')
        message[header_name] = h
    else:
        message[header_name] = header_value
    return message


def send_results(email, time):
    msg = MIMEMultipart()
    subject = 'DNA-STORAGE-TOOL results'
    msg = add_header(msg, 'Subject', subject)
    msg.set_charset('us-ascii')
    msg['To'] = email
    if os.environ.get('mode') == 'prod':
        with open('/etc/config.json') as config_file:
            config = json.load(config_file)
        email = config.get('email')
        msg['From'] = email
    else:
        msg['From'] = os.environ.get('email')
    file = get_dir() + os.sep + 'Output.pdf'
    plain = ' your DNA-STORAGE-TOOL results of run that started on: 0 are now available to Download'
    if (contains_non_ascii_characters(plain)):
        plain_text = MIMEText(plain.encode('utf-8'), 'plain', 'utf-8')
    else:
        plain_text = MIMEText(plain, 'plain')
    msg.attach(plain_text)
    with open(file, "rb") as fil:
        part = MIMEApplication(
            fil.read(),
            Name=basename(file)
        )
    # After the file is closed
    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(file)
    msg.attach(part)
    # try:
    get_mail().send_message(msg)
    # except:
    #     print("COULDN'T SEND EMAIL")
