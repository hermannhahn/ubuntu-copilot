import tkinter as tk
from tkinter import ttk


class Chat:

    def __init__(self, root):
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)
        self.root.title("AI Chat")
        self.root.geometry("800x600")

        # App background
        self.root.configure(bg="#242424")

        # Create UI
        self.create_ui()

    def create_ui(self):
        """Cria a interface gráfica do chat."""
        # Borda simulada
        border_frame = tk.Frame(self.root)
        border_frame.pack(fill=tk.BOTH, expand=True)

        # Estilo da barra de rolagem
        style = ttk.Style()
        style.configure("Custom.Vertical.TScrollbar",
                        gripcount=0,
                        background="#242424",
                        troughcolor="#242424",
                        bordercolor="black",
                        arrowcolor="darkblue")

        # Barra de rolagem vertical
        scrollbar = ttk.Scrollbar(border_frame,
                                  orient=tk.VERTICAL,
                                  style="Custom.Vertical.TScrollbar")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Área de texto com rolagem
        self.chat_area = tk.Text(border_frame,
                                 wrap=tk.WORD,
                                 yscrollcommand=scrollbar.set,
                                 font=("Courier New", 12),
                                 background="#242424",
                                 foreground="#ebebeb",
                                 highlightcolor="#242424",
                                 highlightbackground="#242424",
                                 highlightthickness=0,
                                 insertbackground="white",
                                 state=tk.DISABLED,
                                 padx=5,
                                 pady=5,
                                 relief="groove",
                                 borderwidth=0)
        self.chat_area.pack(expand=True, fill=tk.BOTH)
        scrollbar.config(command=self.chat_area.yview)

        # # Área de chat
        # self.chat_area = scrolledtext.ScrolledText(
        #     self.root,
        #     wrap=tk.WORD,
        #     font=("Arial", 12),
        #     background="#252525",
        #     foreground="#252525",
        #     highlightcolor="#252525",
        #     highlightbackground="#252525",
        #     highlightthickness=0,
        #     borderwidth=0)
        # self.chat_area.config(state=tk.DISABLED)  # Apenas leitura
        # self.chat_area.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

        # Área de entrada e botões
        bottom_frame = tk.Frame(self.root,
                                bg="#252525",
                                padx=5,
                                pady=5,
                                borderwidth=0,
                                highlightcolor="#252525",
                                highlightthickness=0,
                                highlightbackground="#252525")
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Botões de ação
        buttons_frame = tk.Frame(bottom_frame,
                                 bg="#252525",
                                 borderwidth=0,
                                 highlightthickness=0,
                                 highlightbackground="#252525",
                                 highlightcolor="#252525",
                                 padx=5,
                                 pady=5)
        buttons_frame.pack(side=tk.RIGHT)
        buttons_frame.pack_propagate(
            False)  # Evitar redimensionamento automático

        # Criar botões com tamanhos mínimos
        button_width = 5  # Largura mínima dos botões
        send_button = tk.Button(buttons_frame,
                                text="↵",
                                command=self.send_message,
                                font=("Courier New", 18, "bold"),
                                width=2,
                                height=2,
                                highlightbackground=None,
                                highlightcolor=None,
                                highlightthickness=0,
                                background="#353535",
                                foreground="#f1f1f1",
                                activebackground="#454545",
                                activeforeground="#f1f1f1",
                                borderwidth=0)
        send_button.grid(row=0, column=0, padx=2)

        mic_button = tk.Button(buttons_frame,
                               text="🎤",
                               command=lambda: print("Mic clicked"),
                               font=("Courier New", 18, "bold"),
                               width=2,
                               height=2,
                               highlightbackground=None,
                               highlightcolor=None,
                               highlightthickness=0,
                               background="#353535",
                               foreground="#f1f1f1",
                               activebackground="#454545",
                               activeforeground="#f1f1f1",
                               borderwidth=0)
        mic_button.grid(row=0, column=1, padx=2)

        trash_button = tk.Button(buttons_frame,
                                 text="🗑️",
                                 command=lambda: print("Trash clicked"),
                                 font=("Courier New", 18, "bold"),
                                 width=2,
                                 height=2,
                                 highlightbackground=None,
                                 highlightcolor=None,
                                 highlightthickness=0,
                                 background="#353535",
                                 foreground="#f1f1f1",
                                 activebackground="#454545",
                                 activeforeground="#f1f1f1",
                                 borderwidth=0)
        trash_button.grid(row=0, column=2, padx=2)

        settings_button = tk.Button(buttons_frame,
                                    text="🛠",
                                    command=lambda: print("Settings clicked"),
                                    font=("Courier New", 18, "bold"),
                                    width=2,
                                    height=2,
                                    highlightbackground=None,
                                    highlightcolor=None,
                                    highlightthickness=0,
                                    background="#353535",
                                    foreground="#f1f1f1",
                                    activebackground="#454545",
                                    activeforeground="#f1f1f1",
                                    borderwidth=0)
        settings_button.grid(row=0, column=3, padx=2)

        # Área de entrada ajustável
        self.input_area = tk.Text(bottom_frame,
                                  wrap=tk.WORD,
                                  height=3,
                                  font=("Courier New", 12),
                                  background="#353535",
                                  foreground="#ebebeb",
                                  highlightcolor="#252525",
                                  highlightbackground="#252525",
                                  highlightthickness=0,
                                  borderwidth=0,
                                  padx=5,
                                  pady=5,
                                  relief="groove",
                                  insertbackground="white",
                                  state=tk.NORMAL)
        self.input_area.pack(side=tk.LEFT,
                             fill=tk.X,
                             expand=True,
                             padx=0,
                             pady=5)
        self.input_area.focus_set()

        # Configuração para ajustar a largura do input
        self.root.bind("<Configure>", self.adjust_input_width)

    def adjust_input_width(self, event=None):
        """Ajusta a largura do input_area conforme o tamanho da janela."""
        button_area_width = 5 * 4 * 10 + 20  # Largura total dos botões (+ margem)
        total_width = self.root.winfo_width()
        input_width = max(total_width - button_area_width,
                          100)  # Garante largura mínima
        self.input_area.config(width=input_width)

    def send_message(self):
        """Envia a mensagem digitada pelo usuário."""
        user_message = self.input_area.get("1.0", tk.END).strip()
        if user_message:
            self.update_chat(f"User: {user_message}")
            self.update_chat(f"Model: Hello, I received: {user_message}")
        self.input_area.delete("1.0", tk.END)

    def update_chat(self, message):
        """Atualiza a área de chat com uma nova mensagem."""
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.see(tk.END)
        self.chat_area.config(state=tk.DISABLED)
