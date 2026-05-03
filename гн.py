
import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

HISTORY_FILE = "history.json"
TASKS_FILE = "tasks.json"


def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return [
            {"task": "Прочитать статью", "type": "учёба"},
            {"task": "Сделать зарядку", "type": "спорт"},
            {"task": "Написать письмо", "type": "работа"},
            {"task": "Погулять на свежем воздухе", "type": "спорт"},
            {"task": "Изучить новую тему", "type": "учёба"},
        ]


tasks = load_tasks()

if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        history = json.load(f)
else:
    history = []

root = tk.Tk()
root.title("Random Task Generator")
root.geometry("500x700")

filter_var = tk.StringVar()
filter_var.set("Все")
types = ["Все", "учёба", "спорт", "работа"]
ttk.Label(root, text="Фильтр по типу:").pack(pady=5)
filter_combo = ttk.Combobox(root, values=types, textvariable=filter_var, state="readonly")
filter_combo.pack()

history_text = tk.Text(root, height=15, width=60)
history_text.pack(pady=10)


def save_history():
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)


def save_tasks():
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)


def update_history_display():
    history_text.delete("1.0", tk.END)
    current_filter = filter_var.get()
    for item in history:
        if current_filter != "Все" and item['type'] != current_filter:
            continue
        history_text.insert(tk.END, f"{item['task']} ({item['type']})\n")


def generate_task():
    filtered_tasks = tasks
    current_filter = filter_var.get()
    if current_filter != "Все":
        filtered_tasks = [t for t in tasks if t['type'] == current_filter]
    if not filtered_tasks:
        messagebox.showinfo("Информация", "Нет задач для выбранного фильтра")
        return
    selected = random.choice(filtered_tasks)
    history.append(selected)
    save_history()
    update_history_display()


# Ввод задачи
ttk.Label(root, text="Добавить новую задачу").pack(pady=5)
task_entry = ttk.Entry(root, width=40)
task_entry.pack(pady=5)

type_var = tk.StringVar()
type_var.set("учёба")
ttk.Label(root, text="Тип задачи:").pack()
type_combo = ttk.Combobox(root, values=["учёба", "спорт", "работа"], textvariable=type_var, state="readonly")
type_combo.pack(pady=5)


def add_task():
    task_name = task_entry.get().strip()
    task_type = type_var.get()
    if not task_name:
        messagebox.showerror("Ошибка", "Пожалуйста, введите название задачи")
        return
    new_task = {"task": task_name, "type": task_type}
    tasks.append(new_task)

    # Добавление новой задачи в историю
    history.append(new_task)

    save_tasks()  # Сохраняем список задач
    save_history()  # Сохраняем историю
    messagebox.showinfo("Успех", "Задача добавлена")
    task_entry.delete(0, tk.END)
    filter_var.set("Все")
    update_history_display()


ttk.Button(root, text="Добавить задачу", command=add_task).pack(pady=5)
ttk.Button(root, text="Сгенерировать задачу", command=generate_task).pack(pady=10)


def on_filter_change(event):
    update_history_display()


filter_combo.bind("<<ComboboxSelected>>", on_filter_change)

update_history_display()

root.mainloop()
