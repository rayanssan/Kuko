from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess, re, sys, json

app = Flask(__name__)
CORS(app)

@app.route('/question', methods=['GET', 'POST'])
def question():
    """
    Ensures:
    Processing a QUESTION request from a participant
    and returning a JSON response containing the result of processing the question request. 
    The response includes:
    - 'code': The status code indicating the outcome of the request.
    - 'response': A description of the response status.
    - 'question-id' (optional): The identifier of the question (if applicable).
    - 'participant': The participant identifier.
    """
    if request.method == 'GET':
        question = request.args.get('question')
        answers = request.args.get('answers')
        k = request.args.get('k')
    elif request.method == 'POST':
        data = request.get_json()
        question = data.get('question')
        answers = data.get('answers')
        k = data.get('k')
    else:
        return jsonify({'code': 405, 
        'response': 'Method Not Allowed', 
        'participant': id_participant})
    try:
        response = subprocess.run(["python3", "kuko_client.py", id_participant, host, port], 
        capture_output=True, text=True, input=f"10;{question};{answers};{k}\nEXIT").stdout
        match = re.search(r'RECV:({.*?})', response)
        data = json.loads(match.group(1))
        return jsonify(data)
    except AttributeError:
        return jsonify({'code': 503, 
        'response': 'Service Unavailable', 
        'participant': id_participant})
    except Exception:
        return jsonify({'code': 400, 
        'response': 'Bad Request', 
        'participant': id_participant})
    
@app.route('/qset', methods=['GET', 'POST'])
def qset():
    """
    Ensures:
    Processing a QSET request from a participant and returning 
    a JSON response containing the result of processing the question set request. 
    The response includes:
    - 'code': The status code indicating the outcome of the request.
    - 'response': A description of the response status.
    - 'qset-id' (optional): The identifier of the question set (if applicable).
    - 'participant': The participant identifier.
    """
    if request.method == 'GET':
        questions = request.args.get('questions')
    elif request.method == 'POST':
        data = request.get_json()
        questions = data.get('questions')
    else:
        return jsonify({'code': 405, 
        'response': 'Method Not Allowed', 
        'participant': id_participant})
    try:
        response = subprocess.run(["python3", "kuko_client.py", id_participant, host, port], 
        capture_output=True, text=True, input=f"20;{questions}\nEXIT").stdout
        match = re.search(r'RECV:\{(.*?)\}', response)
        data = re.findall(r"'(.*?)'", match.group(1))
        return jsonify({
            'code': data[0], 
            'response': data[1], 
            **({'qset-id': data[2]} if len(data) > 2 else {}),
            'participant': id_participant
        })
    except AttributeError:
        return jsonify({'code': 503, 
        'response': 'Service Unavailable', 
        'participant': id_participant})
    except Exception:
        return jsonify({'code': 400, 
        'response': 'Bad Request', 
        'participant': id_participant})
    
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    """
    Ensures:
    Processing a QUIZ request from a participant and returning 
    a JSON response containing the result of processing the quiz request. 
    The response includes:
    - 'code': The status code indicating the outcome of the request.
    - 'response': A description of the response status.
    - 'quiz-id' (optional): The identifier of the quiz (if applicable).
    - 'participant': The participant identifier.
    """
    if request.method == 'GET':
        qset = request.args.get('qset')
        points = request.args.get('points')
    elif request.method == 'POST':
        data = request.get_json()
        qset = data.get('qset')
        points = data.get('points')
    else:
        return jsonify({'code': 405, 
        'response': 'Method Not Allowed', 
        'participant': id_participant})
    try:
        response = subprocess.run(["python3", "kuko_client.py", id_participant, host, port], 
        capture_output=True, text=True, input=f"30;{qset};{points}\nEXIT").stdout
        match = re.search(r'RECV:({.*?})', response)
        data = json.loads(match.group(1))
        return jsonify(data)
    except AttributeError:
        return jsonify({'code': 503, 
        'response': 'Service Unavailable', 
        'participant': id_participant})
    except Exception:
        return jsonify({'code': 400, 
        'response': 'Bad Request', 
        'participant': id_participant})

