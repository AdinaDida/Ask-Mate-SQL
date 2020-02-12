import conection


def sort_dict(type_, direction=False):
    all_questions = conection.get_all_questions()
    all_questions = sorted(all_questions.items(), key=lambda element: element[1][type_], reverse=direction)
    return all_questions