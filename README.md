## OneSecMail
Disposable email is a service, that allows users to generate email address and receive emails at this temporary address. After certain period of time email will be deleted and address will be canceled. Disposable email is also called tempmail, 10minutemail, throwaway email, fake mail or trash mail.

### Why should you use disposable email?
To avoid SPAM. Today, a lot of web pages, blogs, forums and services are asking you to register or provide email address to read comments, download content or register account or profile. Next, a lot of this services will use your private email address to send you spam. That is why you should keep your private email address for your family and friends and should use disposable email always for for untrusted websites, to keep you privacy and avoid spam.

### How to use
The simplest example of use:
```
import time

mail = OneSecMail()
mail.generate_username()

while True:
    if mail.check_mail():
        mail.save_messages()
    time.sleep(5)
```

### What the script can do
1. Use the login entered by the user;
2. Generate login for the user;
3. Check email;
4. Save all emails in the following format:
```
Sender: dats.pavel1999@gmail.com
Subject: 123
To: ucu6h2eo5d@1secmail.net
Date: 2023-09-11 17:30:37
Content: 123
Attachments: deb-requirements.txt, CHANGELOG.md, _gitignore
```
5. Save attached files;
6. Delete temporary mail.

### Examples of use
```
[INFO] Username is not set. Generating...
[+] Your username: ucu6h2eo5d.
[+] Your email address: ucu6h2eo5d@1secmail.net.
[INFO] No new messages.
You have 1 unread message(s).
[INFO] Saving messages' id.
[INFO] Saving attachments.
```
