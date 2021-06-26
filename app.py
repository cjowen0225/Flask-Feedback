from flask import Flask, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm
from flask_wtf import FlaskForm
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///flask_feedback"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "ASecret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.route("/")
def homepage():
    """Site Homepage"""

    return redirect("/register")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register a user by handling the form"""

    if "username" in session:
        return redirect (f"/users/{session['username']}")

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        user = User.register(username, password, first_name, last_name, email)
        db.session.commit()
        session['username'] = user.username
        return redirect(f"/users/{user.username}")

    else:
        return render_template("users/register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Create and handle form to login a User"""

    if 'username' in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid username/password"]
            return render_template("users/login.html", form=form)

    return render_template("users/login.html", form=form)

@app.route("/users/<username>")
def user_details(username):
    """Show logged in user's details"""

    if 'username' not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    form = DeleteForm()

    return render_template("users/details.html", user=user, form=form)

@app.route("/logout")
def logout():
    """Logout User"""

    session.pop("username")
    return redirect("/login")

@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """Delete a User"""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")
    return redirect("/login")

@app.route("/users/<username>/feedback/new", methods=["GET", "POST"])
def new_feedback(username):
    """Show and handle feedback form"""

    if "username" not in session or username != session['username']:
        raise Unauthorized()
    
    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data

        feedback = Feedback(title=title, description=description, username=username)
        db.session.add(feedback)
        db.session.commit()
        return redirect(f"/users/{feedback.username}")

    else:
        return render_template("feedback/new.html", form=form)

@app.route("/feedback/<int:feedback_id>/edit", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Show and handle update Feedback form"""

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session["username"]:
        raise Unauthorize()

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.description = form.description.data
        db.session.commit()
        return redirect(f"/users/{feedback.username}")
    
    return render_template("/feedback/edit.html", form=form, feedback=feedback)

@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete Feedback"""

    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")


