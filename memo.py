import tkinter as tk
from tkinter import ttk, messagebox
import random

class MemoryPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Pro - Number Span Training")
        self.root.geometry("900x750")
        self.root.minsize(800, 700)
        
        # Paleta de cores Profissional (Dark Mode - Slate Theme)
        self.colors = {
            "bg": "#0f172a",          # Fundo geral (Escuro)
            "card": "#1e293b",        # Fundo dos painéis
            "text": "#f8fafc",        # Texto principal (Claro)
            "text_muted": "#94a3b8",  # Texto secundário
            "primary": "#8b5cf6",     # Roxo principal (Foco mental)
            "primary_hover": "#7c3aed",
            "accent": "#c084fc",      # Roxo claro para os números
            "success": "#22c55e",     # Verde para acertos
            "danger": "#ef4444",      # Vermelho para erros
            "display_bg": "#020617",  # Fundo ultra escuro pro visor
            "input_bg": "#334155"     # Fundo da caixa de texto
        }

        self.root.configure(bg=self.colors["bg"])
        self.is_fullscreen = False

        # Variáveis de estado
        self.current_sequence = ""
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

        # Inputs (Spinbox)
        style.configure("TSpinbox", fieldbackground=self.colors["input_bg"], foreground=self.colors["text"], borderwidth=0, arrowcolor=self.colors["text"])

    def create_interface(self):
        # Container principal expansível
        self.main_container = tk.Frame(self.root, bg=self.colors["bg"])
        self.main_container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.95)

        # 1. CABEÇALHO
        header = tk.Frame(self.main_container, bg=self.colors["bg"])
        header.pack(fill="x", pady=(0, 20))
        
        title_frame = tk.Frame(header, bg=self.colors["bg"])
        title_frame.pack(side="left")
        
        tk.Label(title_frame, text="🧠 MEMORY PRO", font=("Segoe UI", 24, "bold"), bg=self.colors["bg"], fg=self.colors["text"]).pack(anchor="w")
        tk.Label(title_frame, text="Short-Term Memory & Number Span Training", font=("Segoe UI", 11), bg=self.colors["bg"], fg=self.colors["text_muted"]).pack(anchor="w")

        self.fullscreen_btn = ttk.Button(header, text="⛶ Tela Cheia (F11)", style="Secondary.TButton", command=self.toggle_fullscreen)
        self.fullscreen_btn.pack(side="right", pady=10)

        # 2. CONFIGURAÇÕES
        config_frame = ttk.LabelFrame(self.main_container, text=" Parâmetros do Treino ", style="Card.TLabelframe", padding=20)
        config_frame.pack(fill="x", pady=10)

        self.digits = tk.IntVar(value=5)
        self.flash_time = tk.IntVar(value=1500)

        # Usando grid centralizado no frame de config
        config_container = tk.Frame(config_frame, bg=self.colors["card"])
        config_container.pack(expand=True)

        ttk.Label(config_container, text="Quantidade de Dígitos:", style="Card.TLabel").grid(row=0, column=0, sticky="e", pady=5, padx=10)
        ttk.Spinbox(config_container, from_=1, to=100, textvariable=self.digits, width=8, font=("Segoe UI", 11), style="TSpinbox").grid(row=0, column=1, sticky="w", padx=10)

        ttk.Label(config_container, text="Tempo de Exposição (ms):", style="Card.TLabel").grid(row=0, column=2, sticky="e", pady=5, padx=(30, 10))
        ttk.Spinbox(config_container, from_=100, to=15000, textvariable=self.flash_time, width=10, font=("Segoe UI", 11), style="TSpinbox").grid(row=0, column=3, sticky="w", padx=10)

        # 3. VISOR DIGITAL
        self.display_frame = tk.Frame(self.main_container, bg=self.colors["display_bg"], bd=2, relief="flat")
        self.display_frame.pack(fill="both", expand=True, pady=20)
        
        self.display_frame.config(highlightbackground=self.colors["primary"], highlightcolor=self.colors["primary"], highlightthickness=1)

        self.display = tk.Label(self.display_frame, text="PRONTO?", 
                                font=("Consolas", 65, "bold"), 
                                bg=self.colors["display_bg"], 
                                fg=self.colors["text_muted"],
                                wraplength=700) # Evita que o texto saia da tela se for muito longo
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

        tk.Label(response_frame, text="Digite a Sequência:", font=("Segoe UI", 14, "bold"), bg=self.colors["bg"], fg=self.colors["text_muted"]).pack(side="left", padx=10)
        
        self.answer_entry = tk.Entry(response_frame, font=("Consolas", 22, "bold"), justify="center", width=18, 
                                     bg=self.colors["input_bg"], fg=self.colors["text"], bd=0, insertbackground=self.colors["primary"])
        self.answer_entry.pack(side="left", padx=10, ipady=8)
        self.answer_entry.bind("<Return>", lambda event: self.check_answer())
        self.answer_entry.config(state="disabled")

        self.submit_button = tk.Button(response_frame, text="CONFIRMAR", font=("Segoe UI", 12, "bold"), 
                                       bg=self.colors["card"], fg=self.colors["text"], bd=0, cursor="hand2",
                                       command=self.check_answer, padx=20, pady=10)
        self.submit_button.pack(side="left", padx=10)
        self.submit_button.config(state="disabled")

        # 5. RESULTADOS E ESTATÍSTICAS
        self.result_label = tk.Label(self.main_container, text="", font=("Segoe UI", 14, "bold"), bg=self.colors["bg"])
        self.result_label.pack(pady=5)

        self.stats_label = tk.Label(self.main_container, text="Rodadas: 0   |   Acertos: 0   |   Erros: 0   |   Precisão: 0.0%", 
                                     font=("Segoe UI", 11), bg=self.colors["bg"], fg=self.colors["text_muted"])
        self.stats_label.pack(side="bottom", pady=10)

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

    # --- Lógica do Treinamento de Memória ---
    def start_training(self):
        try:
            if not 1 <= self.digits.get() <= 100: raise ValueError("Use entre 1 e 100 dígitos.")
            if self.flash_time.get() < 100: raise ValueError("Tempo de exposição mínimo é 100ms.")
        except tk.TclError:
            messagebox.showerror("Erro", "Valores numéricos inválidos.")
            return
        except ValueError as error:
            messagebox.showerror("Configuração Inválida", str(error))
            return

        self.active = True
        self.result_label.config(text="")
        
        # Gera a string de números baseada na quantidade desejada
        self.current_sequence = "".join([str(random.randint(0, 9)) for _ in range(self.digits.get())])

        # Prepara a interface
        self.answer_entry.config(state="normal")
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.config(state="disabled")
        
        self.submit_button.config(state="disabled", bg=self.colors["bg"])
        self.start_button.config(state="disabled", bg=self.colors["card"], text="MEMORIZE...")

        self.display.config(text="PREPARE-SE!", fg=self.colors["text_muted"])
        
        # Ajusta dinamicamente a fonte se os números forem muito compridos
        font_size = 65 if self.digits.get() <= 12 else 45
        self.display.config(font=("Consolas", font_size, "bold"))

        self.root.after(1000, self.show_sequence)

    def show_sequence(self):
        # Exibe os números
        self.display.config(text=self.current_sequence, fg=self.colors["accent"])
        # Esconde depois do tempo configurado
        self.root.after(self.flash_time.get(), self.hide_sequence)

    def hide_sequence(self):
        if not self.active: return
        
        # Mostra interrogações de acordo com a quantidade de números
        hidden_text = "?" * len(self.current_sequence)
        
        # Adiciona um espaço a cada 4 caracteres para ficar esteticamente bonito na tela
        formatted_hidden = " ".join(hidden_text[i:i+4] for i in range(0, len(hidden_text), 4))

        self.display.config(text=formatted_hidden, fg=self.colors["text_muted"])
        
        # Libera para o usuário digitar
        self.answer_entry.config(state="normal")
        self.submit_button.config(state="normal", bg=self.colors["primary"], fg="white")
        self.answer_entry.focus_set()

    def check_answer(self):
        if not self.active: return
        user_input = self.answer_entry.get().strip()
        if not user_input: return

        # Remove espaços caso o usuário tenha digitado com espaços
        user_input = user_input.replace(" ", "")

        if not user_input.isdigit():
            messagebox.showwarning("Atenção", "Digite apenas números.")
            self.answer_entry.delete(0, tk.END)
            return

        self.rounds += 1
        
        if user_input == self.current_sequence:
            self.score += 1
            self.result_label.config(text=f"✓ PERFEITO! A sequência era {self.current_sequence}", fg=self.colors["success"])
        else:
            self.errors += 1
            self.result_label.config(text=f"✗ INCORRETO. Era {self.current_sequence} (Você digitou {user_input})", fg=self.colors["danger"])

        precision = (self.score / self.rounds) * 100
        self.stats_label.config(text=f"Rodadas: {self.rounds}   |   Acertos: {self.score}   |   Erros: {self.errors}   |   Precisão: {precision:.1f}%")

        self.reset_ui()

    def reset_ui(self):
        self.active = False
        self.display.config(text="FIM DA RODADA", fg=self.colors["text_muted"])
        self.answer_entry.config(state="disabled")
        self.submit_button.config(state="disabled", bg=self.colors["card"], fg=self.colors["text"])
        self.start_button.config(state="normal", bg=self.colors["primary"], text="INICIAR TREINAMENTO")
        self.start_button.focus_set()


if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryPro(root)
    root.mainloop()
