import datetime
import re
import time
import os
import subprocess
import sys
import traceback
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
    files_dict['after_alignment.csv']=files_list[1]
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


def timeDiff(time1,time2):
    timeA = datetime.datetime.strptime(time1, "%H:%M:%S")
    timeB = datetime.datetime.strptime(time2, "%H:%M:%S")
    newTime = timeA - timeB
    return newTime

def DeleteSavedFiles(run_id):
    path_to_files=get_dir() + os.sep + input_files_dir+ os.sep
    debugPrint('in DeleteSavedFiles\nthe path to files is '+str(path_to_files))
    file_suffixes=['_design.csv','_after_alignment.csv','_after_matching.csv','_reads.fastq']
    for suffix in file_suffixes:
        if os.path.exists(str(path_to_files)+str(run_id)+str(suffix)):
            os.remove(str(path_to_files)+str(run_id)+str(suffix))
        else:
            debugPrint('the file '+str(path_to_files)+str(run_id)+str(suffix)+'didnt exist')



def RunDNATool(tool_path,run_id,analyzers,email):
    cmd = sys.executable + ' ' + tool_path + ' ' + str(run_id)
    debug_print('b4 process. the cmd is '+cmd)
    start_time = strftime("%H:%M:%S", gmtime())
    try:
        process_output = subprocess.check_output(cmd,stderr=subprocess.STDOUT)
        path_to_output =get_dir()+os.sep+ str(run_id)+'_report.pdf'
        if os.path.exists(path_to_output):
            debugPrint('file is existing.\n\tNOW EMAIL CODE')
            # send_good_results(email,start_time,path_to_output)
            # send_mail_aux(email,start_time,path_to_output)
        else:
            debugPrint('file is None')
    except Exception as e:
        debugPrint('there was an err')
        debugPrint(e.output)
        traceback_regex = re.search(r'Traceback \(most recent call last\)[\S\s]*',e.output)
        if traceback_regex:
            traceback_str = traceback_regex.group()
        # traceback_str = traceback.format_exc()
        # end_time = strftime("%H:%M:%S", gmtime())
        # run_time = timeDiff(end_time, start_time)
        # time.sleep(7)
        debugPrint('THE TRACEBACK\n'+traceback_str)
        # send_bad_results(email, start_time,run_time,traceback_str)
    finally:
        debugPrint("in Finally statement")
        DeleteSavedFiles(run_id)


def send_bad_results(email, start_time,run_time, traceback_str):
    msg = MIMEMultipart()
    msg['Subject'] = 'DNA-STORAGE-TOOL Run FAILED!'
    msg['To'] = ','.join([email])
    msg['From'] = os.environ.get('email')
    msg.attach(
        MIMEText('Hello,\nYour DNA-STORAGE-TOOL run that started on: ' + start_time + ' failed.'
                  '\nYour total runtime was: ' +str(run_time)+'.'
                  '\nThe traceback for the error was:\n'+str(traceback_str)+
                  '\n\nFor more info regarding your failure please contact the tool owners.'
                  '\nTheir info is on the website.'
                  '\nThanks! See you next time!'))
    try:
        # get_mail().sendmail()
        get_mail().send_message(msg)
    except Exception as e:
        debugPrint('COULDNT SEND BAD MAIL')
        debugPrint(e.message)


# def send_mail_aux(email, time,path_to_output):
#     msg = MIMEMultipart()
#     msg['Subject'] = 'DNA-STORAGE-TOOL results'
#     msg['To'] = ','.join([email])
#     msg['From'] = os.environ.get('email')
#     msg.attach(MIMEText(' your DNA-STORAGE-TOOL results of run that started on: ' + time + ', are now available to Download'))
#     part = MIMEBase('application', "octet-stream")
#     part.set_payload(open(path_to_output, "rb").read())
#     Encoders.encode_base64(part)
#     part.add_header('Content-Disposition', 'attachment; filename="'+path_to_output+'"')
#     msg.attach(part)
#
#     server = smtplib.SMTP('smtp.gmail.com')
#     server.sendmail(msg['From'], msg['To'], msg.as_string())


def send_good_results(email, time,path_to_output):
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
        # get_mail().sendmail()
        get_mail().send_message(msg)
    except Exception as e:
        debugPrint('COULDNT SEND GOOD MAIL')
        debugPrint(e.message)
