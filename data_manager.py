import conection


def sort_dict(type_, direction=False):
    print(type_)
    all_questions = conection.get_all_questions()
    all_questions_sorted = sorted(all_questions.items(
    ), key=lambda element: element[1][type_], reverse=direction)
    return all_questions_sorted


# print(sort_dict('title', False))
