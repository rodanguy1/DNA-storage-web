import requests


class checker:
    # '/home/omersabary/DNA-storage-tool/test.csv',
    if __name__ == '__main__':
        with open('./test.csv', 'rb') as f:
            r = requests.post('http://dmz-045.cs.technion.ac.il/upload', files={'1.csv': f})
            print(r.status_code)