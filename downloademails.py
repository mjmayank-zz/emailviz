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


userid = "mjmayank"
gmailpwd = "wiliuscavdnmvqkq"
SenderName = 'Mayank Jain'



# This function simply extracts the body of an email
def extract_body(payload):
    if isinstance(payload,str):
        return payload
    else:
        return '\n'.join([extract_body(part.get_payload()) for part in payload])

def get_emails():

    jobj = []
    stop = stopwords.words('english')
    stop.extend(['<', '>', '--', '-', 'gt', 'It', '@', '%', 'lt'])
    # Create a connection to gmail through port 993
    conn = imaplib.IMAP4_SSL("imap.gmail.com", 993)

    #Logs in to Gmail
    conn.login(userid, gmailpwd)

    #Selects the INBOX mailbox
    conn.select("[Gmail]/Sent Mail")

    # This contains the data that we want
    # Format: email_dict[year][monthname][word]
    m_email_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    y_email_dict = defaultdict(lambda: defaultdict(int))

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
                            bodytext = bleach.clean(part.get_payload())

                            # filtering
                            text = nltk.word_tokenize(bodytext)
                            text = [i for i in text if i not in stop]
                            taggedtext = nltk.tag.pos_tag(text)
                            nouns = [word for word,pos in taggedtext if pos == 'NN' or pos == 'NP']
                            for word in nouns:
                                m_email_dict[year][monthname][word] += 1
                                y_email_dict[year][word] += 1

                            # #shows nouns from each email in a string
                            # nounstring = ' '.join(nouns)
                            # emails.append(nounstring)
            if x%20 == 0:
                print x
            x += 1
            if x == 1000:
                break;

    finally:
        try:
            conn.close()

        except:
            pass
        for year in m_email_dict.keys():
            for month in m_email_dict[year].keys():
                for word in m_email_dict[year][month].keys():
                    if m_email_dict[year][month][word] < 3 or m_email_dict[year][month][word] > 55:
                        del m_email_dict[year][month][word]

        for year in y_email_dict.keys():
            for word in y_email_dict[year].keys():
                if y_email_dict[year][word] < 3 or y_email_dict[year][word] > 55:
                    del y_email_dict[year][word]

        m_email_dict = json.dumps(m_email_dict, sort_keys=True, indent=4, separators=(',', ': '))
        y_email_dict = json.dumps(y_email_dict, sort_keys=True, indent=4, separators=(',', ': '))
        open("m_emails.json", 'w').writelines(m_email_dict)
        open("y_emails.json", 'w').writelines(y_email_dict)
        conn.logout()
        return m_email_dict, y_email_dict


if __name__ == '__main__':
  get_emails()

