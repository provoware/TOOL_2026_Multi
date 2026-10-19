"""Benutzbare Formulardatensätze mit ausdrücklicher Rechtebestätigung."""
from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit, QLabel, QListWidget, QMessageBox, QPushButton
from app import module_permissions, module_runtime


class ModuleRecordsDialog(QDialog):
    def __init__(self, root, module_id, parent=None):
        super().__init__(parent)
        self.root, self.module_id = root, module_id
        self.blueprint = module_runtime.definition(root, module_id)
        if self.blueprint is None:
            raise ValueError("Modulentwurf nicht vorhanden.")
        self.setWindowTitle("Moduldaten · " + self.blueprint["title"])
        self.resize(660, 550)
        layout=QVBoxLayout(self)
        layout.addWidget(QLabel("Nur freigegebene Datenfelder. Keine fremde Programmausführung."))
        self.search=QLineEdit()
        self.search.setPlaceholderText("Gespeicherte Inhalte suchen")
        self.search.setEnabled("search" in self.blueprint["capabilities"])
        layout.addWidget(self.search)
        self.items=QListWidget()
        self.items.setAccessibleName("Gespeicherte Moduldatensätze")
        layout.addWidget(self.items)
        form=QFormLayout()
        layout.addLayout(form)
        self.editors={}
        for field in self.blueprint["fields"]:
            editor=QTextEdit() if field["type"]=="paragraph" else QLineEdit()
            editor.setAccessibleName(field["label"])
            if field["type"]=="paragraph":
                editor.setMaximumHeight(100)
            editor.setEnabled("edit" in self.blueprint["capabilities"])
            form.addRow(field["label"],editor)
            self.editors[field["id"]]=editor
        self.status=QLabel("")
        self.status.setWordWrap(True)
        layout.addWidget(self.status)
        self.save_button=QPushButton("Datensatz nach Bestätigung speichern")
        self.save_button.setEnabled("edit" in self.blueprint["capabilities"])
        self.save_button.clicked.connect(self.save_record)
        layout.addWidget(self.save_button)
        self.search.textChanged.connect(self.refresh)
        self.refresh()

    def refresh(self):
        try:
            records=module_runtime.query(self.root,self.module_id,self.search.text())
            self.items.clear()
            for record in records:
                preview=" · ".join(str(v)[:55] for v in record["values"].values())
                self.items.addItem(preview or "Leerer Datensatz")
            self.status.setText(str(len(records))+" Datensätze vorhanden.")
        except (OSError,ValueError) as exc:
            self.status.setText("Daten nicht lesbar: "+str(exc))

    def save_record(self):
        if QMessageBox.question(self,"Bearbeitung freigeben",
            "Einen neuen lokalen Datensatz in diesem Modul speichern?",
            QMessageBox.Yes|QMessageBox.No,QMessageBox.No)!=QMessageBox.Yes:
            return False
        values={key:(editor.toPlainText() if isinstance(editor,QTextEdit) else editor.text())
                for key,editor in self.editors.items()}
        try:
            module_permissions.dispatch(self.root,self.module_id,"edit",
                                         approved=True,values=values)
            self.refresh()
            self.status.setText("Datensatz sicher gespeichert.")
            return True
        except (ValueError,OSError,PermissionError) as exc:
            self.status.setText("Nicht gespeichert: "+str(exc))
            return False
