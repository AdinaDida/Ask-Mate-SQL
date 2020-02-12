import conection
from operator import itemgetter


def sort_list(type_, direction=False):
    print(type_)
    all_questions = conection.get_all_questions()
    all_questions_sorted = convert_to_int(all_questions)
    if direction == "ascending":
        all_questions_sorted = sorted(all_questions_sorted, key=itemgetter(type_))
    if direction == "descending":
        all_questions_sorted = sorted(all_questions_sorted, key=itemgetter(type_), reverse=True)
    return all_questions_sorted


def convert_to_int(list_of_dicts):
    for dictionary in list_of_dicts:
        dictionary['submission_time'] = int(dictionary['submission_time'])
        dictionary['view_number'] = int(dictionary['view_number'])
        dictionary['vote_number'] = int(dictionary['vote_number'])
    return list_of_dicts

