import pysftp
import os
import settings
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
    def start(self, remote_dir, local_dir, preserve_mtime=False):
        with pysftp.Connection(
            self.host, 
            username=self.username, 
            password=self.password, 
            cnopts=self.option
        ) as sftp:
            print('Connection successfully established ...')

            for entry in sftp.listdir_attr(remote_dir):
                remote_path = remote_dir + '/' + entry.filename
                local_path = os.path.join(local_dir, entry.filename) 
                mode = entry.st_mode

                if S_ISDIR(mode):
                    try:
                        os.mkdir(local_path)
                    except OSError:
                        pass
                    self.start(remote_dir, local_dir, preserve_mtime)      
                elif S_ISREG(mode):
                    sftp.get(remote_path, local_path, preserve_mtime=preserve_mtime)
    
if __name__ == '__main__':
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None  
    auto_backup = AutoBackup(
        os.getenv("HOST"),
        os.getenv("HOST_USERNAME"),
        os.getenv("HOST_PASSWORD"),
        cnopts   
    )
    auto_backup.start(
        '/home/hbladmin/hbposts.com/', 
        'D:\Programming\hbl\local_backup'
        preserve_mtime=False
    )


    