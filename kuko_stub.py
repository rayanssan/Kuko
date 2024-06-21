"""
Aplicações Distribuídas - Projeto 3 - kuko_stub.py
Grupo: 01
Números de aluno: 60282
"""

from kuko_data import *
from kuko_skel import *
from kazoo.client import KazooClient

class KukoStub:
    """
    Represents a set of methods which interpret client requests.
    """

    def __init__(self: object, requests_list: list[str], skel: KukoSkeleton, kuko: Kuko) -> None:
        """
        Initializes a KukoStub instance.

        Requires:
        requests_list (list[str]): a list of client requests as strings.
        skel (KukoSkeleton): a KukoSkeleton object.
        kuko (Kuko): a Kuko object.
        Ensures:
        Initialiazing a KukoStub object with the given attributes.
        """
        self._requests_list = requests_list
        self._skel = skel
        self._kuko = kuko

    # Getters and Setters
        
    @property
    def requests_list(self: object) -> list[str]:
        """
        Ensures:
        Returning a list of client requests.
        """
        return self._requests_list 
    
    @property
    def skel(self: object) -> KukoSkeleton:
        """
        Ensures:
        Returning the KukoSkeleton object associated with this KukoStub instance.
        """
        return self._skel
    
    @property
    def kuko(self: object) -> Kuko:
        """
        Ensures:
        Returning the Kuko object associated with this KukoStub instance.
        """
        return self._kuko
    
    @requests_list.setter
    def requests_list(self: object, requests_list: list[str]) -> None:
        """
        Sets the list of client requests.

        Requires:
        requests_list (list[str]): The new list of client requests.
        Ensures:
        Setting the list of client requests of this instance 
        equal to the given value.
        """
        self._requests_list = requests_list 

    @skel.setter
    def skel(self: object, skel: KukoSkeleton) -> None:
        """
        Sets the KukoSkeleton object associated with this KukoStub instance.

        Requires:
        skel (KukoSkeleton): The new KukoSkeleton object.
        Ensures:
        Setting the KukoSkeleton object of this instance equal to the given value.
        """
        self._skel = skel
    
    @kuko.setter
    def kuko(self: object, kuko: Kuko) -> None:
        """
        Sets the Kuko object associated with this KukoStub instance.

        Requires:
        kuko (Kuko): The new Kuko object.
        Ensures:
        Setting the Kuko object of this instance equal to the given value.
        """
        self._kuko = kuko
    
    # Methods
        
    def question(self: object, zookeeper: KazooClient) -> list[str]:
        """
        Processeses QUESTION requests.

        Requires:
        zookeeper (KazooClient): An apache zookeeper client object.
        Ensures:
        Processesing QUESTION (code: 10) requests from the client and
        returning a list containing the server response.
        """
        k_value = int(self.requests_list[-2])
        question = self.requests_list[1]
        question_answers = self.requests_list[2:-2]
        if k_value < 1 or k_value > len(question_answers):
            server_ans = ["11", "False - parâmetro k inválido"]
        else:
            question_id_value = next(self.kuko.questions_id_counter)
            self.kuko.questions.append(Question(
            question_id_value, question, question_answers, k_value))
            self.kuko.cursor.execute('INSERT INTO question VALUES (?, ?, ?, ?)', 
            [question_id_value, question, ';'.join(question_answers), k_value])
            self.kuko.conn.commit()
            server_ans = ["11", "True", str(question_id_value)]
            if not zookeeper.exists("/question"):
                zookeeper.create("/question")
            zookeeper.set("/question", str(question_id_value).encode())
        server_ans = json.dumps({
            'code': server_ans[0], 
            'response': server_ans[1], 
            **({'question-id': server_ans[2]} if len(server_ans) > 2 else {}),
            'participant': self.requests_list[-1]
        }, ensure_ascii=False)
        print(f"SENT:{server_ans}")
        self.skel.send_all(server_ans)

    def qset(self: object) -> list[str]:
        """
        Ensures:
        Processing QSET (code: 20) requests from the client.
        and returning a list containing the server response.
        """
        question_ids_list = [int(a) for a in self.requests_list[1:-1]]
        question_ids_set = set(q.id_question for q in self.kuko.questions)
        if any(int(id) not in question_ids_set for id in question_ids_list):
            server_ans = ["21", "False - um dos IDs de questões dados não existe"]
        else:
            qsets_id_value = next(self.kuko.q_sets_id_counter)
            self.kuko.q_sets.append(QSet(qsets_id_value, question_ids_list))
            self.kuko.cursor.execute('INSERT INTO qset VALUES (?, ?)', [qsets_id_value, json.dumps(question_ids_list)])
            self.kuko.conn.commit()
            server_ans = ["21", "True", str(qsets_id_value)]
        server_ans = json.dumps({
            'code': server_ans[0], 
            'response': server_ans[1], 
            **({'qset-id': server_ans[2]} if len(server_ans) > 2 else {}),
            'participant': self.requests_list[-1]
        }, ensure_ascii=False)
        print(f"SENT:{server_ans}")
        self.skel.send_all(server_ans)

    def quiz(self: object) -> list[str]:
        """
        Ensures:
        Processing QUIZ (code: 30) requests from the client.
        and returning a list containing the server response.
        """
        q_set_id, question_points = int(self.requests_list[1]), [int(a) for a in self.requests_list[2:-1]]
        q_set_exists = any(q_set.id_set == q_set_id for q_set in self.kuko.q_sets)

        if q_set_exists:
            q_set = next(q_set for q_set in self.kuko.q_sets if q_set.id_set == q_set_id)
            # Verify if the number of points is equal to the number of questions in the QSet
            if len(question_points) == len(q_set.q_set):
                quiz_id = next(self.kuko.quiz_id_counter)
                question_objects = [q for q in self.kuko.questions if q.id_question in q_set.q_set]
                quiz = Quiz(quiz_id, q_set_id, list(zip(question_objects, question_points)))
                quiz.replies = {}
                self.kuko.quizzes.append(quiz)
                self.kuko.cursor.execute('INSERT INTO quiz VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
                (quiz_id, q_set_id, json.dumps(list(zip([i.id_question for i in question_objects], question_points))), 
                "PREPARED", round(time.time()), 0, 1, json.dumps([])))
                self.kuko.conn.commit()
                server_ans = ["31", "True", str(quiz_id)]
            else:
                server_ans = ["31", "False - número de pontuações dadas é diferente do número de questões no QSet"]
        else:
            server_ans = ["31", f"False - QSet {q_set_id} não existe"]
        server_ans = json.dumps({
            'code': server_ans[0], 
            'response': server_ans[1], 
            **({'quiz-id': server_ans[2]} if len(server_ans) > 2 else {}),
            'participant': self.requests_list[-1]
        }, ensure_ascii=False)
        print(f"SENT:{server_ans}")
        self.skel.send_all(server_ans)

    def launch(self: object) -> list[str]:
        """
        Ensures:
        Processing LAUNCH (code: 40) requests from the client.
        and returning a list containing the server response.
        """
        quiz_id = int(self.requests_list[1])
        quiz_exists = any(q.id_quiz == quiz_id for q in self.kuko.quizzes)

        if quiz_exists:
            quiz = next(q for q in self.kuko.quizzes if q.id_quiz == quiz_id)
            if quiz.state == "PREPARED":
                quiz.state = "ONGOING"
                self.kuko.cursor.execute(f'UPDATE quiz SET state="ONGOING" WHERE id_quiz={quiz_id};')
                self.kuko.conn.commit()
                server_ans = ["41", "True", str(quiz_id)]
            else:
                server_ans = ["41", f"False - Quiz {quiz_id} está em progresso ou já terminou"]
        else:
            server_ans = ["41", f"False - Quiz {quiz_id} não existe"]
        server_ans = json.dumps({
            'code': server_ans[0], 
            'response': server_ans[1], 
            'participant': self.requests_list[-1]
        }, ensure_ascii=False)
        print(f"SENT:{server_ans}")
        self.skel.send_all(server_ans)

    def next(self: object) -> list[str]:
        """
        Ensures:
        Processing NEXT (code: 50) requests from the client.
        and returning a list containing the server response.
        """
        quiz_id = int(self.requests_list[1])
        quiz_found = any(q.id_quiz == quiz_id for q in self.kuko.quizzes)
        if quiz_found:
            quiz = next(q for q in self.kuko.quizzes if q.id_quiz == quiz_id)
            total_questions = len(quiz.question_set)
            current_question_index = quiz.question_i 
            if quiz.state != "ONGOING":
                server_ans = ["51", "False - Quiz não está em progresso"]
            else:
                if current_question_index == total_questions:
                    quiz.state = 'ENDED'
                    quiz.timestamp_E = round(time.time())
                    self.kuko.cursor.execute(f'UPDATE quiz SET state="ENDED" WHERE id_quiz={quiz_id};')
                    self.kuko.cursor.execute(f'UPDATE quiz SET timestamp_e={quiz.timestamp_E} WHERE id_quiz={quiz_id};')
                    server_ans = ["51", "True - Quiz terminou"]
                else:
                    quiz.question_i += 1
                    self.kuko.cursor.execute(f'UPDATE quiz SET question_i={quiz.question_i} WHERE id_quiz={quiz_id};')
                    server_ans = ["51", "True"]
                self.kuko.conn.commit()
        else:
            server_ans = ["51", f"False - Quiz {quiz_id} não existe"]
        server_ans = json.dumps({
            'code': server_ans[0], 
            'response': server_ans[1], 
            'participant': self.requests_list[-1]
        }, ensure_ascii=False)
        print(f"SENT:{server_ans}")
        self.skel.send_all(server_ans)

    def reg(self: object) -> list[str]:
        """
        Ensures:
        Processing REG (code: 60) requests from the client.
        and returning a list containing the server response.
        """
        quiz_id = int(self.requests_list[1])
        participant_id = self.requests_list[-1]
        
        quiz_exists = any(q.id_quiz == quiz_id for q in self.kuko.quizzes)
        if not quiz_exists:
            server_ans = ["61", f"False - Quiz {quiz_id} não existe"]
        else:
            quiz = next(q for q in self.kuko.quizzes if q.id_quiz == quiz_id)
            if quiz.state == "ONGOING":
                server_ans = ["61", f"False - Quiz {quiz_id} já começou"]
            elif quiz.state == "ENDED":
                server_ans = ["61", f"False - Quiz {quiz_id} já terminou"]
            else:
                if participant_id not in quiz.participants:
                    # Clear participants of other quizzes
                    for other_quiz in self.kuko.quizzes:
                        if other_quiz.id_quiz != quiz_id:
                            other_quiz.participants = []
                    # Register participant only to this quiz
                    quiz.participants.append(participant_id)
                    self.kuko.cursor.execute(f"UPDATE quiz SET participants='{json.dumps(quiz.participants)}' WHERE id_quiz={quiz_id};")
                    self.kuko.conn.commit()
                server_ans = ["61", f"True - participante {participant_id} registado no Quiz {quiz_id}"]
        server_ans = json.dumps({
            'code': server_ans[0], 
            'response': server_ans[1], 
            'participant': participant_id
        }, ensure_ascii=False)
        print(f"SENT:{server_ans}")
        self.skel.send_all(server_ans)

    def get(self: object) -> list[str]:
        """
        Ensures:
        Processing GET (code: 70) requests from the client.
        and returning a list containing the server response.
        """
        quiz_id = int(self.requests_list[1])
        quiz_found = any(q.id_quiz == quiz_id for q in self.kuko.quizzes)
        if quiz_found:
            quiz = next(q for q in self.kuko.quizzes if q.id_quiz == quiz_id)
            if quiz.state != "ONGOING":
                server_ans = ["71", "False - Quiz não está em progresso"]
            else:
                current_question = quiz.question_set[quiz.question_i - 1][0]
                server_ans = ["71", "True", str(current_question.question)]
                server_ans.extend(current_question.answers)
        else:
            server_ans = ["71", f"False - Quiz {quiz_id} não existe"]
        server_ans = json.dumps({
            'code': server_ans[0], 
            'response': server_ans[1],  
            **({'question': server_ans[2]} if len(server_ans) > 2 else {}),
            **({'answers': ';'.join(server_ans[3:])} if len(server_ans) > 2 else {}),
            'participant': self.requests_list[-1]
        }, ensure_ascii=False)
        print(f"SENT:{server_ans}")
        self.skel.send_all(server_ans)

    def ans(self: object) -> list[str]:
        """
        Ensures:
        Processing ANS (code: 80) requests from the client.
        and returning a list containing the server response.
        """
        quiz_id = int(self.requests_list[1])
        selected_answer = int(self.requests_list[2])

        quiz_exists = any(q.id_quiz == quiz_id for q in self.kuko.quizzes)
        if not quiz_exists:
            server_ans = ["81", f"False - Quiz {quiz_id} não existe"]
        else:
            quiz = next(q for q in self.kuko.quizzes if q.id_quiz == quiz_id)
            current_question_index = quiz.question_i 
            if quiz.state == "ONGOING":
                participant_id = self.requests_list[-1]
                if participant_id not in quiz.participants:
                    server_ans = ["81", "False - participante não está registado neste quiz"]
                else:
                    # Get current question
                    current_question = next(q for q in self.kuko.questions if q.id_question == current_question_index)

                    if selected_answer < 1 or selected_answer > len(current_question.answers):
                        server_ans = ["81", "False - o índice de resposta dado é inválido"]
                    else:
                        try:
                            self.kuko.cursor.execute('INSERT INTO results(id_quiz, question_i, participant, answer) VALUES (?, ?, ?, ?)', 
                            (quiz_id, current_question_index, int(participant_id), selected_answer))
                        except sqlite3.IntegrityError:
                            self.kuko.cursor.execute(f'UPDATE results SET answer = {selected_answer}\
                            WHERE id_quiz = {quiz_id} AND question_i = {current_question_index} AND participant = {participant_id}')
                        self.kuko.conn.commit()
                        # Dictionary of replies 
                        replies = {}
                        results = self.kuko.cursor.execute(f'SELECT * FROM results WHERE id_quiz = {quiz_id}').fetchall()
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
                        quiz.replies = replies
                        server_ans = ["81", "True"]
            else:
                server_ans = ["81", f"False - Quiz {quiz_id} não está em progresso"]
        server_ans = json.dumps({
            'code': server_ans[0], 
            'response': server_ans[1], 
            'participant': self.requests_list[-1]
        }, ensure_ascii=False)
        print(f"SENT:{server_ans}")
        self.skel.send_all(server_ans)

    def rel(self: object) -> list[str]:
        """
        Ensures:
        Processing REL (code: 90) requests from the client.
        and returning a list containing the server response.
        """
        quiz_id = int(self.requests_list[1])
        participant_id = int(self.requests_list[-1])
        quiz_found = any(q.id_quiz == quiz_id for q in self.kuko.quizzes)
        
        if quiz_found:
            quiz = next(q for q in self.kuko.quizzes if q.id_quiz == quiz_id)
            total_questions = len(quiz.question_set)
            current_question_index = quiz.question_i 
            if current_question_index == total_questions and quiz.state == "ENDED":
                correct_answers = 0
                points = 0
                i = 0
                question_i = 1
                if participant_id in quiz.replies:
                    for que in quiz.question_set:
                        if question_i in quiz.replies[participant_id][i]:
                            if quiz.replies[participant_id][i][question_i] == que[0].k:
                                correct_answers += 1
                                points += que[1]
                            i += 1
                        question_i += 1
                server_ans = ["91", "True", str(quiz_id), f"acertou {correct_answers} em {total_questions}, com pontuação {points}"]
            else:
                server_ans = ["91", f"False - Quiz {quiz_id} não começou ou ainda está em progresso"]
        else:
            server_ans = ["91", f"False - Quiz {quiz_id} não existe"]
        server_ans = json.dumps({
            'code': server_ans[0], 
            'response': server_ans[1], 
            **({'quiz': server_ans[2]} if len(server_ans) > 2 else {}),
            **({'report': server_ans[3]} if len(server_ans) > 2 else {}),
            'participant': participant_id
        }, ensure_ascii=False)
        print(f"SENT:{server_ans}")
        self.skel.send_all(server_ans)
        
    def error(self: object) -> list[str]:
        """
        Ensures:d
        Processing invalid requests from the client
        and returning a list containing an invalid command response.
        """
        # Invalid command -> ERROR
        server_ans = ['ERROR - comando inválido']
        server_ans = json.dumps({
            'response': server_ans[0], 
            'participant': self.requests_list[-1]
        }, ensure_ascii=False)
        print(f"SENT:{server_ans}")
        self.skel.send_all(server_ans)