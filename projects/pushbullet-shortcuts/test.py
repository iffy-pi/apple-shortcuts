import sys
import os
from PushBulletFileServer import *
import time

ACCESS_TOKEN = os.environ.get('CHATBERTA_PBFS_ACCESS_TOKEN')

def main():
    PushBulletFileServer.http_success(300, throw_exception=True)


    # mime_cont = open('mime.txt', 'rb').read()

    # if pbfs.save_file('/mime.txt', mime_cont) == 0:
    #     print('Save successful')
    # else:
    #     print('Save Failed')
    #     print('Error: {}'.format(pbfs.error_msg))

    # mime_cont = pbfs.get_file('/mime.txt')

    # if mime_cont is None:
    #     print('Error: {}'.format(pbfs.error_msg))
    #     return 0

    # print(mime_cont.decode('utf-8'))
    return 0
    

if __name__ == "__main__":
    sys.exit(main())
