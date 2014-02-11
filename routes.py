from flask import Flask, render_template, request, url_for, redirect
from downloademails import get_emails
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/viz')
def viz():
	emails = get_emails()
	return render_template('viz.html', emails=emails)

if __name__ == '__main__':
	app.debug = True
	app.run()