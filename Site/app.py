from flask import Flask, render_template, url_for, request, redirect, jsonify, session, g
import psycopg2
from psycopg2 import pool
import logging
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import win32com.client as win32
import random
import string
import pythoncom
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

try:
    outlook = win32.Dispatch('outlook.application')
    print("Outlook instanciado com sucesso")
except Exception as e:
    print(f"Erro ao instanciar o Outlook: {e}")

# Conexao banco de dados
# Conexão com o banco de dados
try:
    con = psycopg2.connect(database = "sejamais",
                       host ="localhost",
                       user = "postgres",
                       password = "edua1428",
                       port = "5432")
    print('Conexão estabelecida.')
    cursor = con.cursor()

except psycopg2.Error as error:
    print('Erro:', error)


# Arquivo.html inicial
html_inicio = 'templates/inicio.html'

app = Flask(__name__)
app.jinja_env.cache = None
app.secret_key = 'sua_chave_secreta'



# Criando os destaques
# Quadrado 1


import datetime

def pega_noticia_hoje():
    # Vê o dia atual
    hoje = datetime.date.today()
    dateatual = hoje.strftime("%d/%m/%Y")

    print(f'Data atual: {dateatual}')

    # Faz a consulta SQL
    cursor.execute("SELECT id FROM manchete WHERE data_publicacao = %s ORDER BY id DESC LIMIT 3", (dateatual,))
    rows = cursor.fetchall()

    # Extrai os três últimos registros
    resultados = [row[0] for row in rows]  # Extrai apenas o primeiro elemento de cada tupla

    # Se houver menos de três registros, preencha com notícias do dia anterior
    while len(resultados) < 3:
        dia_anterior = hoje - datetime.timedelta(days=1)
        dateanterior = dia_anterior.strftime("%d/%m/%Y")
        cursor.execute("SELECT id FROM manchete WHERE data_publicacao = %s ORDER BY id DESC LIMIT %s", (dateanterior, 3 - len(resultados)))
        rows_anterior = cursor.fetchall()
        resultados.extend([row[0] for row in rows_anterior])

    # Retorna os resultados
    return resultados

# Supondo que você já tenha uma conexão e um cursor estabelecidos
cursor = con.cursor()
id1, id2, id3 = pega_noticia_hoje()

print(f'Resultado 1: {id1}')
print(f'Resultado 2: {id2}')
print(f'Resultado 3: {id3}')

def obter_detalhes_noticia(id):
    if id is None:
        return None, None, None, None
    cursor.execute("SELECT link_imagem, tema, titulo, resumo FROM manchete WHERE id = %s", (id,))
    return cursor.fetchone()

linkdanoticia, temadanoticia, titulodanoticia, resumodanoticia = obter_detalhes_noticia(id1)
linkdanoticia2, temadanoticia2, titulodanoticia2, resumodanoticia2 = obter_detalhes_noticia(id2)
linkdanoticia3, temadanoticia3, titulodanoticia3, resumodanoticia3 = obter_detalhes_noticia(id3)

def pega_noticia_outros():
    # Obtém os IDs das notícias de hoje
    id1, id2, id3 = pega_noticia_hoje()

    # Monta a consulta SQL excluindo os IDs obtidos
    cursor.execute("SELECT id FROM manchete WHERE id NOT IN (%s, %s, %s) ORDER BY id DESC LIMIT 8", (id1, id2, id3,))
    rows = cursor.fetchall()

    # Retorna os resultados
    return rows

ido1, ido2, ido3, ido4, ido5, ido6, ido7, ido8 = pega_noticia_outros()

print(f'Resultado 1: {ido1}')
print(f'Resultado 2: {ido2}')
print(f'Resultado 3: {ido3}')
print(f'Resultado 3: {ido4}')
print(f'Resultado 3: {ido5}')
print(f'Resultado 3: {ido6}')
print(f'Resultado 3: {ido7}')
print(f'Resultado 3: {ido8}')

def obter_detalhes_noticia_outros(ido):
    if ido is None:
        return None, None, None
    cursor.execute("SELECT link_imagem, tema, titulo FROM manchete WHERE id = %s", (ido,))
    return cursor.fetchone()

linkdanoticiaoutros, temadanoticiaoutros, titulodanoticiaoutros = obter_detalhes_noticia_outros(ido1)
linkdanoticiaoutros2, temadanoticiaoutros2, titulodanoticiaoutros2 = obter_detalhes_noticia_outros(ido2)
linkdanoticiaoutros3, temadanoticiaoutros3, titulodanoticiaoutros3 = obter_detalhes_noticia_outros(ido3)
linkdanoticiaoutros4, temadanoticiaoutros4, titulodanoticiaoutros4 = obter_detalhes_noticia_outros(ido4)
linkdanoticiaoutros5, temadanoticiaoutros5, titulodanoticiaoutros5 = obter_detalhes_noticia_outros(ido5)
linkdanoticiaoutros6, temadanoticiaoutros6, titulodanoticiaoutros6 = obter_detalhes_noticia_outros(ido6)
linkdanoticiaoutros7, temadanoticiaoutros7, titulodanoticiaoutros7 = obter_detalhes_noticia_outros(ido7)
linkdanoticiaoutros8, temadanoticiaoutros8, titulodanoticiaoutros8 = obter_detalhes_noticia_outros(ido8)


