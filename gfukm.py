
import json
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

date = 0
temp = 0
weather = 0
osad = 0

window = tk.Tk()
window.title("Weather Diary")
window.geometry("700x700")

tk.Label(text="Дата(дд.мм.гг)", font=("Arial", 12)).pack(pady = 5)
date_entry = tk.Entry(width=20, font=("Arial", 12))
date_entry.pack(padx = 10, pady = 5)

tk.Label(text="Температура(число)", font=("Arial", 12)).pack(pady = 10)
temp_entry = tk.Entry(width=20, font=("Arial", 12))
temp_entry.pack(padx = 10, pady = 5)

tk.Label(text="Описание погоды", font=("Arial", 12)).pack(pady = 15)
weather_entry = tk.Entry(width=20, font=("Arial", 12))
weather_entry.pack(padx = 10, pady = 15)

tk.Label(text="Осадки (да/нет)", font=("Arial", 12)).pack(pady = 15)
osad_entry = tk.Entry(width=20, font=("Arial", 12))
osad_entry.pack(padx = 10, pady = 15)

def is_valid_date(date_str, date_format="%d.%m.%y"):
    try:
        datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False

def load_file(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                return []
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return []

def add_record():
    date = date_entry.get()
    temp = temp_entry.get()
    weather = weather_entry.get()
    osad = osad_entry.get()
    if not is_valid_date(date):
        messagebox.showerror("Ошибка, неверный формат даты")
        return
    if not temp.isdigit():
        messagebox.showerror("Ошибка, неверный формат температуры")
        return
    if len(weather) == 0:
        messagebox.showerror("Ошибка, введите описание погоды")
        retfurn
    if osad.lower() not in ["да", "нет"]:
        messagebox.showerror("Ошибка, введите да/нет")
        return
    new_entry = {"Дата": date, "Температура": temp, "Погода": weather, "Осадки": osad}
    data = load_file(".venv/weather.json")
    data.append(new_entry)
    with open(".venv/weather.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    messagebox.showinfo("Запись добавлена")
    clear_entries()

def clear_entries():
    temp_entry.delete(0, tk.END)
    weather_entry.delete(0, tk.END)
    osad_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)

def filter_record():
    filter_date = filter_date_entry.get()
    filter_temp = filter_temp_entry.get()

    data = load_file(".venv/weather.json")
    filtered = []

    if not isinstance(data, list):
        data = []

    for record in data:
        if filter_date:
            if record.get("Дата") != filter_date:
                continue

        if filter_temp:
            if not filter_temp.isdigit():
                messagebox.showerror("Ошибкаб введите число")
                return
        if record.get("Темпе") != int(filter_temp):
            continue

        filtered.append(record)

    result_text.delete("1.0", tk.END)

    if not filtered:
        result_text.insert(tk.END, "Записей нет")
    else:
        for r in filtered:
            result_text.insert("1.0", f"{r}\n")

tk.Button(text="Добавить запись",
          width=20,
          height=2,
          command=add_record).pack(pady = 10)

tk.Label(text="Фильтр по дате", font=("Arial", 10)).pack(pady = 5)
filter_date_entry = tk.Entry(window, width=20, font=("Arial", 12))
filter_date_entry.pack( pady = 5)

tk.Label(text="Фильтр по температуре", font=("Arial", 10)).pack(pady = 5)
filter_temp_entry = tk.Entry(window, width=20, font=("Arial", 12))
filter_temp_entry.pack( pady = 5)

tk.Button(text="Показать отфильтрованные записи", command=filter_record).pack(pady = 5)

result_text = tk.Text(window, height=10, width=50)
result_text.pack(pady = 10)

window.mainloop()
