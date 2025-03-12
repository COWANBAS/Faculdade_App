import sys
import os
from PyQt5.QtCore import QUrl, Qt, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings


class BrowserApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Criando as abas com as URLs
        self.create_browser_tab("Ava", "https://www.colaboraread.com.br/")
        self.create_browser_tab("Kroton Login", "https://login.kroton.com.br/")
        self.create_browser_tab("Prova", "https://provadigital.kroton.com.br/") 

        self.setWindowTitle("Faculdade")
        self.setGeometry(100, 100, 1024, 768)

        self.enable_hardware_acceleration()

        self.start_focus_timer()

    def create_browser_tab(self, title, url):
        profile = QWebEngineProfile.defaultProfile()
        profile.setPersistentStoragePath(os.path.join(os.path.expanduser("~"), f".browser_profile_{title}"))

        settings = QWebEngineSettings.defaultSettings()
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)

        browser = QWebEngineView()
        browser.setUrl(QUrl(url))
        browser.setContextMenuPolicy(Qt.NoContextMenu)
        profile.setPersistentCookiesPolicy(QWebEngineProfile.AllowPersistentCookies)

        tab_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(browser)
        tab_widget.setLayout(layout)

        self.tabs.addTab(tab_widget, title)

    def enable_hardware_acceleration(self):
        os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--enable-accelerated-2d-canvas --enable-webgl --ignore-gpu-blacklist"

    def start_focus_timer(self):
        timer = QTimer(self)
        timer.timeout.connect(self.simulate_focus)
        timer.start(1000)

    def simulate_focus(self):
        current_browser = self.tabs.currentWidget().findChild(QWebEngineView)
        if current_browser:
            current_browser.page().runJavaScript("window.focus();")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F5:
            self.reload_page()

    def reload_page(self):
        current_browser = self.tabs.currentWidget().findChild(QWebEngineView)
        if current_browser:
            current_browser.reload()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrowserApp()
    window.show()
    sys.exit(app.exec_())
