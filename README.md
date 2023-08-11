# PROJETO EVENTEX

Como começar a desenvolver hoje? Siga este guia!

# Como desenvolver?

1. Clone o repositório;
2. Crie um virtualenv com python;
3. Ative o virtual env;
4. Instale as dependências;
5. Configure a instância com o .env;
6. Execute os testes.

```console
git clone git@github:vitorpestana94/portifolio3.2.16 wttd
cd wttd
python -m venv .wttd
source .wttd/bin/activate
pip install -r requirements-dev.txt
cp contrib/env-sample .env
python manage.py test
```

# Como fazer o deploy?

1. Crie uma instância no heroku;
2. Envie as configurações para o heroku;
3. Defina uma SECRET_KEY segura para a instância;
4. Defina DEBUG=False;
5. Configure o serviço de email;
6. Envie o código para o heroku.