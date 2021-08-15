from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user, login_user, logout_user
from .models import User, Tasks, PeriodTasks, DateTasks
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func
from SaveAndStartYourPlans import db
from datetime import datetime

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        pass_user = request.form.get('pass')

        user_inserted = User.query.filter_by(username=username).first()

        if user_inserted:
            if check_password_hash(user_inserted.password, pass_user):
                flash('Logged in successfully!', category='success')
                login_user(user_inserted, remember=True)
                return redirect(url_for('auth.user_app'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            if username == '' and pass_user == '':
                flash("Please enter your username and password!", category='error')
            else:
                flash('Username does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('user_email')
        user = request.form.get('username')
        password = request.form.get('pass')
        password_conf = request.form.get('pass_confirm')

        user_inserted = User.query.filter_by(username=user).first()

        if email == '' and user == '' and password == '' and password_conf == '':
            flash('You haven\'t completed all fields!', category='error')
        elif user_inserted:
            flash('User already exists! Try another username.', category='error')
        elif len(user) < 2:
            flash('Username must be greater than 1 characters.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif password != password_conf:
            flash('Password don\'t match.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(username=user, email=email, password=generate_password_hash(
                password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)

# @auth.route('/error404')
# def error_404():
#     return render_template("error404.html")


@auth.route('/user-app', methods=['GET', 'POST'])
@login_required
def user_app():
    if request.method == 'POST' and 'SAVE' == request.form.get('buttSaveTask'):
        selected_radio_butt = request.form.get('plan')
        # print(f'---{selected_radio_butt}--')
        is_name_plan = False
        is_selected_task = False

        if selected_radio_butt == 'addNamePlan':
            name_user_plan = request.form.get('textNamePlan')
            if name_user_plan:
                is_name_plan = True
                is_selected_task = False
        elif selected_radio_butt == 'selectedPlan':
            name_user_plan = request.form.get('listTasks')
            # print(f'--{name_user_plan}--')
            if name_user_plan:
                is_selected_task = True
                is_name_plan = False

        start_plan = request.form.get("timeS")
        end_plan = request.form.get("timeE")

        is_days_week = False
        is_one_time = False
        is_spec_time = False

        checkbox_days_week = request.form.getlist('nameDayWeek')
        if checkbox_days_week:
            is_days_week = True
            is_one_time = False
            is_spec_time = False

        one_time_date = request.form.get('date')
        if one_time_date:
            is_days_week = False
            is_one_time = True
            is_spec_time = False

        specific_dates = []
        spec_date1 = request.form.get('date1')
        spec_date2 = request.form.get('date2')

        if spec_date1 and spec_date2:
            is_days_week = False
            is_one_time = False
            is_spec_time = True
            specific_dates.append(spec_date1)
            specific_dates.append(spec_date2)

            nr = 3
            while(request.form.get('date' + str(nr))):
                spec_date = request.form.get('date' + str(nr))
                specific_dates.append(spec_date)
                nr += 1

        #print(f'{is_name_plan} + {is_selected_task} + {start_plan} + {end_plan} + {is_days_week} + {is_one_time} + {is_spec_time}')
        if((is_name_plan == False and is_selected_task == False) or start_plan == None or end_plan == None or (is_days_week == False and is_one_time == False and is_spec_time == False)):
            flash('Please complete all fields !', category='error')
        else:
            new_user_task = Tasks(
                task=name_user_plan, id_user=current_user.id)
            db.session.add(new_user_task)
            db.session.commit()
            current_task = Tasks.query.filter_by(
                task=name_user_plan, id_user=current_user.id).first()

            if is_days_week:
                for day in checkbox_days_week:
                    new_days_task = PeriodTasks(day_task=day, start_task=func.to_date(
                        start_plan, 'HH24:MI'), end_task=func.to_date(end_plan, 'HH24:MI'), id_task=current_task.id)
                    db.session.add(new_days_task)
                    db.session.commit()
            elif is_one_time:
                new_date_task = DateTasks(date_task=func.to_date(one_time_date, 'YYYY-MM-DD'), start_task=func.to_date(
                    start_plan, 'HH24:MI'), end_task=func.to_date(end_plan, 'HH24:MI'), id_task=current_task.id)
                db.session.add(new_date_task)
                db.session.commit()
            elif is_spec_time:
                for value_date in specific_dates:
                    new_dates_task = DateTasks(date_task=func.to_date(value_date, 'YYYY-MM-DD'), start_task=func.to_date(
                        start_plan, 'HH24:MI'), end_task=func.to_date(end_plan, 'HH24:MI'), id_task=current_task.id)
                    db.session.add(new_dates_task)
                    db.session.commit()
            flash('Task added !', category='success')
    elif request.method == 'POST' and 'CANCEL' == request.form.get('buttCancelTask'):
        pass
    elif request.method == 'POST' and not 'SAVE' == request.form.get('buttSaveTask') and not 'CANCEL' == request.form.get('buttCancelTask'):
        title_task = request.form.get('delete_yes')

        if title_task:
            view_task = Tasks.query.filter_by(task=title_task).first()
            rows_perT = PeriodTasks.query.filter(
                PeriodTasks.id_task == view_task.id).count()
            rows_dateT = DateTasks.query.filter(
                DateTasks.id_task == view_task.id).count()

            if rows_perT:
                PeriodTasks.query.filter(
                    PeriodTasks.id_task == view_task.id).delete()
                db.session.commit()

            if rows_dateT:
                DateTasks.query.filter(
                    DateTasks.id_task == view_task.id).delete()
                db.session.commit()

            Tasks.query.filter(Tasks.task == title_task).delete()
            db.session.commit()

            flash('Task was successfully deleted!', category='success')

    user_tasks = Tasks.query.filter_by(id_user=current_user.id).all()
    max_rows = Tasks.query.filter(Tasks.id_user == current_user.id).count()

    list_user_tasks = [''] * max_rows
    count = 0
    check_today_PT, check_today_DT = (False, False)

    date_today = datetime.now()
    name_day_today = date_today.strftime('%A')
    format_date_today = "{}-{}-{}".format(date_today.day,
                                          date_today.month, date_today.year)

    for i in range(0, max_rows):
        array = []

        period_tasks = PeriodTasks.query.filter_by(
            id_task=user_tasks[i].id).all()
        nb_rows_per_t = PeriodTasks.query.filter(
            PeriodTasks.id_task == user_tasks[i].id).count()
        #print(f'nr per task: {nb_rows_per_t}')

        date_tasks = DateTasks.query.filter_by(id_task=user_tasks[i].id)
        nb_rows_dt = DateTasks.query.filter(
            DateTasks.id_task == user_tasks[i].id).count()

        check_today_PT = False
        check_today_DT = False

        if nb_rows_per_t:

            for j in range(0, nb_rows_per_t):
                #print(f'per task: {period_tasks[j].day_task}')
                nm_weekday = period_tasks[j].day_task

                if nm_weekday.upper() == name_day_today.upper():
                    check_today_PT = True

                    time_1 = period_tasks[j].start_task
                    time_1_h = time_1.hour
                    time_1_min = time_1.minute

                    time_2 = period_tasks[j].end_task
                    time_2_h = time_2.hour
                    time_2_min = time_2.minute

                    calc_time = (60 - time_1_min) + time_2_min
                    if calc_time >= 60:
                        mm = calc_time - 60
                        hh = 0
                    else:
                        mm = calc_time
                        hh = 1

                    dif_hours = time_2_h - time_1_h - hh
                    dif_minutes = mm

                    dif_time = "{}, {}".format(dif_hours, dif_minutes)
                    array.append(dif_time)

                    time_start = str(time_1_h) + ":" + str(time_1_min)
                    array.append(time_start)

                    time_end = str(time_2_h) + ":" + str(time_2_min)
                    array.append(time_end)

        if nb_rows_dt:

            for j in range(0, nb_rows_dt):
                date = date_tasks[j].date_task
                format_date = "{}-{}-{}".format(date.day,
                                                date.month, date.year)

                if format_date == format_date_today:
                    check_today_DT = True

                    time_1 = date_tasks[j].start_task
                    time_1_h = time_1.hour
                    time_1_min = time_1.minute

                    time_2 = date_tasks[j].end_task
                    time_2_h = time_2.hour
                    time_2_min = time_2.minute

                    calc_time = (60 - time_1_min) + time_2_min
                    if calc_time >= 60:
                        mm = calc_time - 60
                        hh = 0
                    else:
                        mm = calc_time
                        hh = 1

                    dif_hours = time_2_h - time_1_h - hh
                    dif_minutes = mm

                    dif_time = "{}, {}".format(dif_hours, dif_minutes)
                    array.append(dif_time)

                    time_start = str(time_1_h) + ":" + str(time_1_min)
                    array.append(time_start)

                    time_end = str(time_2_h) + ":" + str(time_2_min)
                    array.append(time_end)

        if check_today_PT or check_today_DT:
            array.append(user_tasks[i].task)
            list_user_tasks[count] = array
            count += 1

    list_user_tasks = [x for x in list_user_tasks if x != '']

    #print(f'format dt today: {format_date_today}')
    #print(f'lista task user: {list_user_tasks}')
    return render_template("user-page.html", all_user_tasks=list_user_tasks)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
