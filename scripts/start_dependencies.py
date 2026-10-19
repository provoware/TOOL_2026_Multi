"""Prüft installierte feste Paketversionen und den tatsächlich benötigten Qt-Import."""
from importlib.metadata import version
from pathlib import Path


def check(requirements):
    for raw in Path(requirements).read_text(encoding='utf-8').splitlines():
        line = raw.split('#', 1)[0].strip()
        if not line:
            continue
        name, expected = line.split('==')
        if version(name.strip()) != expected.strip():
            raise ValueError('Installierte Paketversion stimmt nicht mit requirements.txt überein.')
    from PySide6.QtWidgets import QApplication
    return QApplication


if __name__ == '__main__':
    check(Path(__file__).resolve().parent.parent / 'requirements.txt')
