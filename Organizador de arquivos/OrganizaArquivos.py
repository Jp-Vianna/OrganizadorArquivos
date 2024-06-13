import os
import shutil
import tkinter as tk
import sys
from tkinter import filedialog
from tkinter import messagebox


class Organiza:
    def __init__(self, caminho):
        # Caminho para a pasta a ser limpa.
        self.caminho = caminho

        # Endereço da pasta da área de trabalho.
        self.Desktop = os.path.join(os.environ['USERPROFILE'], 'Documents')

        # Lista de extensões para imagens.
        self.extensoes_imagens = [
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp', '.heif',
            '.heic', '.ico', '.raw'
        ]

        # Lista de extensões para vídeos
        self.extensoes_videos = [
            '.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.webm', '.mpeg', '.mpg',
            '.m4v', '.3gp', '.3g2', '.ts'
        ]

        # Lista de extensões para executáveis
        self.extensoes_executaveis = [
            '.exe', '.bat', '.sh', '.bin', '.cmd', '.com', '.msi', '.deb', '.rpm',
            '.apk', '.jar', '.app'
        ]

        # Lista de extensões para arquivos gerais.
        self.extensoes_comuns = [
            '.txt', '.md', '.rtf', '.doc', '.docx', '.odt', '.pdf', '.tex', '.wpd',
            '.log', '.cfg', '.ppt', '.pptx', '.odp', '.key', '.xls', '.xlsx', '.ods',
            '.csv', '.tsv'
        ]

        # Lista de extensões para audios.
        self.extensoes_audio = [
            '.mp3', '.wav', '.aac', '.flac', '.ogg', '.wma', '.m4a', '.alac', '.aiff'
        ]

        # Lista para arquivos compactados.
        self.extensoes_compactados = [
            '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.iso', '.tgz'
        ]

        # Lista de extensões de códigos-fonte e scripts.
        self.extensoes_scripts = [
            '.py', '.js', '.java', '.c', '.cpp', '.h', '.rb', '.pl', '.php', '.sh', '.bat',
            '.sql', '.db', '.sqlite', '.accdb', '.mdb'
        ]

    def executa(self):
        caminho_output = os.path.join(self.Desktop, "Bot")
        os.makedirs(caminho_output, exist_ok=True)

        for nome_arquivo in os.listdir(self.caminho):
            caminho_arquivo = os.path.join(self.caminho, nome_arquivo)

            if os.path.isfile(caminho_arquivo):
                self.identifica_extensao(caminho_arquivo, caminho_output)
            else:
                self.altera_pasta(caminho_arquivo, self.cria_pasta(caminho_output, "Pastas"))

    def identifica_extensao(self, caminho_arquivo, caminho_output):
        extensao = os.path.splitext(caminho_arquivo)
        extensao = extensao[1]

        if extensao in self.extensoes_comuns:
            self.altera_pasta(caminho_arquivo, self.cria_pasta(caminho_output, "Geral"))
        elif extensao in self.extensoes_imagens:
            self.altera_pasta(caminho_arquivo, self.cria_pasta(caminho_output, "Imagens"))
        elif extensao in self.extensoes_scripts:
            self.altera_pasta(caminho_arquivo, self.cria_pasta(caminho_output, "Scripts"))
        elif extensao in self.extensoes_compactados:
            self.altera_pasta(caminho_arquivo, self.cria_pasta(caminho_output, "Compactados"))
        elif extensao in self.extensoes_videos:
            self.altera_pasta(caminho_arquivo, self.cria_pasta(caminho_output, "Videos"))
        elif extensao in self.extensoes_executaveis:
            self.altera_pasta(caminho_arquivo, self.cria_pasta(caminho_output, "Executáveis"))
        elif extensao in self.extensoes_audio:
            self.altera_pasta(caminho_arquivo, self.cria_pasta(caminho_output, "Audio"))
        else:
            self.altera_pasta(caminho_arquivo, self.cria_pasta(caminho_output, "Não identificado"))

    def cria_pasta(self, pasta_mae, nome_pasta):
        caminho_pasta = self.cria_caminho(pasta_mae, nome_pasta)
        os.makedirs(caminho_pasta, exist_ok=True)

        return caminho_pasta

    @staticmethod
    def cria_caminho(pasta_mae, nome_pasta):
        return os.path.join(pasta_mae, nome_pasta)

    @staticmethod
    def altera_pasta(origem, destino):
        shutil.move(origem, destino)


class App:
    def __init__(self, raiz):
        self.area_entrada = tk.Frame(raiz)
        self.area_entrada.pack(pady=10)

        self.exibe_pasta = tk.Entry(self.area_entrada, width=40)
        self.exibe_pasta.pack(side=tk.LEFT, padx=5)

        self.pesquisar_bt = tk.Button(self.area_entrada, text="Escolher", command=self.seleciona_pasta)
        self.pesquisar_bt.pack(side=tk.RIGHT, padx=5)

        self.confirmar_bt = tk.Button(raiz, text="Confirmar", command=self.confirma_clickado)
        self.confirmar_bt.pack(side=tk.BOTTOM, padx=10, pady=10)

    def seleciona_pasta(self):
        pasta = filedialog.askdirectory()

        if pasta:
            self.exibe_pasta.delete(0, tk.END)
            self.exibe_pasta.insert(0, pasta)

    def confirma_clickado(self):
        caminho_completo = self.exibe_pasta.get()

        if caminho_completo:
            if self.verif_vazio(caminho_completo):
                org = Organiza(caminho_completo)
                org.executa()
                messagebox.showwarning("Aviso", "Organização concluída!")
                sys.exit()
            else:
                messagebox.showwarning("Aviso", "A pasta está vazia.")
        else:
            messagebox.showwarning("Aviso", "Você deve escolher uma pasta.")

    @staticmethod
    def verif_vazio(caminho_completo):
        # Verifica se a pasta selecionada está vazia.
        return len(os.listdir(caminho_completo)) != 0


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x200")
    root.title("Selecione o Arquivo")
    app = App(root)
    root.mainloop()
