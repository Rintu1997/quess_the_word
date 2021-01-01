import os
from flask import Flask, request, render_template, url_for, jsonify
from multiprocessing import Value
from database import readData

counter = Value('i', 0)
scoreCounter = Value('i', -5)
questionCounter = Value('i', 0)

app = Flask(__name__)

quesData = readData()


def getScore():
    with scoreCounter.get_lock():
        scoreCounter.value += 5
        score = scoreCounter.value
    return score


def getQuestion():
    with questionCounter.get_lock():
        index = questionCounter.value
        questionCounter.value += 1
    # quiz = list(quesData.keys())[index]
    quiz = quesData[index]
    return quiz['q']


@app.route("/try-again", methods=['GET', 'POST'])
def tryAgain():
    with questionCounter.get_lock():
        questionCounter.value -= 1
    with scoreCounter.get_lock():
        scoreCounter.value -= 5
    return game()


@app.route("/resetCount", methods=['GET', 'POST'])
def resetCounter():
    counter.value = 0
    scoreCounter.value = -5
    questionCounter.value = 0
    return game()


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route("/game", methods=['GET', 'POST'])
def game():
    with counter.get_lock():
        counter.value += 1
        out = counter.value
    with questionCounter.get_lock():
        quesIdx = questionCounter.value
    return render_template('game.html', data=getQuestion(), count=out, quesIdx=quesIdx, score=getScore())


@app.route('/guess', methods=['POST'])
def result():
    with questionCounter.get_lock():
        index = questionCounter.value
    print(quesData[index]["a"])
    if request.form['guess'] == quesData[index]["a"]:
        with counter.get_lock():
            counter.value = 0
        answer = "সঠিক উত্তৰ ।"
        return render_template("result.html", answer=answer, correct=1)
    else:
        answer = "ভুল উত্তৰ, খেল অতিৰিক্ত।"
        return render_template("result.html", answer=answer, correct=0)


if __name__ == '__main__':
    app.run(debug=True)