@app.route('/launch', methods=['GET', 'POST'])
def launch():
    """
    Ensures:
    Processing a LAUNCH request from a participant and returning 
    a JSON response containing the result of launching the quiz. The response includes:
    - 'code': The status code indicating the outcome of the request.
    - 'response': A description of the response status.
    - 'participant': The participant identifier.
    """
    if request.method == 'GET':
        quiz = request.args.get('quiz')
    elif request.method == 'POST':
        data = request.get_json()
        quiz = data.get('quiz')
    else:
        return jsonify({'code': 405, 
        'response': 'Method Not Allowed', 
        'participant': id_participant})
    try:
        response = subprocess.run(["python3", "kuko_client.py", id_participant, host, port], 
        capture_output=True, text=True, input=f"40;{quiz}\nEXIT").stdout
        match = re.search(r'RECV:({.*?})', response)
        data = json.loads(match.group(1))
        return jsonify(data)
    except AttributeError:
        return jsonify({'code': 503, 
        'response': 'Service Unavailable', 
        'participant': id_participant})
    except Exception:
        return jsonify({'code': 400, 
        'response': 'Bad Request', 
        'participant': id_participant})
    
@app.route('/next', methods=['GET', 'POST'])
def next():
    """
    Ensures:
    Processing a NEXT request from a participant and returning 
    a JSON response containing the next question in the quiz. The response includes:
    - 'code': The status code indicating the outcome of the request.
    - 'response': A description of the response status.
    - 'participant': The participant identifier.
    """
    if request.method == 'GET':
        quiz = request.args.get('quiz')
    elif request.method == 'POST':
        data = request.get_json()
        quiz = data.get('quiz')
    else:
        return jsonify({'code': 405, 
        'response': 'Method Not Allowed', 
        'participant': id_participant})
    try:
        response = subprocess.run(["python3", "kuko_client.py", id_participant, host, port], 
        capture_output=True, text=True, input=f"50;{quiz}\nEXIT").stdout
        match = re.search(r'RECV:({.*?})', response)
        data = json.loads(match.group(1))
        return jsonify(data)
    except AttributeError:
        return jsonify({'code': 503, 
        'response': 'Service Unavailable', 
        'participant': id_participant})
    except Exception:
        return jsonify({'code': 400, 
        'response': 'Bad Request', 
        'participant': id_participant})
    
@app.route('/reg', methods=['GET', 'POST'])
def reg():
    """
    Ensures:
    Processing a REG request from a participant and returning 
    a JSON response containing the result of registering the participant for the quiz. 
    The response includes:
    - 'code': The status code indicating the outcome of the request.
    - 'response': A description of the response status.
    - 'participant': The participant identifier.
    """
    if request.method == 'GET':
        quiz = request.args.get('quiz')
    elif request.method == 'POST':
        data = request.get_json()
        quiz = data.get('quiz')
    else:
        return jsonify({'code': 405, 
        'response': 'Method Not Allowed', 
        'participant': id_participant})
    try:
        response = subprocess.run(["python3", "kuko_client.py", id_participant, host, port], 
        capture_output=True, text=True, input=f"60;{quiz}\nEXIT").stdout
        match = re.search(r'RECV:({.*?})', response)
        data = json.loads(match.group(1))
        return jsonify(data)
    except AttributeError:
        return jsonify({'code': 503, 
        'response': 'Service Unavailable', 
        'participant': id_participant})
    except Exception:
        return jsonify({'code': 400, 
        'response': 'Bad Request', 
        'participant': id_participant})
    