def pegando_destaques():
    cursor.execute("SELECT idnew FROM destaques ORDER BY id DESC LIMIT 3")
    rows = cursor.fetchall()

    # Extrai os três últimos registros
    resultados = [row[0] for row in rows]  # Extrai apenas o primeiro elemento de cada tupla
    con.closed
    return resultados

idd1, idd2, idd3 = pegando_destaques()


def obter_detalhes_noticia_destaque(idd):
    if idd is None:
        return None, None, None
    cursor = con.cursor()
    cursor.execute("SELECT titulo, tema, link_imagem FROM manchete WHERE id = %s", (idd,))
    return cursor.fetchone()

titulodestaque1, temadestaque1, linkdestaque1 = obter_detalhes_noticia_destaque(idd1)
titulodestaque2, temadestaque2, linkdestaque2 = obter_detalhes_noticia_destaque(idd2)
titulodestaque3, temadestaque3, linkdestaque3 = obter_detalhes_noticia_destaque(idd3)



@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/login", methods=['GET', 'POST'])
def pegandologin():

     username = request.form['username']
     password = request.form['password']
     print(f'Nome de Usuário: {username}')
     print(f'Senha: {password}')

     # Consultar se o email já está cadastrado
     cursor.execute('SELECT email FROM cadastros WHERE email = %s', (username,))
     nome = cursor.fetchone()
     if nome:
         nome = nome[0]
         print(f'O nome no banco é:  {nome} ')

         cursor.execute('SELECT senha FROM cadastros WHERE email = %s', (username,))
         senha = cursor.fetchone()
         senha = senha[0]

         cursor.execute('SELECT nome FROM cadastros WHERE email = %s', (username,))
         nomepss = cursor.fetchone()
         nomepss = nomepss[0]
         print('O nome do usuario é ', nomepss)

         print(f'A senha no banco é:  {senha} ')

         if username == nome and password == senha:
             session['nomepss'] = nomepss
             return redirect(url_for('inicio'))
         else:
             mensagem = 'Usuário ou senha incorreta'
             return render_template('login.html', mensagem=mensagem)
     else:
         mensagem = 'Usuário não encontrado'
         return render_template('login.html', mensagem=mensagem)



linkdanoticiaoutros, temadanoticiaoutros, titulodanoticiaoutros = obter_detalhes_noticia_outros(ido1)
linkdanoticiaoutros2, temadanoticiaoutros2, titulodanoticiaoutros2 = obter_detalhes_noticia_outros(ido2)
linkdanoticiaoutros3, temadanoticiaoutros3, titulodanoticiaoutros3 = obter_detalhes_noticia_outros(ido3)
linkdanoticiaoutros4, temadanoticiaoutros4, titulodanoticiaoutros4 = obter_detalhes_noticia_outros(ido4)

@app.route("/")
def inicio():
    
    idd1nv, idd2nv, idd3nv = pegando_destaques()
    print(idd1nv, idd2nv, idd3nv)
    
    titulodestaque1, temadestaque1, linkdestaque1 = obter_detalhes_noticia_destaque(idd1nv)
    titulodestaque2, temadestaque2, linkdestaque2 = obter_detalhes_noticia_destaque(idd2nv)
    titulodestaque3, temadestaque3, linkdestaque3 = obter_detalhes_noticia_destaque(idd3nv)

    if 'nomepss' in session:
        nome_usuario = session['nomepss']
        return render_template('inicio.html', 
                               nome_usuario=nome_usuario, 

                               # DESTAQUES
                               titulodestaque1=titulodestaque1, 
                               temadestaque1=temadestaque1, 
                               linkdestaque1=linkdestaque1, 
                               titulodestaque2=titulodestaque2, 
                               temadestaque2=temadestaque2, 
                               linkdestaque2=linkdestaque2, 
                               titulodestaque3=titulodestaque3, 
                               temadestaque3=temadestaque3, 
                               linkdestaque3=linkdestaque3, 
                               
                               # OUTRAS NOTICIAS
                               titulodanoticiaoutros=titulodanoticiaoutros,
                               titulodanoticiaoutros2=titulodanoticiaoutros2,
                               titulodanoticiaoutros3=titulodanoticiaoutros3,
                               titulodanoticiaoutros4=titulodanoticiaoutros4

                               )
    else:
        return render_template('inicio.html', 
                               
                               # DESTAQUES
                               titulodestaque1=titulodestaque1, 
                               temadestaque1=temadestaque1, 
                               linkdestaque1=linkdestaque1, 
                               titulodestaque2=titulodestaque2, 
                               temadestaque2=temadestaque2, 
                               linkdestaque2=linkdestaque2, 
                               titulodestaque3=titulodestaque3, 
                               temadestaque3=temadestaque3, 
                               linkdestaque3=linkdestaque3, 
                               
                               # OUTRAS NOTICIAS
                               titulodanoticiaoutros=titulodanoticiaoutros,
                               titulodanoticiaoutros2=titulodanoticiaoutros2,
                               titulodanoticiaoutros3=titulodanoticiaoutros3,
                               titulodanoticiaoutros4=titulodanoticiaoutros4

                               )

