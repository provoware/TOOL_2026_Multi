"""Freie Kontometadaten als bearbeitbare Tabelle statt sichtbarem Speicherformat."""
import json
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QApplication, QLineEdit
from app.module_widgets import button, t


class CustomFieldsEditor(QWidget):
    def __init__(self):
        super().__init__()
        box=QVBoxLayout(self);box.setContentsMargins(0,0,0,0)
        self.table=QTableWidget(0,2)
        self.table.setAccessibleName(t('account_custom','Eigene Zusatzfelder'))
        self.table.setHorizontalHeaderLabels([t('custom_name','Feldname'),t('custom_value','Wert')])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setMinimumHeight(130);self.table.setMaximumHeight(220)
        box.addWidget(self.table)
        row=QHBoxLayout();box.addLayout(row)
        self.add_button=button(row,t('custom_add','Feld ergänzen'),self.add_field)
        button(row,t('custom_remove','Ausgewähltes Feld entfernen'),self.remove_field)

    def rows(self):
        rows = [(self.table.item(row,0).text() if self.table.item(row,0) else '',
                 self.table.item(row,1).text() if self.table.item(row,1) else '')
                for row in range(self.table.rowCount())]
        focused = QApplication.focusWidget()
        index = self.table.currentIndex()
        if isinstance(focused, QLineEdit) and self.table.isAncestorOf(focused) and index.isValid():
            row = list(rows[index.row()])
            row[index.column()] = focused.text()
            rows[index.row()] = tuple(row)
        return rows

    def text(self):
        # Snapshot enthält auch leere/noch doppelte Entwurfszeilen, ohne sie zu speichern.
        return json.dumps(self.rows(),ensure_ascii=False)

    def values(self):
        result,seen={},set()
        for raw_name,value in self.rows():
            name=raw_name.strip()
            if not name and not value:continue
            if not name or name.casefold() in seen:
                raise ValueError(t('custom_duplicate','Jedes Zusatzfeld braucht einen eigenen, nicht leeren Namen.'))
            seen.add(name.casefold());result[name]=value
        return result

    def setText(self,value):
        raw=json.loads(value)
        if not isinstance(raw,dict):raise ValueError('Zusatzfelder benötigen eine Feldzuordnung.')
        self.clear()
        for name,text in raw.items():
            row=self.table.rowCount();self.table.insertRow(row)
            self.table.setItem(row,0,QTableWidgetItem(name));self.table.setItem(row,1,QTableWidgetItem(text))
        self.add_button.setEnabled(self.table.rowCount()<30)

    def clear(self):
        self.table.setRowCount(0);self.add_button.setEnabled(True)

    def add_field(self):
        if self.table.rowCount()>=30:return
        row=self.table.rowCount();self.table.insertRow(row)
        self.table.setItem(row,0,QTableWidgetItem(''));self.table.setItem(row,1,QTableWidgetItem(''))
        self.table.setCurrentCell(row,0);self.table.editItem(self.table.item(row,0))
        self.add_button.setEnabled(self.table.rowCount()<30)

    def remove_field(self):
        row=self.table.currentRow()
        if row>=0:self.table.removeRow(row)
        self.add_button.setEnabled(self.table.rowCount()<30)
