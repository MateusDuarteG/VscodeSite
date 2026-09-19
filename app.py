import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, render_template, request, abort
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

# Dicionário de projetos com as chaves exatas esperadas pelos templates
PROJETOS = {
    "portfolio-pessoal": {
        "titulo": "Portfólio Pessoal",
        "kicker": "~/projetos/portfolio-pessoal",
        "descricao_curta": "Site feito em Flask com foco em performance, visual próprio e apresentação de trabalhos e projetos pessoais.",
        "descricao_completa": "Este é o meu portfólio profissional web, desenvolvido utilizando Flask no backend e um design minimalista inspirado em interfaces de terminal. O objetivo principal é centralizar meus projetos, habilidades técnicas e canais de contato de forma performática e responsiva.",
        "github": "https://github.com/MateusDuarteG/VscodeSite",
        "tecnologias": ["Python", "Flask", "HTML5", "CSS3", "Jinja2"],
        "funcionalidades": [
            "Arquitetura leve e modular com Flask.",
            "Design minimalista estilo Dark/Terminal responsivo.",
            "Formulário de contato com envio de e-mails.",
            "Páginas dedicadas para detalhamento de cada projeto."
        ],
        "imagem": "/static/img/portfolio-preview.png"
    },
    "api-flask": {
        "titulo": "API Flask",
        "kicker": "~/projetos/api-flask",
        "descricao_curta": "Uma API completa para gerenciamento de pedidos de lanches, com autenticação baseada em tokens JWT e integração com banco de dados.",
        "descricao_completa": "API RESTful desenvolvida para gerenciar o fluxo completo de pedidos. Inclui controle de autenticação de usuários via tokens JWT, gerenciamento de cardápio e status de pedidos integrados ao banco de dados.",
        "github": "https://github.com/MateusDuarteG/PORJETOFASTAPI",
        "tecnologias": ["Python", "Flask", "MySQL", "JWT", "SQLAlchemy"],
        "funcionalidades": [
            "Autenticação e autorização de usuários via tokens JWT.",
            "CRUD completo para produtos e pedidos.",
            "Integração e persistência com banco de dados MySQL.",
            "Tratamento centralizado de erros e respostas em formato JSON."
        ],
        "imagem": "/static/img/api-flask-preview.png"
    },
    "automacao-tarefas": {
        "titulo": "Automação de Tarefas",
        "kicker": "~/projetos/automacao-tarefas",
        "descricao_curta": "API Flask simples, com automação para resposta automática de e-mails do dia a dia.",
        "descricao_completa": "Serviço construído em Python para automatizar rotinas operacionais repetitivas, realizando a leitura de mensagens de entrada e respostas automáticas.",
        "github": "https://github.com/MateusDuarteG",
        "tecnologias": ["Python", "Flask", "SMTP", "Automations"],
        "funcionalidades": [
            "Conexão automatizada via protocolo SMTP.",
            "Processamento e envio de respostas padrão.",
            "Log de execuções para acompanhamento."
        ],
        "imagem": "/static/img/automacao-preview.png"
    }
}

@app.route("/")
def index():
    return render_template("index.html", ano=datetime.now().year)

@app.route('/projetos')
def projetos():
    return render_template('projetos.html', projetos=PROJETOS, ano=datetime.now().year)

@app.route('/projetos/<slug>')
def detalhe_projeto(slug):
    projeto = PROJETOS.get(slug)
    if not projeto:
        abort(404)
    return render_template('projeto_detalhe.html', projeto=projeto, ano=datetime.now().year)

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
