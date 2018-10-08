import os, sys
from stat import S_ISDIR,S_ISREG
import configparser
# from pyArango.connection import *
from pyArango.connection import Connection, CreationError


def get_conn_details():
    config = configparser.ConfigParser()
    config.read('config.ini')
    details={}
    details['uname'] = config['DEFAULT']['arangodb_username']
    details['passwd'] = config['DEFAULT']['arangodb_password']
    return(details)

def start(uname,passwd):
    conn = Connection(username=uname, password=passwd)
    db = conn["mydrives"]
    filesCollection = db["files"]
    students = [('Oscar', 'Wilde', 3.5), ('Thomas', 'Hobbes', 3.2), 
        ('Mark', 'Twain', 3.0), ('Kate', 'Chopin', 3.8), ('Fyodor', 'Dostoevsky', 3.1), 
        ('Jane', 'Austen',3.4), ('Mary', 'Wollstonecraft', 3.7), ('Percy', 'Shelley', 3.5), 
        ('William', 'Faulkner', 3.8), ('Charlotte', 'Bronte', 3.0)]
    for (first, last, gpa) in students:
        doc = filesCollection.createDocument()
        doc['name'] = "%s %s" % (first, last)
        doc['gpa'] = gpa 
        doc['year'] = 2017
        doc._key = ''.join([first, last]).lower() 
        try: 
            doc.save()
        except CreationError:
            pass
def walktree(top, callback):
    '''recursively descend the directory tree rooted at top,
       calling the callback function for each regular file'''

    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        mode = os.stat(pathname).st_mode
        print(os.stat(pathname))
        print(os.path.getsize(pathname))
        if S_ISDIR(mode):
            # It's a directory, recurse into it
            walktree(pathname, callback)
        elif S_ISREG(mode):
            # It's a file, call the callback function
            callback(pathname)
        else:
            # Unknown file type, print a message
            print('Skipping %s' % pathname)

def visitfile(file):
    print('visiting', file)


    
def main():
    details = get_conn_details()
    start(details['uname'],details['passwd'])
    walktree('.', visitfile)


if __name__ == '__main__':
    main()


