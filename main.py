import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")
        self.entries = []
        self.load_data()
        self.create_widgets()

    def create_widgets(self):
        # Поля ввода
        tk.Label(self.root, text="Дата (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Температура (°C):").grid(row=1, column=0, padx=5, pady=5)
        self.temp_entry = tk.Entry(self.root)
        self.temp_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Описание погоды:").grid(row=2, column=0, padx=5, pady=5)
        self.desc_entry = tk.Entry(self.root)
        self.desc_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Осадки:").grid(row=3, column=0, padx=5, pady=5)
        self.precip_var = tk.BooleanVar()
        tk.Checkbutton(self.root, variable=self.precip_var).grid(row=3, column=1, padx=5, pady=5)

        # Кнопка добавления
        tk.Button(self.root, text="Добавить запись", command=self.add_entry).grid(row=4, column=0, columnspan=2, pady=10)

        # Таблица для отображения записей
        self.tree = ttk.Treeview(self.root, columns=("Date", "Temp", "Desc", "Precip"), show="headings")
        self.tree.heading("Date", text="Дата")
        self.tree.heading("Temp", text="Температура")
        self.tree.heading("Desc", text="Описание")
        self.tree.heading("Precip", text="Осадки")
        self.tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # Фильтры
        tk.Label(self.root, text="Фильтр по дате:").grid(row=6, column=0, padx=5, pady=5)
        self.filter_date_entry = tk.Entry(self.root)
        self.filter_date_entry.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Фильтр по температуре (>):").grid(row=7, column=0, padx=5, pady=5)
        self.filter_temp_entry = tk.Entry(self.root)
        self.filter_temp_entry.grid(row=7, column=1, padx=5, pady=5)

        tk.Button(self.root, text="Применить фильтры", command=self.apply_filters).grid(row=8, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Сбросить фильтры", command=self.reset_filters).grid(row=9, column=0, columnspan=2, pady=5)

        self.update_table()

    def validate_input(self):
        try:
            date = datetime.strptime(self.date_entry.get(), "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте YYYY-MM-DD.")
            return False

        try:
            temp = float(self.temp_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом.")
            return False

        if not self.desc_entry.get():
            messagebox.showerror("Ошибка", "Описание не может быть пустым.")
            return False

        return True

    def add_entry(self):
        if self.validate_input():
            entry = {
                "date": self.date_entry.get(),
                "temperature": float(self.temp_entry.get()),
                "description": self.desc_entry.get(),
                "precipitation": self.precip_var.get()
            }
            self.entries.append(entry)
            self.save_data()
            self.update_table()
            self.clear_inputs()

    def clear_inputs(self):
        self.date_entry.delete(0, tk.END)
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.precip_var.set(False)

    def update_table(self, entries=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        entries = entries or self.entries
        for entry in entries:
            self.tree.insert("", "end", values=(
                entry["date"],
                entry["temperature"],
                entry["description"],
                "Да" if entry["precipitation"] else "Нет"
            ))

    def apply_filters(self):
        filtered = self.entries
        date_filter = self.filter_date_entry.get()
        if date_filter:
            filtered = [e for e in filtered if e["date"] == date_filter]
        temp_filter = self.filter_temp_entry.get()
        if temp_filter:
            try:
                temp_filter = float(temp_filter)
                filtered = [e for e in filtered if e["temperature"] > temp_filter]
            except ValueError:
                messagebox.showerror("Ошибка", "Температура фильтра должна быть числом.")
                return
        self.update_table(filtered)

    def reset_filters(self):
        self.filter_date_entry.delete(0, tk.END)
        self.filter_temp_entry.delete(0, tk.END)
        self.update_table()

    def save_data(self):
        with open("weather_data.json", "w", encoding="utf-8") as f:
            json.dump(self.entries, f, ensure_ascii=False, indent=4)

    def load_data(self):
        try:
            with open("weather_data.json", "r", encoding="utf-8") as f:
                self.entries = json.load(f)
        except FileNotFoundError:
            self.entries = []

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()
