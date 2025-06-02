from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from PyQt5.QtCore import QObject, pyqtSignal
from cctv_veiwer import CCTVViewer
from image_list import ImageBrowserWidget
from PyQt5.QtCore import QTimer, QDateTime


class WorkerSignals(QObject):
    detection_made = pyqtSignal()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("app.ui", self)
        self.signals = WorkerSignals()
        self.cctv_viewer = CCTVViewer(signals=self.signals)
        self.start_clock() # 시간 업데이트 시작

        # 📌 중앙 영상 출력 레이아웃 구성
        if not self.cctvviwer_screen.layout():
            self.cctvviwer_screen.setLayout(QVBoxLayout())
        layout = self.cctvviwer_screen.layout()
        layout.addWidget(self.cctv_viewer.video_frame)
        layout.addWidget(self.cctv_viewer.play_button)
        layout.addWidget(self.cctv_viewer.stop_button)

        # 📌 오른쪽 이미지 리스트 연결
        self.image_browser = ImageBrowserWidget()
        self.signals.detection_made.connect(self.image_browser.handle_new_detection)
        if hasattr(self, "right_panel") and self.right_panel:
            if not self.right_panel.layout():
                self.right_panel.setLayout(QVBoxLayout())
            self.right_panel.layout().addWidget(self.image_browser)

        # 📌 ComboBox에 서울 CCTV 리스트 추가
        self.seoul_cctvs = [
            c for c in self.cctv_viewer.cctv_list if "서울" in c["cctvname"]
        ]
        for cctv in self.seoul_cctvs:
            self.SEOUL_button.addItem(cctv["cctvname"])

        self.SEOUL_button.currentTextChanged.connect(self.on_location_selected)

    def on_location_selected(self, selected_name):
        # 이름으로 CCTV 검색
        match = next((c for c in self.seoul_cctvs if c["cctvname"] == selected_name), None)
        if match:
            self.cctv_viewer.play_stream(match["cctvurl"], match["cctvname"])
        else:
            print("선택한 이름에 해당하는 CCTV 없음")

    def closeEvent(self, event):
        if self.cctv_viewer.worker:
            self.cctv_viewer.worker.stop()
            self.cctv_viewer.worker.join()
        event.accept()

    def start_clock(self): # 시간표시기능 함수1
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 1초마다 업데이트

    def update_time(self): # 시간표시기능 함수2
        current_time = QDateTime.currentDateTime()
        self.timescreen.setDateTime(current_time)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

