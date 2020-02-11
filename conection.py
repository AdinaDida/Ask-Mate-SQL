import csv

def get_all_questions():
    all_questions = {}
    with open('sample_data/question.csv', 'r') as question_obj:
        reader = csv.DictReader(question_obj)
        for row in reader:
            all_questions[row['id']] = {'submission_time': row['submission_time'],
                                        'view_number': row['view_number'],
                                        'vote_number': row['vote_number'],
                                        'title': row['title'],
                                        'message': row['message'],
                                        'image': row['image']}
    sorted_all_questions = sorted(all_questions.items(), key=lambda element: element[1]['submission_time'],
                                  reverse=True)
    return dict(sorted_all_questions)


def get_answers(question_id):
    answers_for_question = []
    with open('sample_data/answer.csv', 'r') as answer_obj:
        reader = csv.reader(answer_obj)
        for row in reader:
            if row[3] == question_id:
                answers_for_question.append(row[4])
    return answers_for_question

