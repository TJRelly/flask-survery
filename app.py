from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "4534gdghjk5d#$RGR^HDG"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    """Root Route"""
    return render_template('home.html', satisfaction_survey=satisfaction_survey)

@app.route('/responses', methods=["POST"])
def set_reponses():
    session["responses"] = []
    return redirect('/question/0')

@app.route('/answer', methods=["POST"])
def capture_answer():
    """Listens for answers"""
    
    choice = request.form.get("choice")
    session["responses"].append(choice)
    session["adding_this_made_sessions_work"] = "why?"
    responses = session["responses"]
    
    if len(responses) == len(satisfaction_survey.questions):
        return redirect("/thanks")
    else:
        return redirect(f'/question/{len(responses)}')

@app.route('/question/<int:id>')
def ask_question(id):
    """Dynamic Question Routes"""

    responses = session["responses"]

    if len(responses) == len(satisfaction_survey.questions):
        flash("Invalid entry: Thanks for participating!")
        return redirect("/thanks")
    elif id != len(responses):
        
        flash("Invalid entry: Please continue where you left off.")
        return redirect(f"/question/{len(responses)}") 
    
    question = satisfaction_survey.questions[id] 
    return render_template("question.html", question=question, responses=session['responses']) 

@app.route('/thanks')
def render_thanks():
    """Renders Thanks Page"""
    return render_template('thanks.html', responses=session['responses'])


  