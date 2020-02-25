import conection
from operator import itemgetter
import database_common


@database_common.connection_handler
def display_latest_five_questions(cursor):
    cursor.execute("""
                    SELECT title FROM question
                    ORDER BY submission_time DESC 
                    LIMIT 5;
                    """)
    questions = cursor.fetchall()
    return questions


@database_common.connection_handler
def display_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question
                    ORDER BY submission_time DESC;
                    """)
    all_questions = cursor.fetchall()
    return all_questions


@database_common.connection_handler
def question(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id': question_id})
    question = cursor.fetchone()
    return question


@database_common.connection_handler
def sort_all_questions(cursor, order_by, order_direction):
    cursor.execute(f"""
                    SELECT * FROM question
                    ORDER BY {order_by} {order_direction};
                    """)
    questions = cursor.fetchall()
    return questions


def convert_to_int(list_of_dicts):
    for dictionary in list_of_dicts:
        dictionary['submission_time'] = int(dictionary['submission_time'])
        dictionary['view_number'] = int(dictionary['view_number'])
        dictionary['vote_number'] = int(dictionary['vote_number'])
    return list_of_dicts
