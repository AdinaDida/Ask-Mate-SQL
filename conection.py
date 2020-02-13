import csv


def get_all_questions():
    all_questions = []
    with open('sample_data/question.csv', 'r') as question_obj:
        reader = csv.DictReader(question_obj)
        for row in reader:
            all_questions.append(dict(row))
    return all_questions


def get_answers(question_id):
    answers_for_question = []
    with open('sample_data/answer.csv', 'r') as answer_obj:
        reader = csv.reader(answer_obj)
        for row in reader:
            if row[3] == question_id:
                answers_for_question.append(row[4])
    return answers_for_question


def add_question(data):
    with open('sample_data/question.csv', 'a') as new_question_obj:
        writer = csv.writer(new_question_obj)
        writer.writerow(data)


def get_latest_id(file):
    with open(file, 'r') as id_obj:
        reader = csv.reader(id_obj)
        id_ = -2
        for row in reader:
            id_ += 1
    return id_


def add_answer(data):
    with open('sample_data/answer.csv', 'a') as new_answer_obj:
        writer = csv.writer(new_answer_obj)
        writer.writerow(data)


def update_question(data):
    with open("sample_data/question.csv", "w") as update_obj:
        file_write = csv.writer(update_obj)
        file_write.writerows(data)


def convert_to_list():
    list_of_questions = []
    with open("sample_data/question.csv", "r") as list_obj:
        file_reader = csv.reader(list_obj)
        next(file_reader)
        for row in file_reader:
            list_of_questions.append(row)
    return list_of_questions
