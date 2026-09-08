import tkinter as tk
import unittest

from app.ui import Dashboard


class FakeTexts:
    def get(self, _key, default=""):
        return default


class FakeLogger:
    def recent(self, _limit=100):
        return [
            {"time": "2026-09-08T01:00:00+00:00", "severity": "INFO", "area": "START", "summary": "Start ok",
             "safe_action": "Keine", "next_step": "Nichts", "event_id": "E1", "technical_cause": "Normal",
             "exception_type": None, "trace": None, "regression": None},
            {"time": "2026-09-08T01:01:00+00:00", "severity": "FEHLER", "area": "IMPORT", "summary": "Import fehlgeschlagen",
             "safe_action": "Abgebrochen", "next_step": "Datei prüfen", "event_id": "E2", "technical_cause": "Datei fehlt",
             "exception_type": "FileNotFoundError", "trace": "Spur", "regression": {"count": 3, "first_seen": "2026-09-08T00:30:00+00:00", "signature": "abc"}},
        ]

    @staticmethod
    def human_report(event):
        return str(event)


class RecoveryUiGuiTests(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.geometry("900x650")
        self.dashboard = Dashboard(self.root, FakeTexts(), FakeLogger())
        self.root.update_idletasks()
        self.root.update()

    def tearDown(self):
        for child in list(self.root.winfo_children()):
            if isinstance(child, tk.Toplevel):
                child.destroy()
        self.root.destroy()

    def test_keyboard_focus_chain_and_shortcuts_exist(self):
        self.assertTrue(str(self.dashboard.severity_filter.cget("takefocus")))
        self.assertTrue(str(self.dashboard.area_filter.cget("takefocus")))
        self.assertTrue(str(self.dashboard.zoom_filter.cget("takefocus")))
        self.assertTrue(str(self.dashboard.table.cget("takefocus")))
        self.assertTrue(str(self.dashboard.open_button.cget("takefocus")))
        self.assertTrue(self.dashboard.table.bind("<Return>"))
        self.assertTrue(self.dashboard.table.bind("<Double-1>"))
        self.assertTrue(self.root.bind("<F5>"))
        self.assertTrue(self.root.bind("<Control-plus>"))
        self.assertTrue(self.root.bind("<Control-minus>"))
        first_next = self.root.tk.call("tk_focusNext", self.dashboard.severity_filter._w)
        self.assertTrue(first_next)

    def test_filters_table_and_enter_target(self):
        self.assertEqual(len(self.dashboard.table.get_children()), 2)
        self.dashboard.severity_var.set("FEHLER")
        self.dashboard._apply_filters()
        self.assertEqual(len(self.dashboard.table.get_children()), 1)
        selected = self.dashboard.selected_event()
        self.assertEqual(selected["area"], "IMPORT")

    def test_zoom_changes_central_style_and_keeps_supported_value(self):
        self.dashboard.set_zoom(150)
        self.assertEqual(self.dashboard.zoom_percent, 150)
        self.assertEqual(self.dashboard.zoom_var.get(), "150 %")
        rowheight = int(self.dashboard.table.tk.call("ttk::style", "lookup", "Treeview", "-rowheight"))
        self.assertGreaterEqual(rowheight, 40)

    def test_event_details_open_with_technical_section_collapsed(self):
        self.dashboard.open_selected_event()
        self.root.update_idletasks()
        windows = [child for child in self.root.winfo_children() if isinstance(child, tk.Toplevel)]
        self.assertEqual(len(windows), 1)
        buttons = []
        def walk(widget):
            for child in widget.winfo_children():
                if child.winfo_class() == "TButton":
                    buttons.append(str(child.cget("text")))
                walk(child)
        walk(windows[0])
        self.assertIn("Technische Details anzeigen", buttons)
        self.assertNotIn("Technische Details ausblenden", buttons)
        self.assertTrue(windows[0].bind("<Escape>"))


if __name__ == "__main__":
    unittest.main()
