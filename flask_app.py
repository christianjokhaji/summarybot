import openai

from flask import Flask, render_template, request, redirect, url_for, session

def create_app(test_config = None):
	app = Flask(__name__, instance_relative_config = True)

	app.config.from_mapping(SECRET_KEY = 'dev')

	@app.route('/', methods=('GET', 'POST'))
	def index():
		if request.method == 'POST':

			session['text'] = request.form['box']

			return redirect(url_for('summary'))

		return render_template('index.html')

	@app.route('/summary', methods=('GET', 'POST'))
	def summary():

		if request.method == 'POST':
			session.clear()
			return redirect(url_for('index'))

		openai.api_key = "YOUR_API_KEY_HERE"

		response = openai.Completion.create(
		  model="text-davinci-003",
		  prompt=f"Summarize the article: {session.get('text')}",
		  temperature=0.7,
		  max_tokens=1000,
		  top_p=1,
		  frequency_penalty=0,
		  presence_penalty=1
		)

		return render_template('summary.html', response=response.get('choices')[0].get('text').strip(), link=session.get('text'))

	return app

app = create_app()
