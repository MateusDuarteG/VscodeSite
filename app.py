import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_mail import Mail, Message

load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder="static")

# --- Flask-Mail ---------------------------------------------------------
# Todas as credenciais vêm do .env (veja .env.example). Nada disso deve
# ser commitado no Git com valores reais.
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER", "smtp.gmail.com")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_USERNAME")

# Para onde as mensagens do formulário de contato são enviadas.
# Por padrão, cai na sua própria caixa de entrada.
CONTACT_RECEIVER = os.getenv("CONTACT_RECEIVER", os.getenv("MAIL_USERNAME"))

mail = Mail(app)

PROJECTS = [
    {
        "title": "Portfólio Pessoal",
        "description": "Site feito em Flask com foco em performance e um visual próprio.",
        "link": "https://github.com/MateusDuarteG/site_portfolio",
    },
    {
        "title": "API Flask",
        "description": "API simples para autenticação de usuários.",
        "link": "https://github.com/MateusDuarteG/api_flask",
    },
    {
        "title": "Automação de Tarefas",
        "description": "Scripts para automatizar processos repetitivos do dia a dia.",
        "link": "https://github.com/MateusDuarteG/automacoes",
    },
]


@app.route("/")
def index():
    return render_template("index.html", ano=datetime.now().year)


@app.route("/projetos")
def projetos():
    return render_template("projetos.html", projects=PROJECTS, ano=datetime.now().year)


@app.route("/contato", methods=["GET", "POST"])
def contato():
    status = None

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        mensagem = request.form.get("mensagem", "").strip()

        if not (nome and email and mensagem):
            status = "error"
        else:
            try:
                msg = Message(
                    subject=f"Novo contato pelo portfólio - {nome}",
                    recipients=[CONTACT_RECEIVER],
                    reply_to=email,
                    body=(
                        f"Nome: {nome}\n"
                        f"Email: {email}\n\n"
                        f"Mensagem:\n{mensagem}"
                    ),
                )
                mail.send(msg)
                status = "success"
            except Exception as exc:
                app.logger.error("Falha ao enviar e-mail de contato: %s", exc)
                status = "error"

    return render_template("contato.html", status=status, ano=datetime.now().year)


if __name__ == "__main__":
    app.run(debug=True)
