from flask import Flask, request, render_template, redirect, url_for

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    first, last, github = hackbright.get_student_by_github(github)
    project_grades = hackbright.get_grades_by_github(github)

    return render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           project_grades=project_grades)


@app.route("/student_form")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/add_student")
def add_student():
    """Display form to add a student to the student table in our database."""
    
    return render_template("add_student.html")


@app.route("/process_add", methods=["POST"])
def add_student_to_db():
    """Process the addition to our db and redirect to the student info page."""
    
    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    github = request.form.get('github')

    # add student to db
    hackbright.make_new_student(first_name, last_name, github)

    return redirect(url_for('student_add_success',
                    github=github))


@app.route("/success")
def student_add_success():
    """Displays a success notification."""
    github = request.args.get('github')

    return render_template("student_add_success.html",
                           github=github)


@app.route('/project')
def show_project():
    """Show details about a project."""

    title = request.args.get('title')
    title, description, max_grade = hackbright.get_project_by_title(title)

    return render_template('project_details.html',
                           title=title,
                           description=description,
                           max_grade=max_grade)

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
