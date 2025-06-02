import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

# UI 파일(app.ui) 경로
ui_file = '/Users/gimhuidong/RAG_project/app.ui'

class MyWindow(QMainWindow): # 화면을 띄우는데 사용되는 class선언
    def __init__(self):
        super().__init__()
        uic.loadUi(ui_file, self)  # .ui 파일 로드 # datetimeEdit 위젯을 버튼처럼 클릭 이벤트 연결


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()  # UI 표시
    sys.exit(app.exec_())  # 이벤트 루프 시작
