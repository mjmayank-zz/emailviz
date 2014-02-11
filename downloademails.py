import imaplib
import email
import bleach
import sys
import nltk
import getpass


userid = ""
gmailpwd = ""
SenderName = ''



# This function simply extracts the body of an email
def extract_body(payload):
    if isinstance(payload,str):
        return payload
    else:
        return '\n'.join([extract_body(part.get_payload()) for part in payload])

def get_emails():

    emails = []
    # Create a connection to gmail through port 993
    conn = imaplib.IMAP4_SSL("imap.gmail.com", 993)

    #Logs in to Gmail
    conn.login(userid, gmailpwd)

    #Selects the INBOX mailbox
    conn.select("[Gmail]/Sent Mail")

    #Gets all the email from SenderName. typ has the return code,
    #whereas data has the id of all the email from SenderName

    typ, data = conn.search(None, 'FROM', SenderName)
    x = 0
    try:
        for num in data[0].split():
            typ, msg_data = conn.fetch(num, '(RFC822)') #Gets the content of each email.
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1]) #If you are using Python 2.7 avoid the .decode("utf-8")
                    subject=bleach.clean(msg['subject'])
                    date = msg['date']
                    payload=msg.get_payload()
                    #body=bleach.clean(extract_body(payload)).replace('\n', ' ')
                    bodytext=msg.get_payload()[0].get_payload();
                    if type(bodytext) is list:
                        bodytext=','.join(str(v) for v in bodytext)
                        # print bodytext

                    # This is what helps with the language processing and tagging words
                    #text = nltk.word_tokenize(body)
                    emails.append(bodytext.strip())
            #limits number of emails that it pulls
            print x
            x = x + 1
            if x > 15:
                break
    finally:
        try:
            conn.close()

        except:
            pass
        conn.logout()
        return emails
