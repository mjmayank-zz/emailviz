import imaplib
import email

userid = "tjhackathon"
gmailpwd = "hackTJ1234"
SenderName = 'hackTJ'

emails = []

# This function simply extracts the body of an email
def extract_body(payload):
    if isinstance(payload,str):
        return payload
    else:
        return '\n'.join([extract_body(part.get_payload()) for part in payload])

# Create a connection to gmail through port 993
conn = imaplib.IMAP4_SSL("imap.gmail.com", 993)

#Logs in to Gmail
conn.login(userid, gmailpwd)

#Selects the INBOX mailbox
conn.select("[Gmail]/Sent Mail")

#Gets all the email from SenderName. typ has the return code,
#whereas data has the id of all the email from SenderName
typ, data = conn.search(None, 'FROM', SenderName)
try:
    for num in data[0].split():
        typ, msg_data = conn.fetch(num, '(RFC822)') #Gets the content of each email.
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(response_part[1].decode("utf-8")) #If you are using Python 2.7 avoid the .decode("utf-8")
                subject=msg['subject']                  
                payload=msg.get_payload()
                body=extract_body(payload)
                emails.append((subject,body))
finally:
    try:
        print emails
        conn.close()
    except:
        pass
    conn.logout()