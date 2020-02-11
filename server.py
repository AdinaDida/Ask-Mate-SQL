from flask import Flask, render_template, redirect, request, url_for

import data_manager
import conection
import time

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_list():
    questions_dict = conection.get_all_questions()

    return render_template('list.html', questions_dict=questions_dict)


@app.route('/question/<question_id>')
def route_question(question_id):
    answers = conection.get_answers(question_id)
    questions_dict = conection.get_all_questions()
    question = questions_dict[question_id]['title']
    question_message = questions_dict[question_id]['message']

    return render_template('question.html', question_id=question_id, answers=answers, question=question,
                           question_message=question_message)


@app.route('/add-question', methods=['GET', 'POST'])
def route_add_question():
    questions_dict = conection.get_all_questions()
    id_ = conection.get_latest_id()
    if request.method == 'POST':
        id_ +=1
        id_ = str(id_)
        submission_time = int(time.time())
        view_number = 1
        vote_number = 0
        title = request.form['title']
        message = request.form['message']
        image = ''
        new_question = [id_, submission_time, view_number, vote_number, title, message, image]
        conection.add_question(new_question)
        return redirect(url_for('route_question', question_id=id_))
    return render_template('add_question.html')


if __name__ == '__main__':
    app.run(debug=True)
