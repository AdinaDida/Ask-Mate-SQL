import csv

def get_all_questions():
    all_questions = {}
    with open('sample_data/question.csv', 'r') as question_obj:
        reader = csv.DictReader(question_obj)
        for row in reader:
            all_questions[row['id']] = {'submission_time': row['submission_time'],
                                        'view_number': row['view_number'],
                                        'title': row['title'],
                                        'message': row['message'],
                                        'image': row['image']}
    return all_questions