@app.route("/abrenoticia/<titulo>")
def abrenoticia(titulo):
    idd1nv, idd2nv, idd3nv = pegando_destaques()

    titulodestaque1, temadestaque1, linkdestaque1 = obter_detalhes_noticia_destaque(idd1nv)
    titulodestaque2, temadestaque2, linkdestaque2 = obter_detalhes_noticia_destaque(idd2nv)
    titulodestaque3, temadestaque3, linkdestaque3 = obter_detalhes_noticia_destaque(idd3nv)

    cursor.execute("SELECT jornalista FROM manchete WHERE titulo = %s", (titulo,))
    jornalista = cursor.fetchall()

    # Verifica se a consulta retornou algum resultado
    if jornalista:
        jornalista = jornalista[0][0]
        print(jornalista)
    else:
        jornalista = "Desconhecido"  # Definindo um valor padrão
        print("No results found for the specified title.")

    # Executa as consultas e define valores padrão para variáveis, se necessário
    cursor.execute("SELECT data_publicacao FROM manchete WHERE titulo = %s", (titulo,))
    data_publicacao = cursor.fetchone()
    data_publicacao = data_publicacao[0] if data_publicacao else "Data desconhecida"

    cursor.execute("SELECT hora_publicacao FROM manchete WHERE titulo = %s", (titulo,))
    hora_publicacao = cursor.fetchone()
    hora_publicacao = hora_publicacao[0] if hora_publicacao else "Hora desconhecida"

    cursor.execute("SELECT tema FROM manchete WHERE titulo = %s", (titulo,))
    tema = cursor.fetchone()
    tema = tema[0] if tema else "Tema desconhecido"

    cursor.execute("SELECT resumo FROM manchete WHERE titulo = %s", (titulo,))
    resumo = cursor.fetchone()
    resumo = resumo[0] if resumo else "Resumo desconhecido"

    cursor.execute("SELECT link_imagem FROM manchete WHERE titulo = %s", (titulo,))
    link_imagem = cursor.fetchone()
    link_imagem = link_imagem[0] if link_imagem else "Link de imagem desconhecido"

    cursor.execute("SELECT texto1 FROM manchete WHERE titulo = %s", (titulo,))
    texto1 = cursor.fetchone()
    texto1 = texto1[0] if texto1 else "Texto1 desconhecido"

    cursor.execute("SELECT texto2 FROM manchete WHERE titulo = %s", (titulo,))
    texto2 = cursor.fetchone()
    texto2 = texto2[0] if texto2 else "Texto2 desconhecido"

    cursor.execute("SELECT titulo_paragrafo3 FROM manchete WHERE titulo = %s", (titulo,))
    titulo_paragrafo3 = cursor.fetchone()
    titulo_paragrafo3 = titulo_paragrafo3[0] if titulo_paragrafo3 else "Título parágrafo 3 desconhecido"

    cursor.execute("SELECT texto_paragrafo3 FROM manchete WHERE titulo = %s", (titulo,))
    texto_paragrafo3 = cursor.fetchone()
    texto_paragrafo3 = texto_paragrafo3[0] if texto_paragrafo3 else "Texto parágrafo 3 desconhecido"

    cursor.execute("SELECT titulo_paragrafo4 FROM manchete WHERE titulo = %s", (titulo,))
    titulo_paragrafo4 = cursor.fetchone()
    titulo_paragrafo4 = titulo_paragrafo4[0] if titulo_paragrafo4 else "Título parágrafo 4 desconhecido"

    cursor.execute("SELECT texto_paragrafo4 FROM manchete WHERE titulo = %s", (titulo,))
    texto_paragrafo4 = cursor.fetchone()
    texto_paragrafo4 = texto_paragrafo4[0] if texto_paragrafo4 else "Texto parágrafo 4 desconhecido"

    # Adiciona as últimas três notícias do mesmo tema
    cursor.execute('SELECT titulo FROM manchete WHERE tema = %s and titulo != %s  ORDER BY data_publicacao DESC LIMIT 3', (tema, titulo,))
    rows = cursor.fetchall()
    resultados = [row[0] for row in rows]  # Extrai apenas o primeiro elemento de cada tupla

    if len(resultados) == 3:
        tema1, tema2, tema3 = resultados
        titulotema = 'Notícias Relacionadas'
        nome_usuario = session.get('nomepss')  # Define um valor padrão se a chave não estiver na session

        if titulo_paragrafo3 == 'NONE' and texto_paragrafo3 == 'NONE':
            return render_template('noticias/noticia.html',
                                    nome_usuario=nome_usuario,
                                    titulo=titulo,
                                    jornalista=jornalista,
                                    data_publicacao=data_publicacao,
                                    hora_publicacao=hora_publicacao,
                                    tema=tema,
                                    resumo=resumo,
                                    link_imagem=link_imagem,
                                    texto1=texto1,
                                    texto2=texto2,

                                    # Relacionados
                                    titulotema=titulotema,
                                    tema1=tema1,
                                    tema2=tema2,
                                    tema3=tema3
                                    )
        elif titulo_paragrafo4 == 'NONE' and texto_paragrafo4 == 'NONE':
            return render_template('noticias/noticia.html',
                                    nome_usuario=nome_usuario,
                                    titulo=titulo,
                                    jornalista=jornalista,
                                    data_publicacao=data_publicacao,
                                    hora_publicacao=hora_publicacao,
                                    tema=tema,
                                    resumo=resumo,
                                    link_imagem=link_imagem,
                                    texto1=texto1,
                                    texto2=texto2,
                                    titulo_paragrafo3=titulo_paragrafo3,
                                    texto_paragrafo3=texto_paragrafo3,

                                    # Relacionados
                                    titulotema=titulotema,
                                    tema1=tema1,
                                    tema2=tema2,
                                    tema3=tema3
                                    )
        else:
            return render_template('noticias/noticia.html',
                                    titulo=titulo,
                                    jornalista=jornalista,
                                    data_publicacao=data_publicacao,
                                    hora_publicacao=hora_publicacao,
                                    tema=tema,
                                    resumo=resumo,
                                    link_imagem=link_imagem,
                                    texto1=texto1,
                                    texto2=texto2,
                                    titulo_paragrafo3=titulo_paragrafo3,
                                    texto_paragrafo3=texto_paragrafo3,
                                    titulo_paragrafo4=titulo_paragrafo4,
                                    texto_paragrafo4=texto_paragrafo4,

                                    # Relacionados
                                    titulotema=titulotema,
                                    tema1=tema1,
                                    tema2=tema2,
                                    tema3=tema3
                                    )
    else:
        titulotema = 'Notícias de Destaque'
        nome_usuario = session.get('nomepss')  # Define um valor padrão se a chave não estiver na session

        if titulo_paragrafo3 == 'NONE' and texto_paragrafo3 == 'NONE':
            return render_template('noticias/noticia.html',
                                    nome_usuario=nome_usuario,
                                    titulo=titulo,
                                    jornalista=jornalista,
                                    data_publicacao=data_publicacao,
                                    hora_publicacao=hora_publicacao,
                                    tema=tema,
                                    resumo=resumo,
                                    link_imagem=link_imagem,
                                    texto1=texto1,
                                    texto2=texto2,

                                    # Relacionados
                                    titulotema=titulotema,
                                    tema1=titulodestaque1,
                                    tema2=titulodestaque2,
                                    tema3=titulodestaque3
                                    )
        elif titulo_paragrafo4 == 'NONE' and texto_paragrafo4 == 'NONE':
            return render_template('noticias/noticia.html',
                                    nome_usuario=nome_usuario,
                                    titulo=titulo,
                                    jornalista=jornalista,
                                    data_publicacao=data_publicacao,
                                    hora_publicacao=hora_publicacao,
                                    tema=tema,
                                    resumo=resumo,
                                    link_imagem=link_imagem,
                                    texto1=texto1,
                                    texto2=texto2,
                                    titulo_paragrafo3=titulo_paragrafo3,
                                    texto_paragrafo3=texto_paragrafo3,

                                    # Relacionados
                                    titulotema=titulotema,
                                    tema1=titulodestaque1,
                                    tema2=titulodestaque2,
                                    tema3=titulodestaque3
                                    )
        else:
            return render_template('noticias/noticia.html',
                                    titulo=titulo,
                                    jornalista=jornalista,
                                    data_publicacao=data_publicacao,
                                    hora_publicacao=hora_publicacao,
                                    tema=tema,
                                    resumo=resumo,
                                    link_imagem=link_imagem,
                                    texto1=texto1,
                                    texto2=texto2,
                                    titulo_paragrafo3=titulo_paragrafo3,
                                    texto_paragrafo3=texto_paragrafo3,
                                    titulo_paragrafo4=titulo_paragrafo4,
                                    texto_paragrafo4=texto_paragrafo4,

                                    # Relacionados
                                    titulotema=titulotema,
                                    tema1=titulodestaque1,
                                    tema2=titulodestaque2,
                                    tema3=titulodestaque3
                                    )



