"""Optionale deutsche Rechtschreibprüfung ohne Netzübertragung oder neue Pflichtpakete."""
from __future__ import annotations

import re
import shutil
import subprocess
from PySide6.QtWidgets import QInputDialog, QMessageBox
from app.module_widgets import t


def check_words(content):
    command = shutil.which('aspell')
    if command is None:
        raise ValueError(t('spell_missing', 'Die lokale Rechtschreibprüfung benötigt aspell und aspell-de. Unter Kubuntu können diese über die Softwareverwaltung installiert werden.'))
    # List-Modus liefert nur unbekannte Wörter; keine Protokoll-Steuerzeichen aus Nutzertext.
    result = subprocess.run([command, 'list', '--lang=de_DE'], input=content,
                            capture_output=True, text=True, timeout=5, check=False)
    if result.returncode:
        raise ValueError(t('dictionary_missing', 'Das deutsche Wörterbuch ist nicht verfügbar. Bitte aspell-de installieren.'))
    return list(dict.fromkeys(result.stdout.splitlines()))


def check_editor(parent, editor):
    try:
        words = check_words(editor.toPlainText())
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        QMessageBox.information(parent, t('spelling', 'Rechtschreibung prüfen'), str(error))
        return
    if not words:
        QMessageBox.information(parent, t('spelling', 'Rechtschreibung prüfen'),
                                t('spell_ok', 'Keine unbekannten Wörter gefunden. Namen und Fachbegriffe bitte selbst prüfen.'))
        return
    word, ok = QInputDialog.getItem(parent, t('spelling', 'Rechtschreibung prüfen'),
                                    t('unknown_word', 'Unbekanntes Wort auswählen (Namen können korrekt sein):'), words, 0, False)
    if not ok:
        return
    replacement, ok = QInputDialog.getText(parent, t('replace', 'Wort korrigieren'),
                                          t('replacement', 'Korrekte Schreibweise (ersetzt alle gleichen Wörter):'), text=word)
    if ok and replacement and replacement != word:
        cursor = editor.textCursor()
        cursor.select(cursor.SelectionType.Document)
        cursor.insertText(re.sub(r'(?<!\w)' + re.escape(word) + r'(?!\w)', lambda _: replacement, editor.toPlainText()))
