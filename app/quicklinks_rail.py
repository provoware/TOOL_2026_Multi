"""Kompakte rechte Schnellstarter-Leiste, bei wenig Platz bewusst ausgeblendet."""
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout, QWidget
from app import quicklinks_store as store
from app.account_store import validate_url


class QuicklinksRail(QFrame):
    def __init__(self, root, on_manage, parent=None):
        super().__init__(parent)
        self.root, self.on_manage = root, on_manage
        self.setObjectName('quicklinksRail')
        self.setFixedWidth(92)
        self.box = QVBoxLayout(self)
        self.box.setContentsMargins(4, 6, 4, 6)
        self.box.setSpacing(5)
        title = QLabel('Links')
        title.setAccessibleName('Rechte Link-Schnellstarter-Leiste')
        self.box.addWidget(title)
        self.items = QVBoxLayout()
        self.box.addLayout(self.items)
        self.box.addStretch(1)
        manage = QPushButton('Liste')
        manage.setObjectName('quicklinks_manage_button')
        manage.setAccessibleName('Link-Schnellstarter verwalten')
        manage.setToolTip('Namen, Gruppen und Webadressen der Schnellstarter verwalten')
        manage.clicked.connect(on_manage)
        self.box.addWidget(manage)
        self.refresh()

    def refresh(self):
        while self.items.count():
            item = self.items.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        try:
            links = store.load(self.root)['links']
        except (ValueError, OSError):
            message = QLabel('Links nicht lesbar')
            message.setWordWrap(True)
            self.items.addWidget(message)
            return
        for entry in sorted(links, key=lambda x: (x['group'].casefold(), x['name'].casefold()))[:6]:
            name, url = entry['name'], entry['url']
            label = (entry['icon'] or '↗') + '\n' + (name[:10] + '…' if len(name) > 11 else name)
            action = QPushButton(label)
            action.setAccessibleName('Webseite öffnen: ' + name)
            action.setToolTip(name + '\n' + url)
            action.clicked.connect(lambda _checked=False, target=url: self.open_url(target))
            self.items.addWidget(action)
        if not links:
            hint = QLabel('Keine Links')
            hint.setWordWrap(True)
            self.items.addWidget(hint)
        elif len(links) > 6:
            rest = QPushButton('Weitere…')
            rest.setAccessibleName('Weitere Schnellstarter verwalten')
            rest.clicked.connect(self.on_manage)
            self.items.addWidget(rest)

    @staticmethod
    def open_url(url):
        try:
            return bool(QDesktopServices.openUrl(QUrl(validate_url(url))))
        except ValueError:
            return False
