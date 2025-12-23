from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog


def print_widget_with_dialog(parent, widget, title: str = "Print") -> bool:
    """Open a print dialog and render the given widget if accepted."""
    printer = QPrinter(QPrinter.PrinterMode.HighResolution)
    dialog = QPrintDialog(printer, parent)
    dialog.setWindowTitle(title)

    if dialog.exec() != QPrintDialog.DialogCode.Accepted:
        return False

    painter = QPainter(printer)
    try:
        viewport = painter.viewport()
        size = widget.size()
        size.scale(viewport.size(), Qt.AspectRatioMode.KeepAspectRatio)
        painter.setViewport(viewport.x(), viewport.y(), size.width(), size.height())
        painter.setWindow(widget.rect())
        widget.render(painter)
    finally:
        painter.end()

    return True