@app.route('/voltar', methods=['POST'])
def voltar():
    # Logic for what happens when "Voltar" is clicked
    return 'Redirected to inicio', 200

@app.route("/meuperfil", methods=["GET", "POST"])
def desconectar():
    nome_usuario = session['nomepss']
    return render_template('meuperfil.html', nome_usuario=nome_usuario)


@app.route("/vagasdeemprego")
def vagas():
    if 'nomepss' in session:
        nome_usuario = session['nomepss']
        return render_template('vagas.html', nome_usuario=nome_usuario)
    else:
        return render_template('vagas.html')


@app.route("/vagasdeemprego", methods=['POST'])
def buscar_vagas():
    if 'nomepss' in session:
        nome_usuario = session['nomepss']

        # Obter os dados do formulário
        local = request.form['local']
        tipo = request.form['tipo']

        # Adicionar os caracteres curinga para a consulta
        local = f"%{local}%"
        tipo = f"%{tipo}%"

        query = """
            SELECT titulo, resumovaga, id FROM vagas
            WHERE local LIKE %s AND tipodecontrato LIKE %s
        """
        cursor.execute(query, (local, tipo,))
        vagas = cursor.fetchall()

        # Transformar os resultados em uma lista de dicionários
        resultados = [{'titulo': vaga[0], 'resumo': vaga[1], 'id': vaga[2]} for vaga in vagas]

        # Renderizar um template com os resultados
        return render_template('vagas.html', vagas=resultados, nome_usuario=nome_usuario)
    return redirect(url_for('desconectar'))

