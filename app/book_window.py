"""Einfacher Bucharbeitsplatz: Vorlage wählen, Kapitel ordnen, schreiben und ausgeben."""
from __future__ import annotations

from copy import deepcopy
import json
from PySide6.QtCore import QSignalBlocker, Qt, QTimer
from PySide6.QtWidgets import (
    QComboBox, QFileDialog, QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QMessageBox, QSplitter, QTabWidget, QTextEdit, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget,
)
from app import book_store as store
from app.module_archive import export_target
from app.atomic_io import atomic_write_text
from app.character_combo import refresh_character_combo
from app.character_store import character_marker
from app.module_widgets import ModuleWindow, button, scroll_panel, t
from app.spelling import check_editor


class BookWindow(ModuleWindow):
    module, collection = store.MODULE, 'books'
    validate = staticmethod(store.validate)

    def __init__(self, root, zoom_percent=100, parent=None):
        super().__init__(root, t('books', 'Buchwerkstatt'), zoom_percent, parent)
        self.book = store.new_book()
        self.current_chapter = None
        self._loading = False
        self._build()
        self._display_book()
        self.finish()
        self.refresh()
        self.autosave = QTimer(self)
        self.autosave.setInterval(60_000)
        self.autosave.timeout.connect(self._autosave)
        self.autosave.start()

    def load_state(self):
        return store.load(self.root)

    def import_copies(self, data):
        return store.import_copies(self.root, data)

    def _build(self):
        self.tabs = QTabWidget()
        self.outer.addWidget(self.tabs, 1)
        self._library()
        self._workspace()
        self._details()

    def _library(self):
        panel, layout = scroll_panel()
        self.tabs.addTab(panel, t('library', 'Bücher & Vorlagen').replace('&', '&&'))
        hint = QLabel(t('book_hint', '1. Vorlage wählen und neues Buch beginnen. 2. Titel eingeben. 3. Kapitel auswählen und schreiben. Strg+S speichert; betitelte Entwürfe werden zusätzlich jede Minute gespeichert.'))
        hint.setWordWrap(True)
        layout.addWidget(hint)
        self.template = QComboBox()
        self.template.addItems(store.KINDS)
        self.template.setAccessibleName(t('template', 'Buchvorlage'))
        layout.addWidget(self.template)
        button(layout, t('new_book', 'Neues Buch aus Vorlage'), self.new_book)
        self.library_search = QLineEdit()
        self.library_search.setPlaceholderText(t('find_book', 'Bücher nach Titel suchen …'))
        self.library_search.setAccessibleName(t('find_book', 'Bücher nach Titel suchen …'))
        self.library_search.textChanged.connect(self.refresh)
        layout.addWidget(self.library_search)
        self.books = QComboBox()
        self.books.setAccessibleName(t('saved_books', 'Gespeicherte Bücher'))
        layout.addWidget(self.books)
        button(layout, t('open_book', 'Gewähltes Buch öffnen'), self.open_book)
        button(layout, t('copy_book', 'Aktuelles Buch als neue Fassung kopieren'), self.copy_book)
        button(layout, t('manuscript', 'Manuskript als Markdown oder Text exportieren'), self.export_manuscript)
        layout.addStretch()

    def _workspace(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        self.tabs.addTab(page, t('write', 'Kapitel & Schreiben').replace('&', '&&'))
        self.title = QLineEdit()
        self.title.setPlaceholderText(t('book_title', 'Buchtitel *'))
        self.title.setAccessibleName(t('book_title', 'Buchtitel *'))
        layout.addWidget(self.title)
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self._chapter_panel())
        self.splitter.addWidget(self._editor_panel())
        self.splitter.setSizes([320, 740])
        layout.addWidget(self.splitter, 1)
        self.count = QLabel()
        self.count.setWordWrap(True)
        layout.addWidget(self.count)
        button(layout, t('save_book', 'Buch jetzt speichern'), self.save).setObjectName('primaryButton')

    def _chapter_panel(self):
        left, tree_box = scroll_panel()
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel(t('chapters', 'Kapitel und Unterkapitel'))
        self.tree.setAccessibleName(t('chapters', 'Kapitel und Unterkapitel'))
        self.tree.setMinimumHeight(180)
        self.tree.currentItemChanged.connect(self._select_chapter)
        tree_box.addWidget(self.tree, 1)
        actions = QGridLayout()
        options = [(t('add_chapter', '＋ Kapitel'), lambda: self.add_chapter(False)),
                   (t('add_subchapter', '＋ Unterkapitel'), lambda: self.add_chapter(True)),
                   (t('up', '↑ Nach oben'), lambda: self.move(-1)),
                   (t('down', '↓ Nach unten'), lambda: self.move(1)),
                   (t('outdent', 'Eine Ebene höher'), self.outdent),
                   (t('remove_chapter', 'Kapitel entfernen'), self.remove_chapter)]
        for index, (label, action) in enumerate(options):
            cell = QHBoxLayout()
            button(cell, label, action)
            actions.addLayout(cell, index // 2, index % 2)
        tree_box.addLayout(actions)
        return left

    def _editor_panel(self):
        right, work = scroll_panel()
        self.chapter_title = QLineEdit()
        self.chapter_title.setAccessibleName(t('chapter_title', 'Kapiteltitel'))
        self.chapter_title.setPlaceholderText(t('chapter_title', 'Kapiteltitel'))
        work.addWidget(self.chapter_title)
        self.chapter_status = QComboBox()
        self.chapter_status.addItems(['Entwurf', 'Überarbeiten', 'Fertig'])
        self.chapter_status.setAccessibleName(t('chapter_status', 'Bearbeitungsstand des Kapitels'))
        work.addWidget(self.chapter_status)
        self.content = QTextEdit()
        self.content.setAcceptRichText(False)
        self.content.setMinimumHeight(230)
        self.content.setAccessibleName(t('chapter_text', 'Kapiteltext'))
        self.content.textChanged.connect(self._count)
        work.addWidget(self.content, 1)
        self.elements = QComboBox()
        self.elements.setAccessibleName(t('elements', 'Hilfreiche Textelemente'))
        work.addWidget(self.elements)
        button(work, t('insert_element', 'Textelement an Schreibposition einfügen'), self.insert_element)
        self.characters = QComboBox()
        self.characters.setAccessibleName(t('characters', 'Figuren aus der Charakterfibel'))
        work.addWidget(self.characters)
        button(work, t('insert_character', 'Figur aus Charakterfibel einfügen'), self.insert_character)
        button(work, t('spelling', 'Rechtschreibung prüfen'), lambda: check_editor(self, self.content))
        work.addWidget(QLabel(t('chapter_notes', 'Kapitelnotizen – erscheinen nicht im Manuskript')))
        self.chapter_notes = QTextEdit()
        self.chapter_notes.setAccessibleName(t('chapter_notes', 'Kapitelnotizen – erscheinen nicht im Manuskript'))
        self.chapter_notes.setMaximumHeight(100)
        work.addWidget(self.chapter_notes)
        return right

    def _details(self):
        panel, layout = scroll_panel()
        self.tabs.addTab(panel, t('planning', 'Planung & Notizen').replace('&', '&&'))
        layout.addWidget(QLabel(t('audience', 'Für wen schreibst du?')))
        self.audience = QLineEdit()
        self.audience.setAccessibleName(t('audience', 'Für wen schreibst du?'))
        layout.addWidget(self.audience)
        layout.addWidget(QLabel(t('book_notes', 'Ideen, Recherche, Quellen, rote Fäden und offene Punkte')))
        self.notes = QTextEdit()
        self.notes.setAccessibleName(t('book_notes', 'Ideen, Recherche, Quellen, rote Fäden und offene Punkte'))
        self.notes.setMinimumHeight(220)
        layout.addWidget(self.notes, 1)
        note = QLabel(t('book_export_hint', 'JSON-Export sichert Bücher einschließlich Kapitelstruktur und Notizen. Manuskript-Export enthält Buchtitel, Kapitelüberschriften und Texte in deiner Reihenfolge.'))
        note.setWordWrap(True)
        layout.addWidget(note)

    def _draft(self):
        draft = deepcopy(self.book)
        draft.update(title=self.title.text(), audience=self.audience.text(), notes=self.notes.toPlainText())
        for chapter in draft['chapters']:
            if chapter['id'] == self.current_chapter:
                chapter.update(title=self.chapter_title.text(), content=self.content.toPlainText(),
                               notes=self.chapter_notes.toPlainText(), status=self.chapter_status.currentText())
        return draft

    def snapshot(self):
        return json.dumps(self._draft(), ensure_ascii=False, sort_keys=True)

    def _flush(self):
        self.book = self._draft()

    def _display_book(self):
        self._loading = True
        self.current_chapter = None
        self.title.setText(self.book['title'])
        self.audience.setText(self.book['audience'])
        self.notes.setPlainText(self.book['notes'])
        self.elements.clear()
        for name, content in store.ELEMENTS[self.book['kind']].items():
            self.elements.addItem(name, content)
        self._tree()
        self._loading = False
        first = self.tree.topLevelItem(0)
        self.tree.setCurrentItem(first)
        if first is None:
            self._show_chapter(None)
        self._count()

    def _tree(self, selected=None):
        with QSignalBlocker(self.tree):
            self.tree.clear()
            items = {}
            for chapter, level in store.ordered_chapters(self.book):
                parent = items.get(chapter['parent'])
                item = QTreeWidgetItem([chapter['title'] + ' · ' + chapter['status']])
                item.setData(0, Qt.UserRole, chapter['id'])
                if parent:
                    parent.addChild(item)
                else:
                    self.tree.addTopLevelItem(item)
                items[chapter['id']] = item
            self.tree.expandAll()
            if selected in items:
                self.tree.setCurrentItem(items[selected])

    def _select_chapter(self, current, previous):
        if self._loading:
            return
        self._flush()
        key = current.data(0, Qt.UserRole) if current else None
        self._show_chapter(key)
        # Aktualisiert auch umbenannte Überschriften, ohne das Schreibfeld neu aufzubauen.
        if previous and previous.data(0, Qt.UserRole) != key:
            old = next((c for c in self.book['chapters'] if c['id'] == previous.data(0, Qt.UserRole)), None)
            if old:
                previous.setText(0, old['title'] + ' · ' + old['status'])

    def _show_chapter(self, key):
        self.current_chapter = key
        chapter = next((c for c in self.book['chapters'] if c['id'] == key), None)
        self.chapter_title.setText(chapter['title'] if chapter else '')
        self.content.setPlainText(chapter['content'] if chapter else '')
        self.chapter_notes.setPlainText(chapter['notes'] if chapter else '')
        self.chapter_status.setCurrentText(chapter['status'] if chapter else 'Entwurf')
        for widget in (self.chapter_title, self.content, self.chapter_notes, self.chapter_status):
            widget.setEnabled(chapter is not None)
        self._count()

    def refresh(self, *_args):
        try:
            state = self.load_state()
            refresh_character_combo(self.characters, self.root)
        except Exception as error:
            self.error(t('load_failed', 'Modulbestand nicht lesbar'), error)
            return
        selected = self.books.currentData()
        self.books.clear()
        needle = self.library_search.text().casefold()
        for book in state['books']:
            if needle in book['title'].casefold():
                self.books.addItem(book['title'] + ' · ' + book['kind'], book['id'])
        index = self.books.findData(selected)
        if index >= 0:
            self.books.setCurrentIndex(index)

    def discard_draft(self):
        self.book = store.new_book(self.template.currentText())
        self._display_book()
        self.remember()

    def new_book(self):
        if not self.confirm_leave():
            return
        self.book = store.new_book(self.template.currentText())
        self._display_book()
        self.remember()
        self.tabs.setCurrentIndex(1)
        self.title.setFocus()

    def open_book(self):
        key = self.books.currentData()
        if not key:
            self.status.setText(t('choose_book', 'Bitte zuerst ein gespeichertes Buch wählen.'))
            return
        if not self.confirm_leave():
            return
        try:
            self.book = next(b for b in self.load_state()['books'] if b['id'] == key)
        except Exception as error:
            self.error(t('load_failed', 'Modulbestand nicht lesbar'), error)
            return
        self._display_book()
        self.remember()
        self.tabs.setCurrentIndex(1)

    def save(self):
        try:
            self.book = store.put(self.root, self._draft())
        except Exception as error:
            self.error(t('save_failed', 'Nicht gespeichert'), error)
            return False
        self.remember()
        self._tree(self.current_chapter)
        self.refresh()
        self.status.setText(t('saved', 'Sicher gespeichert.'))
        return True

    def _autosave(self):
        if self.title.text().strip() and self.snapshot() != self._baseline:
            self.save()

    def add_chapter(self, subchapter):
        self._flush()
        if subchapter and not self.current_chapter:
            self.status.setText(t('choose_chapter', 'Bitte zuerst ein Kapitel auswählen.'))
            return
        parent = self.current_chapter if subchapter else None
        new = store.new_chapter(t('new_chapter', 'Neues Kapitel'), parent=parent)
        candidate = deepcopy(self.book)
        candidate['chapters'].append(new)
        # Strukturprüfung auch vor dem Speichern; temporärer Titel nur für die Prüfung.
        try:
            store.validate_book({**candidate, 'title': candidate['title'] or 'Entwurf'})
        except ValueError as error:
            self.error(t('chapter_failed', 'Kapitel nicht angelegt'), error)
            return
        self.book = candidate
        self._tree(new['id'])
        self._show_chapter(new['id'])
        self.chapter_title.setFocus()
        self.chapter_title.selectAll()

    def move(self, direction):
        if not self.current_chapter:
            return
        self._flush()
        store.move_chapter(self.book, self.current_chapter, direction)
        self._tree(self.current_chapter)

    def outdent(self):
        self._flush()
        chapter = next((c for c in self.book['chapters'] if c['id'] == self.current_chapter), None)
        if chapter and chapter['parent']:
            parent = next(c for c in self.book['chapters'] if c['id'] == chapter['parent'])
            chapter['parent'] = parent['parent']
            self._tree(self.current_chapter)

    def remove_chapter(self):
        if not self.current_chapter:
            return
        self._flush()
        keys = {self.current_chapter}
        for _ in range(8):
            keys.update(c['id'] for c in self.book['chapters'] if c['parent'] in keys)
        if QMessageBox.question(self, t('remove_chapter', 'Kapitel entfernen'),
                                t('remove_chapter_confirm', '{count} Kapitel einschließlich Unterkapiteln entfernen?').format(count=len(keys)),
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No) != QMessageBox.Yes:
            return
        self.book['chapters'] = [c for c in self.book['chapters'] if c['id'] not in keys]
        self.current_chapter = None
        self._tree()
        self._show_chapter(None)

    def copy_book(self):
        candidate = self._draft()
        try:
            candidate = store.validate_book(candidate)
        except ValueError as error:
            self.error(t('copy_failed', 'Nicht kopiert'), error)
            return
        if not self.confirm_leave():
            return
        self.book = store.copy_book(candidate)
        self.book['title'] += t('new_edition', ' – neue Fassung')
        self._display_book()
        self._baseline = 'unsaved-copy'
        self.tabs.setCurrentIndex(1)
        self.status.setText(t('copy_draft', 'Neue Fassung als Entwurf angelegt. Zum Behalten speichern.'))

    def insert_element(self):
        if self.current_chapter:
            self.content.insertPlainText(self.elements.currentData() or '')
            self.content.setFocus()

    def insert_character(self):
        key = self.characters.currentData()
        if not key or not self.current_chapter:
            self.status.setText(t('choose_character', 'Bitte ein Kapitel und eine Figur auswählen.'))
            return
        try:
            self.content.insertPlainText(character_marker(self.root, key))
        except Exception as error:
            self.error(t('character_failed', 'Figur nicht eingefügt'), error)

    def _count(self):
        if not hasattr(self, 'count') or not hasattr(self, 'notes'):
            return
        draft = self._draft()
        words = sum(len(c['content'].split()) for c in draft['chapters'])
        finished = sum(c['status'] == 'Fertig' for c in draft['chapters'])
        self.count.setText(t('word_count', '{words} Wörter · {finished}/{total} Kapitel fertig · ca. {minutes} Minuten bei 150 Wörtern/Minute').format(
            words=words, finished=finished, total=len(draft['chapters']), minutes=round(words / 150, 1)))

    def export_manuscript(self):
        try:
            draft = store.validate_book(self._draft())
        except ValueError as error:
            self.error(t('export_failed', 'Export fehlgeschlagen'), error)
            return
        target, selected = QFileDialog.getSaveFileName(self, t('manuscript', 'Manuskript als Markdown oder Text exportieren'),
                                                       'manuskript.md', 'Markdown (*.md);;Text (*.txt)')
        if target:
            try:
                atomic_write_text(export_target(self.root, target), store.manuscript(draft, not ('*.txt' in selected)))
                self.status.setText(t('manuscript_exported', 'Manuskript exportiert. Notizen bleiben im Buchbestand.'))
            except Exception as error:
                self.error(t('export_failed', 'Export fehlgeschlagen'), error)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._layout_direction()

    def set_zoom(self, percent):
        super().set_zoom(percent)
        self._layout_direction()

    def _layout_direction(self):
        if hasattr(self, 'splitter'):
            vertical = self.width() < 900 or self.zoom_percent >= 150
            self.splitter.setOrientation(Qt.Vertical if vertical else Qt.Horizontal)
