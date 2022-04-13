# Importing Libraries
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from flask import Flask, render_template, request

# variables
name =''
flag = 0
bot = ''
answers = [
    ("Dexter", "Welcome to the Service. What is your Name?")
]

# main
app = Flask(__name__)


@app.route('/')
def home():
    BotInit()
    return render_template('index.html', ans=answers)


@app.route('/answer', methods=['POST'])
def answer():
    global flag, name
    if flag == 0:
        name = request.form.get("query")
        flag = 1
        answers.append(
            (
                name,
                request.form.get("query")
            )
        )
        answers.append(
            (
                "Dexter",
                "How Can I Help You?"
            )
        )
    else:
        answers.append(
            (
                name,
                request.form.get("query")
            )
        )
        if request.form.get('query').lower().startswith("bye"):
            home()
        else:
            response = Chatbot(request.form.get('query'))
            answers.append(
                (
                    "Dexter",
                    response
                )
            )
    return render_template('index.html', ans=answers)

def BotInit():
    # Intialize the bot
    global bot
    bot = ChatBot("Dexter",
                  logic_adapters=['chatterbot.logic.BestMatch',
                                  'chatterbot.logic.MathematicalEvaluation'])
    # Training bot
    trainer = ChatterBotCorpusTrainer(bot)
    trainer.train("chatterbot.corpus.english")


def Chatbot(query):
    response = bot.get_response(query)
    return response

if __name__ == '__main__':
    app.run(debug=True)
