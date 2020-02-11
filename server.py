from flask import Flask, render_template

import data_manager
import conection

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


if __name__ == '__main__':
    app.run(debug=True)
