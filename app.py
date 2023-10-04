from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"

debug = DebugToolbarExtension(app)

survey = satisfaction_survey

@app.route('/')
def home():
    """Show survey title, instructions, and start button"""
    return render_template("home.html", survey=survey)

@app.route('/start', methods=["POST"])
def start():
    """Initialize session storage to an empty list and redirect user to first question"""
    session["responses"] = []
    return redirect("/questions/0")

@app.route("/questions/<idx>")
def questions(idx):
    """Show survey questions one by one"""
    if int(idx) != len(session["responses"]):
        flash("Invalid URL entered, redirected to correct URL.")
        idx = len(session["responses"])
    if int(idx) >= len(survey.questions):
        return redirect("/thanks")
    question = survey.questions[int(idx)].question
    choices = survey.questions[int(idx)].choices
    return render_template("questions.html", idx=idx, question=question, choices=choices)

    

@app.route("/answer/<idx>", methods=["POST"])
def answer(idx):
    """Append the user's answer to the responses list and redirect to the next question"""
    responses = session["responses"]
    responses.append(request.form[idx])
    session["responses"] = responses
    if len(session["responses"]) < len(survey.questions):
        return redirect(f"/questions/{int(idx)+1}")
    return redirect("/thanks")

@app.route("/thanks")
def thanks():
    """Thank the user when they have completed the survey"""
    return render_template("thanks.html")
    