from tkinter import PhotoImage, messagebox, Tk, Button, Label, Scrollbar, Listbox, StringVar, Entry, W, E, N, S, END
from tkinter import ttk
from PIL import Image, ImageTk
import pypyodbc as pyo

from sqlserver_config import dbConfig

class Bookdb:
    def __init__(self):
        self.con = pyo.connect(**dbConfig)
        self.cursor = self.con.cursor()
        print("Estamos conectados com o banco de dados")

    def __del__(self):
        self.con.close()

    def view(self):
        self.cursor.execute("SELECT * FROM books")
        rows = self.cursor.fetchall()
        return rows

    def insert(self, title, author, isbn):
        sql = "INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)"
        values = [title, author, isbn]
        self.cursor.execute(sql, values)
        self.con.commit()
        messagebox.showinfo(title="BANCO DE DADOS", message="CADASTRO REALIZADO COM SUCESSO")

    def update(self, id, title, author, isbn):
        tsql = "UPDATE books SET title = ?, author = ?, isbn = ? WHERE id = ?"
        self.cursor.execute(tsql, [title, author, isbn, id])
        self.con.commit()
        messagebox.showinfo(title="BANCO DE DADOS", message="CADASTRO ATUALIZADO COM SUCESSO")

    def delete(self, id):
        delquery = "DELETE FROM books WHERE id = ?"
        self.cursor.execute(delquery, [id])
        self.con.commit()
        messagebox.showinfo(title="BANCO DE DADOS", message="CADASTRO DELETADO COM SUCESSO")

db = Bookdb()

def get_selected_row(event):
    global selected_tuple
    try:
        index = list_box.curselection()[0]
        selected_tuple = list_box.get(index)
        title_entry.delete(0, END)
        title_entry.insert(END, selected_tuple[1])
        author_entry.delete(0, END)
        author_entry.insert(END, selected_tuple[2])
        isbn_entry.delete(0, END)
        isbn_entry.insert(END, selected_tuple[3])
    except IndexError:
        pass

def view_records():
    list_box.delete(0, END)
    for row in db.view():
        list_box.insert(END, row)

def add_book():
    db.insert(title_text.get(), author_text.get(), isbn_text.get())
    list_box.delete(0, END)
    list_box.insert(END, (title_text.get(), author_text.get(), isbn_text.get()))
    title_entry.delete(0, END)
    author_entry.delete(0, END)
    isbn_entry.delete(0, END)

def delete_records():
    db.delete(selected_tuple[0])

def clear_screen():
    list_box.delete(0, END)
    title_entry.delete(0, END)
    author_entry.delete(0, END)
    isbn_entry.delete(0, END)

def update_records():
    db.update(selected_tuple[0], title_text.get(), author_text.get(), isbn_text.get())
    title_entry.delete(0, END)
    author_entry.delete(0, END)
    isbn_entry.delete(0, END)

def confirmar_saida():
    if messagebox.askokcancel("Confirmação", "Tem certeza que deseja sair?"):
        root.quit()

root = Tk()

root.iconbitmap(default='icone.ico')
root.title("Aplicação em Python, Usando Dois Bancos de Dados")

png_image = Image.open("aluno.png")
png_image.save("icone.ico")
root.iconbitmap(default='icone.ico')

root.configure(background="dark khaki")
root.geometry("1100x750")
root.resizable(width=False, height=False)

style = ttk.Style()
style.configure("TLabel", font=("TkDefaultFont", 14))
style.configure("TEntry", font=("TkDefaultFont", 12))

title_label = ttk.Label(root, text="Title", font=("TkDefaultFont", 16), background="dark khaki")
title_label.grid(row=0, column=0, sticky=W, padx=5, pady=5)

title_text = StringVar()
title_entry = ttk.Entry(root, width=24, textvariable=title_text)
title_entry.grid(row=0, column=1, sticky=W, padx=5, pady=5)

author_label = ttk.Label(root, text="Autor", background="dark khaki")
author_label.grid(row=0, column=2, sticky=W)

author_text = StringVar()
author_entry = ttk.Entry(root, width=50, textvariable=author_text)
author_entry.grid(row=0, column=3, sticky=W)

isbn_label = ttk.Label(root, text="Codigo", background="dark khaki")
isbn_label.grid(row=0, column=4, sticky=W, padx=5, pady=5)

isbn_text = StringVar()
isbn_entry = ttk.Entry(root, width=24, textvariable=isbn_text)
isbn_entry.grid(row=0, column=5, sticky=W, padx=5, pady=5)

add_btn = Button(root, text="Cadastrar", bg="green", fg="yellow", font="helvetica 10 bold", command=add_book)
add_btn.grid(row=0, column=6, sticky=W, padx=5, pady=5)

list_box = Listbox(root, height=25, width=80, font="helvetica 13", bg="light goldenrod yellow")
list_box.grid(row=1, column=0, columnspan=7, sticky=W+E, pady=20, padx=20)
list_box.bind('<<ListboxSelect>>', get_selected_row)

scroll_bar = Scrollbar(root)
scroll_bar.grid(row=1, column=7, sticky=N+S+W)

list_box.configure(yscrollcommand=scroll_bar.set)
scroll_bar.configure(command=list_box.yview)

button_frame = ttk.Frame(root)
button_frame.grid(row=2, column=0, columnspan=7, pady=20)

modificar_btn = Button(button_frame, text="Alterar Cadastro", bg="teal", fg="white", font="helvetica 10 bold", command=update_records)
modificar_btn.grid(row=0, column=0, padx=5, pady=5)

delete_btn = Button(button_frame, text="Deletar Cadastro", bg="red", fg="white", font="helvetica 10 bold", command=delete_records)
delete_btn.grid(row=0, column=1, padx=5, pady=5)

view_btn = Button(button_frame, text="Visualizar Cadastro", bg="black", fg="white", font="helvetica 10 bold", command=view_records)
view_btn.grid(row=0, column=2, padx=5, pady=5)

clear_btn = Button(button_frame, text="Limpar Cadastro", bg="maroon", fg="white", font="helvetica 10 bold", command=clear_screen)
clear_btn.grid(row=0, column=3, padx=5, pady=5)

exit_btn = Button(button_frame, text="Sair/Fechar", bg="teal", fg="white", font="helvetica 10 bold", command=confirmar_saida)
exit_btn.grid(row=0, column=4, padx=5, pady=5)

rodape_label = ttk.Label(root, text="Todos os direitos reservados !", font=("TkDefaultFont", 16), background="dark khaki")
rodape_label.grid(row=3, column=0, columnspan=7, pady=20)

root.mainloop()
