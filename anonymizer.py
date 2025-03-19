import tkinter as tk
from tkinter import ttk, scrolledtext
from tkinter import filedialog, messagebox
import re
import nltk
from nltk.tokenize import word_tokenize


class AnonimizareNume:
    def __init__(self, root):
        try:
            icon_image = tk.PhotoImage(file="inf.png")
            root.iconphoto(False, icon_image)
        except Exception as e:
            print(f"Nu s-a putut încărca imaginea: {e}")

        # Încercare de a descărca resursele NLTK necesare
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')

        try:
            nltk.data.find('taggers/maxent_ne_chunker')
        except LookupError:
            nltk.download('maxent_ne_chunker')

        try:
            nltk.data.find('taggers/averaged_perceptron_tagger')
        except LookupError:
            nltk.download('averaged_perceptron_tagger')

        try:
            nltk.data.find('corpora/words')
        except LookupError:
            nltk.download('words')

        self.root = root
        self.root.title("Anonimizare Nume în Text")
        self.root.geometry("700x600")
        self.root.configure(bg="#f5f5f5")

        # Stilizare
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 11))
        self.style.configure('TLabel', font=('Arial', 11), background="#f5f5f5")
        self.style.configure('Header.TLabel', font=('Arial', 16, 'bold'), background="#f5f5f5")

        # Titlu
        self.header = ttk.Label(root, text="Anonimizare Nume în Text", style='Header.TLabel')
        self.header.pack(pady=15)

        # Frame principal
        self.main_frame = tk.Frame(root, bg="#f5f5f5")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Frame pentru opțiuni
        self.options_frame = tk.Frame(self.main_frame, bg="#f5f5f5")
        self.options_frame.pack(fill="x", pady=10)

        # Metodă de detecție
        self.method_label = ttk.Label(self.options_frame, text="Metodă de detecție:")
        self.method_label.pack(side=tk.LEFT, padx=(0, 10))

        self.method_var = tk.StringVar(value="toate")
        self.method_combo = ttk.Combobox(self.options_frame, textvariable=self.method_var,
                                         values=["majuscule", "minuscule", "toate"],
                                         width=10, state="readonly")
        self.method_combo.pack(side=tk.LEFT, padx=(0, 20))

        # String de înlocuire
        self.replace_label = ttk.Label(self.options_frame, text="Înlocuiește cu:")
        self.replace_label.pack(side=tk.LEFT, padx=(0, 10))

        self.replace_var = tk.StringVar(value="XXX")
        self.replace_entry = ttk.Entry(self.options_frame, textvariable=self.replace_var, width=10)
        self.replace_entry.pack(side=tk.LEFT)

        # Butoane pentru încărcare și salvare fișier
        self.file_frame = tk.Frame(self.main_frame, bg="#f5f5f5")
        self.file_frame.pack(fill="x", pady=10)

        self.load_btn = ttk.Button(self.file_frame, text="Încarcă fișier text", command=self.load_file)
        self.load_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.save_btn = ttk.Button(self.file_frame, text="Salvează rezultat", command=self.save_file)
        self.save_btn.pack(side=tk.LEFT)

        # Frame pentru text
        self.text_frame = tk.Frame(self.main_frame, bg="#f5f5f5")
        self.text_frame.pack(fill="both", expand=True, pady=10)

        # Text inițial
        self.input_label = ttk.Label(self.text_frame, text="Text inițial:")
        self.input_label.pack(anchor="w")

        self.input_text = scrolledtext.ScrolledText(self.text_frame, height=10,
                                                    width=80, font=('Consolas', 11))
        self.input_text.pack(fill="both", expand=True, pady=(0, 10))

        # Buton pentru anonimizare
        self.anon_btn = ttk.Button(self.text_frame, text="Anonimizează", command=self.anonymize_text)
        self.anon_btn.pack(pady=10)

        # Text rezultat
        self.output_label = ttk.Label(self.text_frame, text="Text anonimizat:")
        self.output_label.pack(anchor="w")

        self.output_text = scrolledtext.ScrolledText(self.text_frame, height=10,
                                                     width=80, font=('Consolas', 11))
        self.output_text.pack(fill="both", expand=True)

    def detect_names_uppercase(self, text):
        """Detectează nume proprii care încep cu majusculă"""
        words = text.split()
        potential_names = []

        for i, word in enumerate(words):
            # Verifică dacă cuvântul începe cu literă mare și nu este primul cuvânt din propoziție
            if word and word[0].isupper() and len(word) > 1:
                # Ignoră primul cuvânt din text sau primul cuvânt după punct, dacă e majuscul
                if i > 0 and not words[i - 1].endswith(('.', '!', '?', ':', ';')):
                    # Verifică să nu fie abreviere (majuscule multiple)
                    upper_count = sum(1 for c in word if c.isupper())
                    if upper_count == 1:  # Doar prima literă e majusculă
                        potential_names.append(word)

        return potential_names

    def detect_names_lowercase(self, text):
        """Detectează nume proprii care apar cu literă mică în text"""
        # Mai întâi găsim toate numele cu majuscule
        uppercase_names = self.detect_names_uppercase(text)

        # Apoi creăm o listă cu variantele lor cu literă mică
        lowercase_names = [name.lower() for name in uppercase_names]

        return lowercase_names

    def detect_names_all(self, text):
        """Detectează toate numele proprii, atât cu majuscule cât și cu minuscule"""
        # Obținem numele cu majuscule
        uppercase_names = self.detect_names_uppercase(text)

        # Obținem numele cu minuscule
        lowercase_names = self.detect_names_lowercase(text)

        # Combinăm listele
        all_names = uppercase_names + lowercase_names

        # Eliminăm duplicatele
        all_names = list(set(all_names))

        return all_names

    def detect_names_nltk(self, text):
        """Detectează nume proprii folosind NLTK"""
        tokens = word_tokenize(text)
        tagged = nltk.pos_tag(tokens)
        entities = nltk.chunk.ne_chunk(tagged)

        names = []
        for subtree in entities:
            if isinstance(subtree, nltk.tree.Tree) and subtree.label() == 'PERSON':
                name = ' '.join([leaf[0] for leaf in subtree.leaves()])
                names.append(name)
                # Adăugăm și varianta cu litere mici
                names.append(name.lower())

        # Eliminăm duplicatele
        names = list(set(names))
        return names

    def anonymize_text(self):
        """Anonimizează numele din text în funcție de metoda selectată"""
        text = self.input_text.get(1.0, tk.END)
        method = self.method_var.get()
        replacement = self.replace_var.get()

        if not text.strip():
            messagebox.showwarning("Avertisment", "Introduceți text pentru anonimizare!")
            return

        try:
            # Selectăm metoda de detectare în funcție de opțiunea aleasă
            if method == "majuscule":
                names = self.detect_names_uppercase(text)
                case_sensitive = True  # Înlocuim doar numele cu majuscule
            elif method == "minuscule":
                names = self.detect_names_lowercase(text)
                case_sensitive = True  # Înlocuim doar numele cu minuscule
            elif method == "toate":
                names = self.detect_names_all(text)
                case_sensitive = False  # Înlocuim toate variantele, case-insensitive
            else:  # nltk
                names = self.detect_names_nltk(text)
                case_sensitive = False  # Înlocuim toate variantele, case-insensitive

            # Sortează numele în ordine descrescătoare după lungime pentru a le înlocui corect
            names = sorted(names, key=len, reverse=True)

            # Anonimizează textul
            anonymized_text = text
            for name in names:
                if name.strip():  # Verifică să nu fie string gol
                    pattern = r'\b' + re.escape(name) + r'\b'

                    if case_sensitive:
                        # Înlocuiește exact cum este scris numele (case-sensitive)
                        anonymized_text = re.sub(pattern, replacement, anonymized_text)
                    else:
                        # Înlocuiește indiferent de majuscule/minuscule (case-insensitive)
                        anonymized_text = re.sub(pattern, replacement, anonymized_text, flags=re.IGNORECASE)

            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, anonymized_text)

            # Afișează numele detectate
            if names:
                messagebox.showinfo("Info", f"Nume detectate: {', '.join(names)}")
            else:
                messagebox.showinfo("Info", "Nu s-au detectat nume în text!")

        except Exception as e:
            messagebox.showerror("Eroare", f"A apărut o eroare: {str(e)}")

    def load_file(self):
        """Încarcă text dintr-un fișier"""
        file_path = filedialog.askopenfilename(
            title="Selectează fișier text",
            filetypes=(("Fișiere text", "*.txt"), ("Toate fișierele", "*.*"))
        )

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.input_text.delete(1.0, tk.END)
                    self.input_text.insert(tk.END, content)
            except Exception as e:
                messagebox.showerror("Eroare", f"Nu s-a putut citi fișierul: {e}")

    def save_file(self):
        """Salvează textul anonimizat într-un fișier"""
        anonymized_text = self.output_text.get(1.0, tk.END)

        if not anonymized_text.strip():
            messagebox.showwarning("Avertisment", "Nu există text anonimizat de salvat!")
            return

        file_path = filedialog.asksaveasfilename(
            title="Salvează textul anonimizat",
            defaultextension=".txt",
            filetypes=(("Fișiere text", "*.txt"), ("Toate fișierele", "*.*"))
        )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(anonymized_text)
                messagebox.showinfo("Succes", f"Textul a fost salvat în {file_path}")
            except Exception as e:
                messagebox.showerror("Eroare", f"Nu s-a putut salva fișierul: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = AnonimizareNume(root)
    root.mainloop()
