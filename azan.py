import tkinter as tk
from tkinter import ttk, messagebox
import random

class FlashAnzanPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Flash Anzan Pro - Mental Training")
        self.root.geometry("900x750")
        self.root.minsize(800, 700) # Tamanho mínimo para não quebrar o layout
        
        # Paleta de cores Profissional (Dark Mode - Slate Theme)
        self.colors = {
            "bg": "#0f172a",          # Fundo geral (Escuro)
            "card": "#1e293b",        # Fundo dos painéis
            "text": "#f8fafc",        # Texto principal (Claro)
            "text_muted": "#94a3b8",  # Texto secundário
            "primary": "#3b82f6",     # Azul principal (Botões de destaque)
            "primary_hover": "#2563eb",
            "accent": "#0ea5e9",      # Azul ciano para o texto do visor
            "success": "#22c55e",     # Verde para acertos
            "danger": "#ef4444",      # Vermelho para erros
            "display_bg": "#020617",  # Fundo ultra escuro pro visor
            "input_bg": "#334155"     # Fundo da caixa de texto
        }

        self.root.configure(bg=self.colors["bg"])
        self.is_fullscreen = False

        # Variáveis de estado
        self.numbers = []
        self.answer = 0
        self.index = 0
        self.score = 0
        self.errors = 0
        self.rounds = 0
        self.active = False

        # Atalhos de teclado para tela cheia
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)

        self.setup_styles()
        self.create_interface()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam") 

        # Configurações globais
        style.configure(".", font=("Segoe UI", 11), background=self.colors["bg"], foreground=self.colors["text"])
        
        # Estilos dos Cards (Painéis)
        style.configure("Card.TFrame", background=self.colors["card"])
        style.configure("Card.TLabel", background=self.colors["card"], foreground=self.colors["text"], font=("Segoe UI", 11))
        style.configure("Card.TLabelframe", background=self.colors["card"], bordercolor=self.colors["text_muted"])
        style.configure("Card.TLabelframe.Label", background=self.colors["card"], foreground=self.colors["primary"], font=("Segoe UI", 11, "bold"))

        # Botão Primário (Iniciar)
        style.configure("Primary.TButton", font=("Segoe UI", 12, "bold"), 
                        background=self.colors["primary"], foreground="white", borderwidth=0, focuscolor="")
        style.map("Primary.TButton", background=[("active", self.colors["primary_hover"])])

        # Botão Secundário (Tela Cheia / Confirmar)
        style.configure("Secondary.TButton", font=("Segoe UI", 10, "bold"), 
                        background=self.colors["card"], foreground=self.colors["text"], borderwidth=1, bordercolor=self.colors["text_muted"], focuscolor="")
        style.map("Secondary.TButton", background=[("active", self.colors["input_bg"])])

        # Inputs (Spinbox e Combobox)
        style.configure("TSpinbox", fieldbackground=self.colors["input_bg"], foreground=self.colors["text"], borderwidth=0, arrowcolor=self.colors["text"])
        style.configure("TCombobox", fieldbackground=self.colors["input_bg"], foreground=self.colors["text"], borderwidth=0, arrowcolor=self.colors["text"])

    def create_interface(self):
        # Container principal expansível (Mantém tudo centralizado em Tela Cheia)
        self.main_container = tk.Frame(self.root, bg=self.colors["bg"])
        self.main_container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.95)

        # 1. CABEÇALHO
        header = tk.Frame(self.main_container, bg=self.colors["bg"])
        header.pack(fill="x", pady=(0, 20))
        
        title_frame = tk.Frame(header, bg=self.colors["bg"])
        title_frame.pack(side="left")
        
        tk.Label(title_frame, text="⚡ FLASH ANZAN", font=("Segoe UI", 24, "bold"), bg=self.colors["bg"], fg=self.colors["text"]).pack(anchor="w")
        tk.Label(title_frame, text="Professional Mental Soroban Training", font=("Segoe UI", 11), bg=self.colors["bg"], fg=self.colors["text_muted"]).pack(anchor="w")

        self.fullscreen_btn = ttk.Button(header, text="⛶ Tela Cheia (F11)", style="Secondary.TButton", command=self.toggle_fullscreen)
        self.fullscreen_btn.pack(side="right", pady=10)

        # 2. CONFIGURAÇÕES
        config_frame = ttk.LabelFrame(self.main_container, text=" Parâmetros do Treino ", style="Card.TLabelframe", padding=20)
        config_frame.pack(fill="x", pady=10)

        self.quantity = tk.IntVar(value=10)
        self.digits = tk.IntVar(value=2)
        self.flash_time = tk.IntVar(value=500)
        self.interval = tk.IntVar(value=250)
        self.operation = tk.StringVar(value="Soma")

        # Layout em Grid inteligente de 4 colunas
        self.add_setting(config_frame, "Qtd. de Números:", self.quantity, 0, 0)
        self.add_setting(config_frame, "Qtd. de Dígitos:", self.digits, 0, 2)
        self.add_setting(config_frame, "Exposição (ms):", self.flash_time, 1, 0)
        self.add_setting(config_frame, "Intervalo (ms):", self.interval, 1, 2)

        ttk.Label(config_frame, text="Modo de Operação:", style="Card.TLabel").grid(row=2, column=0, sticky="w", pady=(15, 0))
        combo = ttk.Combobox(config_frame, textvariable=self.operation, values=["Soma", "Soma e Subtração"], state="readonly", width=18, font=("Segoe UI", 11))
        combo.grid(row=2, column=1, columnspan=3, sticky="w", padx=10, pady=(15, 0))

        # 3. VISOR DIGITAL (Área de Exibição)
        self.display_frame = tk.Frame(self.main_container, bg=self.colors["display_bg"], bd=2, relief="flat")
        self.display_frame.pack(fill="both", expand=True, pady=20)
        
        # Borda sutil no visor
        self.display_frame.config(highlightbackground=self.colors["primary"], highlightcolor=self.colors["primary"], highlightthickness=1)

        self.display = tk.Label(self.display_frame, text="PRONTO?", 
                                font=("Consolas", 65, "bold"), 
                                bg=self.colors["display_bg"], 
                                fg=self.colors["text_muted"])
        self.display.place(relx=0.5, rely=0.5, anchor="center")

        # 4. CONTROLES E RESPOSTA
        action_frame = tk.Frame(self.main_container, bg=self.colors["bg"])
        action_frame.pack(fill="x", pady=10)

        self.start_button = tk.Button(action_frame, text="INICIAR TREINAMENTO", font=("Segoe UI", 14, "bold"), 
                                      bg=self.colors["primary"], fg="white", activebackground=self.colors["primary_hover"], activeforeground="white",
                                      bd=0, cursor="hand2", command=self.start_training, pady=12)
        self.start_button.pack(fill="x", pady=(0, 20))

        response_frame = tk.Frame(action_frame, bg=self.colors["bg"])
        response_frame.pack()

        tk.Label(response_frame, text="Sua Resposta:", font=("Segoe UI", 14, "bold"), bg=self.colors["bg"], fg=self.colors["text_muted"]).pack(side="left", padx=10)
        
        self.answer_entry = tk.Entry(response_frame, font=("Consolas", 22, "bold"), justify="center", width=12, 
                                     bg=self.colors["input_bg"], fg=self.colors["text"], bd=0, insertbackground=self.colors["primary"])
        self.answer_entry.pack(side="left", padx=10, ipady=8)
        self.answer_entry.bind("<Return>", lambda event: self.check_answer())
        self.answer_entry.config(state="disabled")

        self.submit_button = tk.Button(response_frame, text="CONFIRMAR", font=("Segoe UI", 12, "bold"), 
                                       bg=self.colors["card"], fg=self.colors["text"], bd=0, cursor="hand2",
                                       command=self.check_answer, padx=20, pady=10)
        self.submit_button.pack(side="left", padx=10)
        self.submit_button.config(state="disabled")

        # 5. RESULTADOS E RODAPÉ
        self.result_label = tk.Label(self.main_container, text="", font=("Segoe UI", 14, "bold"), bg=self.colors["bg"])
        self.result_label.pack(pady=5)

        self.stats_label = tk.Label(self.main_container, text="Rodadas: 0   |   Acertos: 0   |   Erros: 0   |   Precisão: 0.0%", 
                                     font=("Segoe UI", 11), bg=self.colors["bg"], fg=self.colors["text_muted"])
        self.stats_label.pack(side="bottom", pady=10)

    def add_setting(self, parent, label, variable, row, col):
        ttk.Label(parent, text=label, style="Card.TLabel").grid(row=row, column=col, sticky="e", pady=10, padx=(15, 5))
        spin = ttk.Spinbox(parent, from_=1, to=10000, textvariable=variable, width=10, font=("Segoe UI", 11), style="TSpinbox")
        spin.grid(row=row, column=col+1, sticky="w", padx=(0, 20))

    # --- Lógica de Tela Cheia ---
    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes("-fullscreen", self.is_fullscreen)
        if self.is_fullscreen:
            self.fullscreen_btn.config(text="✖ Sair Tela Cheia (ESC)")
        else:
            self.fullscreen_btn.config(text="⛶ Tela Cheia (F11)")

    def exit_fullscreen(self, event=None):
        self.is_fullscreen = False
        self.root.attributes("-fullscreen", False)
        self.fullscreen_btn.config(text="⛶ Tela Cheia (F11)")

    # --- Lógica do Treinamento ---
    def generate_numbers(self):
        quantity = self.quantity.get()
        digits = self.digits.get()
        minimum = 10 ** (digits - 1) if digits > 1 else 1
        maximum = (10 ** digits) - 1

        numbers = []
        total = 0

        for i in range(quantity):
            number = random.randint(minimum, maximum)
            operation = "+" if i == 0 or self.operation.get() == "Soma" else random.choice(["+", "-"])
            
            if operation == "-" and (total < minimum or total - number < 0):
                operation = "+"

            if operation == "+":
                total += number
                numbers.append(number)
            else:
                total -= number
                numbers.append(-number)

        self.answer = total
        self.numbers = numbers

    def start_training(self):
        try:
            if not 1 <= self.quantity.get() <= 500: raise ValueError("Use entre 1 e 500 números.")
            if not 1 <= self.digits.get() <= 8: raise ValueError("Use entre 1 e 8 dígitos.")
            if self.flash_time.get() < 50 or self.interval.get() < 0: raise ValueError("Tempos muito curtos.")
        except tk.TclError:
            messagebox.showerror("Erro", "Valores numéricos inválidos.")
            return
        except ValueError as error:
            messagebox.showerror("Configuração Inválida", str(error))
            return

        self.active = True
        self.index = 0
        self.result_label.config(text="")
        
        self.answer_entry.config(state="normal")
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.config(state="disabled")
        
        self.submit_button.config(state="disabled", bg=self.colors["bg"])
        self.start_button.config(state="disabled", bg=self.colors["card"], text="TREINAMENTO EM ANDAMENTO...")

        self.generate_numbers()
        
        self.display.config(text="PREPARE-SE!", fg=self.colors["text_muted"])
        self.root.after(1000, self.show_next_number)

    def show_next_number(self):
        if self.index >= len(self.numbers):
            self.display.config(text="CALCULE!", fg=self.colors["primary"])
            self.answer_entry.config(state="normal")
            self.submit_button.config(state="normal", bg=self.colors["primary"], fg="white")
            self.answer_entry.focus_set()
            return

        number = self.numbers[self.index]
        self.display.config(text=f"- {abs(number)}" if number < 0 else str(number), fg=self.colors["accent"])

        self.index += 1
        self.root.after(self.flash_time.get(), self.hide_number)

    def hide_number(self):
        self.display.config(text="")
        self.root.after(self.interval.get(), self.show_next_number)

    def check_answer(self):
        if not self.active: return
        user_input = self.answer_entry.get().strip()
        if not user_input: return

        try:
            user_answer = int(user_input)
        except ValueError:
            messagebox.showwarning("Atenção", "Digite apenas números inteiros.")
            self.answer_entry.delete(0, tk.END)
            return

        self.rounds += 1
        if user_answer == self.answer:
            self.score += 1
            self.result_label.config(text=f"✓ CORRETO! O resultado é {self.answer}", fg=self.colors["success"])
        else:
            self.errors += 1
            self.result_label.config(text=f"✗ INCORRETO. Você digitou {user_answer}, o correto era {self.answer}", fg=self.colors["danger"])

        precision = (self.score / self.rounds) * 100
        self.stats_label.config(text=f"Rodadas: {self.rounds}   |   Acertos: {self.score}   |   Erros: {self.errors}   |   Precisão: {precision:.1f}%")

        self.display.config(text="FIM DA RODADA", fg=self.colors["text_muted"])
        self.reset_ui()

    def reset_ui(self):
        self.active = False
        self.answer_entry.config(state="disabled")
        self.submit_button.config(state="disabled", bg=self.colors["card"], fg=self.colors["text"])
        self.start_button.config(state="normal", bg=self.colors["primary"], text="INICIAR TREINAMENTO")
        self.start_button.focus_set()

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashAnzanPro(root)
    root.mainloop()
