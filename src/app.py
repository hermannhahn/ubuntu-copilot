import gi
import asyncio
from openai import AsyncOpenAI
from settings import load_api_key, SettingsWindow

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

# Configure a chave de API OpenAI carregada do arquivo de configurações
api_key = load_api_key()
client = AsyncOpenAI(api_key=api_key)

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

        # Botão para abrir configurações
        settings_button = Gtk.Button(label="Configurações")
        settings_button.connect("clicked", self.open_settings)
        layout.pack_start(settings_button, False, False, 0)

    def on_message_sent(self, widget):
        # Captura o texto da entrada
        message = self.entry.get_text()
        if message.strip():
            # Exibe a mensagem no chat
            buffer = self.chat_display.get_buffer()
            buffer.insert(buffer.get_end_iter(), f"Você: {message}\n")

            # Chama a API OpenAI de forma assíncrona
            asyncio.create_task(self.get_bot_response_async(message))

        # Limpa o campo de entrada
        self.entry.set_text("")

    async def get_bot_response_async(self, message):
        try:
            chat_completion = await client.chat.completions.create(
                messages=[
                    {"role": "user", "content": message}
                ],
                model="gpt-4o"
            )
            response_content = chat_completion["choices"][0]["message"]["content"]

            # Atualiza o TextView com a resposta
            buffer = self.chat_display.get_buffer()
            GLib.idle_add(buffer.insert, buffer.get_end_iter(), f"Bot: {response_content}\n")

        except Exception as e:
            buffer = self.chat_display.get_buffer()
            GLib.idle_add(buffer.insert, buffer.get_end_iter(), f"Erro ao obter resposta: {e}\n")

    def open_settings(self, widget):
        # Abre a janela de configurações
        settings_window = SettingsWindow()
        settings_window.show_all()

async def main_async():
    app = ChatBotApp()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    await asyncio.get_event_loop().run_in_executor(None, Gtk.main)

if __name__ == "__main__":
    asyncio.run(main_async())
