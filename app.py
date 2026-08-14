import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from cotacoes.ui.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Sistema de Cotações Pro v3.1")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())
