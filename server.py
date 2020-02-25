from flask import Flask, render_template, redirect, request, url_for
import data_manager
import conection
import time
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def route_index():
    questions = data_manager.display_latest_five_questions()
    return render_template('index.html', questions=questions)


@app.route('/list', methods=['GET', 'POST'])
def route_list():
    questions_list = conection.get_all_questions()
    if request.method == 'POST':
        type_ = request.form['sorting']
        direction = request.form['sort']
        question_sort = data_manager.sort_list(type_, direction)
        return render_template('list.html', questions_list=question_sort, type_=type_, direction=direction)
    return render_template('list.html', questions_list=questions_list)


@app.route('/question/<question_id>')
def route_question(question_id):
    questions_list = conection.get_all_questions()
    question_dict = questions_list[int(question_id)]
    question = question_dict['title']
    question_message_dict = questions_list[int(question_id)]
    question_message = question_message_dict['message']
    image = url_for('static', filename=question_dict['image'])
    answer_images = conection.all_answer_content(question_id)
    return render_template('question.html', question_id=question_id, question=question,
                           question_message=question_message, image=image, answer_images=answer_images)


@app.route('/add-question', methods=['GET', 'POST'])
def route_add_question():
    id_ = conection.get_latest_id("sample_data/question.csv")
    if request.method == 'POST':
        id_ += 1
        submission_time = int(time.time())
        view_number = 1
        vote_number = 0
        title = request.form['title']
        message = request.form['message']
        if 'image_file' not in request.files:
            return redirect(url_for('route_question', question_id=id_))
        file = request.files['image_file']
        if file.filename == '':
            return redirect(url_for('route_question', question_id=id_))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image = file.filename
        new_question = [id_, submission_time, view_number,
                        vote_number, title, message, image]
        conection.add_question(new_question)

        return redirect(url_for('route_question', question_id=id_))
    return render_template('add_question.html')


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def route_add_answer(question_id):
    answer_id = conection.get_latest_id('sample_data/answer.csv')
    if request.method == 'POST':
        answer_id += 1
        answer_id = str(answer_id)
        submission_time = int(time.time())
        vote_number = 0
        message = request.form['message']
        if 'image_file' not in request.files:
            return redirect(url_for('route_question', question_id=question_id))
        file = request.files['image_file']
        if file.filename != '':
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image = file.filename
        else:
            image = ""
        new_answer = [answer_id, submission_time,
                      vote_number, question_id, message, image]
        conection.add_answer(new_answer)
        return redirect(url_for('route_question', question_id=question_id))
    return render_template('new_answer.html', question_id=question_id)


@app.route('/question/<int:question_id>/edit', methods=["GET", "POST"])
def route_update_question(question_id):
    questions_list = conection.convert_to_list()
    old_question = questions_list[question_id]
    questions_list.remove(old_question)
    if request.method == 'POST':
        id_ = question_id
        submission_time = int(time.time())
        view_number = 1
        vote_number = 0
        title = request.form['title']
        message = request.form['message']
        image = ''
        question_updated = [id_, submission_time, view_number,
                            vote_number, title, message, image]
        questions_list.insert(question_id, question_updated)
        questions_list.insert(0, ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"])
        conection.update_question(questions_list)
        return redirect(url_for('route_question', question_id=id_))
    return render_template('update_question.html', question_id=question_id, message=old_question[5],
                           title=old_question[4])


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    id_ = conection.get_latest_id("sample_data/question.csv")
    questions_list = conection.convert_to_list()
    question_to_delete = questions_list[int(question_id)]
    print(question_to_delete)
    questions_list.remove(question_to_delete)
    print(questions_list)
    questions_list.insert(0, ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"])
    for i in range(1, int(id_)):
        if int(questions_list[i + 1][0]) - int(questions_list[i][0]) != 1:
            new_id = int(questions_list[i + 1][0])
            new_id -= 1
            questions_list[i + 1][0] = new_id
    conection.update_question(questions_list)
    return redirect('/list')


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    final_id = conection.get_latest_id('sample_data/answer.csv')
    answers = conection.all_answer_contents()
    for answer in answers:
        if answer[0] == answer_id:
            id_ = answer[3]
            answers.remove(answer)
    for i in range(1, int(final_id)):
        if int(answers[i + 1][0]) - int(answers[i][0]) != 1:
            new_id = int(answers[i + 1][0])
            new_id -= 1
            answers[i + 1][0] = new_id
    conection.update_answer(answers)
    return redirect(url_for('route_question', question_id=id_))


@app.route("/question/<question_id>/vote_up")
def vote_up_question(question_id):
    all_question = conection.convert_to_list()
    for row in all_question:
        if row[0] == question_id:
            vote_number = int(row[3])
            vote_number += 1
            row[3] = vote_number
    all_question.insert(0, ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"])
    conection.update_question(all_question)
    return redirect("/")


@app.route("/question/<question_id>/vote_down")
def vote_down_question(question_id):
    all_question = conection.convert_to_list()
    for row in all_question:
        if row[0] == question_id:
            vote_number = int(row[3])
            vote_number -= 1
            row[3] = vote_number
    all_question.insert(0, ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"])
    conection.update_question(all_question)
    return redirect("/")


@app.route("/answer/<answer_id>/vote_up")
def vote_up_answer(answer_id):
    all_answers = conection.all_answer_contents()
    for row in all_answers:
        if row[0] == answer_id:
            vote_number = int(row[2])
            vote_number += 1
            row[2] = vote_number
            id_ = row[3]
    conection.update_answer(all_answers)
    return redirect(url_for('route_question', question_id=id_))


@app.route("/answer/<answer_id>/vote_down")
def vote_down_answer(answer_id):
    all_answers = conection.all_answer_contents()
    for row in all_answers:
        if row[0] == answer_id:
            vote_number = int(row[2])
            vote_number -= 1
            row[2] = vote_number
            id_ = row[3]
    conection.update_answer(all_answers)
    return redirect(url_for('route_question', question_id=id_))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(debug=True)