@app.route("/maisdavaga/<titulo>/<int:id>")
def maisdavaga(titulo, id):
    # Consultar os dados da vaga usando o ID fornecido
    cursor.execute("SELECT titulo, area, resumovaga, nomedaempresa, local, escolaridademin, idademin, tipodecontrato, emailempresa FROM vagas WHERE id = %s", (id,))
    vaga = cursor.fetchone()

    if vaga:
        titulo, areadavaga, resumovaga, empresavaga, localvaga, escominvaga, idadevaga, tipovaga, emailvaga = vaga

        # Traduzir tipo de contrato, se necessário
        if tipovaga == 'JVP':
            tipovaga = 'Jovem Aprendiz'
        elif tipovaga == 'ESTG':
            tipovaga = 'Estágio'

        # Formatar título para uso em email
        formatted_titulo = '@sjob' + titulo.lower().replace(' ', '')

        return render_template('vagaporcompleto.html', titulo=titulo,
                               areadavaga=areadavaga,
                               resumovaga=resumovaga,
                               empresavaga=empresavaga,
                               localvaga=localvaga,
                               escominvaga=escominvaga,
                               idadevaga=idadevaga,
                               tipovaga=tipovaga,
                               emailvaga=emailvaga,
                               formatted_titulo=formatted_titulo)
    else:
        # Trate o caso em que a vaga com o ID especificado não foi encontrada
        return "Vaga não encontrada"



@app.route("/logout", methods=['GET', 'POST'])
def logout():
    if request.method == 'GET':
        # Se o método for GET, renderiza o template logout.html
        return render_template('logout.html')
    elif request.method == 'POST':
        # Se o método for POST, realiza o logout
        session.pop('nomepss', None)
        # Redireciona para a página inicial após o logout
        return redirect(url_for('inicio'))





# Envio de email e verificação
# Gera um código de verificação aleatório
def generate_verification_code():
    letters = ''.join(random.choices(string.ascii_uppercase, k=3))
    numbers = ''.join(random.choices(string.digits, k=3))
    code = letters + numbers
    return code

# Função para enviar o e-mail de verificação
def send_verification_email(to_email, username):
    
    pythoncom.CoInitialize()
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = to_email
    mail.Subject = "Teste de Email"

    # URL para a rota de teste
    test_url = url_for('testeum', _external=True)

    mail.HTMLBody = f"""
    <p>Olá, {username}</p>
    <p>Clique no botão abaixo para verificar seu e-mail e criar sua conta:</p>
    <form action="{test_url}" method="get">
        <button type="submit" style="padding: 10px 20px; background-color: #007bff; color: white; border: none; cursor: pointer; text-decoration: none;">
            Verificar Email
        </button>
    </form>
    """
    mail.Send()
    print("Email enviado com sucesso")



@app.route("/registro")
def registro():
    return render_template('registro.html')

@app.route("/registro", methods=['POST'])
def pegandoregistro():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    print(f'Nome de Usuário: {username}')
    print(f'Senha: {password}')

    # Consultar se o email já está cadastrado
    cursor.execute("SELECT email FROM cadastros WHERE email = %s", (email,))
    result = cursor.fetchone()

    if result:
        mensagem = 'Este email já está sendo usado.'
        return render_template('registro.html', mensagem=mensagem)
    else:
        vefcode = generate_verification_code()
        send_verification_email(email, username)
        return redirect(url_for('avisocodigo', username=username, email=email, password=password))

@app.route("/avisocodigo")
def avisocodigo():
    # Receber os parâmetros da URL
    global username
    username = request.args.get('username')

    global email
    email = request.args.get('email')

    global password
    password = request.args.get('password')
    if request:
        send_verification_email(email, username)
        print("Email foi reenviado")
        print(email, username)
        redirect(url_for('testeum', username=username, email=email, password=password))
    return render_template('enviodocod.html', username=username, email=email, password=password)


@app.route("/testeum")
def testeum():
    # Recebendo as var
    global username
    global email
    global password

    cursor.execute('INSERT INTO cadastros (nome, email, senha) VALUES (%s, %s, %s)', (username, email, password))
    con.commit()
    return redirect(url_for('login'))

@app.route("/verify_email", methods=['GET'])
def verify_email():
    username = request.args.get('username')
    verification_code = request.args.get('verification_code')

    # Simula a verificação do código (você pode implementar sua lógica real aqui)
    if verification_code == generate_verification_code():
        # Marca que o link de verificação foi clicado (aqui, apenas imprime uma mensagem)
        print(f"O usuário {username} clicou no link de verificação.")
        return "Link de verificação clicado com sucesso!"
    else:
        return "Código de verificação inválido ou expirado."





















@app.route('/botao_clicado', methods=['POST'])
def botao_clicado():
    return render_template('oplano.html')

@app.route("/quemsomos", methods=['GET', 'POST'])
def quemsomos():
    # Puxa os IDs dos últimos 4 registros inseridos
    cursor.execute("SELECT id FROM vagas ORDER BY id DESC LIMIT 4")
    ultimos_ids = cursor.fetchall()

    # Extrai os IDs em uma lista
    ids = [id[0] for id in ultimos_ids]

    # Consulta os títulos e datas formatadas baseados nos IDs
    vagas_formatadas = []
    for id in ids:
        cursor.execute("SELECT titulo, diadavaga FROM vagas WHERE id = %s", (id,))
        titulo, diadavaga = cursor.fetchone()
        # Verifica se diadavaga é do tipo correto antes de converter
        if isinstance(diadavaga, datetime.date):
            diadavaga_formatada = diadavaga.strftime('%d/%m/%Y')
            vagas_formatadas.append((titulo, diadavaga_formatada))

    if 'nomepss' in session:
        nome_usuario = session['nomepss']
        return render_template('quemsomos.html', nome_usuario=nome_usuario, vagas_formatadas=vagas_formatadas, is_logged_in=True)
    else:
        return render_template('quemsomos.html', vagas_formatadas=vagas_formatadas, is_logged_in=False)


