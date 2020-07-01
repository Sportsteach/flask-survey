from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "dans-the-man"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

ANSWERS = "answers"


@app.route('/')
def home_page():
    """Shows home page"""

    return redirect("/start")


@app.route('/start')
def start_page():
    """Shows link to survey link"""
    session[ANSWERS] = []
    return render_template('/start.html', survey=survey)


@ app.route('/questions/<int:id>')
def questions_page(id):
    """Shows the prompts for the questions"""
    responses = session.get(ANSWERS)

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    if (len(responses) != id):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {id}.")
        return redirect(f"/questions/{len(responses)}")
    question = survey.questions[id]
    return render_template('questions.html', question=question)


@app.route("/answer", methods=["POST"])
def handle_question():
    """Save response and redirect to next question."""
    # get the response choice
    choice = request.form['answer']

    # add this response to the session
    responses = session[ANSWERS]
    responses.append(choice)
    session[ANSWERS] = responses

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")


@app.route('/complete')
def complete_page():
    """Shows the complete page after survey"""
    return render_template('/complete.html')
