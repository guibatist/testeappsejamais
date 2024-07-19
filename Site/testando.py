# import win32com.client as win32

# try:
#     outlook = win32.Dispatch('outlook.application')
#     print("Outlook instanciado com sucesso")
# except Exception as e:
#     print(f"Erro ao instanciar o Outlook: {e}")




# # Criando o código
# import random
# import string

# def generate_verification_code():
#     letters = ''.join(random.choices(string.ascii_uppercase, k=3))
#     numbers = ''.join(random.choices(string.digits, k=3))
#     code = letters + numbers
#     return code

# # Exemplo de uso
# verification_code = generate_verification_code()
# print(verification_code)

# # Função para ler o conteúdo do arquivo HTML
# def load_html_template(file_path):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         return file.read()

# # Caminho para o arquivo HTML
# html_file_path = 'teste.html'

# # Carregue o conteúdo do arquivo HTML
# html_content = load_html_template(html_file_path)


# email = outlook.CreateItem(0)

# # configurar as informações do seu email
# codigo = 1234

# email.To = "contato.guibatist@gmail.com" # para quem
# email.Subject = "Teste de Email" 
# email.HTMLBody = html_content
# email.Send()
# print("Deu certo")
# import psycopg2

# try:
#     con = psycopg2.connect(database = "sejamais", 
#                        host ="localhost", 
#                        user = "postgres", 
#                        password = "edua1428",
#                        port = "5432")
#     print('Conexão estabelecida.')
#     cursor = con.cursor()

# except psycopg2.Error as error:
#     print('Erro:', error)



# import datetime

# def pega_noticia_hoje():
#     # Vê o dia atual
#     hoje = datetime.date.today()
#     dateatual = hoje.strftime("%d/%m/%Y")
    
#     print(f'Data atual: {dateatual}')

#     # Faz a consulta SQL
#     cursor.execute("SELECT id FROM manchete WHERE data_publicacao = %s ORDER BY id DESC LIMIT 3", (dateatual,))
#     rows = cursor.fetchall()

#     # Extrai os três últimos registros
#     resultados = [row[0] for row in rows]  # Extrai apenas o primeiro elemento de cada tupla

#     # Se houver menos de três registros, preencha com None
#     while len(resultados) < 3:
#         resultados.append(None)

#     # Retorna os resultados
#     return resultados

# # Supondo que você já tenha uma conexão e um cursor estabelecidos
# cursor = con.cursor()
# id1, id2, id3 = pega_noticia_hoje()

# print(f'Resultado 1: {id1}')
# print(f'Resultado 2: {id2}')
# print(f'Resultado 3: {id3}')

# # Pegando a primeira manchete
# if id1 is not None:
#     cursor.execute("SELECT tema, titulo, resumo FROM manchete WHERE id = %s", (id1,))
#     rt1 = cursor.fetchone()
#     if rt1:
#         tema1, titulo1, resumo1 = rt1
#         print(f'Manchete 1 - Tema: {tema1}, Título: {titulo1}, Resumo: {resumo1}')


# # Pegando a segunda manchete
# if id2 is not None:
#     cursor.execute("SELECT tema, titulo, resumo FROM manchete WHERE id = %s", (id2,))
#     rt2 = cursor.fetchall()
#     print(f'Manchete 2: {rt2}')

# # Pegando a terceira manchete
# if id3 is not None:
#     cursor.execute("SELECT tema, titulo, resumo FROM manchete WHERE id = %s", (id3,))
#     rt3 = cursor.fetchall()
#     print(f'Manchete 3: {rt3}')


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Função para ler o conteúdo do arquivo HTML
def load_html_template(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Caminho para o arquivo HTML
html_file_path = 'teste.html'

# Carregue o conteúdo do arquivo HTML
html_content = load_html_template(html_file_path)

servidor = smtplib.SMTP('smtp.gmail.com', 587)
servidor.starttls()
servidor.login('guibatist2007@gmail.com', 'elsxhojgdyvgqnxl')

mensagem = MIMEMultipart()
mensagem['From'] = 'guibatist2007@@gmail.com'
mensagem['To'] = 'contato.guibatist@gmail.com'
mensagem['Subject'] = 'Meu Primeiro Email HTML'

# Corpo do email em HTML
html = html_content

# Anexar o corpo do email à mensagem
parte_html = MIMEText(html, 'html')
mensagem.attach(parte_html)

servidor.sendmail(mensagem['From'], mensagem['To'], mensagem.as_string())
servidor.quit()

# elsx hojg dyvg qnxl