# IDs de notícias a serem excluídas
id1, id2, id3 = pega_noticia_hoje()
ido1, ido2, ido3, ido4, ido5, ido6, ido7, ido8 = pega_noticia_outros()

# Todos os IDs a serem excluídos
ids_excluidos = [id1, id2, id3, ido1, ido2, ido3, ido4, ido5, ido6, ido7, ido8]









@app.route("/portaldoembu")
def portaldoembu():

    id1, id2, id3 = pega_noticia_hoje()

    linkdanoticia, temadanoticia, titulodanoticia, resumodanoticia = obter_detalhes_noticia(id1)
    linkdanoticia2, temadanoticia2, titulodanoticia2, resumodanoticia2 = obter_detalhes_noticia(id2)
    linkdanoticia3, temadanoticia3, titulodanoticia3, resumodanoticia3 = obter_detalhes_noticia(id3)

    # Pegando os Outros
    linkdanoticiaoutros, temadanoticiaoutros, titulodanoticiaoutros = obter_detalhes_noticia_outros(ido1)
    linkdanoticiaoutros2, temadanoticiaoutros2, titulodanoticiaoutros2 = obter_detalhes_noticia_outros(ido2)
    linkdanoticiaoutros3, temadanoticiaoutros3, titulodanoticiaoutros3 = obter_detalhes_noticia_outros(ido3)
    linkdanoticiaoutros4, temadanoticiaoutros4, titulodanoticiaoutros4 = obter_detalhes_noticia_outros(ido4)
    linkdanoticiaoutros5, temadanoticiaoutros5, titulodanoticiaoutros5 = obter_detalhes_noticia_outros(ido5)
    linkdanoticiaoutros6, temadanoticiaoutros6, titulodanoticiaoutros6 = obter_detalhes_noticia_outros(ido6)
    linkdanoticiaoutros7, temadanoticiaoutros7, titulodanoticiaoutros7 = obter_detalhes_noticia_outros(ido7)
    linkdanoticiaoutros8, temadanoticiaoutros8, titulodanoticiaoutros8 = obter_detalhes_noticia_outros(ido8)

    idd1nv, idd2nv, idd3nv = pegando_destaques()
    print(idd1nv, idd2nv, idd3nv)
    
    titulodestaque1, temadestaque1, linkdestaque1 = obter_detalhes_noticia_destaque(idd1nv)
    titulodestaque2, temadestaque2, linkdestaque2 = obter_detalhes_noticia_destaque(idd2nv)
    titulodestaque3, temadestaque3, linkdestaque3 = obter_detalhes_noticia_destaque(idd3nv)

    # Buscar todas as notícias exceto as excluídas
    cursor.execute("SELECT id, link_imagem, tema, titulo, data_publicacao, hora_publicacao FROM manchete WHERE id NOT IN %s ORDER BY id DESC", (tuple(ids_excluidos),))
    todas_noticias = cursor.fetchall()

    if 'nomepss' in session:
        nome_usuario = session['nomepss']
        return render_template('portaldoembu.html',
                               nome_usuario=nome_usuario,

                               # DESTAQUES
                               titulodestaque1=titulodestaque1, 
                               temadestaque1=temadestaque1, 
                               linkdestaque1=linkdestaque1, 
                               titulodestaque2=titulodestaque2, 
                               temadestaque2=temadestaque2, 
                               linkdestaque2=linkdestaque2, 
                               titulodestaque3=titulodestaque3, 
                               temadestaque3=temadestaque3, 
                               linkdestaque3=linkdestaque3, 

                               # HOJE
                               temadanoticia=temadanoticia,
                               titulodanoticia=titulodanoticia,
                               resumodanoticia=resumodanoticia,
                               linkdanoticia=linkdanoticia,

                               temadanoticia2=temadanoticia2,
                               titulodanoticia2=titulodanoticia2,
                               resumodanoticia2=resumodanoticia2,
                               linkdanoticia2=linkdanoticia2,

                               temadanoticia3=temadanoticia3,
                               titulodanoticia3=titulodanoticia3,
                               resumodanoticia3=resumodanoticia3,
                               linkdanoticia3=linkdanoticia3,

                               # Outros
                               linkdanoticiaoutros=linkdanoticiaoutros,
                               temadanoticiaoutros=temadanoticiaoutros,
                               titulodanoticiaoutros=titulodanoticiaoutros,

                               linkdanoticiaoutros2=linkdanoticiaoutros2,
                               temadanoticiaoutros2=temadanoticiaoutros2,
                               titulodanoticiaoutros2=titulodanoticiaoutros2,

                               linkdanoticiaoutros3=linkdanoticiaoutros3,
                               temadanoticiaoutros3=temadanoticiaoutros3,
                               titulodanoticiaoutros3=titulodanoticiaoutros3,

                               linkdanoticiaoutros4=linkdanoticiaoutros4,
                               temadanoticiaoutros4=temadanoticiaoutros4,
                               titulodanoticiaoutros4=titulodanoticiaoutros4,

                               linkdanoticiaoutros5=linkdanoticiaoutros5,
                               temadanoticiaoutros5=temadanoticiaoutros5,
                               titulodanoticiaoutros5=titulodanoticiaoutros5,

                               linkdanoticiaoutros6=linkdanoticiaoutros6,
                               temadanoticiaoutros6=temadanoticiaoutros6,
                               titulodanoticiaoutros6=titulodanoticiaoutros6,

                               linkdanoticiaoutros7=linkdanoticiaoutros7,
                               temadanoticiaoutros7=temadanoticiaoutros7,
                               titulodanoticiaoutros7=titulodanoticiaoutros7,

                               linkdanoticiaoutros8=linkdanoticiaoutros8,
                               temadanoticiaoutros8=temadanoticiaoutros8,
                               titulodanoticiaoutros8=titulodanoticiaoutros8,

                               # TUDO
                               todas_noticias=todas_noticias

                               )
    else:
        return render_template('portaldoembu.html',
                               # DESTAQUES
                               # DESTAQUES
                               titulodestaque1=titulodestaque1, 
                               temadestaque1=temadestaque1, 
                               linkdestaque1=linkdestaque1, 
                               titulodestaque2=titulodestaque2, 
                               temadestaque2=temadestaque2, 
                               linkdestaque2=linkdestaque2, 
                               titulodestaque3=titulodestaque3, 
                               temadestaque3=temadestaque3, 
                               linkdestaque3=linkdestaque3, 

                               # HOJE
                               temadanoticia=temadanoticia,
                               titulodanoticia=titulodanoticia,
                               resumodanoticia=resumodanoticia,
                               linkdanoticia=linkdanoticia,

                               temadanoticia2=temadanoticia2,
                               titulodanoticia2=titulodanoticia2,
                               resumodanoticia2=resumodanoticia2,
                               linkdanoticia2=linkdanoticia2,

                               temadanoticia3=temadanoticia3,
                               titulodanoticia3=titulodanoticia3,
                               resumodanoticia3=resumodanoticia3,
                               linkdanoticia3=linkdanoticia3,

                               # Outros
                               linkdanoticiaoutros=linkdanoticiaoutros,
                               temadanoticiaoutros=temadanoticiaoutros,
                               titulodanoticiaoutros=titulodanoticiaoutros,

                               linkdanoticiaoutros2=linkdanoticiaoutros2,
                               temadanoticiaoutros2=temadanoticiaoutros2,
                               titulodanoticiaoutros2=titulodanoticiaoutros2,

                               linkdanoticiaoutros3=linkdanoticiaoutros3,
                               temadanoticiaoutros3=temadanoticiaoutros3,
                               titulodanoticiaoutros3=titulodanoticiaoutros3,

                               linkdanoticiaoutros4=linkdanoticiaoutros4,
                               temadanoticiaoutros4=temadanoticiaoutros4,
                               titulodanoticiaoutros4=titulodanoticiaoutros4,

                               linkdanoticiaoutros5=linkdanoticiaoutros5,
                               temadanoticiaoutros5=temadanoticiaoutros5,
                               titulodanoticiaoutros5=titulodanoticiaoutros5,

                               linkdanoticiaoutros6=linkdanoticiaoutros6,
                               temadanoticiaoutros6=temadanoticiaoutros6,
                               titulodanoticiaoutros6=titulodanoticiaoutros6,

                               linkdanoticiaoutros7=linkdanoticiaoutros7,
                               temadanoticiaoutros7=temadanoticiaoutros7,
                               titulodanoticiaoutros7=titulodanoticiaoutros7,

                               linkdanoticiaoutros8=linkdanoticiaoutros8,
                               temadanoticiaoutros8=temadanoticiaoutros8,
                               titulodanoticiaoutros8=titulodanoticiaoutros8,
                               todas_noticias=todas_noticias)



