import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib

import threading
import google.generativeai as genai
import vertexai
from vertexai.generative_models import GenerativeModel

from settings import SettingsWindow, load_api_key, load_project_id, load_region

class ChatWindow:
    def __init__(self):
        # Configuração do Vertex AI
        self.settings_window = SettingsWindow()
        self.api_key = load_api_key()
        self.project_id = load_project_id()
        self.region = load_region()

        # Configuração do Generative AI
        genai.configure(api_key=self.api_key)
        vertexai.init(project=self.project_id, location=self.region)
        self.model = GenerativeModel("gemini-1.5-flash-002")
        
        self.build()

    def build(self):
        # Layout principal
        self.layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.layout.set_margin_top(10)
        self.layout.set_margin_bottom(10)
        self.layout.set_margin_start(10)
        self.layout.set_margin_end(10)

        # Área de exibição do chat
        self.chat_display = Gtk.TextView()
        self.chat_display.set_wrap_mode(Gtk.WrapMode.WORD)
        self.chat_display.set_editable(False)
        self.chat_display.set_cursor_visible(False)
        self.chat_display.set_margin_top(10)
        self.chat_display.set_margin_bottom(10)
        self.chat_display.set_margin_start(10)
        self.chat_display.set_margin_end(10)

        # Scroll para a área de chat
        self.chat_scroll = Gtk.ScrolledWindow()
        self.chat_scroll.set_vexpand(True)

        # Bottom
        self.bottom = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

        # Campo de entrada
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Digite sua mensagem...")
        self.entry.connect("activate", self.on_message_sent)

        # Botão de enviar
        self.send_button = Gtk.Button(label="Enviar")
        self.send_button.connect("clicked", self.on_message_sent)

        # Botão para abrir configurações
        self.settings_button = Gtk.Button(label="⚙")
        self.settings_button.connect("clicked", self.open_settings)
            
        # api key alert message
        self.api_alert = Gtk.MessageDialog(
            transient_for=None,
            title="Settings",
            modal=True,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.OK,
            text="Por favor, configure as credenciais antes de continuar.",
        )
        self.api_alert.connect("response", lambda d, r: self.close_alert(d))

        self.layout.append(self.chat_scroll)
        self.layout.append(self.bottom)
        self.bottom.append(self.entry)
        self.bottom.append(self.send_button)
        self.bottom.append(self.settings_button)

        # Verifica se as credenciais estão configuradas
        if not self.api_key or not self.project_id or not self.region:
            self.api_alert.show()
            return

        self.chat_scroll.set_child(self.chat_display)

    def close_alert(self, d):
        d.close()
        self.open_settings()
        self.chat_scroll.set_child(self.chat_display)

    def on_message_sent(self, widget):
        # Captura o texto da entrada
        message = self.entry.get_text()
        # Limpa o campo de entrada
        self.entry.set_text("")
        # Exibe a mensagem no chat
        buffer = self.chat_display.get_buffer()
        buffer.insert(buffer.get_end_iter(), f"Você: {message}\n")

        # Verifica se a mensagem não está vazia
        if message.strip():
            # Envia a mensagem para o modelo de linguagem e exibe a resposta
            threading.Thread(target=self.gemini_response, args=(message,), daemon=True).start()

    def gemini_response(self, message):
        jsonResponse = self.model.generate_content(message)
        response = jsonResponse.candidates[0].content.parts[0].text
        buffer = self.chat_display.get_buffer()
        buffer.insert(buffer.get_end_iter(), f"Bot: {response}\n")

    def open_settings(self):
        # Abre a janela de configurações
        self.settings_window.show()
