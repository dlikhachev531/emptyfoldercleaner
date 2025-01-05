import os
import sys
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

# Функция для удаления пустых папок или по условиям

def delete_empty_folders(folder_path, size_limit=0, file_type=None):
    deleted_count = 0
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            # Проверка размера папки
            total_size = sum(os.path.getsize(os.path.join(dir_path, f)) for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)))
            # Проверка типа файла
            contains_file_type = any(f.endswith(file_type) for f in os.listdir(dir_path)) if file_type else False
            # Условие удаления
            if (not os.listdir(dir_path)) or (size_limit > 0 and total_size < size_limit) or (file_type and contains_file_type):
                shutil.rmtree(dir_path)
                deleted_count += 1
                print(f"Удалена папка: {dir_path}")
    return deleted_count

# Функция для GUI

def open_folder_dialog():
    folder_selected = filedialog.askdirectory()
    folder_path_var.set(folder_selected)

def execute_cleanup():
    folder = folder_path_var.get()
    size_limit = int(size_limit_var.get()) * 1024  # KB to Bytes
    file_type = file_type_var.get()

    if not folder:
        messagebox.showerror("Ошибка", "Выберите папку")
        return

    if not os.path.exists(folder):
        messagebox.showerror("Ошибка", "Папка не найдена")
        return

    deleted = delete_empty_folders(folder, size_limit, file_type)
    messagebox.showinfo("Готово", f"Удалено {deleted} папок.")

# GUI интерфейс

root = tk.Tk()
root.title("Likhachvev folder cleaner v1.05.01.2024")

# Установка окна по центру экрана
root.update_idletasks()
width = 400
height = 200
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f"{width}x{height}+{x}+{y}")

folder_path_var = tk.StringVar()
size_limit_var = tk.StringVar(value="0")
file_type_var = tk.StringVar()

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="Выберите папку:").grid(row=0, column=0)
entry_folder = tk.Entry(frame, textvariable=folder_path_var, width=40)
entry_folder.grid(row=0, column=1)
tk.Button(frame, text="Обзор", command=open_folder_dialog).grid(row=0, column=2)

tk.Label(frame, text="Лимит размера (КБ):").grid(row=1, column=0)
tk.Entry(frame, textvariable=size_limit_var).grid(row=1, column=1)

tk.Label(frame, text="Тип файла (например, .nfo):").grid(row=2, column=0)
tk.Entry(frame, textvariable=file_type_var).grid(row=2, column=1)

tk.Button(frame, text="Удалить", command=execute_cleanup).grid(row=3, column=0, columnspan=3, pady=10)

root.mainloop()
