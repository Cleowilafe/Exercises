import random
import tkinter as tk
from tkinter import ttk, messagebox


class TreinoTabuada:
    def __init__(self, root):
        self.root = root
        self.root.title("Treino de Tabuada")
        self.root.geometry("620x680")
        self.root.minsize(540, 620)

        # Configurações da sessão
        self.dificuldade = tk.StringVar(value="Fácil")
        self.digitos_a = tk.StringVar(value="1")
        self.digitos_b = tk.StringVar(value="1")
        self.quantidade_questoes = tk.IntVar(value=10)
        self.resposta = tk.StringVar()

        # Estado do jogo
        self.questao_atual = 0
        self.total_questoes = 10
        self.acertos = 0
        self.erros = 0
        self.pontos = 0
        self.a = 0
        self.b = 0
        self.respondida = False
        self.ativa = False
        self.tempo_restante = 0
        self.timer_id = None

        # Pontos por acerto e tempo de resposta por dificuldade
        self.config_dificuldade = {
            "Fácil": {"pontos": 1, "tempo": 60},
            "Médio": {"pontos": 2, "tempo": 30},
            "Difícil": {"pontos": 3, "tempo": 15},
        }

        self.criar_interface()
        self.atualizar_estatisticas()

    def criar_interface(self):
        """Cria os componentes gráficos e associa os eventos."""
        principal = ttk.Frame(self.root, padding=20)
        principal.pack(fill="both", expand=True)

        ttk.Label(
            principal,
            text="Treino de Tabuada",
            font=("Arial", 22, "bold")
        ).pack(pady=(0, 5))

        ttk.Label(
            principal,
            text="Pratique multiplicação no seu ritmo!",
            font=("Arial", 11)
        ).pack(pady=(0, 20))

        # Configurações
        config = ttk.LabelFrame(
            principal, text="Configurações", padding=12
        )
        config.pack(fill="x", pady=5)

        ttk.Label(config, text="Dificuldade:").grid(
            row=0, column=0, sticky="w", padx=5, pady=7
        )

        self.combo_dificuldade = ttk.Combobox(
            config,
            textvariable=self.dificuldade,
            values=["Fácil", "Médio", "Difícil"],
            state="readonly",
            width=12
        )
        self.combo_dificuldade.grid(
            row=0, column=1, sticky="w", padx=5, pady=7
        )

        ttk.Label(config, text="Dígitos do 1º número:").grid(
            row=1, column=0, sticky="w", padx=5, pady=7
        )

        self.combo_a = ttk.Combobox(
            config,
            textvariable=self.digitos_a,
            values=["1", "2", "3"],
            state="readonly",
            width=12
        )
        self.combo_a.grid(
            row=1, column=1, sticky="w", padx=5, pady=7
        )

        ttk.Label(config, text="Dígitos do 2º número:").grid(
            row=2, column=0, sticky="w", padx=5, pady=7
        )

        self.combo_b = ttk.Combobox(
            config,
            textvariable=self.digitos_b,
            values=["1", "2", "3"],
            state="readonly",
            width=12
        )
        self.combo_b.grid(
            row=2, column=1, sticky="w", padx=5, pady=7
        )

        ttk.Label(config, text="Número de questões:").grid(
            row=3, column=0, sticky="w", padx=5, pady=7
        )

        self.combo_quantidade = ttk.Combobox(
            config,
            textvariable=self.quantidade_questoes,
            values=[5, 10, 15, 20, 30, 50],
            state="readonly",
            width=12
        )
        self.combo_quantidade.grid(
            row=3, column=1, sticky="w", padx=5, pady=7
        )

        config.columnconfigure(2, weight=1)

        self.botao_iniciar = ttk.Button(
            config,
            text="Iniciar treino",
            command=self.iniciar_treino
        )
        self.botao_iniciar.grid(
            row=0, column=2, rowspan=2, padx=12, sticky="nsew"
        )

        # Área da questão
        area = ttk.LabelFrame(
            principal, text="Sua questão", padding=18
        )
        area.pack(fill="x", pady=12)

        self.label_progresso = ttk.Label(
            area, text="Questão 0 de 10"
        )
        self.label_progresso.pack()

        self.label_tempo = ttk.Label(
            area, text="Tempo: --",
            font=("Arial", 11, "bold")
        )
        self.label_tempo.pack(pady=5)

        self.label_conta = ttk.Label(
            area,
            text="Clique em 'Iniciar treino'!",
            font=("Arial", 25, "bold")
        )
        self.label_conta.pack(pady=15)

        self.entrada_resposta = ttk.Entry(
            area,
            textvariable=self.resposta,
            font=("Arial", 16),
            justify="center",
            width=18,
            state="disabled"
        )
        self.entrada_resposta.pack(pady=5)

        # Pressionar Enter envia a resposta
        self.entrada_resposta.bind(
            "<Return>", self.evento_enter
        )

        botoes = ttk.Frame(area)
        botoes.pack(pady=10)

        self.botao_responder = ttk.Button(
            botoes,
            text="Responder",
            command=self.verificar_resposta,
            state="disabled"
        )
        self.botao_responder.pack(side="left", padx=5)

        self.botao_proxima = ttk.Button(
            botoes,
            text="Próxima questão",
            command=self.proxima_questao,
            state="disabled"
        )
        self.botao_proxima.pack(side="left", padx=5)

        self.label_feedback = ttk.Label(
            area,
            text="",
            font=("Arial", 12, "bold"),
            wraplength=480,
            justify="center"
        )
        self.label_feedback.pack(pady=8)

        # Estatísticas
        stats = ttk.LabelFrame(
            principal, text="Estatísticas", padding=12
        )
        stats.pack(fill="x", pady=5)

        self.label_acertos = ttk.Label(stats, text="Acertos: 0")
        self.label_acertos.grid(
            row=0, column=0, padx=10, pady=5, sticky="w"
        )

        self.label_erros = ttk.Label(stats, text="Erros: 0")
        self.label_erros.grid(
            row=0, column=1, padx=10, pady=5, sticky="w"
        )

        self.label_pontos = ttk.Label(stats, text="Pontos: 0")
        self.label_pontos.grid(
            row=1, column=0, padx=10, pady=5, sticky="w"
        )

        self.label_percentual = ttk.Label(
            stats, text="Aproveitamento: 0%"
        )
        self.label_percentual.grid(
            row=1, column=1, padx=10, pady=5, sticky="w"
        )

        stats.columnconfigure((0, 1), weight=1)

        self.barra_progresso = ttk.Progressbar(
            principal,
            mode="determinate",
            maximum=10,
            value=0
        )
        self.barra_progresso.pack(fill="x", pady=10)

        ttk.Label(
            principal,
            text="Fácil: 60 s | Médio: 30 s | Difícil: 15 s"
        ).pack(pady=3)

    def iniciar_treino(self):
        """Evento do botão Iniciar treino."""
        self.cancelar_timer()

        try:
            quantidade = int(self.quantidade_questoes.get())
            dig_a = int(self.digitos_a.get())
            dig_b = int(self.digitos_b.get())
        except (ValueError, tk.TclError):
            messagebox.showerror(
                "Configuração inválida",
                "Selecione todas as opções corretamente."
            )
            return

        if quantidade not in [5, 10, 15, 20, 30, 50]:
            messagebox.showerror(
                "Erro", "Quantidade de questões inválida."
            )
            return

        if dig_a not in [1, 2, 3] or dig_b not in [1, 2, 3]:
            messagebox.showerror(
                "Erro", "Escolha entre 1 e 3 dígitos."
            )
            return

        self.total_questoes = quantidade
        self.questao_atual = 0
        self.acertos = 0
        self.erros = 0
        self.pontos = 0
        self.ativa = True

        self.botao_iniciar.configure(text="Reiniciar treino")
        self.combo_dificuldade.configure(state="disabled")
        self.combo_a.configure(state="disabled")
        self.combo_b.configure(state="disabled")
        self.combo_quantidade.configure(state="disabled")

        self.barra_progresso.configure(maximum=quantidade, value=0)
        self.atualizar_estatisticas()
        self.proxima_questao()

    def gerar_numero(self, digitos):
        """Gera um inteiro com exatamente a quantidade de dígitos."""
        minimo = 1 if digitos == 1 else 10 ** (digitos - 1)
        maximo = (10 ** digitos) - 1
        return random.randint(minimo, maximo)

    def proxima_questao(self):
        """Gera uma questão e inicia seu cronômetro."""
        if not self.ativa:
            return

        self.cancelar_timer()

        if self.questao_atual >= self.total_questoes:
            self.finalizar_treino()
            return

        self.questao_atual += 1

        self.a = self.gerar_numero(int(self.digitos_a.get()))
        self.b = self.gerar_numero(int(self.digitos_b.get()))

        self.respondida = False
        self.resposta.set("")
        self.label_feedback.configure(text="")
        self.label_conta.configure(text=f"{self.a} × {self.b} = ?")
        self.label_progresso.configure(
            text=f"Questão {self.questao_atual} "
                 f"de {self.total_questoes}"
        )

        self.barra_progresso.configure(
            value=self.questao_atual - 1
        )

        self.entrada_resposta.configure(state="normal")
        self.botao_responder.configure(state="normal")
        self.botao_proxima.configure(state="disabled")

        self.tempo_restante = self.config_dificuldade[
            self.dificuldade.get()
        ]["tempo"]

        self.atualizar_tempo()
        self.entrada_resposta.focus_set()

    def atualizar_tempo(self):
        """Atualiza o cronômetro sem bloquear a interface."""
        if not self.ativa or self.respondida:
            return

        self.label_tempo.configure(
            text=f"Tempo restante: {self.tempo_restante} s"
        )

        if self.tempo_restante <= 0:
            self.encerrar_por_tempo()
            return

        self.tempo_restante -= 1
        self.timer_id = self.root.after(
            1000, self.atualizar_tempo
        )

    def verificar_resposta(self):
        """Evento do botão Responder ou da tecla Enter."""
        if not self.ativa or self.respondida:
            return

        texto = self.resposta.get().strip()

        if not texto:
            self.label_feedback.configure(
                text="Digite uma resposta primeiro!",
                foreground="#b36b00"
            )
            self.entrada_resposta.focus_set()
            return

        try:
            valor = int(texto)
        except ValueError:
            self.label_feedback.configure(
                text="Digite um número inteiro válido.",
                foreground="#b00020"
            )
            return

        self.cancelar_timer()
        self.respondida = True
        resultado = self.a * self.b

        if valor == resultado:
            ganho = self.config_dificuldade[
                self.dificuldade.get()
            ]["pontos"]

            self.acertos += 1
            self.pontos += ganho

            self.label_feedback.configure(
                text=f"Correto! Muito bem! +{ganho} ponto(s).",
                foreground="#16803c"
            )
        else:
            self.erros += 1
            self.label_feedback.configure(
                text=f"Resposta incorreta. O correto é {resultado}.",
                foreground="#b00020"
            )

        self.encerrar_resposta()

    def encerrar_por_tempo(self):
        """Evento chamado quando o cronômetro chega a zero."""
        self.cancelar_timer()

        if not self.ativa or self.respondida:
            return

        self.respondida = True
        self.erros += 1

        self.label_feedback.configure(
            text=f"Tempo esgotado! A resposta era {self.a * self.b}.",
            foreground="#b00020"
        )

        self.encerrar_resposta()

    def encerrar_resposta(self):
        """Desabilita a resposta e permite avançar."""
        self.entrada_resposta.configure(state="disabled")
        self.botao_responder.configure(state="disabled")
        self.botao_proxima.configure(state="normal")

        self.label_tempo.configure(text="Questão respondida")
        self.barra_progresso.configure(
            value=self.questao_atual
        )

        self.atualizar_estatisticas()

        if self.questao_atual >= self.total_questoes:
            self.botao_proxima.configure(
                text="Ver resultado",
                command=self.finalizar_treino
            )

    def evento_enter(self, evento):
        """Permite responder usando a tecla Enter."""
        self.verificar_resposta()
        return "break"

    def atualizar_estatisticas(self):
        """Atualiza os indicadores na interface."""
        respondidas = self.acertos + self.erros

        percentual = (
            self.acertos / respondidas * 100
            if respondidas > 0 else 0
        )

        self.label_acertos.configure(
            text=f"Acertos: {self.acertos}"
        )
        self.label_erros.configure(
            text=f"Erros: {self.erros}"
        )
        self.label_pontos.configure(
            text=f"Pontos: {self.pontos}"
        )
        self.label_percentual.configure(
            text=f"Aproveitamento: {percentual:.1f}%"
        )

    def finalizar_treino(self):
        """Encerra a sessão e mostra o resultado final."""
        self.cancelar_timer()
        self.ativa = False

        self.entrada_resposta.configure(state="disabled")
        self.botao_responder.configure(state="disabled")
        self.botao_proxima.configure(state="disabled")
        self.combo_dificuldade.configure(state="readonly")
        self.combo_a.configure(state="readonly")
        self.combo_b.configure(state="readonly")
        self.combo_quantidade.configure(state="readonly")

        self.label_conta.configure(text="Treino concluído!")
        self.label_tempo.configure(text="Fim do cronômetro")
        self.label_feedback.configure(
            text="Parabéns por praticar!",
            foreground="#16803c"
        )

        self.barra_progresso.configure(
            value=self.total_questoes
        )

        respondidas = self.acertos + self.erros
        percentual = (
            self.acertos / respondidas * 100
            if respondidas else 0
        )

        messagebox.showinfo(
            "Resultado final",
            f"Treino concluído!\n\n"
            f"Questões: {self.total_questoes}\n"
            f"Acertos: {self.acertos}\n"
            f"Erros: {self.erros}\n"
            f"Pontos: {self.pontos}\n"
            f"Aproveitamento: {percentual:.1f}%"
        )

        self.botao_iniciar.configure(text="Novo treino")
        self.botao_proxima.configure(
            text="Próxima questão",
            command=self.proxima_questao
        )

    def cancelar_timer(self):
        """Cancela um evento de cronômetro pendente."""
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None


if __name__ == "__main__":
    janela = tk.Tk()
    app = TreinoTabuada(janela)
    janela.mainloop()
