import contextlib
import ftplib
import logging
import re
from ftplib import FTP
from io import StringIO
from pathlib import Path
from typing import List

import click

dir_parse = re.compile(r"^([\w-]+)(?:\s+)(\d+)(?:\s)(\d)(?:\s+)(\d)(?:\s+)(\d+)(?:\s)(\w+)(?:\s+)(\d{1,2})(?:\s+)(\d{"
                       r"4}|\d{2}:\d{2})(?:\s)(.+)")

logger = logging.getLogger(__name__)


class FTPUploader:
    """
    Convenience class for uploading binary files to an FTP Server
    """

    def __init__(self, ftp_url: str, target_folder: str = "/", user='', passwd='',
                 create_not_existing: bool = True):
        """

        Parameters
        ----------

        ftp_url
            Server Address to Connect To
        target_folder
            Directory on FTP Server to Upload File(s) To
        user
            Defaults to ''. Username credential
        passwd
            Defaults to ''. Password credential
        create_not_existing
            If True, and ``target_folder`` does not exist the directory is recursively created.

        """
        self.ftp_url = ftp_url
        self.target_folder = target_folder
        self.create_not_existing = create_not_existing
        self.session = FTP(self.ftp_url)
        self.session.login(user, passwd)
        try:
            self.session.cwd(self.target_folder)
        except ftplib.error_temp as e:
            if self.create_not_existing:
                self._create_not_existing()
            else:
                raise e

    def upload(self, local_file_path: str) -> bool:
        """

        Parameters
        ----------
        local_file_path
            Filepath of local file

        Returns
        -------
        bool
            True if file was uploaded successfully. False if upload failed

        Notes
        -----

        A successful upload is determined by checking if the file exists. No integrity checks are performed

        """
        file = open(local_file_path, 'rb')
        file_name = str(Path(local_file_path).name)
        self.session.storbinary('STOR {}'.format(file_name), file)
        file.close()

        # confirm file uploaded
        file_list = self.session.nlst()
        if file_name in file_list:
            return True
        else:
            return False

    def shutdown(self):
        """
        Closes the FTP Session
        """
        self.session.quit()

    def _create_not_existing(self):
        target_parts = list(reversed(Path(self.target_folder).parts))

        while len(target_parts) > 0:
            try:
                part = target_parts.pop()
                # Does the directory exist?
                if part == "/":
                    continue
                if f"/{part}" == self.pwd():
                    continue
                if part in self.get_dir():
                    self.cd(part)
                else:
                    logger.info(f"Making Directory {part}")
                    self.mkdir(part)
                    self.cd(part)
            except Exception as e:
                raise e

    def get_dir(self) -> List[str]:
        """
        Get directories present in the current working directory


        Notes
        -----
        Internally, calls ``FTP.dir()`` and parses ``stdout`` response

        Returns
        -------
        List[str]
            List of directory names
        """
        dirs = []
        s = StringIO()
        with contextlib.redirect_stdout(s):
            self.session.dir()
        s = s.getvalue()
        for line in s.splitlines():
            try:
                folder_name = dir_parse.search(line).groups()[-1]
                dirs.append(folder_name)
            except AttributeError:
                continue
        return dirs

    def pwd(self):
        """
        Calls ``FTP.pwd()``
        """
        return self.session.pwd()

    def cd(self, dirname: str):
        """
        Change directory

        Parameters
        ----------
        dirname
            Directory to change to


        """
        return self.session.cwd(dirname)

    def mkdir(self, dirname: str):
        """
        Calls ``FTP.mkdir``

        Parameters
        ----------
        dirname
            Name of directory to create
        """
        return self.session.mkd(dirname)


@click.command()
@click.argument("fp", type=click.Path(exists=True))
@click.argument("url", type=str)
@click.argument("dst_dir", type=str)
def ftp_upload_script(fp: str, url: str, dst_dir: str):
    uploader = FTPUploader(ftp_url=url, target_folder=dst_dir)
    result = uploader.upload(fp)
    if result:
        click.echo(f"Upload {fp} Succeeded")
    else:
        click.echo(f"Upload {fp} Failed")


def ftp_upload(fp: str, url: str, dst_dir: str) -> bool:
    uploader = FTPUploader(ftp_url=url, target_folder=dst_dir)
    result = uploader.upload(fp)
    if result:
        return True
    else:
        return False


if __name__ == '__main__':
    ftp_upload_script()
