"""
Aplicações Distribuídas - Projeto 3 - kuko_data.py
Grupo: 01
Números de aluno: 60282
"""

import time, copy, json, sqlite3
from database import connect_db
from itertools import count

class Question:
    """
    Represents a question with a given list of possible answers, 
    with only one of them being correct.
    """

    def __init__(self: object, id_question: int, question: str, answers: list[str], k: int) -> None:
        """
        Initializes a Question object.

        Requires:
        id_question (int): a natural number uniquely identifying a question.
        question (str): the text displaying the question.
        answers (list): a list of strings containing the possible answers to the question.
        k (int): a natural number which corresponds to index of the correct answer on the answers list.
        Ensures:
        Initialiazing a Question object with the given attributes.
        """
        self._id_question = id_question
        self._question = question
        self._answers = answers
        self._k = k
       
    # Getters
        
    @property
    def id_question(self: object) -> int:
        """
        Ensures:
        Returns the id_question of this Question.
        """
        return self._id_question
    
    @property
    def question(self: object) -> str:
        """
        Ensures:
        Returns the question text of this Question.
        """
        return self._question
    
    @property
    def answers(self: object) -> list[str]:
        """
        Ensures:
        Returns the answers of this Question.
        """
        return self._answers
    
    @property
    def k(self: object) -> int:
        """
        Ensures:
        Returns the k value of this Question.
        """
        return self._k
    
    # Setters

    @id_question.setter
    def id_question(self: object, id_question: int) -> None:
        """
        Sets the id_question of this Question to a new value.

        Requires:
        id_question (int): a natural number uniquely identifying a question.
        Ensures:
        Setting the id_question equal to the new given value.
        """
        self._id_question = id_question
    
    @question.setter
    def question(self: object, question: str) -> None:
        """
        Sets the question text of this Question to a new value.

        Requires:
        question (str): the text displaying the question.
        Ensures:
        Setting the question text equal to the new given value.
        """
        self._question = question
    
    @answers.setter
    def answers(self: object, answers: list[str]) -> None:
        """
        Sets the answers of this Question to a new value.

        Requires:
        answers (list): a list of strings containing the possible answers to the question.
        Ensures:
        Setting the answers equal to the new given value.
        """
        self._answers = answers

    @k.setter   
    def k(self: object, k: int) -> None:
        """
        Sets the k value of this Question to a new value.

        Requires:
        k (int): a natural number which corresponds to index of the correct answer on the answers list.
        Ensures:
        Setting the k value equal to the new given value.
        """
        self._k = k
    
    # Methods
        
    def __str__(self: object) -> str:
        """
        Ensures:
        Returning a string containing the details of this Question.
        """
        return f"Question ID: {self.id_question}\n" \
        f"Question: {self.question}\n" \
        f"Answers: {self.answers}\n" \
        f"Correct Answer (k): {self.k}"

class QSet(set):
    """
    Represents a collection of questions.
    """
        
    def __init__(self: object, id_set: int, questions: list[int] = []) -> None:
        """
        Initializes a QSet object.

        Requires:
        id_set (int): a natural number uniquely identifying this QSet.
        questions (list): a list of question IDs.
        Ensures:
        Initialiazing a QSet object with the given attributes.
        """
        self._id_set = id_set
        self._questions = questions
        self._q_set = set()
        for question in questions:
            self._q_set.add(question)
        
    # Getters
            
    @property
    def id_set(self: object) -> int:
        """
        Ensures:
        Returns the id_set of this QSet.
        """
        return self._id_set

    @property
    def questions(self: object) -> list[int]:
        """
        Ensures:
        Returns the list of questions in this QSet.
        """
        return self._questions
    
    @property
    def q_set(self: object) -> set:
        """
        Ensures:
        Returns the set of questions in this QSet.
        """
        return self._q_set
    
    # Setters

    @id_set.setter
    def id_set(self: object, id_set: int) -> None:
        """
        Sets the id_set of this QSet to a new value.

        Requires:
        id_set (int): a natural number uniquely identifying a set of questions.
        Ensures:
        Setting id_set equal to the new given value.
        """
        self._id_set = id_set
    
    @questions.setter
    def questions(self: object, questions: list[int]) -> None:
        """
        Sets the questions of this QSet to a new value.

        Requires:
        questions (list): a list of question IDs.
        Ensures:
        Setting the questions equal to the new given value.
        """
        self._questions = questions

    @q_set.setter
    def q_set(self: object, q_set: set) -> None:
        """
        Sets the set of this QSet to a new set.

        Requires:
        q_set (set): a set of lists of question IDs.
        Ensures:
        Setting q_set equal to the new given value.
        """
        self._q_set = q_set

    # Methods
        
    def __str__(self: object) -> str:
        """
        Ensures:
        Returning a string containing the details of this QSet.
        """
        return f"Set ID: {self.id_set}\n" \
        f"Questions: {self.questions}\n" \
        f"QSet: {self.q_set}"

