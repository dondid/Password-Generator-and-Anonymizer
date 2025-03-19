import random
import string
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class GeneratorParole:
    def __init__(self, root):
        try:
            icon_image = tk.PhotoImage(file="inf.png")
            root.iconphoto(False, icon_image)
        except Exception as e:
            print(f"Nu s-a putut încărca imaginea: {e}")

        self.root = root
        self.root.title("Generator de Parole")
        self.root.geometry("600x700")  # Am mărit dimensiunea ferestrei
        self.root.resizable(True, True)  # Am permis redimensionarea
        self.root.configure(bg="#f0f0f0")

        # Stilizare
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 12))
        self.style.configure('TLabel', font=('Arial', 12), background="#f0f0f0")
        self.style.configure('Header.TLabel', font=('Arial', 18, 'bold'), background="#f0f0f0")
        self.style.configure('Subheader.TLabel', font=('Arial', 14, 'bold'), background="#f0f0f0")

        # Titlu principal
        self.header = ttk.Label(root, text="Generator de Parole Securizate", style='Header.TLabel')
        self.header.pack(pady=15)

        # Notebook pentru tab-uri
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)

        # Tab pentru versiunea inițială (fixă)
        self.tab_fixed = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_fixed, text="Versiune standard (12 caractere)")

        # Tab pentru versiunea personalizată
        self.tab_custom = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_custom, text="Versiune personalizată")

        # Configurare tab versiune fixă
        self.setup_fixed_tab()

        # Configurare tab versiune personalizată
        self.setup_custom_tab()

    def setup_fixed_tab(self):
        # Subtitlu
        self.fixed_title = ttk.Label(self.tab_fixed, text="Generator Standard", style='Subheader.TLabel')
        self.fixed_title.pack(pady=10)

        # Frame pentru setări
        self.fixed_settings_frame = ttk.Frame(self.tab_fixed)
        self.fixed_settings_frame.pack(fill="both", padx=20)

        # Informații despre formatul parolei
        self.fixed_info_label = ttk.Label(self.fixed_settings_frame,
                                          text="Formatul parolei (12 caractere):\n"
                                               "• Primele 3 caractere: cifre\n"
                                               "• Următoarele 3 caractere: semne de punctuație\n"
                                               "• Următoarele 3 caractere: majuscule\n"
                                               "• Ultimele 3 caractere: minuscule",
                                          justify=tk.LEFT)
        self.fixed_info_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=10)

        # Număr parole
        self.fixed_count_label = ttk.Label(self.fixed_settings_frame, text="Număr de parole:")
        self.fixed_count_label.grid(row=1, column=0, sticky="w", pady=5)

        self.fixed_count_var = tk.StringVar(value="1")
        self.fixed_count_spin = ttk.Spinbox(self.fixed_settings_frame, from_=1, to=20,
                                            textvariable=self.fixed_count_var, width=5)
        self.fixed_count_spin.grid(row=1, column=1, sticky="w", pady=5)

        # Buton pentru generare
        self.fixed_generate_btn = ttk.Button(self.tab_fixed, text="Generează Parole",
                                             command=self.generate_fixed_passwords)
        self.fixed_generate_btn.pack(pady=15)

        # Rezultate
        self.fixed_result_frame = tk.Frame(self.tab_fixed, bg="white", bd=1, relief=tk.SOLID)
        self.fixed_result_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.fixed_result_label = ttk.Label(self.fixed_result_frame, text="Parolele generate vor apărea aici:",
                                            background="white")
        self.fixed_result_label.pack(anchor="w", padx=10, pady=10)

        # Am mărit înălțimea textului și am adăugat scroll bar
        self.fixed_result_text = tk.Text(self.fixed_result_frame, height=10, width=45, font=('Consolas', 12))
        self.fixed_result_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Adăugare scrollbar
        self.fixed_scrollbar = ttk.Scrollbar(self.fixed_result_text, command=self.fixed_result_text.yview)
        self.fixed_result_text.configure(yscrollcommand=self.fixed_scrollbar.set)
        self.fixed_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Buton de copiere
        self.fixed_copy_btn = ttk.Button(self.tab_fixed, text="Copiază în clipboard",
                                         command=lambda: self.copy_to_clipboard(self.fixed_result_text))
        self.fixed_copy_btn.pack(pady=10)

    def setup_custom_tab(self):
        # Subtitlu
        self.custom_title = ttk.Label(self.tab_custom, text="Generator Personalizat", style='Subheader.TLabel')
        self.custom_title.pack(pady=10)

        # Frame pentru setări
        self.custom_settings_frame = ttk.Frame(self.tab_custom)
        self.custom_settings_frame.pack(fill="both", padx=20)

        # Informații despre personalizarea parolei
        self.custom_info_label = ttk.Label(self.custom_settings_frame,
                                           text="Personalizează numărul de caractere pentru fiecare tip:",
                                           justify=tk.LEFT)
        self.custom_info_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=10)

        # Setări pentru fiecare tip de caracter
        self.digit_label = ttk.Label(self.custom_settings_frame, text="Cifre:")
        self.digit_label.grid(row=1, column=0, sticky="w", pady=5)
        self.digit_var = tk.StringVar(value="3")
        self.digit_spin = ttk.Spinbox(self.custom_settings_frame, from_=0, to=10, textvariable=self.digit_var, width=5)
        self.digit_spin.grid(row=1, column=1, sticky="w", pady=5)

        self.punct_label = ttk.Label(self.custom_settings_frame, text="Semne de punctuație:")
        self.punct_label.grid(row=2, column=0, sticky="w", pady=5)
        self.punct_var = tk.StringVar(value="3")
        self.punct_spin = ttk.Spinbox(self.custom_settings_frame, from_=0, to=10, textvariable=self.punct_var, width=5)
        self.punct_spin.grid(row=2, column=1, sticky="w", pady=5)

        self.upper_label = ttk.Label(self.custom_settings_frame, text="Majuscule:")
        self.upper_label.grid(row=3, column=0, sticky="w", pady=5)
        self.upper_var = tk.StringVar(value="3")
        self.upper_spin = ttk.Spinbox(self.custom_settings_frame, from_=0, to=10, textvariable=self.upper_var, width=5)
        self.upper_spin.grid(row=3, column=1, sticky="w", pady=5)

        self.lower_label = ttk.Label(self.custom_settings_frame, text="Minuscule:")
        self.lower_label.grid(row=4, column=0, sticky="w", pady=5)
        self.lower_var = tk.StringVar(value="3")
        self.lower_spin = ttk.Spinbox(self.custom_settings_frame, from_=0, to=10, textvariable=self.lower_var, width=5)
        self.lower_spin.grid(row=4, column=1, sticky="w", pady=5)

        # Amestecă caracterele
        self.shuffle_var = tk.BooleanVar(value=True)
        self.shuffle_check = ttk.Checkbutton(self.custom_settings_frame, text="Amestecă caracterele",
                                             variable=self.shuffle_var)
        self.shuffle_check.grid(row=5, column=0, columnspan=2, sticky="w", pady=5)

        # Număr parole
        self.custom_count_label = ttk.Label(self.custom_settings_frame, text="Număr de parole:")
        self.custom_count_label.grid(row=6, column=0, sticky="w", pady=5)
        self.custom_count_var = tk.StringVar(value="1")
        self.custom_count_spin = ttk.Spinbox(self.custom_settings_frame, from_=1, to=20,
                                             textvariable=self.custom_count_var, width=5)
        self.custom_count_spin.grid(row=6, column=1, sticky="w", pady=5)

        # Buton pentru generare
        self.custom_generate_btn = ttk.Button(self.tab_custom, text="Generează Parole",
                                              command=self.generate_custom_passwords)
        self.custom_generate_btn.pack(pady=15)

        # Rezultate
        self.custom_result_frame = tk.Frame(self.tab_custom, bg="white", bd=1, relief=tk.SOLID)
        self.custom_result_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.custom_result_label = ttk.Label(self.custom_result_frame, text="Parolele generate vor apărea aici:",
                                             background="white")
        self.custom_result_label.pack(anchor="w", padx=10, pady=10)

        # Am mărit înălțimea textului și am adăugat scroll bar
        self.custom_result_text = tk.Text(self.custom_result_frame, height=10, width=45, font=('Consolas', 12))
        self.custom_result_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Adăugare scrollbar
        self.custom_scrollbar = ttk.Scrollbar(self.custom_result_text, command=self.custom_result_text.yview)
        self.custom_result_text.configure(yscrollcommand=self.custom_scrollbar.set)
        self.custom_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Buton de copiere
        self.custom_copy_btn = ttk.Button(self.tab_custom, text="Copiază în clipboard",
                                          command=lambda: self.copy_to_clipboard(self.custom_result_text))
        self.custom_copy_btn.pack(pady=10)

    def generate_fixed_password(self):
        # Primele 3 caractere: cifre
        digits = ''.join(random.choices(string.digits, k=3))

        # Următoarele 3 caractere: semne de punctuație
        punctuation = ''.join(random.choices(string.punctuation, k=3))

        # Următoarele 3 caractere: majuscule
        uppercase = ''.join(random.choices(string.ascii_uppercase, k=3))

        # Ultimele 3 caractere: minuscule
        lowercase = ''.join(random.choices(string.ascii_lowercase, k=3))

        # Combinarea tuturor părților
        password = digits + punctuation + uppercase + lowercase

        return password

    def generate_custom_password(self):
        # Obținem numărul de caractere pentru fiecare tip
        digits_count = int(self.digit_var.get())
        punct_count = int(self.punct_var.get())
        upper_count = int(self.upper_var.get())
        lower_count = int(self.lower_var.get())

        # Verificăm dacă avem cel puțin un caracter
        if digits_count + punct_count + upper_count + lower_count == 0:
            messagebox.showerror("Eroare", "Trebuie să selectați cel puțin un caracter!")
            return None

        # Generăm fiecare parte a parolei
        digits = ''.join(random.choices(string.digits, k=digits_count))
        punctuation = ''.join(random.choices(string.punctuation, k=punct_count))
        uppercase = ''.join(random.choices(string.ascii_uppercase, k=upper_count))
        lowercase = ''.join(random.choices(string.ascii_lowercase, k=lower_count))

        # Combinăm părțile
        password = digits + punctuation + uppercase + lowercase

        # Amestecăm caracterele dacă este activată opțiunea
        if self.shuffle_var.get():
            password_list = list(password)
            random.shuffle(password_list)
            password = ''.join(password_list)

        return password

    def generate_fixed_passwords(self):
        try:
            count = int(self.fixed_count_var.get())
            if count < 1 or count > 20:
                raise ValueError("Numărul de parole trebuie să fie între 1 și 20")

            self.fixed_result_text.delete(1.0, tk.END)

            for i in range(count):
                password = self.generate_fixed_password()
                self.fixed_result_text.insert(tk.END, f"{password}\n")

        except ValueError as e:
            messagebox.showerror("Eroare", str(e))

    def generate_custom_passwords(self):
        try:
            count = int(self.custom_count_var.get())
            if count < 1 or count > 20:
                raise ValueError("Numărul de parole trebuie să fie între 1 și 20")

            self.custom_result_text.delete(1.0, tk.END)

            for i in range(count):
                password = self.generate_custom_password()
                if password:
                    self.custom_result_text.insert(tk.END, f"{password}\n")

        except ValueError as e:
            messagebox.showerror("Eroare", str(e))

    def copy_to_clipboard(self, text_widget):
        passwords = text_widget.get(1.0, tk.END).strip()
        if passwords:
            self.root.clipboard_clear()
            self.root.clipboard_append(passwords)
            messagebox.showinfo("Info", "Parole copiate în clipboard!")
        else:
            messagebox.showwarning("Avertisment", "Nu există parole pentru copiere!")


if __name__ == "__main__":
    root = tk.Tk()
    app = GeneratorParole(root)
    root.mainloop()
