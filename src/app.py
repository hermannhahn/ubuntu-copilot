import tkinter as tk
from tkinter import messagebox
import threading
from pynput import keyboard


class CrossPlatformApp:
    def __init__(self, root):
        self.root = root
        self.root.title("App Multiplataforma")
        self.root.geometry("400x300")

        # Adiciona um rótulo informativo
        label = tk.Label(root, text="Pressione F1 para interagir!", font=("Arial", 14))
        label.pack(expand=True)

        # Iniciar o monitor de teclado em thread separada
        self.start_keyboard_monitor()

    def start_keyboard_monitor(self):
        """Inicia o monitor de teclado em uma thread separada."""
        threading.Thread(target=self.keyboard_listener, daemon=True).start()

    def keyboard_listener(self):
        """Monitora eventos globais de teclado."""
        def on_press(key):
            try:
                if key == keyboard.Key.f1:
                    # A chamada para mostrar a mensagem precisa ser feita na thread principal do Tkinter
                    self.root.after(0, self.on_f1_pressed)
            except Exception as e:
                print(f"Erro no listener de teclado: {e}")

        # Inicia o listener de teclado
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()

    def on_f1_pressed(self):
        """Ação executada ao pressionar F1."""
        messagebox.showinfo("Tecla F1 Pressionada", "Você pressionou F1!")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = CrossPlatformApp(root)
    app.run()
