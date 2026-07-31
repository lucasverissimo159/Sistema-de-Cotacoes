def get_light_theme():
    return """
    QMainWindow {
        background-color: #FFFFFF;
    }
    
    QWidget {
        background-color: #FFFFFF;
        color: #1A1A1A;
        font-family: 'Inter', 'Segoe UI', sans-serif;
        font-size: 14px;
    }
    
    QPushButton {
        background-color: #4F46E5;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        font-size: 14px;
    }
    
    QPushButton:hover {
        background-color: #4338CA;
    }
    
    QPushButton:pressed {
        background-color: #3730A3;
    }
    
    QPushButton:disabled {
        background-color: #E5E7EB;
        color: #9CA3AF;
    }
    
    QPushButton#importButton {
        background-color: #F59E0B;
    }
    
    QPushButton#importButton:hover {
        background-color: #D97706;
    }
    
    QPushButton#compareButton {
        background-color: #10B981;
    }
    
    QPushButton#compareButton:hover {
        background-color: #059669;
    }
    
    QTableView {
        background-color: white;
        alternate-background-color: #F9FAFB;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        gridline-color: #E5E7EB;
    }
    
    QTableView::item {
        padding: 8px;
        border-bottom: 1px solid #F3F4F6;
    }
    
    QTableView::item:selected {
        background-color: #EEF2FF;
        color: #1A1A1A;
    }
    
    QHeaderView::section {
        background-color: #4F46E5;
        color: white;
        padding: 12px;
        border: none;
        font-weight: 600;
        font-size: 13px;
    }
    
    QSlider::groove:horizontal {
        border: 1px solid #E5E7EB;
        height: 6px;
        background: #F3F4F6;
        border-radius: 3px;
    }
    
    QSlider::handle:horizontal {
        background: #4F46E5;
        border: none;
        width: 16px;
        height: 16px;
        margin: -5px 0;
        border-radius: 8px;
    }
    
    QSlider::handle:horizontal:hover {
        background: #4338CA;
    }
    
    QProgressBar {
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        text-align: center;
        background-color: #F3F4F6;
        color: #1A1A1A;
        font-weight: 600;
    }
    
    QProgressBar::chunk {
        background-color: #4F46E5;
        border-radius: 7px;
    }
    
    QLabel {
        color: #1A1A1A;
        font-size: 14px;
    }
    
    QLabel#titleLabel {
        font-size: 24px;
        font-weight: 700;
        color: #1A1A1A;
    }
    
    QLabel#subtitleLabel {
        font-size: 14px;
        color: #6B7280;
    }
    
    QToolButton {
        background-color: transparent;
        border: none;
        border-radius: 6px;
        padding: 8px;
    }
    
    QToolButton:hover {
        background-color: #F3F4F6;
    }
    
    QToolButton:checked {
        background-color: #EEF2FF;
        color: #4F46E5;
    }
    
    QScrollBar:vertical {
        border: none;
        background: #F9FAFB;
        width: 12px;
        border-radius: 6px;
    }
    
    QScrollBar::handle:vertical {
        background: #D1D5DB;
        border-radius: 6px;
        min-height: 20px;
    }
    
    QScrollBar::handle:vertical:hover {
        background: #9CA3AF;
    }
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }
    """

def get_dark_theme():
    return """
    QMainWindow {
        background-color: #0F172A;
    }
    
    QWidget {
        background-color: #0F172A;
        color: #F1F5F9;
        font-family: 'Inter', 'Segoe UI', sans-serif;
        font-size: 14px;
    }
    
    QPushButton {
        background-color: #6366F1;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        font-size: 14px;
    }
    
    QPushButton:hover {
        background-color: #4F46E5;
    }
    
    QPushButton:pressed {
        background-color: #4338CA;
    }
    
    QPushButton:disabled {
        background-color: #1E293B;
        color: #475569;
    }
    
    QPushButton#importButton {
        background-color: #F59E0B;
    }
    
    QPushButton#importButton:hover {
        background-color: #D97706;
    }
    
    QPushButton#compareButton {
        background-color: #10B981;
    }
    
    QPushButton#compareButton:hover {
        background-color: #059669;
    }
    
    QTableView {
        background-color: #1E293B;
        alternate-background-color: #0F172A;
        border: 1px solid #334155;
        border-radius: 8px;
        gridline-color: #334155;
        color: #F1F5F9;
    }
    
    QTableView::item {
        padding: 8px;
        border-bottom: 1px solid #1E293B;
    }
    
    QTableView::item:selected {
        background-color: #312E81;
        color: #F1F5F9;
    }
    
    QHeaderView::section {
        background-color: #1E293B;
        color: #F1F5F9;
        padding: 12px;
        border: 1px solid #334155;
        font-weight: 600;
        font-size: 13px;
    }
    
    QSlider::groove:horizontal {
        border: 1px solid #334155;
        height: 6px;
        background: #1E293B;
        border-radius: 3px;
    }
    
    QSlider::handle:horizontal {
        background: #6366F1;
        border: none;
        width: 16px;
        height: 16px;
        margin: -5px 0;
        border-radius: 8px;
    }
    
    QSlider::handle:horizontal:hover {
        background: #4F46E5;
    }
    
    QProgressBar {
        border: 1px solid #334155;
        border-radius: 8px;
        text-align: center;
        background-color: #1E293B;
        color: #F1F5F9;
        font-weight: 600;
    }
    
    QProgressBar::chunk {
        background-color: #6366F1;
        border-radius: 7px;
    }
    
    QLabel {
        color: #F1F5F9;
        font-size: 14px;
    }
    
    QLabel#titleLabel {
        font-size: 24px;
        font-weight: 700;
        color: #F1F5F9;
    }
    
    QLabel#subtitleLabel {
        font-size: 14px;
        color: #94A3B8;
    }
    
    QToolButton {
        background-color: transparent;
        border: none;
        border-radius: 6px;
        padding: 8px;
        color: #F1F5F9;
    }
    
    QToolButton:hover {
        background-color: #1E293B;
    }
    
    QToolButton:checked {
        background-color: #312E81;
        color: #A5B4FC;
    }
    
    QScrollBar:vertical {
        border: none;
        background: #1E293B;
        width: 12px;
        border-radius: 6px;
    }
    
    QScrollBar::handle:vertical {
        background: #475569;
        border-radius: 6px;
        min-height: 20px;
    }
    
    QScrollBar::handle:vertical:hover {
        background: #64748B;
    }
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }
    """
