from flask import Flask, request, render_template, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'brockisgood'
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


@app.route('/')
def homepage():
    '''The homepage needs to contain the title of the survey, instructions, and a start button'''
    return render_template('homepage.html', survey=survey)

@app.route('/begin', methods=['POST'])
def begin_survey():
    '''A place to reset responses to empty and then redirect to the first question'''
    session['responses'] = []
    return redirect('/question/0')


@app.route('/question/<int:num>')
def questions(num):
    '''Display current question and possible choices'''

    responses = session.get('responses')

    if len(responses) != num:
        flash('Invalid question')
        return redirect(f'/question/{len(responses)}')

    question = survey.questions[num]
    return render_template('question.html', question=question, num=num)


@app.route('/answer', methods=['POST'])
def handle_question():
    '''Take the answer and append it to responses'''
    responses = session['responses']
    choice = request.form['answer']
    responses.append(choice)
    session['responses'] = responses

    if (len(responses) == len(survey.questions)):
        return redirect('/complete')
    else:
        return redirect(f'/question/{len(responses)}')


@app.route('/complete')
def finished():
    '''Survey is complete'''
    return render_template('complete.html')

    