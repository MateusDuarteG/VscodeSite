# 🌐 Portfólio — Mateus Gomes

Portfólio pessoal em Flask, com páginas de Início, Projetos e Contato.
O formulário de contato envia e-mail de verdade via Flask-Mail.

## 🚀 Tecnologias

- Python + Flask
- Flask-Mail (envio de e-mail do formulário de contato)
- HTML + CSS (sem framework de CSS — design próprio)

## ⚙️ Como rodar localmente

```bash
pip install -r requirements.txt
cp .env.example .env
# edite o .env com seu email e senha de app
python app.py
```

O site sobe em `http://localhost:5000`.

## 🔐 Configurando o e-mail do formulário de contato

1. Copie `.env.example` para `.env`
2. Se usar Gmail, gere uma senha de app em https://myaccount.google.com/apppasswords
   (senha normal da conta não funciona com o Gmail)
3. Preencha `MAIL_USERNAME`, `MAIL_PASSWORD` e `CONTACT_RECEIVER` no `.env`
4. **Nunca** commite o `.env` com valores reais — ele já está no `.gitignore`

## 📈 Próximos passos

- Adicionar mais projetos reais conforme forem surgindo
- Seção de blog/artigos
- Testes automatizados para a rota de contato

---
Desenvolvido e mantido por Mateus.
