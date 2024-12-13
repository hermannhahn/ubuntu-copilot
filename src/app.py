import gi
import openai
from settings import load_api_key

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# Configure a chave de API OpenAI carregada do arquivo de configurações
openai.api_key = load_api_key()

class ChatBotApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="Linux Co-Pilot Chatbot")
        self.set_default_size(600, 400)

        # Layout principal
        layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(layout)

        # Área de exibição do chat
        self.chat_display = Gtk.TextView()
        self.chat_display.set_wrap_mode(Gtk.WrapMode.WORD)
        self.chat_display.set_editable(False)
        self.chat_display.set_cursor_visible(False)

        # Scroll para a área de chat
        chat_scroll = Gtk.ScrolledWindow()
        chat_scroll.set_vexpand(True)
        chat_scroll.add(self.chat_display)
        layout.pack_start(chat_scroll, True, True, 0)

        # Campo de entrada
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Digite sua mensagem...")
        self.entry.connect("activate", self.on_message_sent)
        layout.pack_start(self.entry, False, False, 0)

        # Botão de enviar
        send_button = Gtk.Button(label="Enviar")
        send_button.connect("clicked", self.on_message_sent)
        layout.pack_start(send_button, False, False, 0)

    def on_message_sent(self, widget):
        # Captura o texto da entrada
        message = self.entry.get_text()
        if message.strip():
            # Exibe a mensagem no chat
            buffer = self.chat_display.get_buffer()
            buffer.insert(buffer.get_end_iter(), f"Você: {message}\n")

            # Chama a API OpenAI
            response = self.get_bot_response(message)
            buffer.insert(buffer.get_end_iter(), f"Bot: {response}\n")

        # Limpa o campo de entrada
        self.entry.set_text("")

    def get_bot_response(self, message):
        try:
            # Solicitação para a API OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Modelo pode ser ajustado conforme necessário
                messages=[
                    {"role": "system", "content": "Você é um assistente útil."},
                    {"role": "user", "content": message}
                ]
            )
            # Retorna o conteúdo da resposta
            return response['choices'][0]['message']['content'].strip()
        except Exception as e:
            return f"Erro ao obter resposta: {e}"

if __name__ == "__main__":
    app = ChatBotApp()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()