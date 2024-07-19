from flask import Flask, render_template, url_for, request, redirect, jsonify, session
import psycopg2
import logging
from bs4 import BeautifulSoup
import requests


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

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)