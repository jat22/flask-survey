from flask import Flask, render_template, request, redirect, url_for
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secert'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []
ques_num = 0

@app.route('/')
def landing ():
	survey_title = satisfaction_survey.title
	survey_instructions = satisfaction_survey.instructions
	return render_template('landing.html', title = survey_title, instructions = survey_instructions)

@app.route('/questions/<int:count>')
def gen_ques(count):
	global ques_num
	global responses
	if ques_num != len(responses):
		raise
		return redirect('/questions/<len(responses)>')
	question = satisfaction_survey.questions[count].question
	choices = satisfaction_survey.questions[count].choices
	return render_template('questions.html', question = question, choices = choices)
	

@app.route('/answers', methods=["POST"])
def answers():
	response = request.form['choice']
	responses.append(response)
	global ques_num
	if ques_num == len(satisfaction_survey.questions) - 1:
		return redirect('/thank_you')
	else:
		ques_num += 1
		return redirect(url_for('gen_ques', count = ques_num))

@app.route('/thank_you')
def thanks():
	survey_title = satisfaction_survey.title
	return render_template('thank_you.html', title = survey_title)