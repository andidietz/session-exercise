from flask import Flask, request, render_template, redirect, flash, session
from surveys import satisfaction_survey as survey
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-goes-here'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route('/')
def show_home():
    return render_template('/home.html', survey=survey)

@app.route('/start', methods=['POST'])
def start_survey():
    session['responses'] = []

    return redirect('/question/0')

@app.route('/question/<int:num>') 
def display_question(num):
    question = survey.questions[num]

    responses = session.get('responses')
    
    if len(responses) == len(survey.questions):
        return redirect('/thank_you')
    elif num != len(responses):
        flash(f'Invalid access to question {num}. Please complete form in the provide order.')
        return redirect(f'/question/{len(responses)}', )
    else:
        return render_template('questions.html', question=question, num=num)

@app.route('/answer', methods=['POST'])
def handle_answer():
    answer = request.form['answer']

    responses = session['responses']
    responses.append('answer')
    session['responses'] = responses

    if len(responses) == len(survey.questions):
        return redirect('/thank_you')
    else:
        return redirect(f'/question/{len(responses)}')

@app.route('/thank_you')
def thank():
    return render_template('thank_you.html')