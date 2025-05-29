import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

# UI 파일 경로
ui_file = '/Users/gimhuidong/RAG_project/app.ui'

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(ui_file, self)  # .ui 파일 로드

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()  # UI 표시
    sys.exit(app.exec_())  # 이벤트 루프 시작
