from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    from .models import Course
    course = Course.query.all()
    return render_template("home.html", user=current_user, course=course)


@views.route('/view-profile', methods=['GET', 'POST'])
@login_required
def view_profile():
    return render_template("profile_page.html", user=current_user)


@views.route('/edit-profile-page', methods=['GET', 'POST'])
@login_required
def edit_profile_page():
    try:
        if request.method == 'POST':
            email = request.form.get('email')
            fullname = request.form.get('name')
            city = request.form.get('city')
            user_id = current_user.id
            current_user_email = current_user.email

            from .models import User
            user = User.query.filter_by(email=email).first()
            if user and current_user_email != email:
                flash('Email is already taken, Use Differernt email ', category='error')
            elif len(fullname) < 3:
                flash('Enter a valif name ', category='error')
            elif len(email) < 4:
                flash('Enter a valid email', category='error')
            else:
                from .models import User
                edit_user = User.query.get(user_id)

                from . import db

                edit_user.fullname = fullname
                edit_user.email = email
                edit_user.city = city

                db.session.commit()
                flash('Profile update kar diya', category='success')
                return redirect(url_for('views.view_profile'))
    except Exception as e:
        print(e)
        flash('Error Exception Refresh the database', category='error')
    return render_template("edit_profile_page.html", user=current_user)


@views.route('/add-course-page', methods=['GET', 'POST'])
@login_required
def add_course_page():
    try:
        if request.method == 'POST':
            name = request.form.get('name')
            description = request.form.get('description')
            course_type = request.form.get('type')
            settings = request.form.get('settings')

            from .models import Course
            current_user_id = current_user.id
            course = Course.query.filter_by(name=name).first()
            if course and current_user_id == course.user_id:
                flash('The comment by this name ->  "' + name + '" is already added by you .', category='error')
                return redirect(url_for('views.home'))
            else:
                from . import db
                new_course = Course(name=name, description=description, course_type=course_type, settings=settings,
                                      user_id=current_user_id)
                db.session.add(new_course)
                db.session.commit()
                flash('New course Added. Thanks for contributing knowledge !!!', category='success')
                return redirect(url_for('views.home'))
    except Exception as e:
        print(e)
        flash('#Error', category='error')
    return render_template("add_course_page.html", user=current_user)


@views.route('/delete-course/<int:record_id>', methods=['GET', 'POST'])
@login_required
def delete_course(record_id):
    try:
        from .models import Course
        Course_details = Course.query.get(record_id)
        Course_name = Course_details.name
        from . import db
        db.session.delete(Course_details)
        db.session.commit()
        flash(Course_name + ' Course removed Successfully -> Do contact us if deleted by mistake. ', category='success')
    except Exception as e:
        print(e)
         
    return redirect(url_for('views.home'))


@views.route('/edit-course/<int:record_id>', methods=['GET', 'POST'])
@login_required
def edit_course(record_id):
    from .models import Course
    this_course = Course.query.get(record_id)
    this_course_name = this_course.name
    try:
        if request.method == 'POST':
            name = request.form.get('name')
            description = request.form.get('description')
            course_type = request.form.get('type')
            settings = request.form.get('settings')

            current_user_id = current_user.id
            course = Course.query.filter_by(name=name).first()
            if course and course.user_id == current_user_id and this_course_name != name:
                flash('The Course by the name ->  "' + name + '" is already added byy u, Try a differnt name for the course of the same field',
                      category='error')
            else:
                from . import db

                this_course.name = name
                this_course.description = description
                this_course.course_type = course_type
                this_course.settings = settings

                db.session.commit()
                flash('Course Updated Successfully__', category='success')
                return redirect(url_for('views.home'))
    except Exception as e:
        print(e)
         

    return render_template("edit_course_page.html", user=current_user, course=this_course)


@views.route('/add-log-page/<int:record_id>', methods=['GET', 'POST'])
@login_required
def add_log(record_id):
    from .models import Course, Log
    this_course = Course.query.get(record_id)
    import datetime
    now = datetime.datetime.now()
    try:
        if request.method == 'POST':
            when = request.form.get('date')
            value = request.form.get('value')
            notes = request.form.get('notes')
            from . import db
            new_log = Log(timestamp=when, value=value, notes=notes, course_id=record_id, user_id=current_user.id,
                          added_date_time=now)
            db.session.add(new_log)
            db.session.commit()
            flash(' Comment added successfully  ' + this_course.name + ' COMMENT', category='success')
            return redirect(url_for('views.home'))
    except Exception as e:
        print(e)
         
    return render_template("add_log_page.html", user=current_user, course=this_course, now=now)


@views.route('/view-course-graph-logs/<int:record_id>', methods=['GET', 'POST'])
@login_required
def view_course(record_id):
    from .models import Course, Log
    import datetime
    now = datetime.datetime.now()
    selected_course = Course.query.get(record_id)
    logs = Log.query.all()
    try:
        import sqlite3
        con = sqlite3.connect('E:\Quantified_Self_App\website\database.db')
        print("Database opened successfully")
        c = con.cursor()
        c.execute('SELECT timestamp, value FROM Log WHERE user_id={} AND course_id={}'.format(current_user.id,
                                                                                               selected_course.id))
        
       
        return render_template("logs_page.html", )
    except Exception as e:
        print(e)
         
        return render_template("logs_page.html", user=current_user, course=selected_course,
                               logs=logs)


@views.route('/delete-log/<int:record_id>', methods=['GET', 'POST'])
@login_required
def delete_log(record_id):
    from .models import Log
    Log_details = Log.query.get(record_id)
    course_id = Log_details.course_id
    try:
        from . import db
        db.session.delete(Log_details)
        db.session.commit()
        flash('Log Removed Successfully.', category='success')
    except Exception as e:
        print(e)
         
    return redirect(url_for('views.view_course', record_id=course_id))


@views.route('/edit-log/<int:record_id>', methods=['GET', 'POST'])
@login_required
def edit_log(record_id):
    from .models import Log, Course
    from . import db
    this_log = Log.query.get(record_id)
    this_course = Course.query.get(this_log.course_id)
    try:
        if request.method == 'POST':
            when = request.form.get('date')
            value = request.form.get('value')
            notes = request.form.get('notes')

            this_log.timestamp = when
            this_log.value = value
            this_log.notes = notes

            db.session.commit()
            flash(this_course.name + ' Log Updated Successfully.', category='success')
            return redirect(url_for('views.view_course', record_id=this_log.course_id))
    except Exception as e:
        print(e)
         

    return render_template("edit_log_page.html", user=current_user, course=this_course, log=this_log)
