import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import Qt, QRect

class NineZoneBox(QWidget):
    def __init__(self):
        super().__init__()
        # 在 __init__ 中添加这两行
        self.setObjectName("niri-snip-box")
        self.setWindowTitle("niri-snip-box")
        # 设置窗口无边框、置顶、背景透明
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # 初始样式：亮绿色方框
        self.setStyleSheet("border: 3px solid #00ff00; background-color: rgba(0, 255, 0, 30);")
        
        # 获取屏幕尺寸并计算九宫格
        self.screen_geom = QApplication.primaryScreen().geometry()
        self.setup_initial_zone()
        self.show()

    def setWindowProperties(self):
        # 这一行决定了 Niri 能不能抓到 app-id
        self.setWindowRole("niri-snip-box")
        self.setObjectName("niri-snip-box")
        # 在 Wayland 下，Qt 通常使用程序名作为 app-id
        QApplication.setDesktopFileName("niri-snip-box")
    def setup_initial_zone(self):
        print("请在小键盘或数字键选择区域 (1-9):")
        # 简化逻辑：直接选定一个默认区域或等待输入
        # 这里默认选正中间 (区域5)
        self.move_to_zone(5)

    def move_to_zone(self, zone):
        w = self.screen_geom.width() // 3
        h = self.screen_geom.height() // 3
        idx = zone - 1
        x = (idx % 3) * w
        y = (idx // 3) * h
        self.setGeometry(x + 50, y + 50, w - 100, h - 100)

    def keyPressEvent(self, event):
        key = event.key()
        mod = event.modifiers()
        step = 20  # 移动/缩放步长
        geom = self.geometry()

        # Alt 键按下：调整边界 (Size)
        if mod & Qt.KeyboardModifier.AltModifier:
            if key == Qt.Key.Key_I: self.setFixedHeight(geom.height() - step)
            elif key == Qt.Key.Key_K: self.setFixedHeight(geom.height() + step)
            elif key == Qt.Key.Key_J: self.setFixedWidth(geom.width() - step)
            elif key == Qt.Key.Key_L: self.setFixedWidth(geom.width() + step)
        # 普通按下：移动位置 (Move)
        else:
            if key == Qt.Key.Key_I: self.move(geom.x(), geom.y() - step)
            elif key == Qt.Key.Key_K: self.move(geom.x(), geom.y() + step)
            elif key == Qt.Key.Key_J: self.move(geom.x() - step, geom.y())
            elif key == Qt.Key.Key_L: self.move(geom.x() + step, geom.y())
            # 数字键切换区域
            elif Qt.Key.Key_1 <= key <= Qt.Key.Key_9:
                self.move_to_zone(key - Qt.Key.Key_0)
            # 退出
            elif key == Qt.Key.Key_Escape:
                self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NineZoneBox()
    sys.exit(app.exec())
