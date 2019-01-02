import os
import subprocess
import sys
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
from utils.config import *
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders

def PrepareDict(files_list):
    files_dict={}
    files_dict['design.csv']=files_list[0]
    files_dict['after_align.csv']=files_list[1]
    files_dict['after_matching.csv']=files_list[2]
    files_dict['reads.fastq']=files_list[3]
    return files_dict

def SaveFilesOnServer(files_list,run_id):
    files_dict=PrepareDict(files_list)
    debugPrint("in SaveFilesOnServer")
    if not os.path.isdir(get_dir() + os.sep + input_files_dir):
        debugPrint('in SaveFilesOnServer: the input path didnt exist')
        os.mkdir(get_dir() + os.sep + input_files_dir)
    directory_path = get_dir() + os.sep + input_files_dir + os.sep
    for name,fd in files_dict.items():
        file_path = directory_path+str(run_id)+'_'+ name
        fd.save(file_path)

def debug_print(message):
    current_time = strftime("%H:%M:%S", gmtime())
    print("\n*****DEBUG: " + str(current_time) + " - " + str(message) + " ****************\n")


def RunDNATool(tool_path,run_id,analyzers,email):
    cmd = sys.executable + ' ' + tool_path + ' ' + str(run_id)
    debug_print('b4 process. the cmd is '+cmd)
    start_time = strftime("%H:%M:%S", gmtime())
    process_output = subprocess.check_output(cmd)
    path_to_output = input_files_dir + os.sep + str(run_id)+'_output.pdf'
    if os.path.exists(path_to_output):
        debugPrint('file is existing')
        send_results(email,start_time,path_to_output)
        send_mail_aux(email,start_time,path_to_output)
    else:
        debugPrint('file is None')

def send_mail_aux(email, time,path_to_output):
    msg = MIMEMultipart()
    msg['Subject'] = 'DNA-STORAGE-TOOL results'
    msg['To'] = ','.join([email])
    msg['From'] = os.environ.get('email')
    msg.attach(MIMEText(' your DNA-STORAGE-TOOL results of run that started on: ' + time + ', are now available to Download'))
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(path_to_output, "rb").read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="'+path_to_output+'"')
    msg.attach(part)

    server = smtplib.SMTP(msg.EMAIL_SERVER)
    server.sendmail(msg.EMAIL_FROM, msg.EMAIL_TO, msg.as_string())


def send_results(email, time,path_to_output):
    msg = MIMEMultipart()
    msg['Subject'] = 'DNA-STORAGE-TOOL results'
    msg['To'] = ','.join([email])
    msg['From'] = os.environ.get('email')
    msg.attach(
        MIMEText(' your DNA-STORAGE-TOOL results of run that started on: ' + time + ', are now available to Download'))
    with open(path_to_output, "rb") as fil:
        part = MIMEApplication(
            fil.read(),
            Name=basename(path_to_output)
        )
    # After the file is closed
    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(path_to_output)
    msg.attach(part)
    try:
        get_mail().sendmail()
        get_mail().send_message(msg)
    except Exception as e:
        debugPrint('COULDNT SEND MAIL')
        debugPrint(e.message)
