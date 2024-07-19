import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import psycopg2

class CriarNoticiaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Criar Notícia")

        # Variáveis para armazenar os valores dos campos
        self.jornalista_var = tk.StringVar()
        self.tema_var = tk.StringVar()
        self.titulo_var = tk.StringVar()
        self.resumo_var = tk.StringVar()
        self.link_imagem_var = tk.StringVar()
        self.texto1_var = tk.StringVar()
        self.texto2_var = tk.StringVar()
        self.titulo_paragrafo3_var = tk.StringVar()
        self.texto_paragrafo3_var = tk.StringVar()
        self.titulo_paragrafo4_var = tk.StringVar()
        self.texto_paragrafo4_var = tk.StringVar()
        self.data_var = tk.StringVar()
        self.hora_var = tk.StringVar()

        # Definindo os jornalistas e temas disponíveis
        self.jornalistas = ['Guilherme', 'Junior', 'João']
        self.temas = ['Política', 'Esporte', 'Religião', 'Cultura', 'Mundo']

        # Criando os widgets
        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(self.frame, text="Jornalista:").grid(row=0, column=0, sticky=tk.W)
        self.jornalista_combo = ttk.Combobox(self.frame, textvariable=self.jornalista_var, values=self.jornalistas, state="readonly")
        self.jornalista_combo.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Tema:").grid(row=1, column=0, sticky=tk.W)
        self.tema_combo = ttk.Combobox(self.frame, textvariable=self.tema_var, values=self.temas, state="readonly")
        self.tema_combo.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Título:").grid(row=2, column=0, sticky=tk.W)
        self.titulo_entry = ttk.Entry(self.frame, textvariable=self.titulo_var, width=60)
        self.titulo_entry.grid(row=2, column=1, padx=5, pady=5, columnspan=2)

        ttk.Label(self.frame, text="Resumo (até 250 caracteres):").grid(row=3, column=0, sticky=tk.W)
        self.resumo_entry = ttk.Entry(self.frame, textvariable=self.resumo_var, width=60)
        self.resumo_entry.grid(row=3, column=1, padx=5, pady=5, columnspan=2)

        ttk.Label(self.frame, text="Link da Imagem:").grid(row=4, column=0, sticky=tk.W)
        self.link_imagem_entry = ttk.Entry(self.frame, textvariable=self.link_imagem_var, width=60)
        self.link_imagem_entry.grid(row=4, column=1, padx=5, pady=5, columnspan=2)

        ttk.Label(self.frame, text="Texto 1 (obrigatório):").grid(row=5, column=0, sticky=tk.W)
        self.texto1_text = tk.Text(self.frame, width=60, height=6)
        self.texto1_text.grid(row=5, column=1, padx=5, pady=5, columnspan=2)

        ttk.Label(self.frame, text="Texto 2 (obrigatório):").grid(row=6, column=0, sticky=tk.W)
        self.texto2_text = tk.Text(self.frame, width=60, height=6)
        self.texto2_text.grid(row=6, column=1, padx=5, pady=5, columnspan=2)

        ttk.Label(self.frame, text="Título Parágrafo 3:").grid(row=7, column=0, sticky=tk.W)
        self.titulo_paragrafo3_entry = ttk.Entry(self.frame, textvariable=self.titulo_paragrafo3_var, width=60)
        self.titulo_paragrafo3_entry.grid(row=7, column=1, padx=5, pady=5, columnspan=2)

        ttk.Label(self.frame, text="Texto Parágrafo 3:").grid(row=8, column=0, sticky=tk.W)
        self.texto_paragrafo3_text = tk.Text(self.frame, width=60, height=4)
        self.texto_paragrafo3_text.grid(row=8, column=1, padx=5, pady=5, columnspan=2)

        ttk.Label(self.frame, text="Título Parágrafo 4:").grid(row=9, column=0, sticky=tk.W)
        self.titulo_paragrafo4_entry = ttk.Entry(self.frame, textvariable=self.titulo_paragrafo4_var, width=60)
        self.titulo_paragrafo4_entry.grid(row=9, column=1, padx=5, pady=5, columnspan=2)

        ttk.Label(self.frame, text="Texto Parágrafo 4:").grid(row=10, column=0, sticky=tk.W)
        self.texto_paragrafo4_text = tk.Text(self.frame, width=60, height=4)
        self.texto_paragrafo4_text.grid(row=10, column=1, padx=5, pady=5, columnspan=2)

        ttk.Button(self.frame, text="Criar Notícia", command=self.criar_noticia).grid(row=12, column=1, pady=10, columnspan=2)

    def limpar_campos(self):
        self.jornalista_var.set('')
        self.tema_var.set('')
        self.titulo_var.set('')
        self.resumo_var.set('')
        self.link_imagem_var.set('')
        self.texto1_text.delete("1.0", "end")
        self.texto2_text.delete("1.0", "end")
        self.titulo_paragrafo3_var.set('')
        self.texto_paragrafo3_text.delete("1.0", "end")
        self.titulo_paragrafo4_var.set('')
        self.texto_paragrafo4_text.delete("1.0", "end")

    def criar_noticia(self):
        # Validação básica dos campos obrigatórios
        if not self.texto1_text.get("1.0", "end-1c").strip() or not self.texto2_text.get("1.0", "end-1c").strip():
            messagebox.showerror("Erro", "Os campos Texto 1 e Texto 2 são obrigatórios.")
            return

        # Obter valores dos campos
        jornalista = self.jornalista_var.get()
        tema = self.tema_var.get()
        titulo = self.titulo_var.get()
        resumo = self.resumo_var.get()
        link_imagem = self.link_imagem_var.get()
        texto1 = self.texto1_text.get("1.0", "end-1c")
        texto2 = self.texto2_text.get("1.0", "end-1c")
        titulo_paragrafo3 = self.titulo_paragrafo3_var.get()
        texto_paragrafo3 = self.texto_paragrafo3_text.get("1.0", "end-1c").strip()
        titulo_paragrafo4 = self.titulo_paragrafo4_var.get()
        texto_paragrafo4 = self.texto_paragrafo4_text.get("1.0", "end-1c").strip()

        # Obter data e hora atuais
        data_atual = datetime.now().strftime("%d/%m/%Y")
        hora_atual = datetime.now().strftime("%Hh%M")

        # Formatando data e hora
        data_hora_formatada = f"{hora_atual}"

        # Definir 'NONE' se os parágrafos 3 ou 4 estiverem vazios
        if not texto_paragrafo3:
            texto_paragrafo3 = 'NONE'
        if not texto_paragrafo4:
            texto_paragrafo4 = 'NONE'
        if not titulo_paragrafo3:
            titulo_paragrafo3 = 'NONE'
        if not titulo_paragrafo4:
            titulo_paragrafo4 = 'NONE'

        # Conectar ao banco de dados PostgreSQL
        try:
            conn = psycopg2.connect(database = "sejamais", 
                       host ="localhost", 
                       user = "postgres", 
                       password = "edua1428",
                       port = "5432")
            cursor = conn.cursor()

            # Comando SQL INSERT INTO
            sql_insert = """
            INSERT INTO manchete (jornalista, tema, titulo, resumo, link_imagem, texto1, texto2, 
                                 titulo_paragrafo3, texto_paragrafo3, titulo_paragrafo4, texto_paragrafo4, 
                                 data_publicacao, hora_publicacao)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            # Executando o comando SQL
            cursor.execute(sql_insert, (
                jornalista, tema, titulo, resumo, link_imagem, texto1, texto2,
                titulo_paragrafo3, texto_paragrafo3, titulo_paragrafo4, texto_paragrafo4,
                data_atual, data_hora_formatada
            ))
            conn.commit()
            messagebox.showinfo("Notícia Criada", "Notícia inserida com sucesso no banco de dados.")
            self.limpar_campos()
        except psycopg2.Error as e:
            conn.rollback()
            messagebox.showerror("Erro", f"Erro ao inserir notícia no banco de dados: {e}")

        finally:
            if conn:
                cursor.close()
                conn.close()

# Função principal para iniciar o aplicativo
def main():
    root = tk.Tk()
    app = CriarNoticiaApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
