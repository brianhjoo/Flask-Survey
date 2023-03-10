from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


responses = []


@app.get('/')
def display_start_page():
    """ renders survery_start.html template, displaying the title and
    instructions of survey with survey start button """

    return render_template(
        'survey_start.html',
        title=survey.title,
        instructions=survey.instructions
    )

@app.post('/begin')
def handle_start():
    """ redirects user to first question of survey """

    responses.clear()

    return redirect('/questions/0')

@app.get('/questions/<int:num>')
def display_question(num):
    """ renders question.html template, displaying a form asking the
    question and radio button choices """

    return render_template('question.html', question=survey.questions[num])

@app.post('/answer')
def handle_answer():
    """ appends answer to responses list and redirects user to next question"""

    responses.append(request.form['answer'])

    if len(responses) == len(survey.questions):
        return redirect('/completion')
    else:
        return redirect(f'questions/{len(responses)}')

@app.get('/completion')
def thank_user():
    """ renders completion.html template, thanking the user and providing them
    with their survey results """

    return render_template(
        'completion.html',
        questions=survey.questions,
        answers=responses
    )




