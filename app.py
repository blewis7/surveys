from flask import Flask, request, render_template, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'brockisgood'
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

responses = []


@app.route('/')
def homepage():
    '''The homepage needs to contain the title of the survey, instructions, and a start button'''
    return render_template('homepage.html', survey=survey)

@app.route('/begin')
def begin_survey():
    '''A place to reset responses to empty and then redirect to the first question'''
    if (len(responses) > len(survey.questions)):
        responses.clear()
    return redirect('/question/0')


@app.route('/question/<int:num>')
def questions(num):
    '''Display current question and possible choices'''

    if len(responses) != num:
        flash('Invalid question')
        return redirect(f'/question/{len(responses)}')

    question = survey.questions[num]
    return render_template('question.html', question=question, num=num)


@app.route('/answer')
def handle_question():
    '''Take the answer and append it to responses'''
    choice = request.args['answer']
    responses.append(choice)

    if (len(responses) == len(survey.questions)):
        return redirect('/complete')
    else:
        return redirect(f'/question/{len(responses)}')


@app.route('/complete')
def finished():
    answers = responses
    responses.clear()
    return render_template('complete.html')

    