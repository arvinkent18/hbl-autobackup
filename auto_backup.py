import pysftp
import os
import settings
import sys
from stat import S_ISDIR, S_ISREG

class AutoBackup:
    """
    Automates the backup of files via remote and local
    """

    # Constructor
    def __init__(self, host, username, password, option):
        self._host=host
        self._username=username
        self._password=password
        self._option=option

    # Host Property Decorator
    @property
    def host(self):
        return self._host

    # Host Setter
    @host.setter
    def host(self, x):
        self._host = x

    # Username Property Decorator
    @property
    def username(self):
        return self._username
    
    # Username Setter
    @username.setter
    def username(self, str):
        self._username = str
    
    # Password Property Decorator
    @property
    def password(self):
        return self._password

    # Password Setter
    @password.setter
    def password(self, str):
        self._password = str
    
    # Option Property Decorator
    @property
    def option(self):
        return self._option
    
    # Option Setter
    @option.setter
    def option(self, x):
        self._option = x  

    # Connection to SFTP
    def connect(self):
        return pysftp.Connection(self.host, username=self.username, password=self.password, cnopts=self.option) 

    # Starts the backing up of files in the remote server to local
    def start(self, sftp, remote_dir, local_dir, preserve_mtime=False):
        for index, entry in enumerate(sftp.listdir_attr(remote_dir)):
            print('Downloading {}'.format(entry.filename))

            remote_path = remote_dir + '/' + entry.filename
            local_path = os.path.join(local_dir, entry.filename) 
            mode = entry.st_mode

            print('Directory? {}'.format(S_ISDIR(mode)))

            if S_ISDIR(mode):
                try:
                    os.mkdir(local_path)
                    print('Generated Directory: {}'.format(local_path))
                except OSError:     
                    pass
                self.start(sftp, remote_path, local_path, preserve_mtime)  
            elif S_ISREG(mode):
                sftp.get(remote_path, local_path, preserve_mtime=preserve_mtime) 

                print('Downloaded {}'.format(entry.filename))             
    
if __name__ == '__main__':
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None  
    auto_backup = AutoBackup(
        os.getenv("HOST"),
        os.getenv("HOST_USERNAME"),
        os.getenv("HOST_PASSWORD"),
        cnopts   
    )
    sftp = auto_backup.connect()
    auto_backup.start(sftp, sys.argv[1], sys.argv[2], preserve_mtime=False)
    