@app.route('/get', methods=['GET', 'POST'])
def get():
    """
    Ensures:
    Processing a GET request from a participant and returning 
    a JSON response containing the requested quiz data. The response includes:
    - 'code': The status code indicating the outcome of the request.
    - 'response': A description of the response status.
    - 'question' (optional): The question in the quiz (if applicable).
    - 'answers' (optional): The answers to the question (if applicable), separated by semicolons.
    - 'participant': The participant identifier.
    """
    if request.method == 'GET':
        quiz = request.args.get('quiz')
    elif request.method == 'POST':
        data = request.get_json()
        quiz = data.get('quiz')
    else:
        return jsonify({'code': 405, 
        'response': 'Method Not Allowed', 
        'participant': id_participant})
    try:
        response = subprocess.run(["python3", "kuko_client.py", id_participant, host, port], 
        capture_output=True, text=True, input=f"70;{quiz}\nEXIT").stdout
        match = re.search(r'RECV:({.*?})', response)
        data = json.loads(match.group(1))
        return jsonify(data)
    except AttributeError:
        return jsonify({'code': 503, 
        'response': 'Service Unavailable', 
        'participant': id_participant})
    except Exception:
        return jsonify({'code': 400, 
        'response': 'Bad Request', 
        'participant': id_participant})
    
@app.route('/ans', methods=['GET', 'POST'])
def ans():
    """
    Ensures:
    Processing an ANS request from a participant and returning 
    a JSON response containing the result of submitting the answer. The response includes:
    - 'code': The status code indicating the outcome of the request.
    - 'response': A description of the response status.
    - 'participant': The participant identifier.
    """
    if request.method == 'GET':
        quiz = request.args.get('quiz')
        answer = request.args.get('answer')
    elif request.method == 'POST':
        data = request.get_json()
        quiz = data.get('quiz')
        answer = data.get('answer')
    else:
        return jsonify({'code': 405, 
        'response': 'Method Not Allowed', 
        'participant': id_participant})
    try:
        response = subprocess.run(["python3", "kuko_client.py", id_participant, host, port], 
        capture_output=True, text=True, input=f"80;{quiz};{answer}\nEXIT").stdout
        match = re.search(r'RECV:({.*?})', response)
        data = json.loads(match.group(1))
        return jsonify(data)
    except AttributeError:
        return jsonify({'code': 503, 
        'response': 'Service Unavailable', 
        'participant': id_participant})
    except Exception:
        return jsonify({'code': 400, 
        'response': 'Bad Request', 
        'participant': id_participant})

@app.route('/rel', methods=['GET', 'POST'])
def rel():
    """
    Ensures:
    Processing a REL request from a participant and returning 
    a JSON response containing the quiz report for the participant. The response includes:
    - 'code': The status code indicating the outcome of the request.
    - 'response': A description of the response status.
    - 'quiz' (optional): The identifier of the quiz (if applicable).
    - 'report' (optional): The report of the quiz (if applicable).
    - 'participant': The participant identifier.
    """
    if request.method == 'GET':
        quiz = request.args.get('quiz')
    elif request.method == 'POST':
        data = request.get_json()
        quiz = data.get('quiz')
    else:
        return jsonify({'code': 405, 
        'response': 'Method Not Allowed', 
        'participant': id_participant})
    try:
        response = subprocess.run(["python3", "kuko_client.py", id_participant, host, port], 
        capture_output=True, text=True, input=f"90;{quiz}\nEXIT").stdout
        match = re.search(r'RECV:({.*?})', response)
        data = json.loads(match.group(1))
        return jsonify(data)
    except AttributeError:
        return jsonify({'code': 503, 
        'response': 'Service Unavailable', 
        'participant': id_participant})
    except Exception:
        return jsonify({'code': 400, 
        'response': 'Bad Request', 
        'participant': id_participant})
    
if __name__ == '__main__':
    # Collect arguments
    id_participant = sys.argv[1]
    host = sys.argv[2]
    port = sys.argv[3]
    # Run flask app
    app.run(host='127.0.0.1', port=5005)


