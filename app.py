from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secert'
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

QUES_NUM = 'ques_num'
RESPONSES = 'responses'

@app.route('/')
def landing ():
	survey_title = satisfaction_survey.title
	survey_instructions = satisfaction_survey.instructions
	return render_template('landing.html', title = survey_title, instructions = survey_instructions)

@app.route('/reset_responses', methods=['POST'])
def response_reset():
	session[RESPONSES] = []
	session[QUES_NUM] = 0
	return redirect(url_for('gen_ques', count = session[QUES_NUM]))	

@app.route('/questions/<int:count>')
def gen_ques(count):
	print(session)
	##global ques_num
	# if count != len(session['responses']):
	# 	flash("You are attempting to access an invalid question")
	# 	return redirect(url_for('gen_ques', count = len(session['responses'])))
	question = satisfaction_survey.questions[count].question
	choices = satisfaction_survey.questions[count].choices
	return render_template('questions.html', question = question, choices = choices)
	

@app.route('/answers', methods=["POST"])
def answers():
	response = request.form['choice']
	ans = session['responses']
	ans.append(response)
	session['responses'] = ans
	print(session['responses'])
	print(response)
	global ques_num
	if session[QUES_NUM] == len(satisfaction_survey.questions) - 1:
		return redirect('/thank_you')
	else:
		ques_num = session[QUES_NUM] + 1
		session[QUES_NUM] = ques_num
		return redirect(url_for('gen_ques', count = session[QUES_NUM]))

@app.route('/thank_you')
def thanks():
	survey_title = satisfaction_survey.title
	return render_template('thank_you.html', title = survey_title)