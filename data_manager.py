# import conection
from operator import itemgetter
import database_common


@database_common.connection_handler
def display_latest_five_questions(cursor):
    cursor.execute("""
                    SELECT id,title FROM question
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
    question_data = cursor.fetchone()
    return question_data


@database_common.connection_handler
def sort_all_questions(cursor, order_by, order_direction):
    cursor.execute(f"""
                    SELECT * FROM question
                    ORDER BY {order_by} {order_direction};
                    """)
    questions = cursor.fetchall()
    return questions


@database_common.connection_handler
def add_question(cursor, submission_time, view_number, vote_number, title, message, image):
    cursor.execute("""
                    INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
                    VALUES (%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s); 
                    """,
                   {'submission_time': submission_time,
                    'view_number': view_number,
                    'vote_number': vote_number,
                    'title': title,
                    'message': message,
                    'image': image})


@database_common.connection_handler
def get_id_of_question_by_time(cursor, submission_time):
    cursor.execute("""
                    SELECT id FROM question
                    WHERE submission_time = %(submission_time)s;
                    """,
                   {'submission_time': submission_time})
    question_id = cursor.fetchone()
    return question_id['id']


@database_common.connection_handler
def add_answer(cursor, submission_time, vote_number, question_id, message, image):
    cursor.execute("""
                    INSERT INTO answer (submission_time, vote_number, question_id, message, image)
                    VALUES (%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s);
                    """,
                   {'submission_time': submission_time,
                    'vote_number': vote_number,
                    'question_id': question_id,
                    'message': message,
                    'image': image})


@database_common.connection_handler
def get_answers_by_question_id(cursor, question_id):
    cursor.execute("""
                    SELECT id, vote_number, message, image FROM answer
                    WHERE question_id = %(question_id)s;
                    """,
                   {'question_id': question_id})
    answers = cursor.fetchall()
    return answers


@database_common.connection_handler
def update_question(cursor, question_id, submission_time, title, message):
    cursor.execute("""
                    UPDATE question
                    SET submission_time = %(submission_time)s, title = %(title)s, message = %(message)s
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id': question_id,
                    'submission_time': submission_time,
                    'title': title,
                    'message': message})


@database_common.connection_handler
def edit_answer(cursor, answer_id, submission_time, message):
    cursor.execute("""
                    UPDATE answer
                    SET submission_time = %(submission_time)s, message = %(message)s
                    WHERE id = %(answer_id)s;
                    """,
                   {'answer_id': answer_id,
                    'submission_time': submission_time,
                    'message': message})


@database_common.connection_handler
def edit_comment(cursor, comment_id, submission_time, message):
    cursor.execute("""
                    UPDATE comment
                    SET submission_time = %(submission_time)s, message = %(message)s, edited_count = (edited_count + 1)
                    WHERE id = %(comment_id)s;
                    """,
                   {'comment_id': comment_id,
                    'submission_time': submission_time,
                    'message': message})


@database_common.connection_handler
def get_answers_by_answer_id(cursor, answer_id):
    cursor.execute("""
                    SELECT vote_number, message, image, question_id FROM answer
                    WHERE id = %(answer_id)s;
                    """,
                   {'answer_id': answer_id})
    answers = cursor.fetchone()
    return answers


@database_common.connection_handler
def add_comment(cursor, submission_time, question_id, message):
    cursor.execute("""
                        INSERT INTO comment(submission_time, question_id, message)
                        VALUES (%(submission_time)s, %(question_id)s, %(message)s);
                        """,
                   {'submission_time': submission_time,
                    'question_id': question_id,
                    'message': message})


@database_common.connection_handler
def get_comment_by_question(cursor, question_id):
    cursor.execute("""
                    SELECT submission_time,id, message FROM comment
                    WHERE question_id = %(question_id)s;
                    """,
                   {'question_id': question_id})
    comment = cursor.fetchall()
    return comment


@database_common.connection_handler
def add_comment_to_answer(cursor, submission_time, answer_id, message):
    cursor.execute("""
                        INSERT INTO comment(submission_time, answer_id, message)
                        VALUES (%(submission_time)s, %(answer_id)s, %(message)s);
                        """,
                   {'submission_time': submission_time,
                    'answer_id': answer_id,
                    'message': message})


@database_common.connection_handler
def get_comment_by_answer(cursor):
    cursor.execute("""
                    SELECT submission_time, message, answer_id, id FROM comment
                    WHERE answer_id IS NOT NULL;
                    """)
    comment = cursor.fetchall()
    return comment


@database_common.connection_handler
def get_comment_by_answer_id(cursor, answer_id):
    cursor.execute("""
                    SELECT submission_time, message, answer_id, id FROM comment
                    WHERE answer_id=%(answer_id)s;
                    """,
                   {'answer_id': answer_id})
    comment = cursor.fetchall()
    return comment


