import imaplib
import email
import bleach
import sys
import nltk
import getpass
from nltk.corpus import stopwords
from collections import Counter, defaultdict
from dateutil import parser
import json


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

    # This contains the data that we want
    # Format: email_dict[year][monthname][word]
    email_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

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

                    # date stuff
                    date = msg['date']
                    dateformatted = parser.parse(date)
                    year = dateformatted.year
                    monthnumber = dateformatted.date
                    monthname = dateformatted.strftime("%B")

                    for part in msg.walk():
                        if part.get_content_type() == 'text/plain':
                            bodytext = part.get_payload()

                            # filtering
                            text = nltk.word_tokenize(bodytext)
                            text = [i for i in text if i not in stop]
                            taggedtext = nltk.tag.pos_tag(text)
                            nouns = [word for word,pos in taggedtext if pos == 'NN']
                            for word in nouns:
                                email_dict[year][monthname][word] += 1

                            # #shows nouns from each email in a string
                            # nounstring = ' '.join(nouns)
                            # emails.append(nounstring)
            print x
            x += 1
            if x > 25:
                break
    finally:
        try:
            conn.close()

        except:
            pass
        conn.logout()
        return json.dumps(email_dict)
