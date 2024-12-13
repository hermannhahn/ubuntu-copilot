import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

import asyncio

import google.generativeai as genai
from settings import load_api_key, load_project_id, load_region, SettingsWindow
import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting, Part

import gi
import asyncio
from gi.repository import Gtk, GLib

gi.require_version("Gtk", "3.0")

# Integração do loop de eventos do asyncio com o GTK
def integrate_asyncio_with_glib():
    loop = asyncio.get_event_loop()
    GLib.io_add_watch(
        loop._csock.fileno(),  # File descriptor do asyncio
        GLib.IO_IN,           # Condição de leitura
        lambda fd, cond: loop._read_from_self() or True,
    )

integrate_asyncio_with_glib()

class ChatWindow:
    def __init__(self):
        # Configuração do Vertex AI
        self.api_key = load_api_key()
        genai.configure(api_key=self.api_key)
        self.project_id = load_project_id()
        self.region = load_region()
        vertexai.init(project=self.project_id, location=self.region)
        self.model = GenerativeModel("gemini-1.5-flash-002")
        
        # Layout principal
        self.layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin=10)
        
        # Área de exibição do chat
        self.chat_display = Gtk.TextView()
        self.chat_display.set_wrap_mode(Gtk.WrapMode.WORD)
        self.chat_display.set_editable(False)
        self.chat_display.set_cursor_visible(False)
        self.chat_display.set_left_margin(10)
        self.chat_display.set_right_margin(10)
        self.chat_display.set_top_margin(10)
        self.chat_display.set_bottom_margin(10)

        # Scroll para a área de chat
        chat_scroll = Gtk.ScrolledWindow()
        chat_scroll.set_vexpand(True)
        chat_scroll.add(self.chat_display)
        self.layout.pack_start(chat_scroll, True, True, 0)
        
        # Bottom
        bottom = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        self.layout.pack_start(bottom, False, False, 10)

        # Campo de entrada
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Digite sua mensagem...")
        self.entry.connect("activate", self.on_message_sent)
        bottom.pack_start(self.entry, True, True, 0)

        # Botão de enviar
        send_button = Gtk.Button(label="Enviar")
        send_button.connect("clicked", self.on_message_sent)
        bottom.pack_start(send_button, False, False, 0)

        # Botão para abrir configurações
        settings_button = Gtk.Button(label="⚙")
        settings_button.connect("clicked", self.open_settings)
        bottom.pack_start(settings_button, False, False, 0)

    def on_message_sent(self, widget):
        # Cria uma tarefa assíncrona no loop principal
        asyncio.create_task(self.send_message(widget))

    async def send_message(self, widget):
        # Captura o texto da entrada
        message = self.entry.get_text()
        # Limpa o campo de entrada
        self.entry.set_text("")
        # Exibe a mensagem no chat
        self.buffer = self.chat_display.get_buffer()
        self.buffer.insert(self.buffer.get_end_iter(), f"Você: {message}\n")

        # Verifica se a mensagem não está vazia
        if message.strip():
            # Envia a mensagem para o modelo de linguagem e exibe a resposta
            response = await self.gemini_response(message)
            self.buffer.insert(self.buffer.get_end_iter(), f"Bot: {response}\n")

    async def gemini_response(self, message):
        # Usa asyncio para executar a operação bloqueante no loop
        loop = asyncio.get_event_loop()
        jsonResponse = await loop.run_in_executor(None, self.model.generate_content, message)
        return jsonResponse.candidates[0].content.parts[0].text

    def open_settings(self, widget):
        # Abre a janela de configurações
        settings_window = SettingsWindow()
        settings_window.show_all()
