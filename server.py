from flask import Flask, render_template, redirect, request, url_for

import data_manager
import conection
import time

app = Flask(__name__)


@app.route('/')
@app.route('/list', methods=['GET', 'POST'])
def route_list():
    questions_list = conection.get_all_questions()

    if request.method == 'POST':
        type_ = request.form['sorting']
        direction = bool(request.form['sort'])
        question_sort = data_manager.sort_dict(type_, direction)
        questions_list = dict(question_sort)
        return render_template('list.html', questions_list=questions_list)

    return render_template('list.html', questions_list=questions_list)


@app.route('/question/<question_id>')
def route_question(question_id):
    answers = conection.get_answers(question_id)
    questions_list = conection.get_all_questions()
    question_dict = questions_list[int(question_id)]
    question = question_dict['title']
    question_message_dict = questions_list[int(question_id)]
    question_message = question_message_dict['message']
    return render_template('question.html', question_id=question_id, answers=answers, question=question,
                           question_message=question_message)


@app.route('/add-question', methods=['GET', 'POST'])
def route_add_question():
    id_ = conection.get_latest_id("sample_data/question.csv")
    if request.method == 'POST':
        id_ += 1
        # id_ = str(id_)
        submission_time = int(time.time())
        view_number = 1
        vote_number = 0
        title = request.form['title']
        message = request.form['message']
        image = ''
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
        image = ''
        new_answer = [answer_id, submission_time,
                      vote_number, question_id, message, image]
        conection.add_answer(new_answer)
        return redirect(url_for('route_question', question_id=question_id))

    return render_template('new_answer.html', question_id=question_id)


if __name__ == '__main__':
    app.run(debug=True)
