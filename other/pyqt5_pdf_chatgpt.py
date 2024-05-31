import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QListWidget
import fitz  # PyMuPDF


class PDFProcessor:
    def __init__(self, pdf_path, selected_pages):
        self.pdf_path = pdf_path
        self.selected_pages = selected_pages

    def process_pdf(self):
        # Hier implementieren Sie Ihre Logik zur Verarbeitung der ausgewählten Seiten
        # Zum Beispiel: Extrahieren von Text, Erstellen von Statistiken usw.
        result = f"Verarbeitung der PDF-Datei {self.pdf_path} abgeschlossen.\n"
        result += f"Ausgewählte Seiten: {', '.join(map(str, self.selected_pages))}"
        return result


class PDFViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.pdf_path = None
        self.selected_pages = []

        self.init_ui()

    def init_ui(self):
        # Erste Maske: PDF hochladen
        self.layout1 = QVBoxLayout()

        self.btn_upload = QPushButton('PDF hochladen', self)
        self.btn_upload.clicked.connect(self.upload_pdf)
        self.layout1.addWidget(self.btn_upload)

        self.setLayout(self.layout1)
        self.setWindowTitle('PDF Viewer')
        self.show()

    def upload_pdf(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("PDF-Dateien (*.pdf)")
        file_dialog.setWindowTitle("PDF-Datei auswählen")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setOptions(options)

        if file_dialog.exec_() == QFileDialog.Accepted:
            self.pdf_path = file_dialog.selectedFiles()[0]

            # Aktuelles Layout entfernen
            if self.layout():
                self.layout().deleteLater()

            # Zweite Maske: Seiten auswählen
            self.layout2 = QVBoxLayout()

            self.label2 = QLabel('Wählen Sie die Seiten aus:')
            self.layout2.addWidget(self.label2)

            self.list_widget = QListWidget(self)
            self.layout2.addWidget(self.list_widget)

            self.btn_process = QPushButton('Verarbeiten', self)
            self.btn_process.clicked.connect(self.process_pdf)
            self.layout2.addWidget(self.btn_process)

            # Neues Layout hinzufügen
            self.setLayout(self.layout2)

            self.setWindowTitle('PDF Viewer - Seiten auswählen')
            self.show()

            self.load_pdf_pages()

    def load_pdf_pages(self):
        doc = fitz.open(self.pdf_path)
        for page_num in range(doc.page_count):
            item = self.list_widget.addItem(f"Seite {page_num + 1}")

    def process_pdf(self):
        selected_items = self.list_widget.selectedItems()
        self.selected_pages = [int(item.text().split()[1]) for item in selected_items]

        # Dritte Maske: Ergebnisse anzeigen
        self.layout3 = QVBoxLayout()

        self.label3 = QLabel('Ergebnisse:')
        self.layout3.addWidget(self.label3)

        pdf_processor = PDFProcessor(self.pdf_path, self.selected_pages)
        result_text = pdf_processor.process_pdf()

        self.label_result = QLabel(result_text)
        self.layout3.addWidget(self.label_result)

        self.btn_restart = QPushButton('Zurück zum Start', self)
        self.btn_restart.clicked.connect(self.restart_app)
        self.layout3.addWidget(self.btn_restart)

        self.setLayout(self.layout3)
        self.setWindowTitle('PDF Viewer - Ergebnisse')
        self.show()

    def restart_app(self):
        # Zurück zum Startbildschirm
        self.close()
        self.__init__()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = PDFViewer()
    sys.exit(app.exec_())
