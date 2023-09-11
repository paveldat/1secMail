"""
        ██▄██ ▄▀▄ █▀▄ █▀▀ . █▀▄ █░█
        █░▀░█ █▄█ █░█ █▀▀ . █▀▄ ▀█▀
        ▀░░░▀ ▀░▀ ▀▀░ ▀▀▀ . ▀▀░ ░▀░
▒▐█▀█─░▄█▀▄─▒▐▌▒▐▌░▐█▀▀▒██░░░░▐█▀█▄─░▄█▀▄─▒█▀█▀█
▒▐█▄█░▐█▄▄▐█░▒█▒█░░▐█▀▀▒██░░░░▐█▌▐█░▐█▄▄▐█░░▒█░░
▒▐█░░░▐█─░▐█░▒▀▄▀░░▐█▄▄▒██▄▄█░▐█▄█▀░▐█─░▐█░▒▄█▄░
"""

import requests
import string
import random
from pathlib import Path


class OneSecMail:
    """
    A class for creating one-time temporary mail.
    It issues a temporary email address to which emails can be sent.
    All emails are saved in the `mails/` folder (by default).
    """

    def __init__(self,
                 username: str = None,
                 username_length: int = 10,
                 mails_save_path: [str, Path] = 'mails',
                 save_attachments: bool = True) -> None:
        """
        Constructor.

        Args:
            * username - Username of the user (default: None).
            * username_length - The length of the generated username
                                (default: 10).
            * mails_save_path - Path to save messages (default: mails).
            * save_attachments - Save attachments or not (default: True).
        """

        self.__api = 'https://www.1secmail.com/api/v1/'
        self.__domain_list = (
            "1secmail.com",
            "1secmail.org",
            "1secmail.net"
        )
        self.__domain = random.choice(self.__domain_list)
        self.username = username
        self.__username_length = username_length
        self.__mails_save_path = Path(mails_save_path)
        self.__save_attachments = save_attachments
        self.__id_list = []

    @property
    def domain(self) -> str:
        return self.__domain

    def generate_username(self) -> str:
        """
        Generates username.
        Uses ascii lowercase letters and digits.

        Returns:
            * The generated user name if the username was not specified,
              otherwise the entered username.
        """

        if self.username is None:
            print('[INFO] Username is not set. Generating...')
            characters = string.ascii_lowercase + string.digits
            username = ''.join(random.choice(characters)
                               for _ in range(self.__username_length))
            self.username = username
        else:
            print('[INFO] Username was set manually.')
        print(f'[+] Your username: {self.username}.')
        print(f'[+] Your email address: {self.username}@{self.__domain}.')
        return self.username

    def check_mail(self) -> bool:
        """
        Checks if there are new messages.

        Returns:
            * True - if there are new messages,
              False - otherwise.
        """

        login = f'login={self.username}&domain={self.__domain}'
        req_url = f'{self.__api}?action=getMessages&{login}'
        req = requests.get(req_url).json()

        if len(req) == 0:
            print('[INFO] No new messages.')
            return False
        else:
            print(f'You have {len(req)} unread message(s).')
            print('[INFO] Saving messages\' id.')
            for mail in req:
                for k, v in mail.items():
                    if k == 'id':
                        self.__id_list.append(v)
            return True

    def save_messages(self) -> None:
        """
        Saves messages.
        """

        Path(self.__mails_save_path).mkdir(exist_ok=True, parents=True)
        login = f'login={self.username}&domain={self.__domain}'
        for i in self.__id_list:
            read_msg = f'{self.__api}?action=readMessage&{login}&id={i}'
            req = requests.get(read_msg).json()

            sender = req.get('from')
            subject = req.get('subject')
            date = req.get('date')
            content = req.get('textBody')

            mail_file_path = Path(self.__mails_save_path) / f'{i}' / f'{i}.txt'
            mail_file_path.parent.mkdir(exist_ok=True, parents=True)
            with open(mail_file_path, 'w') as file:
                file.write(f'Sender: {sender}\nSubject: {subject}\n' +
                           f'To: {self.username}@{self.__domain}\n' +
                           f'Date: {date}\nContent: {content}')

            if self.__save_attachments:
                files_to_download = []
                attachments = req.get('attachments')
                for attachment in attachments:
                    for k, v in attachment.items():
                        if k == 'filename':
                            files_to_download.append(v)
                if files_to_download:
                    print('[INFO] Saving attachments.')
                    with open(mail_file_path, 'a') as file:
                        file.write(f'Attachments: ' +
                                   f'{", ".join(files_to_download)}')
                    for file in files_to_download:
                        action = 'action=download'
                        download_files = f'{self.__api}?{action}&{login}'
                        download_files += f'&id={i}&file={file}'
                        file_path = mail_file_path.parent / 'attachments'
                        file_path /= f'{file}'
                        file_path.parent.mkdir(exist_ok=True, parents=True)
                        response = requests.get(download_files)
                        with open(file_path, mode='wb') as file:
                            file.write(response.content)
                else:
                    print('[INFO] No attachments found.')

    def delete_mailbox(self) -> None:
        """
        Removes created mailbox.
        """

        url = 'https://www.1secmail.com/mailbox'
        data = {
            'action': 'deleteMailbox',
            'login': self.username,
            'domain': self.__domain
        }

        req = requests.post(url, data)
        mailbox = f'{self.username}@{self.__domain}'
        print(f'[X] Mailbox {mailbox} was removed.')
