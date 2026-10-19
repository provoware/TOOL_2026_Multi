"""Flüchtige Strukturfarben und begrenzte Gliederung; gespeicherter Text bleibt Klartext."""
import re
from PySide6.QtCore import QEvent, Qt, QSignalBlocker, QTimer
from PySide6.QtGui import QColor, QFont, QSyntaxHighlighter, QTextCharFormat, QTextCursor
from PySide6.QtWidgets import QCheckBox, QComboBox, QHBoxLayout
from app.module_widgets import t
from app.ui_standards import DEFAULT_THEME, theme_colors

MAX_OUTLINE_LINES = 5000
MAX_HEADINGS = 200


def classify(text, in_code=False):
    if text.strip().startswith('```'):
        return 'code', not in_code
    if in_code:
        return 'code', True
    if re.match(r'^\s{0,3}#{1,6}\s+\S', text) or re.fullmatch(r'\[[^\]\r\n]{1,80}\]\s*', text):
        return 'heading', False
    if re.match(r'^\s*(?:[-*]\s*)?\[[ xX]\]\s+\S', text):
        return 'task', False
    return '', False


class StructureHighlighter(QSyntaxHighlighter):
    def __init__(self, editor):
        super().__init__(editor.document())
        self.editor, self.enabled = editor, True
        self.theme_name = None
        self.formats = {}
        self.pending = False
        editor.installEventFilter(self)
        self.refresh_theme()

    def refresh_theme(self):
        self.pending = False
        self.theme_name = getattr(self.editor.window(), 'theme_name', DEFAULT_THEME)
        colors = theme_colors(self.theme_name)
        for kind in ('heading', 'task', 'code'):
            fmt = QTextCharFormat()
            fmt.setForeground(QColor(colors['accent'] if kind != 'code' else colors['text']))
            if kind == 'heading':fmt.setFontWeight(QFont.Bold)
            if kind == 'task':fmt.setFontUnderline(True)
            if kind == 'code':fmt.setFontFamilies(['monospace'])
            self.formats[kind] = fmt
        self.rehighlight()

    def eventFilter(self, watched, event):
        if event.type() in (QEvent.StyleChange, QEvent.PaletteChange) and not self.pending:
            self.pending = True
            QTimer.singleShot(0, self.refresh_theme)
        return super().eventFilter(watched, event)

    def set_enabled(self, enabled):
        self.enabled = bool(enabled)
        self.rehighlight()

    def highlightBlock(self, text):
        kind, code = classify(text, self.previousBlockState() == 1)
        self.setCurrentBlockState(1 if code else 0)
        if self.enabled and kind:
            self.setFormat(0, max(0, self.currentBlock().length() - 1), self.formats[kind])


def install_structure_tools(editor, layout):
    row = QHBoxLayout()
    toggle = QCheckBox(t('structure_colors', 'Strukturfarben'))
    toggle.setChecked(True)
    toggle.setToolTip(t('structure_hint', 'Überschriften (# oder [Bereich]), Aufgaben ([ ]) und Codeblöcke (```) optisch hervorheben. Gespeichert bleibt unveränderter Klartext.'))
    outline = QComboBox()
    outline.setAccessibleName(t('structure_outline', 'Gliederung: zur Überschrift springen'))
    row.addWidget(toggle)
    row.addWidget(outline, 1)
    layout.addLayout(row)
    highlighter = StructureHighlighter(editor)
    toggle.toggled.connect(highlighter.set_enabled)
    timer = QTimer(editor)
    timer.setSingleShot(True)
    timer.setInterval(250)

    def update_outline():
        previous = outline.currentData()
        with QSignalBlocker(outline):
            outline.clear()
            outline.addItem(t('structure_jump', 'Zur Überschrift springen …'), None)
            block, code, count = editor.document().firstBlock(), False, 0
            while block.isValid() and block.blockNumber() < MAX_OUTLINE_LINES and count < MAX_HEADINGS:
                kind, code = classify(block.text(), code)
                if kind == 'heading':
                    outline.addItem(block.text()[:120], block.blockNumber())
                    count += 1
                block = block.next()
            if block.isValid():
                outline.addItem(t('structure_limited', 'Gliederung begrenzt: erste 5000 Zeilen / 200 Überschriften'), None)
            index = outline.findData(previous)
            outline.setCurrentIndex(max(0, index))

    def jump(index):
        number = outline.itemData(index)
        if number is not None:
            block = editor.document().findBlockByNumber(number)
            if block.isValid():
                editor.setTextCursor(QTextCursor(block))
                editor.ensureCursorVisible()
                editor.setFocus()

    editor.textChanged.connect(lambda: timer.start())
    timer.timeout.connect(update_outline)
    outline.activated.connect(jump)
    update_outline()
    # Explizite Referenzen halten die kurzlebigen Qt-Helfer beim Editor.
    editor.structure_highlighter = highlighter
    editor.structure_outline = outline
    editor.structure_toggle = toggle
    editor.structure_timer = timer
    return highlighter
