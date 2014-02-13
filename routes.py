from flask import Flask, render_template, request, url_for, redirect
from downloademails import get_emails
import json
import sys
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/viz/<ty>')
def viz(ty):
	m_emails = ""
	y_emails = ""
	mth = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
	if len(sys.argv) > 1 and str(sys.argv[1]) == 'json':
		m_emails = json.load(open("m_emails.json", "r"), object_hook=_decode_dict)
		y_emails = json.load(open("y_emails.json", "r"), object_hook=_decode_dict)
	else:
		m_emails, y_emails = get_emails()
	if ty == 'year':
		return render_template('yearviz.html', emails=y_emails)
	else:
		return render_template('viz.html', emails=m_emails, mth=mth)

def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv

def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv


if __name__ == '__main__':
	app.debug = True
	app.run()