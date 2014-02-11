import imaplib
import email
import bleach
import sys
import nltk
import getpass
from nltk.corpus import stopwords


userid = "tjhackathon"
gmailpwd = "hackTJ1234"
SenderName = 'hackTJ'



# This function simply extracts the body of an email
def extract_body(payload):
    if isinstance(payload,str):
        return payload
    else:
        return '\n'.join([extract_body(part.get_payload()) for part in payload])

def get_emails():

    emails = []
    stop = stopwords.words('english')
    stop.extend(['<', '>', '--', '-'])
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
                    for part in msg.walk():
                        if part.get_content_type() == 'text/plain':
                            bodytext = part.get_payload()
                            text = nltk.word_tokenize(bodytext)
                            print type(stop)
                            text = [i for i in text if i not in stop]
                            #tags the list with word type and puts it into typles
                            taggedtext = nltk.tag.pos_tag(text)
                            # list of nouns
                            nouns = [word for word,pos in taggedtext if pos == 'NN']
                            emails.append(bodytext.strip())

                    # This is what helps with the language processing and tagging words
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
