import os
import json

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

from main import Application as main_application


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("ULP sorter by molodost vnutri V1.2")
        self.geometry("400x900")
        
        self.processing_folder = ""
        self.results_folder = ""
        
        self.create_widgets()
        
        self.load_settings()

    def load_settings(self):
        if os.path.isfile('config.json'):
            with open('config.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            self.fields["parse_zapros"].set(data["parse_zapros"])
            self.fields["parse_email"].set(data["parse_email"])
            self.fields["parse_login"].set(data["parse_login"])
            self.fields["parse_number"].set(data["parse_number"])
            self.fields["parse_full"].set(data["parse_full"])
            self.fields["thread_auto"].set(data["thread_auto"])
            self.fields["threads"].insert(0, str(data["threads"]))
            self.fields["email_len"].insert(0, str(data.get("email_len", "")))
            self.fields["login_len"].insert(0, str(data.get("login_len", "")))
            self.fields["number_len"].insert(0, str(data.get("number_len", "")))
            self.fields["password_len"].insert(0, str(data.get("password_len", "")))
            self.results_folder = data["folder"]

    def create_widgets(self):
        self.fields = {}

        self.create_checkbox("parse_zapros", "Парсить запросы", False)
        self.create_checkbox("parse_email", "Парсить email", True)
        self.create_checkbox("parse_login", "Парсить login", True)
        self.create_checkbox("parse_number", "Парсить number", True)
        self.create_checkbox("parse_full", "Парсить строки полностью", False)
        
        self.create_checkbox("thread_auto", "Автоматический выбор кол-ва потоков", True)
        
        ttk.Label(self, text="Потоки:").pack(pady=5)
        self.fields["threads"] = tk.Entry(self)
        self.fields["threads"].pack(pady=5)
        
        self.create_length_field("email_len", "Длина email:")
        self.create_length_field("login_len", "Длина login:")
        self.create_length_field("number_len", "Длина number:")
        self.create_length_field("password_len", "Длина password:")
        
        ttk.Label(self, text="Папка для обработки:").pack(pady=5)
        self.fields["processing_folder"] = tk.Entry(self)
        self.fields["processing_folder"].insert(0, "Ну ты выбирай")
        self.fields["processing_folder"].pack(pady=5)

        self.select_processing_button = tk.Button(self, text="Выбрать папку", command=self.select_processing_folder)
        self.select_processing_button.pack(pady=10)
        
        ttk.Label(self, text="Папка для результатов:").pack(pady=5)
        self.fields["results_folder"] = tk.Entry(self)
        self.fields["results_folder"].pack(pady=5)

        self.fields["results_folder"].insert(0, self.results_folder if self.results_folder else "Result")
        
        self.save_button = tk.Button(self, text="Сохранить", command=self.save)
        self.save_button.pack(pady=20)

        self.start_button = tk.Button(self, text="Начать обработку", command=self.start)
        self.start_button.pack(pady=20)
        
    def create_checkbox(self, key, text, default):
        self.fields[key] = tk.BooleanVar(value=default)
        tk.Checkbutton(self, text=text, variable=self.fields[key]).pack(pady=5)
    
    def create_length_field(self, key, label_text):
        ttk.Label(self, text=label_text).pack(pady=5)
        self.fields[key] = tk.Entry(self)
        self.fields[key].pack(pady=5)
    
    def select_processing_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.fields["processing_folder"].delete(0, tk.END)
            self.fields["processing_folder"].insert(0, path)
            self.processing_folder = path
    
    def save(self):
        def parse_list(input_str):
            return list(map(int, input_str.strip("[]").split(',')))
    
        data = {
            "parse_zapros": self.fields["parse_zapros"].get(),
            "parse_email": self.fields["parse_email"].get(),
            "parse_login": self.fields["parse_login"].get(),
            "parse_number": self.fields["parse_number"].get(),
            "parse_full": self.fields["parse_full"].get(),
            "thread_auto": self.fields["thread_auto"].get(),
            "threads": int(self.fields["threads"].get()),
            "email_len": parse_list(self.fields["email_len"].get()),
            "login_len": parse_list(self.fields["login_len"].get()),
            "number_len": parse_list(self.fields["number_len"].get()),
            "password_len": parse_list(self.fields["password_len"].get()),
            "folder": self.fields["results_folder"].get()
        }
    
        json_config = json.dumps(data, indent=2, ensure_ascii=False)
        with open('config.json', 'w', encoding='utf-8') as file:
            file.write(json_config)
        messagebox.showinfo("Сохранение", "Настройки сохранены в config.json")
    
    def start(self):
        if not self.processing_folder:
            messagebox.showerror("Ошибка", "Выберите папку для обработки")
            return
        
        run = main_application(self.processing_folder).run()
        results = ''
        for res in run:
            results = results + f'{res}\n\n\n'
        messagebox.showinfo("Чек завершён", results)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