@database_common.connection_handler
def get_comment_by_comment_id(cursor, comment_id):
    cursor.execute("""
                    SELECT submission_time, message, answer_id, id FROM comment
                    WHERE id=%(comment_id)s;
                    """,
                   {'comment_id': comment_id})
    comment = cursor.fetchone()
    return comment


@database_common.connection_handler
def get_question_by_answer(cursor, answer_id):
    cursor.execute("""
                    SELECT question_id FROM answer
                    WHERE id=%(answer_id)s;
                    """,
                   {'answer_id': answer_id})
    return str(cursor.fetchone()['question_id'])



@database_common.connection_handler
def search_questions_by_pattern(cursor, pattern):
    cursor.execute(f"""
                    SELECT title, id FROM question
                    WHERE title LIKE '%{pattern}%' 
                    OR title LIKE '%{pattern.capitalize()}%'
                    OR title LIKE '%{pattern.upper()}%'
                    OR title LIKE '%{pattern.lower()}%'
                    OR message LIKE '%{pattern}%' 
                    OR message LIKE '%{pattern.capitalize()}%'
                    OR message LIKE '%{pattern.upper()}%'
                    OR message LIKE '%{pattern.lower()}%';
                    """)
    result = cursor.fetchall()
    number = cursor.rowcount
    return result, number


@database_common.connection_handler
def delete_question(cursor, question_id):
    cursor.execute("""
                    DELETE FROM question
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id': question_id})


@database_common.connection_handler
def delete_answer(cursor, answer_id):
    cursor.execute("""
                    DELETE FROM answer
                    WHERE id = %(answer_id)s;
                    """,
                   {'answer_id': answer_id})


@database_common.connection_handler
def delete_comment_answer(cursor, comment_id):
    cursor.execute("""
                    DELETE FROM comment
                    WHERE id = %(comment_id)s;
                    """,
                   {'comment_id': comment_id})


@database_common.connection_handler
def delete_comment_question(cursor, comment_id):
    cursor.execute("""
                    DELETE FROM comment
                    WHERE id = %(comment_id)s;
                    """,
                   {'comment_id': comment_id})


@database_common.connection_handler
def vote_up_question(cursor, question_id):
    cursor.execute("""
                    UPDATE question
                    SET vote_number = (vote_number + 1)
                    WHERE id = %(question_id)s;""",
                   {'question_id': question_id})


@database_common.connection_handler
def vote_down_question(cursor, question_id):
    cursor.execute("""
                    UPDATE question
                    SET vote_number = (vote_number - 1)
                    WHERE id = %(question_id)s;""",
                   {'question_id': question_id})


@database_common.connection_handler
def vote_up_answer(cursor, answer_id):
    cursor.execute("""
                    UPDATE answer
                    SET vote_number = (vote_number + 1)
                    WHERE id = %(answer_id)s;""",
                   {'answer_id': answer_id})


@database_common.connection_handler
def vote_down_answer(cursor, answer_id):
    cursor.execute("""
                    UPDATE answer
                    SET vote_number = (vote_number - 1)
                    WHERE id = %(answer_id)s;""",
                   {'answer_id': answer_id})


@database_common.connection_handler
def get_answer_id_by_comment(cursor, comment_id):
    cursor.execute("""
                        SELECT answer_id FROM comment
                        WHERE id=%(comment_id)s;
                        """,
                   {'comment_id': comment_id})
    return str(cursor.fetchone()['answer_id'])


@database_common.connection_handler
def get_question_id_by_comment(cursor, comment_id):
    cursor.execute("""
                        SELECT question_id FROM comment
                        WHERE id=%(comment_id)s;
                        """,
                   {'comment_id': comment_id})
    return str(cursor.fetchone()['question_id'])

@database_common.connection_handler
def create_tags(cursor):
    cursor.execute("""
    SELECT id,name FROM tag
    """)
    tags = cursor.fetchall()
    return tags


@database_common.connection_handler
def get_tags(cursor, question_id):
    cursor.execute("""
    SELECT id,name FROM tag WHERE question_id = %(question_id)s
    """,
    {'question_id': question_id})
    tags = cursor.fetchall()
    return tags


@database_common.connection_handler
def add_new_tag(cursor, tag, question_id):
    cursor.execute("""
    INSERT INTO tag (name, question_id) VALUES (%(tag)s, %(question_id)s);""",
                   {'tag':tag,'question_id':question_id})

@database_common.connection_handler
def delete_tag(cursor, tag):
    cursor.execute("""
    DELETE FROM tag WHERE id = %(tag)s""",
                   {'tag':tag})

@database_common.connection_handler
def get_question_by_tag(cursor, tag):
    cursor.execute("""
    SELECT question_id FROM tag WHERE id = %(tag)s""", {'tag':tag})
    question = cursor.fetchone()
    return question