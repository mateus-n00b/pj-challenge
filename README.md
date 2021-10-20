# pj-challenge
##Questões Concluídas
- [x] 1
- [x] 2a
- [ ] 2b
- [x] 2c(i)
- [x] 2c(ii)
- [ ] 2c(iii)
- [ ] 3
- [x] Bônus

##Instruções de uso
- Primeiramente, instale as dependências: ```pip install -r requirements.txt```
- Dentro da pasta dados_projetos adicione as planilhas (o git não permitiu o envio das mesmas)
- Para executar a api entre em /api e execute: ```python app.py```
- Em seguida, defina a url da API no arquivo config/environment.py (API_URL)
- Execute a aplicação de visualização usando o comando ```gunicorn app:server 0.0.0.0 8050```

##Observações 
- A aplicação em si está lenta devido ao consumo da API. Os datasets são grandes e demorados para baixar.
- Foi necessário definir o [boot timeout](https://devcenter.heroku.com/changelog-items/364) do heroku em 280s.
- Para executar a api é preciso incluir os .csv enviados por email na pasta dados_projetos.
- Ao selecionar Produto, o gráfico é gerado individualmente.

##BoT
**Para executar o bot, entre no diretório bot/ basta rodar o comando ``python comex_bot.py`` e aguardar :D**.

**Os arquivos gerados são salvos no diretório onde foi executado**

##FIXME
- A API ao inicializar baixa uma parcela do arquivo f_comex.csv (apenas 3%), devido a dimensão do mesmo.
- Estou utilizando ngrok para expôr a API rodando em minha máquina (```ngrok http 5000```).
- Consertar a apresentação do gráfico de pizza, por algum motivo ele só é construído quando se passa números.

##TODO
- Documentar o código

Dúvidas? Contate-me :smile:
