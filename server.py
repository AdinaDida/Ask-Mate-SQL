from flask import Flask, render_template, redirect, request, url_for
import data_manager
import conection
import time
import os
from werkzeug.utils import secure_filename
import datetime

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
@app.route('/search')
def route_index():
    questions = data_manager.display_latest_five_questions()
    query = False
    if request.args:
        quest = request.args.get('q')
        result = data_manager.search_questions_by_pattern(quest)[0]
        count = data_manager.search_questions_by_pattern(quest)[1]
        query = True
        return render_template('index.html', questions=result, query=query, quest=quest, count=count)
    return render_template('index.html', questions=questions, query=query)


@app.route('/list')
def route_list():
    questions_list = data_manager.display_questions()
    if request.args:
        order_by = request.args.get('order_by')
        order_direction = request.args.get('order_direction')
        questions = data_manager.sort_all_questions(order_by, order_direction)
        return render_template('list.html', questions_list=questions, order_by=order_by,
                               order_direction=order_direction)
    return render_template('list.html', questions_list=questions_list)


@app.route('/question/<question_id>')
def route_question(question_id):
    question_data = data_manager.question(question_id)
    answers = data_manager.get_answers_by_question_id(question_id)
    comment_question = data_manager.get_comment_by_question(question_id)
    comment_answer = data_manager.get_comment_by_answer()
    return render_template('question.html', question_id=question_id, question=question_data['title'],
                           question_message=question_data['message'],
                           answer_images=answers, comment=comment_question,
                           answer_comment=comment_answer, )


@app.route('/add-question', methods=['GET', 'POST'])
def route_add_question():
    if request.method == 'POST':
        submission_time = datetime.datetime.now()
        view_number = 1
        vote_number = 0
        title = request.form['title']
        message = request.form['message']

        file = request.files['image_file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image = file.filename

        data_manager.add_question(submission_time, view_number, vote_number, title, message, image)
        id_ = data_manager.get_id_of_question_by_time(submission_time)

        return redirect(url_for('route_question', question_id=id_))
    return render_template('add_question.html')


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def route_add_answer(question_id):
    if request.method == 'POST':
        submission_time = datetime.datetime.now()
        vote_number = 0
        message = request.form['message']

        file = request.files['image_file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image = file.filename
        else:
            image = ""

        data_manager.add_answer(submission_time, vote_number, question_id, message, image)
        return redirect(url_for('route_question', question_id=question_id))
    return render_template('new_answer.html', question_id=question_id)


@app.route('/question/<int:question_id>/edit', methods=["GET", "POST"])
def route_update_question(question_id):
    questions_list = data_manager.question(question_id)

    if request.method == 'POST':
        submission_time = datetime.datetime.now()
        title = request.form['title']
        message = request.form['message']
        data_manager.update_question(question_id, submission_time, title, message)
        return redirect(url_for('route_question', question_id=question_id))
    return render_template('update_question.html', question_id=question_id, message=questions_list['message'],
                           title=questions_list['title'])


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    data_manager.delete_question(question_id)
    return redirect('/list')


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    id_ = data_manager.get_question_by_answer(answer_id)
    data_manager.delete_answer(answer_id)
    return redirect(url_for('route_question', question_id=id_))

@app.route('/comment/<int:comment_id>/delete')
def delete_comment(comment_id):
    id_ = data_manager.get_question_id_by_comment(comment_id)
    data_manager.delete_comment_question(comment_id)


    return redirect(url_for('route_question', question_id=id_))


@app.route("/question/<question_id>/vote_up")
def vote_up_question(question_id):
    data_manager.vote_up_question(question_id)
    return redirect("/")


@app.route("/question/<question_id>/vote_down")
def vote_down_question(question_id):
    data_manager.vote_down_question(question_id)
    return redirect("/")


@app.route("/answer/<answer_id>/vote_up")
def vote_up_answer(answer_id):
    id_ = data_manager.get_question_by_answer(answer_id)
    data_manager.vote_up_answer(answer_id)
    return redirect(url_for('route_question', question_id=id_))


@app.route("/answer/<answer_id>/vote_down")
def vote_down_answer(answer_id):
    id_ = data_manager.get_question_by_answer(answer_id)
    data_manager.vote_down_answer(answer_id)
    return redirect(url_for('route_question', question_id=id_))


@app.route("/answer/<int:answer_id>/edit", methods=['GET', 'POST'])
def edit_answer(answer_id):
    answers_list = data_manager.get_answers_by_answer_id(answer_id)

    if request.method == 'POST':
        submission_time = datetime.datetime.now()
        message = request.form['message']
        data_manager.edit_answer(answer_id, submission_time, message)
        return redirect(url_for('route_question',question_id=answers_list['question_id']))

    return render_template('update_answer.html', answer_id=answer_id, message=answers_list)

@app.route("/question/<question_id>/new-comment", methods=['GET', 'POST'])
def route_add_comment(question_id):
    if request.method == 'POST':
        submission_time = datetime.datetime.now()
        message = request.form['message']
        data_manager.add_comment(submission_time,question_id, message)
        return redirect(url_for('route_question', question_id=question_id))
    return render_template('comment_question.html', question_id=question_id)


@app.route("/answer/<answer_id>/new-comment", methods=['GET', 'POST'])
def add_comment_to_answer(answer_id):
    if request.method == 'POST':
        submission_time = datetime.datetime.now()
        message = request.form['message']
        data_manager.add_comment_to_answer(submission_time,answer_id, message)
        question_id = data_manager.get_question_by_answer(answer_id)
        return redirect('/question/' + question_id)
    return render_template('comment_answer.html', answer_id=answer_id)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(debug=True)
