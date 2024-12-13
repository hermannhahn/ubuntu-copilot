import gi
import asyncio
from openai import AsyncOpenAI
from settings import load_api_key, SettingsWindow

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# Configure a chave de API OpenAI carregada do arquivo de configurações
api_key = load_api_key()
client = AsyncOpenAI(api_key=api_key)

class App(Gtk.Window):
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

        # Botão com ícone para abrir configurações ao lado do botão enviar
        settings_button = Gtk.Button()
        settings_icon = Gtk.Image.new_from_icon_name("emblem-system", Gtk.IconSize.MENU)
        settings_button.set_image(settings_icon)
        settings_button.connect("clicked", self.open_settings)
        layout.pack_start(settings_button, False, False, 0)


    def on_message_sent(self, widget):
        # Captura o texto da entrada
        message = self.entry.get_text()
        if message.strip():
            # Exibe a mensagem no chat
            buffer = self.chat_display.get_buffer()
            buffer.insert(buffer.get_end_iter(), f"Você: {message}\n")

            # Chama a API OpenAI
            asyncio.run(self.get_bot_response(message))

        # Limpa o campo de entrada
        self.entry.set_text("")

    async def get_bot_response(self, message):
        try:
            stream = await client.chat.completions.create(
                messages=[
                    {"role": "user", "content": message}
                ],
                stream=True,
                model="gpt-3.5-turbo"
            )
            
            #response_content = stream["choices"][0]["message"]["content"]

            # Atualiza o TextView com a resposta
            buffer = self.chat_display.get_buffer()
            for chunk in stream:
                buffer.insert(buffer.get_end_iter(), f"Bot: {chunk.choices[0].delta.content or ''}\n")
                self.chat_display.scroll_to_iter(buffer.get_end_iter(), 0, True, 0, 0)
                self.show_all()

        except Exception as e:
            buffer = self.chat_display.get_buffer()
            buffer.insert(buffer.get_end_iter(), f"Erro ao obter resposta: {e}\n")

    def open_settings(self, widget):
        # Abre a janela de configurações
        settings_window = SettingsWindow()
        settings_window.show_all()

if __name__ == "__main__":
    app = App()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()
