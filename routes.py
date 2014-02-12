from flask import Flask, render_template, request, url_for, redirect
from downloademails import get_emails
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/viz')
def viz():
	emails = get_emails()
	return render_template('viz.html', emails=emails, test={2013: {'February': {'code': 5, 'scratch': 1, 'ascript': 1, 'resistance': 1, 'llu': 2, 'month': 1, 'screen': 1, 'follow': 1, 'displaying': 1, 'calculate': 1, 'e-mail': 3}, 
																	'March': {'code': 5, 'scratch': 1, 'ascript': 1, 'resistance': 1, 'llu': 2, 'month': 1, 'screen': 1, 'follow': 1, 'displaying': 1, 'calculate': 1, 'e-mail': 3}}})

if __name__ == '__main__':
	app.debug = True
	app.run()