@app.route("/contato")
def contato():
    if 'nomepss' in session:
        nome_usuario = session['nomepss']
        return render_template('contato.html', nome_usuario=nome_usuario)
    else:
        return render_template('contato.html')

# Criando uma manchete

"""
1. Ele cria o texto, colando:
- titulo, Resumo, tema, Texto 1, Texto2, Paragrafo 1, Texto 1, Texto 2
Se quiser:
Paragrafo 2, Texto 1 e 2
Automatico é: o Dia


2. Salva num banco de dados

"""

@app.route("/logintrabalhador")
def logintrabalhador():
    return render_template('noticias/logintrabalhador.html')

@app.route("/logintrabalhador", methods=['POST'])
def pglogintrabalhador():
    username = request.form['username']
    password = request.form['password']
    print(f'Nome de Usuário: {username}')
    print(f'Senha: {password}')

    # Consultar se o email já está cadastrado
    cursor.execute('SELECT email, senha, nome FROM funcionarios_acesso WHERE email = %s', (username,))
    result = cursor.fetchone()

    if result:
        email_bd, senha_bd, nome_bd = result
        print(f'O nome no banco é:  {nome_bd}')

        if username == email_bd and password == senha_bd:
            return redirect(url_for('menucreator'))
        else:
            mensagem = 'Usuário ou senha incorreta'
            return render_template('noticias/logintrabalhador.html', mensagem=mensagem)
    else:
        mensagem = 'Usuário não encontrado'
        return render_template('noticias/logintrabalhador.html', mensagem=mensagem)

