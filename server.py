from flask import Flask, render_template

import data_manager
import conection

app = Flask(__name__)

@app.route('/')
@app.route('/list')
def route_list():
    questions_dict = conection.get_all_questions()

    return render_template('list.html', questions_dict=questions_dict)

if __name__ == '__main__':
    app.run(debug=True)
