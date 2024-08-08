# 빌드 구문
# pyinstaller --onefile --noconsole --icon=app_icon.ico --add-data "app_icon.png;." main.py

import sys
import os
import csv
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QComboBox
from PyQt5.QtGui import QIcon

class SimpleDiaryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Simple Diary')

        # 아이콘 설정
        icon_path = self.resource_path('app_icon.png')
        self.setWindowIcon(QIcon(icon_path))

        # 레이아웃 설정
        layout = QVBoxLayout()

        # 카테고리 선택 박스
        self.category_combo = QComboBox()
        self.category_combo.addItem("메모")
        self.category_combo.addItem("완료")

        # 텍스트 필드
        self.text_field = QLineEdit()
        self.text_field.setPlaceholderText("내용을 작성하세요...")
        self.text_field.returnPressed.connect(self.save_entry)

        # 확인 버튼
        self.save_button = QPushButton('확인')
        self.save_button.clicked.connect(self.save_entry)

        # 레이아웃 정리
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.category_combo)
        h_layout.addWidget(self.text_field)
        h_layout.addWidget(self.save_button)

        layout.addLayout(h_layout)
        self.setLayout(layout)

    def resource_path(self, relative_path):
        """ PyInstaller로 패키징된 후에도 리소스를 찾기 위한 경로 설정 """
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def save_entry(self):
        # 현재 날짜와 시간
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 선택된 카테고리
        category = self.category_combo.currentText()
        
        # 작성된 내용
        content = self.text_field.text()

        # 데이터가 비어 있지 않은지 확인
        if content.strip():
            # 저장할 파일 경로 설정
            file_path = os.path.join(os.path.dirname(sys.executable), 'simple diary data.tsv')

            # 파일에 데이터 저장
            with open(file_path, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter='\t')
                writer.writerow([now, category, content])

            # 텍스트 필드 초기화
            self.text_field.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    diary_app = SimpleDiaryApp()
    diary_app.show()
    sys.exit(app.exec_())