@app.route("/menucreador")
def menucreator():
    return render_template('noticias/menu.html')

@app.route("/ambientedecreate")
def ambientedecreate():
    return render_template('noticias/hello.html')

@app.route('/exibir_tabela')
def exibir_tabela():
    cursor.execute("SELECT id, titulo, resumo, tema FROM manchete;")
    rows = cursor.fetchall()
    return render_template('noticias/qualdestaque.html', rows=rows)

# Rota para processar seleção de IDs
@app.route('/processar_ids', methods=['POST'])
def processar_ids():
    if request.method == 'POST':
        ids_selecionados = request.form.getlist('ids_selecionados')
        # Aqui você pode processar os IDs selecionados como desejar
        # Por exemplo, salvar em outra tabela no PostgreSQL
        print("IDs selecionados:", ids_selecionados)

        dest1, dest2, dest3 = ids_selecionados
        print(f"Número 1: {dest1}, Número 2: {dest2}, Número 3 {dest3}")
        # Implemente a lógica para salvar os IDs em outra função
        cursor.execute('INSERT INTO destaques (idnew) VALUES (%s), (%s), (%s)', (dest1, dest2, dest3,))
        con.commit()
        print(dest1, dest2, dest3)
        return redirect(url_for('menucreator'))

    return "Método inválido"





@app.route("/destacar_noticias", methods=["POST"])
def destacar_noticias():
    if request.method == "POST":
        try:
            # Obter os IDs das notícias selecionadas para destaque
            noticia1 = request.form.get("noticia1")
            noticia2 = request.form.get("noticia2")
            noticia3 = request.form.get("noticia3")

            print(noticia1, noticia2, noticia3)
        except psycopg2.Error as e:
            con.rollback()  # Reverter a transação em caso de erro
            print(f"Erro ao destacar notícias: {e}")
            return "Erro ao destacar notícias."


@app.route("/newscreate", methods=['POST'])
def newscreate():
    # Vê o dia atual
    hoje = datetime.date.today()
    dateatual = hoje.strftime("%d/%m/%Y")

    # Obtém a hora atual
    agora = datetime.datetime.now()
    hora_atual = agora.strftime("%Hh%M")

    # Transforma a hora em "00h00"
    hora_publicacao = hora_atual

    if request.method == 'POST':
        # Processamento do formulário de criação de notícias
        journalist = request.form['journalist']
        theme = request.form['theme']
        title = request.form['title']
        summary = request.form['summary']
        imagem = request.form['imagem']
        text1 = request.form['text1']
        text2 = request.form['text2']

        # Variáveis para os parágrafos principais
        main_paragraph_1_title = text1 if text1 else 'NONE'
        main_paragraph_1_text = text1 if text1 else 'NONE'
        main_paragraph_2_title = text2 if text2 else 'NONE'
        main_paragraph_2_text = text2 if text2 else 'NONE'

        # Variáveis para os parágrafos adicionais
        additional_paragraph_3_title = request.form.get('title_paragraph_3', 'NONE')
        additional_paragraph_3_text = request.form.get('text_paragraph_3', 'NONE')
        additional_paragraph_4_title = request.form.get('title_paragraph_4', 'NONE')
        additional_paragraph_4_text = request.form.get('text_paragraph_4', 'NONE')

        # Imprimir parágrafos principais
        print(f'Parágrafo 1 - Título: {main_paragraph_1_title}, Texto: {main_paragraph_1_text}')
        print(f'Parágrafo 2 - Título: {main_paragraph_2_title}, Texto: {main_paragraph_2_text}')

        # Imprimir parágrafos adicionais
        print(f'Parágrafo 3 - Título: {additional_paragraph_3_title}, Texto: {additional_paragraph_3_text}')
        print(f'Parágrafo 4 - Título: {additional_paragraph_4_title}, Texto: {additional_paragraph_4_text}')

        # Aqui você pode salvar os dados em variáveis ou processá-los como necessário
        # Por exemplo, você pode inserir no banco de dados ou realizar outras operações

        # Exemplo de impressão dos dados para verificação
        print(f'Jornalista: {journalist}')
        print(f'Tema: {theme}')
        print(f'Título: {title}')
        print(f'Resumo: {summary}')
        print(f'Imagem: {imagem}')
        # Adicionando os valores no banco de dados
        cursor.execute("""
            INSERT INTO manchete
            (jornalista, tema, titulo, resumo, link_imagem, texto1, texto2, titulo_paragrafo3, texto_paragrafo3, titulo_paragrafo4, texto_paragrafo4, data_publicacao, hora_publicacao)
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (journalist, theme, title, summary, imagem, text1, text2, additional_paragraph_3_title, additional_paragraph_3_text, additional_paragraph_4_title, additional_paragraph_4_text, dateatual, hora_publicacao))

        con.commit()


        print(f'Hoje é dia {dateatual}, publicado ás {hora_publicacao}')
        # Aqui você pode redirecionar para uma página de confirmação ou fazer o que for necessário
        return redirect(url_for('menucreator'))



    # Se for método GET ou qualquer outra coisa, renderize o formulário novamente
    return render_template('vagas.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

"""
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'manchete';
"""