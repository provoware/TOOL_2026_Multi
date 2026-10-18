"""Laienfreundliche Textbuttons mit Workflow-Reitern und getrennter Eingabe."""
from __future__ import annotations

from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import (
    QApplication, QButtonGroup, QComboBox, QDateEdit, QFileDialog, QFrame,
    QGridLayout, QHBoxLayout, QInputDialog, QLabel, QLineEdit,
    QPushButton, QTabWidget, QTextEdit, QVBoxLayout, QWidget, QMessageBox,
)
from app import snippet_store as store
from app.module_archive import export_target
from app.atomic_io import atomic_write_text
from app.module_widgets import ModuleWindow, button, scroll_panel, t
from app.spelling import check_editor


class SnippetWindow(ModuleWindow):
    module, collection = store.MODULE, 'snippets'
    validate = staticmethod(store.validate)

    def __init__(self, root, zoom_percent=100, parent=None):
        super().__init__(root, t('snippets', 'Textbaustein-Buttons'), zoom_percent, parent)
        self.current_id = self.variant_of = None
        self.color, self.size = 'Standard', 'Mittel'
        self.state = store.empty_state()
        self._build()
        self.finish()
        self.refresh()

    def load_state(self):
        return store.load(self.root)

    def import_copies(self, data):
        return store.import_copies(self.root, data)

    def _build(self):
        self.tabs = QTabWidget()
        self.outer.addWidget(self.tabs, 1)
        library = QWidget()
        box = QVBoxLayout(library)
        row = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText(t('search_snippets', 'Titel, Kategorie oder Text suchen …'))
        self.search.setAccessibleName(t('search_snippets', 'Titel, Kategorie oder Text suchen …'))
        self.search.textChanged.connect(self._render)
        row.addWidget(self.search, 1)
        button(row, t('new_snippet', 'Neuen Button anlegen'), self.new_snippet)
        button(row, t('new_workflow', 'Workflow ergänzen'), self.add_workflow)
        box.addLayout(row)
        hint = QLabel(t('snippet_hint', 'Button drücken = Inhalt kopieren. Bearbeiten und Variante sind eigene Aktionen. ↑ / ↓ ändern die Reihenfolge innerhalb der Kategorie.'))
        hint.setWordWrap(True)
        box.addWidget(hint)
        self.arrangement = QComboBox()
        self.arrangement.addItems([t('one_column', 'Eine Spalte'), t('two_columns', 'Zwei Spalten'), t('three_columns', 'Drei Spalten')])
        self.arrangement.setCurrentIndex(1)
        self.arrangement.setAccessibleName(t('arrangement', 'Anordnung der Buttons'))
        self.arrangement.currentIndexChanged.connect(self._render)
        box.addWidget(self.arrangement)
        self.workflows = QTabWidget()
        box.addWidget(self.workflows, 1)
        self.tabs.addTab(library, t('choose', 'Buttons verwenden'))
        self._build_editor()
        self._build_stats()

    def _build_editor(self):
        scroll, form = scroll_panel()
        self.tabs.addTab(scroll, t('create_edit', 'Anlegen & bearbeiten').replace('&', '&&'))
        self.edit_heading = QLabel(t('new_snippet', 'Neuen Button anlegen'))
        self.edit_heading.setObjectName('cardTitle')
        form.addWidget(self.edit_heading)
        self.workflow = QComboBox()
        self.workflow.setAccessibleName(t('workflow', 'Workflow – Arbeitsbereich'))
        form.addWidget(QLabel(t('workflow', 'Workflow – Arbeitsbereich')))
        form.addWidget(self.workflow)
        self.category, self.title, self.content = QLineEdit(), QLineEdit(), QTextEdit()
        fields = [(t('category', 'Kategorie *'), self.category),
                  (t('button_title', 'Titel des Buttons *'), self.title),
                  (t('button_content', 'Text oder Textfragment *'), self.content)]
        for label, field in fields:
            form.addWidget(QLabel(label))
            field.setAccessibleName(label)
            form.addWidget(field)
            button(form, t('paste', 'Aus Zwischenablage einfügen'), lambda f=field: self.paste_field(f))
        self.category.setPlaceholderText(t('category_example', 'z. B. Fehleranalyse, Dialoge, Verwaltung'))
        self.content.setMinimumHeight(180)
        self.content.setAcceptRichText(False)
        self.content.setPlaceholderText(t('placeholder_example', 'Text unverändert ablegen. Platzhalter zum Beispiel: Hallo {{Name}}!'))
        tools = QHBoxLayout()
        button(tools, t('insert_placeholder', 'Platzhalter einfügen'), self.insert_placeholder)
        button(tools, t('spelling', 'Rechtschreibung prüfen'), lambda: check_editor(self, self.content))
        form.addLayout(tools)
        for attr, choices, heading in [('color', store.COLORS, t('color', 'Buttonfarbe')),
                                       ('size', store.SIZES, t('size', 'Buttongröße'))]:
            form.addWidget(QLabel(heading))
            row = QGridLayout()
            group = QButtonGroup(self)
            for index, name in enumerate(choices):
                pick = QPushButton(name)
                pick.setCheckable(True)
                pick.setAccessibleName(heading + ': ' + name)
                pick.setChecked(name == getattr(self, attr))
                group.addButton(pick)
                pick.clicked.connect(lambda _=False, a=attr, n=name: setattr(self, a, n))
                row.addWidget(pick, index // 3, index % 3)
            setattr(self, attr + '_group', group)
            form.addLayout(row)
        row = QHBoxLayout()
        button(row, t('save_button', 'Button speichern'), self.save).setObjectName('primaryButton')
        button(row, t('new_snippet', 'Neuen Button anlegen'), self.new_snippet)
        form.addLayout(row)
        form.addStretch()

    def _build_stats(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        self.month = QDateEdit(QDate.currentDate())
        self.month.setDisplayFormat('MM.yyyy')
        self.month.setCalendarPopup(True)
        self.month.setAccessibleName(t('month', 'Monat der Auswertung'))
        self.month.dateChanged.connect(self._stats)
        layout.addWidget(self.month)
        self.report = QTextEdit()
        self.report.setReadOnly(True)
        self.report.setAccessibleName(t('monthly', 'Monatliche Verwendungen'))
        layout.addWidget(self.report, 1)
        button(layout, t('report_export', 'Monatsbericht als Text exportieren'), self.export_report)
        self.tabs.addTab(panel, t('monthly', 'Monatliche Verwendungen'))

    def snapshot(self):
        return (self.workflow.currentText(), self.category.text(), self.title.text(),
                self.content.toPlainText(), self.color, self.size)

    def refresh(self):
        try:
            self.state = self.load_state()
        except Exception as error:
            self.error(t('load_failed', 'Modulbestand nicht lesbar'), error)
            return
        previous = self.workflow.currentText()
        self.workflow.clear()
        self.workflow.addItems(self.state['workflows'])
        self.workflow.setCurrentText(previous or self.state['workflows'][0])
        self._render()
        self._stats()
        # Beim ersten Laden gehört die Vorgabewahl noch nicht zu Nutzeränderungen.
        if self._baseline and self._baseline[0] == '' and not any(self._baseline[1:4]):
            self.remember()

    def _render(self, *_args):
        selected = self.workflows.tabText(self.workflows.currentIndex())
        while self.workflows.count():
            old = self.workflows.widget(0)
            self.workflows.removeTab(0)
            old.deleteLater()
        needle = self.search.text().casefold()
        for workflow in self.state['workflows']:
            scroll, column = scroll_panel()
            self.workflows.addTab(scroll, workflow)
            items = [s for s in self.state['snippets'] if s['workflow'] == workflow
                     and needle in ' '.join(str(s[f]) for f in ('title', 'category', 'content')).casefold()]
            categories = list(dict.fromkeys(s['category'] for s in items))
            if not items:
                label = QLabel(t('no_buttons', 'Noch keine passenden Buttons. Über „Neuen Button anlegen“ starten.'))
                label.setWordWrap(True)
                column.addWidget(label)
            for category in categories:
                label = QLabel(category)
                label.setTextFormat(Qt.PlainText)
                label.setObjectName('cardTitle')
                column.addWidget(label)
                grid = QGridLayout()
                available = max(1, int(self.width() / (340 * self.zoom_percent / 100)))
                columns = min(self.arrangement.currentIndex() + 1, available)
                for index, item in enumerate(s for s in items if s['category'] == category):
                    grid.addWidget(self._card(item), index // columns, index % columns)
                for col in range(columns):
                    grid.setColumnStretch(col, 1)
                column.addLayout(grid)
            column.addStretch()
            if workflow == selected:
                self.workflows.setCurrentWidget(scroll)

    def _card(self, item):
        card = QFrame()
        card.setObjectName('innerCard')
        box = QVBoxLayout(card)
        family = next((s['title'] for s in self.state['snippets'] if s['group'] == item['group']), item['title'])
        caption = QLabel(f"{family} · V{item['version']}")
        caption.setTextFormat(Qt.PlainText)
        box.addWidget(caption)
        copy = button(box, item['title'].replace('&', '&&'), lambda: self.copy(item['id']))
        copy.setAccessibleName(item['title'] + t('copy_suffix', ' – Text kopieren'))
        copy.setToolTip(item['content'][:1200])
        copy.setMinimumHeight(round({'Klein': 34, 'Mittel': 52, 'Groß': 76}[item['size']] * self.zoom_percent / 100))
        color = store.COLORS[item['color']]
        if color:
            copy.setStyleSheet(f'QPushButton {{background: {color}; color: #ffffff;}} QPushButton:focus {{border: 3px solid #ffffff;}}')
        actions = QGridLayout()
        options = [(t('edit', 'Bearbeiten'), lambda: self.edit(item['id'])),
                   (t('variant', 'Variante anlegen'), lambda: self.edit(item['id'], True)),
                   ('↑', lambda: self.move(item['id'], -1)), ('↓', lambda: self.move(item['id'], 1))]
        for col, (label, action) in enumerate(options):
            b = QPushButton(label)
            b.setAccessibleName(label + ' · ' + item['title'])
            b.clicked.connect(lambda _=False, a=action: a())
            actions.addWidget(b, col // 2, col % 2)
        box.addLayout(actions)
        return card

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'workflows'):
            self._render()

    def set_zoom(self, percent):
        super().set_zoom(percent)
        if hasattr(self, 'workflows'):
            self._render()

    def discard_draft(self):
        self.current_id = self.variant_of = None
        for field in (self.category, self.title, self.content):
            field.clear()
        self.edit_heading.setText(t('new_snippet', 'Neuen Button anlegen'))
        self.remember()

    def new_snippet(self):
        if not self.confirm_leave():
            return
        self.current_id = self.variant_of = None
        for field in (self.category, self.title, self.content):
            field.clear()
        self.edit_heading.setText(t('new_snippet', 'Neuen Button anlegen'))
        self.remember()
        self.tabs.setCurrentIndex(1)
        self.title.setFocus()

    def edit(self, key, variant=False):
        if not self.confirm_leave():
            return
        item = next(s for s in self.state['snippets'] if s['id'] == key)
        self.current_id, self.variant_of = (None, key) if variant else (key, None)
        self.workflow.setCurrentText(item['workflow'])
        self.category.setText(item['category'])
        self.title.setText(item['title'])
        self.content.setPlainText(item['content'])
        self.color, self.size = item['color'], item['size']
        for attr in ('color', 'size'):
            for b in getattr(self, attr + '_group').buttons():
                b.setChecked(b.text() == getattr(self, attr))
        self.edit_heading.setText(t('variant', 'Variante anlegen') if variant else t('edit', 'Bearbeiten'))
        self.remember()
        # Eine noch nicht gespeicherte Variante muss auch ohne Textänderung geschützt sein.
        if variant:
            self._baseline = None
            self._baseline = ('unsaved-variant',)
        self.tabs.setCurrentIndex(1)

    def save(self):
        values = dict(zip(('workflow', 'category', 'title', 'content', 'color', 'size'), self.snapshot()))
        if not self.current_id and not self.variant_of:
            duplicate = next((s for s in self.state['snippets'] if s['content'] == values['content']), None)
            if duplicate:
                answer = QMessageBox.question(self, t('duplicate', 'Gleicher Text vorhanden'),
                    t('duplicate_variant', 'Dieser Text ist bereits vorhanden. Als neue Unterversion dieses Buttons speichern?'),
                    QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)
                if answer != QMessageBox.Yes:
                    return False
                self.variant_of = duplicate['id']
        try:
            saved = store.put(self.root, values, self.current_id, self.variant_of)
        except Exception as error:
            self.error(t('save_failed', 'Nicht gespeichert'), error)
            return False
        self.current_id, self.variant_of = saved['id'], None
        self.remember()
        self.refresh()
        self.status.setText(t('saved', 'Sicher gespeichert.'))
        return True

    def copy(self, key):
        item = next(s for s in self.state['snippets'] if s['id'] == key)
        values = {}
        for name in store.placeholders(item['content']):
            value, ok = QInputDialog.getText(self, t('fill_placeholder', 'Platzhalter ausfüllen'), name + ':')
            if not ok:
                self.status.setText(t('copy_cancelled', 'Kopieren abgebrochen.'))
                return
            values[name] = value
        try:
            content = store.render(item['content'], values)
            clipboard = QApplication.clipboard()
            clipboard.setText(content)
            if clipboard.text() != content:
                raise RuntimeError(t('clipboard_failed', 'Zwischenablage hat den Text nicht übernommen.'))
        except Exception as error:
            self.error(t('copy_failed', 'Nicht kopiert'), error)
            return
        try:
            store.record_copy(self.root, key)
        except Exception as error:
            self.status.setText(t('counter_failed', 'Text kopiert; Statistik konnte nicht gespeichert werden: ') + str(error))
            return
        self.state = self.load_state()
        self._stats()
        self.status.setText(t('copied', 'Text kopiert. Mit Strg+V im Zielprogramm einfügen.'))

    def move(self, key, direction):
        try:
            store.move(self.root, key, direction)
            self.refresh()
        except Exception as error:
            self.error(t('move_failed', 'Reihenfolge nicht gespeichert'), error)

    def add_workflow(self):
        name, ok = QInputDialog.getText(self, t('new_workflow', 'Workflow ergänzen'), t('workflow_name', 'Name des neuen Arbeitsbereichs:'))
        if ok:
            try:
                store.add_workflow(self.root, name)
                self.refresh()
            except Exception as error:
                self.error(t('save_failed', 'Nicht gespeichert'), error)

    def insert_placeholder(self):
        name, ok = QInputDialog.getText(self, t('insert_placeholder', 'Platzhalter einfügen'), t('placeholder_name', 'Was soll später ausgefüllt werden? Zum Beispiel Name oder Thema:'))
        if ok and name.strip() and not any(c in name for c in '{}\n'):
            self.content.insertPlainText('{{' + name.strip()[:80] + '}}')

    def _stats(self, *_args):
        if hasattr(self, 'report'):
            self.report.setPlainText(store.monthly_report(self.state, self.month.date().toString('yyyy-MM')))

    def export_report(self):
        target, _ = QFileDialog.getSaveFileName(self, t('report_export', 'Monatsbericht als Text exportieren'), 'textbausteine-' + self.month.date().toString('yyyy-MM') + '.txt', 'Text (*.txt)')
        if target:
            try:
                atomic_write_text(export_target(self.root, target), self.report.toPlainText())
                self.status.setText(t('exported', 'Gespeicherter Modulbestand exportiert.'))
            except Exception as error:
                self.error(t('export_failed', 'Export fehlgeschlagen'), error)