class Quiz:
    """
    Represents a quiz with participants and an associated set of questions.
    """

    def __init__(self: object, id_quiz: int, id_set: int,
    question_set: list[(Question, int)], state: str = "PREPARED", timestamp_p: int = round(time.time()),
    timestamp_E: int = 0, question_i: int = 1, participants: list[int] = [],
    replies: dict = {}) -> None:
        """
        Initializes a Quiz object.

        Requires:
        id_quiz (int): a natural number uniquely identifying this Quiz instance.
        id_set (int): a natural number uniquely identifying the set of 
        questions in this Quiz instance.
        question_set (list[(Question,int)]): a list of tuples containing Question 
        objects and the score associated with the question.
        state (str): the current state of this Quiz. 
        Has to be one of the following three values - ('PREPARED', 'ONGOING', 'ENDED').
        Defaults to 'PREPARED'.
        timestamp_p (int): a natural number matching the instant in which quiz's state was
        set to 'PREPARED'. Defaults to the current time rounded.
        timestamp_E (int): a natural number matching the instant in which quiz's state was
        set to 'ENDED'. Defaults to 0.
        question_i (int): a natural number representing the current question 
        available to participants. Defaults to 1.
        participants (list): a list with the IDs of the participants of this Quiz.
        Defaults to an empty list.
        replies (dict): a dictionary with the participants' IDs as keys and their list of 
        reply dictionaries as values. Reply dictionaries must consist of the index 
        of the question in the quiz as key and the participant's answer as the value. Defaults to an empty dictionary.
        Ensures:
        Initialiazing a Quiz object with the given attributes.
        """
        self._id_quiz = id_quiz
        self._id_set = id_set
        self._question_set = copy.copy(question_set)
        self._state = state
        self._timestamp_p = timestamp_p
        self._timestamp_E = timestamp_E
        self._question_i = question_i
        self._participants = participants
        self._replies = replies

    # Getters
        
    @property
    def id_quiz(self: object) -> int:
        """
        Ensures:
        Returning the id_quiz in this Quiz.
        """
        return self._id_quiz

    @property
    def id_set(self: object) -> int:
        """
        Ensures:
        Returns the id_set of this Quiz.
        """
        return self._id_set

    @property
    def question_set(self: object) -> list[(Question, int)]:
        """
        Ensures:
        Returns the question_set of this Quiz.
        """
        return self._question_set

    @property
    def state(self: object) -> str:
        """
        Ensures:
        Returns the state of this Quiz.
        """
        return self._state

    @property
    def timestamp_p(self: object) -> int:
        """
        Ensures:
        Returns the timestamp_p of this Quiz.
        """
        return self._timestamp_p

    @property
    def timestamp_E(self: object) -> int:
        """
        Ensures:
        Returns the timestamp_E of this Quiz.
        """
        return self._timestamp_E

    @property
    def question_i(self: object) -> int:
        """
        Ensures:
        Returns the question_i of this Quiz.
        """
        return self._question_i

    @property
    def participants(self: object) -> list[int]:
        """
        Ensures:
        Returns the participants of this Quiz.
        """
        return self._participants

    @property
    def replies(self: object) -> dict:
        """
        Ensures:
        Returns the replies of this Quiz.
        """
        return self._replies

    # Setters

    @id_quiz.setter
    def id_quiz(self: object, value: int) -> None:
        """
        Sets the id_quiz of this Quiz to a new value

        Requires:
        value (int): A natural number uniquely identifying this Quiz instance.
        Ensures:
        Setting id_quiz equal to the new given value.
        """
        self._id_quiz = value

    @id_set.setter
    def id_set(self: object, value: int) -> None:
        """
        Sets the id_set of this Quiz to a new value.

        Requires:
        value (int): A natural number uniquely identifying the set of questions in this Quiz instance.
        Ensures:
        Setting id_set to the new given value.
        """
        self._id_set = value

    @question_set.setter
    def question_set(self: object, value: list[(Question, int)]) -> None:
        """
        Sets the question_set of this Quiz to a new value.

        Requires:
        value (QSet): A list of tuples containing Question 
        objects and the score associated with the question.
        Ensures:
        Setting question_set to the new given value.
        """
        self._question_set = value

    @state.setter
    def state(self: object, value: str) -> None:
        """
        Sets the state of this Quiz to a new value.

        Requires:
        value (str): The current state of this Quiz. Has to be one of the following three values - ('PREPARED', 'ONGOING', 'ENDED').
        Ensures:
        Setting state to the new given value.
        """
        self._state = value

    @timestamp_p.setter
    def timestamp_p(self: object, value: int) -> None:
        """
        Sets the timestamp_p of this Quiz to a new value.

        Requires:
        value (int): A natural number matching the instant in which the quiz's state was set to 'PREPARED'.
        Ensures:
        Setting timestamp_p to the new given value.
        """
        self._timestamp_p = value

    @timestamp_E.setter
    def timestamp_E(self: object, value: int) -> None:
        """
        Sets the timestamp_E of this Quiz to a new value.

        Requires:
        value (int): A natural number matching the instant in which the quiz's state was set to 'ENDED'.
        Ensures:
        Setting timestamp_E to the new given value.
        """
        self._timestamp_E = value

    @question_i.setter
    def question_i(self: object, value: int) -> None:
        """
        Sets the question_i of this Quiz to a new value.

        Requires:
        value (int): A natural number representing the current question available to participants.
        Ensures:
        Setting question_i to the new given value.
        """
        self._question_i = value

    @participants.setter
    def participants(self: object, value: list[int]) -> None:
        """
        Sets the participants of this Quiz to a new value.

        Requires:
        value (list): A list with the IDs of the participants of this Quiz.
        Ensures:
        Setting participants to the new given value.
        """
        self._participants = value

    @replies.setter
    def replies(self: object, value: dict) -> None:
        """
        Sets the replies of this Quiz to a new value.

        Requires:
        value (dict): A dictionary with the participants' IDs as keys and their list of replies to each question as values.
        Ensures:
        Setting replies to the new given value.
        """
        self._replies = value

    # Methods
        
    def __str__(self: object) -> str:
        """
        Ensures:
        Returning a string containing the details of this Quiz.
        """
        return f"Quiz ID: {self.id_quiz}\n" \
            f"Set ID: {self.id_set}\n" \
            f"Question Set: {self.question_set}\n" \
            f"State: {self.state}\n" \
            f"Prepared Timestamp: {self.timestamp_p}\n" \
            f"Ended Timestamp: {self.timestamp_E}\n" \
            f"Current Question Index: {self.question_i}\n" \
            f"Participants: {self.participants}\n" \
            f"Replies: {self.replies}" 

