from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)

app.config['SECRET_KEY'] = "love"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

RESPONSES = []
satisfaction_survey = surveys["satisfaction"]

@app.route('/')
def home_page():
    """Root Route"""
    return render_template('home.html', satisfaction_survey=satisfaction_survey)

@app.route('/question/<int:id>')
def ask_question(id):
    """Dynamic Question Routes"""
    resp_length = len(RESPONSES)
    if resp_length == len(satisfaction_survey.questions):
        flash("Invalid entry: Thanks for participating!")
        return redirect("/thanks")
    elif id > resp_length or id < resp_length:
        flash("Invalid entry: Please continue where you left off.")
        id = resp_length
        question = satisfaction_survey.questions[id]
        return redirect(f"/question/{id}")
    else:
        question = satisfaction_survey.questions[id]
        return render_template('question.html', question=question, id=id)

@app.route('/thanks')
def render_thanks():
    """Renders Thanks Page"""
    return render_template('thanks.html')

@app.route('/answer/<int:id>', methods=["POST"])
def capture_answer(id):
    """Listens for answers"""
    choice = request.form.get("choice")
    RESPONSES.append(choice)
    if id < len(satisfaction_survey.questions) - 1:
        id += 1
        return redirect(f"/question/{id}")
    else:
        return redirect(f"/thanks")