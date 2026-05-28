#!/usr/bin/env python3
import sys
import os
import asyncio
import threading
import pyperclip
import subprocess
import signal
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QFrame
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QPoint, QTimer
from PyQt6.QtGui import QCursor
from deep_translator import GoogleTranslator
import edge_tts

# --- 配置 ---
TARGET_LANG = 'zh-CN'
VOICE = 'en-US-GuyNeural' 

# 異步語音迴圈
main_loop = asyncio.new_event_loop()
def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()
threading.Thread(target=start_loop, args=(main_loop,), daemon=True).start()

async def play_audio(text):
    path = "/tmp/niri_voice.mp3"
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(path)
    subprocess.run(["mpv", "--no-video", "--really-quiet", path])

class Worker(QThread):
    new_data = pyqtSignal(str, str)
    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        translator = GoogleTranslator(source='auto', target=TARGET_LANG)
        last_text = ""
        while self._run_flag:
            current_text = pyperclip.paste().strip()
            if current_text and current_text != last_text and len(current_text) < 1000:
                try:
                    trans_text = translator.translate(current_text)
                    self.new_data.emit(current_text, trans_text)
                    asyncio.run_coroutine_threadsafe(play_audio(current_text), main_loop)
                except: pass
                last_text = current_text
            self.msleep(400)

class FloatWindow(QWidget):
    def __init__(self):
        super().__init__()
        # 改用 Window 類型並加上 Bypass 標誌，避開 Wayland 的 Popup 限制
        self.setWindowFlags(
            Qt.WindowType.Window | 
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.X11BypassWindowManagerHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # 給視窗一個固定的標題，方便 Niri 規則匹配
        self.setWindowTitle("NiriPopupTranslator")
        
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(33, 37, 43, 240);
                border: 1px solid #61afef;
                border-radius: 6px;
                padding: 10px;
            }
            QLabel#Orig { color: #5c6370; font-size: 11px; }
            QLabel#Trans { color: #e5c07b; font-size: 15px; font-weight: bold; }
        """)

        layout = QVBoxLayout(self)
        self.container = QFrame()
        self.inner_layout = QVBoxLayout(self.container)
        
        self.orig_label = QLabel("原文")
        self.orig_label.setObjectName("Orig")
        self.orig_label.setWordWrap(True)
        
        self.trans_label = QLabel("翻譯")
        self.trans_label.setObjectName("Trans")
        self.trans_label.setWordWrap(True)
        
        self.inner_layout.addWidget(self.orig_label)
        self.inner_layout.addWidget(self.trans_label)
        layout.addWidget(self.container)
        self.setFixedWidth(280)

    def update_data(self, orig, trans):
        self.orig_label.setText(orig)
        self.trans_label.setText(trans)
        self.adjustSize()
        
        # 獲取滑鼠位置並移動
        pos = QCursor.pos()
        self.move(pos + QPoint(15, 15))
        
        self.show()
        # 自動隱藏計時器（4秒後消失，避免視窗殘留）
        QTimer.singleShot(10000, self.hide)
        
    def mousePressEvent(self, event):
        self.hide()

def shutdown(signum, frame):
    print("\n正在關閉腳本...")
    os._exit(0)

if __name__ == "__main__":
    # 處理 Ctrl+C 退出
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    os.environ["QT_QPA_PLATFORM"] = "wayland"
    app = QApplication(sys.argv)
    
    win = FloatWindow()
    worker = Worker()
    worker.new_data.connect(win.update_data)
    worker.start()
    
    print("🚀 鼠標隨身翻譯已啟動 (Python 3.14)...")
    try:
        sys.exit(app.exec())
    except SystemExit:
        os._exit(0)
