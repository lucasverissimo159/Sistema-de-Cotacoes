from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTableView, QFileDialog, QLabel, 
                             QSlider, QToolButton, QMessageBox, QProgressDialog,
                             QSplitter, QFrame)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QIcon, QFont
from pathlib import Path
import pandas as pd

from .table_model import PandasModel
from ..core.data_manager import DataManager
from ..core.pdf_processor import PDFProcessor
from .styles import get_light_theme, get_dark_theme
from ..config import ZOOM_MIN, ZOOM_MAX, ZOOM_DEFAULT, ZOOM_STEP, OUTPUTS_DIR

class PDFProcessorThread(QThread):
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(list)
    error = pyqtSignal(str)
    
    def __init__(self, pdf_paths, api_key):
        super().__init__()
        self.pdf_paths = pdf_paths
        self.api_key = api_key
    
    def run(self):
        try:
            processor = PDFProcessor(self.api_key)
            all_data = []
            
            for i, pdf_path in enumerate(self.pdf_paths):
                filename = Path(pdf_path).name
                self.progress.emit(
                    int((i / len(self.pdf_paths)) * 100),
                    f"Processando {filename}..."
                )
                
                data = processor.process_pdf_with_ai(pdf_path)
                all_data.extend(data)
            
            self.progress.emit(100, "Processamento concluído!")
            self.finished.emit(all_data)
            
        except Exception as e:
            self.error.emit(str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data_manager = DataManager()
        self.zoom_level = ZOOM_DEFAULT
        self.is_dark_theme = False
        
        self.setWindowTitle("Sistema de Cotações Pro v3.1 - AI Edition")
        self.setGeometry(100, 100, 1400, 800)
        
        self.setup_ui()
        self.apply_theme()
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        header_layout = QHBoxLayout()
        
        title_layout = QVBoxLayout()
        title_label = QLabel("Sistema de Cotações Pro v3.1")
        title_label.setObjectName("titleLabel")
        subtitle_label = QLabel("Processamento inteligente com IA")
        subtitle_label.setObjectName("subtitleLabel")
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        header_layout.addLayout(title_layout)
        
        header_layout.addStretch()
        
        self.theme_button = QToolButton()
        self.theme_button.setText("🌓")
        self.theme_button.setCheckable(True)
        self.theme_button.setFixedSize(40, 40)
        self.theme_button.clicked.connect(self.toggle_theme)
        header_layout.addWidget(self.theme_button)
        
        main_layout.addLayout(header_layout)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        self.import_pdf_btn = QPushButton("🤖 Importar PDFs com IA")
        self.import_pdf_btn.setObjectName("importButton")
        self.import_pdf_btn.setMinimumHeight(45)
        self.import_pdf_btn.clicked.connect(self.import_pdfs)
        button_layout.addWidget(self.import_pdf_btn)
        
        self.load_excel_btn = QPushButton("📂 Carregar Excel")
        self.load_excel_btn.setMinimumHeight(45)
        self.load_excel_btn.clicked.connect(self.load_excel)
        button_layout.addWidget(self.load_excel_btn)
        
        self.save_excel_btn = QPushButton("💾 Salvar")
        self.save_excel_btn.setMinimumHeight(45)
        self.save_excel_btn.clicked.connect(self.save_excel)
        button_layout.addWidget(self.save_excel_btn)
        
        self.compare_btn = QPushButton("🔍 Comparar Preços")
        self.compare_btn.setObjectName("compareButton")
        self.compare_btn.setMinimumHeight(45)
        self.compare_btn.clicked.connect(self.compare_prices)
        button_layout.addWidget(self.compare_btn)
        
        self.clear_btn = QPushButton("🗑️ Limpar")
        self.clear_btn.setMinimumHeight(45)
        self.clear_btn.clicked.connect(self.clear_data)
        button_layout.addWidget(self.clear_btn)
        
        main_layout.addLayout(button_layout)
        
        self.table_view = QTableView()
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSortingEnabled(True)
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        
        self.model = PandasModel()
        self.table_view.setModel(self.model)
        
        main_layout.addWidget(self.table_view, stretch=1)
        
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)
        
        self.status_label = QLabel("Pronto para processar cotações")
        bottom_layout.addWidget(self.status_label)
        
        bottom_layout.addStretch()
        
        zoom_layout = QHBoxLayout()
        zoom_layout.setSpacing(10)
        
        zoom_label = QLabel("Zoom:")
        zoom_layout.addWidget(zoom_label)
        
        self.zoom_slider = QSlider(Qt.Orientation.Horizontal)
        self.zoom_slider.setMinimum(int(ZOOM_MIN * 100))
        self.zoom_slider.setMaximum(int(ZOOM_MAX * 100))
        self.zoom_slider.setValue(int(ZOOM_DEFAULT * 100))
        self.zoom_slider.setFixedWidth(150)
        self.zoom_slider.valueChanged.connect(self.update_zoom)
        zoom_layout.addWidget(self.zoom_slider)
        
        self.zoom_value_label = QLabel(f"{int(ZOOM_DEFAULT * 100)}%")
        self.zoom_value_label.setMinimumWidth(50)
        zoom_layout.addWidget(self.zoom_value_label)
        
        bottom_layout.addLayout(zoom_layout)
        
        main_layout.addLayout(bottom_layout)
    
    def import_pdfs(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Selecionar PDFs de Cotações",
            "",
            "PDF Files (*.pdf)"
        )
        
        if not files:
            return
        
        from ..config import GROQ_API_KEY
        if not GROQ_API_KEY:
            QMessageBox.critical(
                self,
                "API Key não configurada",
                "Configure a variável de ambiente GROQ_API_KEY antes de usar esta funcionalidade.\n\n"
                "Consulte o arquivo CONFIGURACAO_GROQ.md para instruções."
            )
            return
        
        progress_dialog = QProgressDialog("Processando PDFs...", "Cancelar", 0, 100, self)
        progress_dialog.setWindowTitle("Processamento com IA")
        progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        progress_dialog.setMinimumDuration(0)
        progress_dialog.setValue(0)
        
        self.processor_thread = PDFProcessorThread(files, GROQ_API_KEY)
        self.processor_thread.progress.connect(
            lambda val, msg: (progress_dialog.setValue(val), progress_dialog.setLabelText(msg))
        )
        self.processor_thread.finished.connect(
            lambda data: self.on_pdfs_processed(data, progress_dialog)
        )
        self.processor_thread.error.connect(
            lambda msg: self.on_processing_error(msg, progress_dialog)
        )
        
        self.processor_thread.start()
    
    def on_pdfs_processed(self, data, progress_dialog):
        progress_dialog.close()
        
        if not data:
            QMessageBox.warning(self, "Aviso", "Nenhum dado foi extraído dos PDFs.")
            return
        
        self.data_manager.add_rows(data)
        self.model.update_dataframe(self.data_manager.get_dataframe())
        
        self.status_label.setText(f"✅ {len(data)} itens importados com sucesso!")
        
        QMessageBox.information(
            self,
            "Sucesso",
            f"✅ {len(data)} produtos importados!\n\n"
            "⚠️ IMPORTANTE: Revise os dados extraídos antes de salvar.\n"
            "A IA tem ~95% de precisão."
        )
    
    def on_processing_error(self, error_msg, progress_dialog):
        progress_dialog.close()
        QMessageBox.critical(self, "Erro no Processamento", f"Erro ao processar PDFs:\n\n{error_msg}")
        self.status_label.setText("❌ Erro no processamento")
    
    def load_excel(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Abrir Arquivo Excel",
            "",
            "Excel Files (*.xlsx *.xls)"
        )
        
        if file_path:
            try:
                self.data_manager.load_excel(file_path)
                self.model.update_dataframe(self.data_manager.get_dataframe())
                self.status_label.setText(f"✅ Arquivo carregado: {Path(file_path).name}")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao carregar arquivo:\n{str(e)}")
    
    def save_excel(self):
        if self.data_manager.df is None or self.data_manager.df.empty:
            QMessageBox.warning(self, "Aviso", "Não há dados para salvar.")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar Arquivo Excel",
            str(OUTPUTS_DIR / "cotacoes.xlsx"),
            "Excel Files (*.xlsx)"
        )
        
        if file_path:
            try:
                self.data_manager.df = self.model.get_dataframe()
                saved_path = self.data_manager.save_excel(file_path)
                self.status_label.setText(f"✅ Salvo: {Path(saved_path).name}")
                QMessageBox.information(self, "Sucesso", f"Arquivo salvo com sucesso!\n\n{saved_path}")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao salvar arquivo:\n{str(e)}")
    
    def compare_prices(self):
        if self.data_manager.df is None or self.data_manager.df.empty:
            QMessageBox.warning(self, "Aviso", "Carregue dados antes de comparar preços.")
            return
        
        output_path = OUTPUTS_DIR / f"comparacao_precos.xlsx"
        
        try:
            self.data_manager.df = self.model.get_dataframe()
            result_path = self.data_manager.create_comparison(str(output_path))
            
            self.status_label.setText("✅ Comparação gerada!")
            
            QMessageBox.information(
                self,
                "Comparação Gerada",
                f"✅ Comparação de preços criada!\n\n"
                f"📁 Arquivo: {result_path}\n\n"
                f"🟢 Linhas em verde = Melhor preço por produto"
            )
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao criar comparação:\n{str(e)}")
    
    def clear_data(self):
        reply = QMessageBox.question(
            self,
            "Confirmar",
            "Tem certeza que deseja limpar todos os dados?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.data_manager.clear_data()
            self.model.update_dataframe(pd.DataFrame())
            self.status_label.setText("Dados limpos")
    
    def update_zoom(self, value):
        self.zoom_level = value / 100
        self.zoom_value_label.setText(f"{value}%")
        
        font = self.table_view.font()
        base_size = 14
        font.setPointSize(int(base_size * self.zoom_level))
        self.table_view.setFont(font)
        
        self.table_view.verticalHeader().setDefaultSectionSize(int(30 * self.zoom_level))
    
    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        self.apply_theme()
    
    def apply_theme(self):
        if self.is_dark_theme:
            self.setStyleSheet(get_dark_theme())
        else:
            self.setStyleSheet(get_light_theme())