class Kuko:
    """
    Represents Kuko data.
    """

    def __init__(self: object) -> None:
        """
        Ensures:
        Initializing a Kuko object.
        """
        # Connect to database
        self._conn, self._cursor = connect_db('database.db')
        
        # Counters
        curr_questions_count = self._cursor.execute('SELECT max(id_question) FROM question').fetchall()[0][0]
        self._questions_id_counter = count(start=curr_questions_count+1)
        curr_q_sets_count = self._cursor.execute('SELECT max(id_set) FROM qset').fetchall()[0][0]
        self._q_sets_id_counter = count(start=curr_q_sets_count+1)
        curr_quiz_count = self._cursor.execute('SELECT max(id_quiz) FROM quiz').fetchall()[0][0]
        self._quiz_id_counter = count(start=curr_quiz_count+1)

        # List to store Question objects
        self._questions = []
        for q in self._cursor.execute('SELECT * FROM question').fetchall():
            self._questions.append(Question(q[0], # Question ID
                                            q[1], # Question
                                            q[2].split(';'), # Answers List
                                            q[3])) # Correct Answer - K

        # List to store QSet objects
        self._q_sets = []
        for q in self._cursor.execute('SELECT * FROM qset').fetchall():
            self._q_sets.append(QSet(q[0], # QSet ID
                                     json.loads(q[1]))) # Question IDs List

        # List to store Quiz objects
        self._quizzes = []
        for q in self._cursor.execute('SELECT * FROM quiz').fetchall():
            # Dictionary of replies 
            replies = {}
            results = self._cursor.execute(f'SELECT * FROM results WHERE id_quiz = {q[0]}').fetchall()
            for item in results:
                question_i = item[1]
                user_id = item[2]
                answer = item[3]
                # Check if the user_id is already a key in the result dictionary
                if user_id in replies:
                    # If yes, append the answer to the list associated with the user_id
                    replies[user_id].append({question_i: answer})
                else:
                    # If no, create a new list with the answer and associate it with the user_id
                    replies[user_id] = [{question_i: answer}]
            self._quizzes.append(Quiz(q[0], # Quiz ID
            q[1], # QSet ID
            [(next(i for i in self._questions if i.id_question == x), 
              y) for x,y in json.loads(q[2])], # Question Set (Question, Points)
            q[3], # State
            q[4], # Timestamp_P
            q[5], # Timestamp_E
            q[6], # Current Question
            json.loads(q[7]), # Participants
            replies))

    @property
    def conn(self: object) -> sqlite3.Connection:
        """
        Ensures:
        Returning the database Connection object of this Kuko.
        """
        return self._conn
    
    @property
    def cursor(self: object) -> sqlite3.Cursor:
        """
        Ensures:
        Returning the database Cursor object of this Kuko.
        """
        return self._cursor

    @property
    def questions_id_counter(self: object) -> count:
        """
        Ensures:
        Returning the Questions id counter of this Kuko.
        """
        return self._questions_id_counter
    
    @property
    def q_sets_id_counter(self: object) -> count:
        """
        Ensures:
        Returning the QSet id counter id counter of this Kuko.
        """
        return self._q_sets_id_counter

    @property
    def quiz_id_counter(self: object) -> count:
        """
        Ensures:
        Returning the Quiz id counter of this Kuko.
        """
        return self._quiz_id_counter

    @property
    def questions(self: object) -> list[Question]:
        """
        Ensures:
        Returning the Questions list of this Kuko.
        """
        return self._questions
    
    @property
    def q_sets(self: object) -> list[QSet]:
        """
        Ensures:
        Returning the QSets list of this Kuko.
        """
        return self._q_sets
    
    @property
    def quizzes(self: object) -> list[Quiz]:
        """
        Ensures:
        Returning the Quizzes list of this Kuko.
        """
        return self._quizzes
    
    @conn.setter
    def conn(self: object, conn: sqlite3.Connection) -> None:
        """
        Sets the database Connection object of this Kuko to a new value.

        Requires:
        conn (sqlite3.Connection): a database Connection object.
        Ensures:
        Setting this Kuko's database Connection to the new given value.
        """
        self._conn = conn
    
    @cursor.setter
    def cursor(self: object, cursor: sqlite3.Cursor) -> None:
        """
        Sets the database Cursor object of this Kuko to a new value.

        Requires:
        curosr (sqlite3.Connection): a database Cursor object.
        Ensures:
        Setting this Kuko's database Cursor to the new given value.
        """
        self._cursor = cursor

    @questions_id_counter.setter
    def questions_id_counter(self: object, value: count) -> None:
        """
        Sets the Questions id counter of this Kuko to a new value.

        Requires:
        value (count): An itertools count object.
        Ensures:
        Setting this Kuko's Questions id counter to the new given value.
        """
        self._questions_id_counter = value

    @q_sets_id_counter.setter
    def q_sets_id_counter(self: object, value: count) -> None:
        """
        Sets the QSet id counter of this Kuko to a new value.

        Requires:
        value (count): An itertools count object.
        Ensures:
        Setting this Kuko's QSet id counter to the new given value.
        """
        self._q_sets_id_counter = value

    @quiz_id_counter.setter
    def quiz_id_counter(self: object, value: count) -> None:
        """
        Sets the Quiz id counter of this Kuko to a new value.

        Requires:
        value (count): An itertools count object.
        Ensures:
        Setting this Kuko's Quiz id counter to the new given value.
        """
        self._quiz_id_counter = value

    @questions.setter
    def questions(self: object, value: list[Question]) -> None:
        """
        Sets the questions list of this Kuko to a new value.

        Requires:
        value (list[Question]): The new list of Questions.
        Ensures:
        Setting this Kuko's list of questions to the new given value.
        """
        self._questions = value

    @q_sets.setter
    def q_sets(self: object, value: list[QSet]) -> None:
        """
        Sets the QSets list of this Kuko to a new value.

        Requires:
        value (list[QSet]): The new list of QSets.
        Ensures:
        Setting this Kuko's list of QSets to the new given value.
        """
        self._q_sets = value

    @quizzes.setter
    def quizzes(self: object, value: list[Quiz]) -> None:
        """
        Sets the Quizzes list of this Kuko to a new value.

        Requires:
        value (list[Quiz]): The new list of Quizzes.
        Ensures:
        Setting this Kuko's list of Quizzes to the new given value.
        """
        self._quizzes = value