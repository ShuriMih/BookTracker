import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

books = []
genre_filter_values = set()

root = tk.Tk()
root.title("Book Tracker")
root.geometry("800x600")

tk.Label(root, text="Название книги:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
title_entry = tk.Entry(root, width=30)
title_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Автор:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
author_entry = tk.Entry(root, width=30)
author_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Жанр:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
genre_entry = tk.Entry(root, width=30)
genre_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Количество страниц:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
pages_entry = tk.Entry(root, width=30)
pages_entry.grid(row=3, column=1, padx=5, pady=5)

def add_book():
    title = title_entry.get().strip()
    author = author_entry.get().strip()
    genre = genre_entry.get().strip()
    pages = pages_entry.get().strip()

    if not title or not author or not genre:
        messagebox.showerror("Ошибка", "Все поля, кроме количества страниц, должны быть заполнены!")
        return

    if pages:
        if not pages.isdigit() or int(pages) <= 0:
            messagebox.showerror("Ошибка", "Количество страниц должно быть положительным числом!")
            return
    else:
        pages = "0"

    book = {
        "title": title,
        "author": author,
        "genre": genre,
        "pages": int(pages)
    }
    books.append(book)
    genre_filter_values.add(genre)

    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)
    pages_entry.delete(0, tk.END)

    display_books(books)
    update_genre_filter()
    save_books()

add_button = tk.Button(root, text="Добавить книгу", command=add_book)
add_button.grid(row=4, column=0, columnspan=2, pady=10)

tree = ttk.Treeview(root, columns=("Title", "Author", "Genre", "Pages"), show="headings")
tree.heading("Title", text="Название")
tree.heading("Author", text="Автор")
tree.heading("Genre", text="Жанр")
tree.heading("Pages", text="Страниц")
tree.column("Title", width=200)
tree.column("Author", width=150)
tree.column("Genre", width=120)
tree.column("Pages", width=80)
tree.grid(row=6, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

tk.Label(root, text="Фильтр по жанру:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
genre_filter = ttk.Combobox(root, state="readonly")
genre_filter.grid(row=5, column=1, padx=5, pady=5)

tk.Label(root, text="Страниц >:").grid(row=5, column=2, sticky="w", padx=5, pady=5)
pages_filter = tk.Entry(root, width=10)
pages_filter.grid(row=5, column=3, padx=5, pady=5)

def update_genre_filter():
    genre_filter['values'] = sorted(list(genre_filter_values))
    genre_filter.set('')

def apply_filters():
    selected_genre = genre_filter.get()
    pages_threshold = pages_filter.get().strip()

    filtered_books = []
    for book in books:
        genre_match = not selected_genre or book["genre"] == selected_genre
        pages_match = True

        if pages_threshold:
            try:
                pages_match = book["pages"] > int(pages_threshold)
            except ValueError:
                pages_match = False

        if genre_match and pages_match:
            filtered_books.append(book)

    display_books(filtered_books)

genre_filter.bind("<<ComboboxSelected>>", lambda e: apply_filters())
pages_filter.bind("<KeyRelease>", lambda e: apply_filters())

def clear_filter():
    genre_filter.set('')
    pages_filter.delete(0, tk.END)
    display_books(books)

clear_filter_button = tk.Button(root, text="Очистить фильтр", command=clear_filter)
clear_filter_button.grid(row=5, column=4, padx=5, pady=5)

def save_books():
    with open("books.json", "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=4)

def load_books():
    global books, genre_filter_values
    try:
        with open("books.json", "r", encoding="utf-8") as f:
            books = json.load(f)
        genre_filter_values = {book["genre"] for book in books}
        update_genre_filter()
        display_books(books)
    except FileNotFoundError:
        books = []
        genre_filter_values = set()
        display_books(books)

def display_books(book_list):
    for item in tree.get_children():
        tree.delete(item)

    for book in book_list:
        tree.insert("", "end", values=(
            book["title"],
            book["author"],
            book["genre"],
            book["pages"]
        ))

load_books()

root.mainloop()
