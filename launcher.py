"""
MMORPG Store Launcher
PyQt6 + QtWebEngine ile Chromium tabanlı mağaza penceresini başlatır.
FastAPI backend'i arka planda otomatik başlatır, hazır olana kadar bekler.
"""

import sys
import os
import threading
import time
import socket
from pathlib import Path

# ─────────────────────────────────────────────
# PATH SETUP
# ─────────────────────────────────────────────
BASE_DIR    = Path(__file__).parent
BACKEND_DIR = BASE_DIR / "backend"
FRONTEND    = BASE_DIR / "frontend" / "index.html"

sys.path.insert(0, str(BACKEND_DIR))

# ─────────────────────────────────────────────
# PyQt6
# ─────────────────────────────────────────────
try:
    from PyQt6.QtWidgets import QApplication, QMainWindow, QSplashScreen
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    from PyQt6.QtWebEngineCore import QWebEngineSettings
    from PyQt6.QtCore import QUrl, Qt, QSize, QTimer
    from PyQt6.QtGui import QPixmap, QColor, QFont, QPainter, QPen
except ImportError:
    print("❌ PyQt6 veya PyQt6-WebEngine kurulu değil!")
    print("   pip install PyQt6 PyQt6-WebEngine")
    sys.exit(1)


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def port_is_open(host: str, port: int) -> bool:
    """Verilen port açık mı diye kontrol et"""
    try:
        with socket.create_connection((host, port), timeout=0.5):
            return True
    except OSError:
        return False


# ─────────────────────────────────────────────
# BACKEND THREAD
# ─────────────────────────────────────────────

def run_backend():
    """FastAPI + uvicorn'u bu thread içinde çalıştır"""
    try:
        import uvicorn
        uvicorn.run(
            "main:app",
            host="127.0.0.1",
            port=8000,
            log_level="warning",
            reload=False,
        )
    except Exception as e:
        print(f"❌ Backend başlatma hatası: {e}")


def start_backend_thread():
    """Backend'i daemon thread olarak başlat"""
    if port_is_open("127.0.0.1", 8000):
        print("✅ Backend zaten çalışıyor (port 8000 açık).")
        return
    print("🚀 Backend başlatılıyor...")
    t = threading.Thread(target=run_backend, daemon=True, name="FastAPI-Backend")
    t.start()


# ─────────────────────────────────────────────
# SPLASH SCREEN
# ─────────────────────────────────────────────

def make_splash() -> QSplashScreen:
    w, h = 420, 220
    pm = QPixmap(w, h)
    pm.fill(QColor("#0d0704"))

    p = QPainter(pm)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)

    # Dış çerçeve — kırmızı lak
    pen = QPen(QColor("#8c1515"))
    pen.setWidth(2)
    p.setPen(pen)
    p.drawRect(3, 3, w - 7, h - 7)

    # İç çerçeve — altın
    pen2 = QPen(QColor("#c99438"))
    pen2.setWidth(1)
    p.setPen(pen2)
    p.drawRect(8, 8, w - 17, h - 17)

    # Başlık
    p.setPen(QColor("#f5d27a"))
    f = QFont("Serif", 18, QFont.Weight.Bold)
    p.setFont(f)
    p.drawText(0, 15, w, 70, Qt.AlignmentFlag.AlignCenter, "東方 Pazar Yeri")

    # Alt yazı
    p.setPen(QColor("#9e7a3a"))
    f2 = QFont("Serif", 10)
    p.setFont(f2)
    p.drawText(0, 90, w, 35, Qt.AlignmentFlag.AlignCenter, "Pazar Yeri Açılıyor...")

    # Dekorasyon noktaları
    p.setPen(QColor("#c42b31"))
    for i, x in enumerate(range(40, w - 40, 20)):
        p.drawEllipse(x, h - 30, 4, 4)

    p.end()

    splash = QSplashScreen(pm)
    splash.setWindowFlags(
        Qt.WindowType.WindowStaysOnTopHint |
        Qt.WindowType.FramelessWindowHint
    )
    return splash


# ─────────────────────────────────────────────
# ANA PENCERE
# ─────────────────────────────────────────────

class StoreWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pazar Yeri")
        self.setMinimumSize(QSize(1000, 680))
        self.resize(1100, 760)
        self.setStyleSheet("QMainWindow { background: #0d0704; }")

        self.browser = QWebEngineView()

        # Chromium ayarları
        s = self.browser.settings()
        s.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        s.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        s.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        s.setAttribute(QWebEngineSettings.WebAttribute.ScrollAnimatorEnabled, True)
        s.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)

        # HTML yükle
        self.browser.setUrl(QUrl.fromLocalFile(str(FRONTEND)))
        self.browser.page().javaScriptConsoleMessage = self._js_log
        self.setCentralWidget(self.browser)

    def _js_log(self, level, message, line, source):
        if level >= 2 or "error" in message.lower():
            print(f"[JS ERR] {message} (line {line})")

    def closeEvent(self, event):
        print("🔴 Pazar Yeri kapatıldı.")
        event.accept()


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────

def main():
    print("=" * 45)
    print("  🏮 MMORPG Pazar Yeri Başlatılıyor")
    print("=" * 45)

    # 1. Backend thread başlat
    start_backend_thread()

    # 2. Qt uygulaması
    app = QApplication(sys.argv)
    app.setApplicationName("Pazar Yeri")
    app.setStyle("Fusion")

    # 3. Splash göster
    splash = make_splash()
    splash.show()
    app.processEvents()

    # 4. Backend hazır olana kadar bekle (max 15 sn)
    #    Qt event loop'u bloklamadan kısa döngü + processEvents
    print("⏳ Backend bekleniyor", end="", flush=True)
    deadline = time.time() + 15
    while not port_is_open("127.0.0.1", 8000):
        if time.time() > deadline:
            print("\n⚠️  Backend 15 saniyede açılmadı, yine de devam ediliyor.")
            break
        app.processEvents()
        time.sleep(0.25)
        print(".", end="", flush=True)
    else:
        print(" ✅")

    print("✅ Backend hazır, pencere açılıyor...")

    # 5. Ana pencere
    window = StoreWindow()

    def show_main():
        splash.finish(window)
        window.show()
        print("🏮 Pazar Yeri açıldı!")

    QTimer.singleShot(400, show_main)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()