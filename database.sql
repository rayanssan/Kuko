--- Aplicações Distribuídas - Projeto 3 - database.sql
--- Grupo: 01
--- Números de aluno: 60282

PRAGMA foreign_keys = ON;

CREATE TABLE question (
    -- ATTRIBUTES -- 
    id_question INTEGER,
    question TEXT NOT NULL,
    answers TEXT NOT NULL,
    k INTEGER NOT NULL,
    -- CONSTRAINTS -- 
    CONSTRAINT pk_question_id_question PRIMARY KEY (id_question)
);

CREATE TABLE qset (
    -- ATTRIBUTES -- 
    id_set INTEGER,
    questions JSON NOT NULL,
    -- CONSTRAINTS -- 
    CONSTRAINT pk_qset_id_set PRIMARY KEY (id_set)
);

-- Check if all elements of questions attributes in the qset table 
-- reference questions on the question table
CREATE TRIGGER before_insert_qset
BEFORE INSERT ON qset
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'One or more given questions do not exist')
    WHERE EXISTS (
        SELECT 1
        FROM json_each(NEW.questions) AS q
        LEFT JOIN question ON (CAST(q.value AS INTEGER) = question.id_question)
        WHERE question.id_question IS NULL
    );
END;

CREATE TABLE quiz (
    -- ATTRIBUTES -- 
    id_quiz INTEGER,
    id_set INTEGER NOT NULL,
    points JSON NOT NULL,
    state TEXT NOT NULL,
    timestamp_p INTEGER NOT NULL,
    timestamp_e INTEGER,
    question_i INTEGER,
    participants JSON,
    -- CONSTRAINTS -- 
    CONSTRAINT pk_quiz_id_quiz PRIMARY KEY (id_quiz),
    CONSTRAINT fk_quiz_id_set FOREIGN KEY (id_set)
    REFERENCES qset(id_set) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT chk_quiz_question_i
    CHECK (question_i BETWEEN 1 AND json_array_length(points))
);

CREATE TRIGGER before_insert_quiz
BEFORE INSERT ON quiz
FOR EACH ROW
BEGIN
    -- Check if all elements of points attributes in the quiz table 
    -- reference questions on the question table
    SELECT RAISE(ABORT, 'One or more given questions in the question set do not exist')
    WHERE EXISTS (
        SELECT 1
        FROM json_each(NEW.points) AS q_outer
        LEFT JOIN question ON (CAST(json_extract(q_outer.value, '$[0]') AS INTEGER) = question.id_question)
        WHERE question.id_question IS NULL
    );
    -- Check if the length of points matches the 
    --length of the associated qset
    SELECT RAISE(ABORT, 'Invalid question set')
    WHERE NOT EXISTS (
        SELECT 1
        FROM qset
        WHERE id_set = NEW.id_set
        AND json_array_length(NEW.points) = json_array_length(questions)
    );
    -- Ensure no values in points repeat
    SELECT RAISE(ABORT, 'Invalid question set')
    WHERE EXISTS (
        SELECT 1
        FROM json_each(NEW.points) AS q_outer
        GROUP BY json_extract(q_outer.value, '$[0]')
        HAVING COUNT(*) > 1
    );
END;

CREATE TABLE results (
    -- ATTRIBUTES --
    id_quiz INTEGER,
    question_i INTEGER,
    participant INTEGER,
    answer INTEGER NOT NULL,
    -- CONSTRAINTS -- 
    CONSTRAINT pk_results_id_quiz_question_i_participant 
    PRIMARY KEY (id_quiz, question_i, participant),
    CONSTRAINT fk_results_id_quiz FOREIGN KEY (id_quiz)
    REFERENCES quiz(id_quiz) ON DELETE CASCADE ON UPDATE CASCADE
);