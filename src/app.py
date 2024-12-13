import os 
import gi
import asyncio
from settings import load_api_key, load_project_id, load_region, load_endpoint_id, SettingsWindow
import google.generativeai as genai
from google.cloud import aiplatform
import base64
import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting, Part

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class App(Gtk.Window):
    def __init__(self):
        super().__init__(title="Linux Co-Pilot Chatbot")
        self.set_default_size(600, 400)

        # Layout principal
        layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin=10)
        self.add(layout)

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
        layout.pack_start(chat_scroll, True, True, 0)
        
        # Bottom
        bottom = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        layout.pack_start(bottom, False, False, 10)

        # Campo de entrada
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Digite sua mensagem...")
        self.entry.connect("activate", self.on_message_sent)
        bottom.pack_start(self.entry, True, True, 0)

        # Botão de enviar
        send_button = Gtk.Button(label="Enviar")
        send_button.connect("clicked", self.on_message_sent)
        bottom.pack_start(send_button, False, False, 0)

        # Botão para abrir configurações ao lado do botão enviar
        settings_button = Gtk.Button(label="⚙")
        settings_button.connect("clicked", self.open_settings)
        bottom.pack_start(settings_button, False, False, 0)

        # Configuração do Vertex AI
        api_key = load_api_key()
        genai.configure(api_key=api_key)
        self.project_id = load_project_id()
        self.region = load_region()
        self.endpoint_id = load_endpoint_id()
        vertexai.init(project=self.project_id, location=self.region)
        self.model = GenerativeModel("gemini-1.5-flash-002")

    def on_message_sent(self, widget):
        # Captura o texto da entrada
        message = self.entry.get_text()
        # Limpa o campo de entrada
        self.entry.set_text("")

        # Verifica se a mensagem não está vazia
        if message.strip():
            # Exibe a mensagem no chat
            buffer = self.chat_display.get_buffer()
            buffer.insert(buffer.get_end_iter(), f"Você: {message}\n")

            # Chama o Vertex AI para obter a resposta
            jsonResponse = self.model.generate_content(message)
            response = jsonResponse.candidates[0].content.parts.text

            # Exibe a resposta no chat
            buffer.insert(buffer.get_end_iter(), f"Bot: {response}\n")

    def open_settings(self, widget):
        # Abre a janela de configurações
        settings_window = SettingsWindow()
        settings_window.show_all()

if __name__ == "__main__":
    app = App()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()
