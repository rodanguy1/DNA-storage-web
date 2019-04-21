import datetime
import re
import subprocess
import sys
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
from utils.config import *
from time import *


def prepare_dict(files_list):
    files_dict = {'design.csv': files_list[0], 'after_alignment.csv': files_list[1],
                  'after_matching.csv': files_list[2], 'reads.fastq': files_list[3]}
    return files_dict


def save_files_on_server(files_list, run_id):
    files_dict = prepare_dict(files_list)
    # debug_print("in SaveFilesOnServer")
    if not os.path.isdir(get_dir() + os.sep + input_files_dir):
        # debug_print('in SaveFilesOnServer: the input path didnt exist')
        os.mkdir(get_dir() + os.sep + input_files_dir)
    directory_path = get_dir() + os.sep + input_files_dir + os.sep
    for name, fd in files_dict.items():
        file_path = directory_path + str(run_id) + '_' + name
        fd.save(file_path)


def debug_print(message):
    current_time = strftime("%H:%M:%S", gmtime())
    print("\n*****DEBUG: " + str(current_time) + " - " + str(message) + " ****************\n")


def time_diff(time1, time2):
    timeA = datetime.datetime.strptime(time1, "%H:%M:%S")
    timeB = datetime.datetime.strptime(time2, "%H:%M:%S")
    newTime = timeA - timeB
    return newTime


def delete_saved_files(run_id):
    path_to_files = get_dir() + os.sep + input_files_dir + os.sep
    # debug_print('in DeleteSavedFiles\nthe path to files is ' + str(path_to_files))
    file_suffixes = ['_design.csv', '_after_alignment.csv', '_after_matching.csv', '_reads.fastq']
    for suffix in file_suffixes:
        if os.path.exists(str(path_to_files) + str(run_id) + str(suffix)):
            os.remove(str(path_to_files) + str(run_id) + str(suffix))
        else:
            debug_print('Error: the file ' + str(path_to_files) + str(run_id) + str(suffix) + 'didnt exist')


def run_dna_tool(tool_path, run_id, analyzers, email):
    cmd = [sys.executable, tool_path, str(run_id)]
    # debug_print(cmd)
    start_time = strftime("%H:%M:%S", gmtime())
    try:
        process_output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        path_to_output = get_dir() + os.sep + str(run_id) + '_report.pdf'
        if os.path.exists(path_to_output):
            send_good_results(email,start_time,path_to_output)
        else:
            # send_bad_results
            pass
    except Exception as e:
        # send_bad_results
        debug_print('there was an err:')
        for line in e.output.decode('utf-8').split('\n'):
            print(line)
        err = str(e.output)
        traceback_regex = re.search(r'Traceback \(most recent call last\)[\S\s]*', err)
        if traceback_regex:
            traceback_str = traceback_regex.group()
            debug_print('THE TRACEBACK\n')
            for line in traceback_str.split('\n'):
                print(line)
        send_bad_results(email, start_time,run_time,traceback_str)
    finally:
        debug_print("in Finally statement")
        delete_saved_files(run_id)


def send_bad_results(email, start_time, run_time, traceback_str):
    pass


def contains_non_ascii_characters(str):
    return not all(ord(c) < 128 for c in str)


def add_header(message, header_name, header_value):
    if contains_non_ascii_characters(header_value):
        h = Header(header_value, 'utf-8')
        message[header_name] = h
    else:
        message[header_name] = header_value
    return message


def send_good_results(email, time,path_to_output):
    debug_print('in send_good_results')
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
    plain = ' your DNA-STORAGE-TOOL results of run that started on: '+ str(time)+' are now available to Download'
    if contains_non_ascii_characters(plain):
        plain_text = MIMEText(plain.encode('utf-8'), 'plain', 'utf-8')
    else:
        plain_text = MIMEText(plain, 'plain')
    msg.attach(plain_text)
    with open(path_to_output, "rb") as fil:
        part = MIMEApplication(
            fil.read(),
            Name=basename(path_to_output)
        )
    # After the file is closed
    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(path_to_output)
    msg.attach(part)
    # try:
    get_mail().send_message(msg)
    # except:
    #     print("COULDN'T SEND EMAIL")
