"""Zentrale, UI-unabhängige Hilfetexte und Suche für Provoware."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HelpTopic:
    """Ein laienfreundliches Hilfethema mit klaren Handlungsschritten."""

    key: str
    title: str
    keywords: tuple[str, ...]
    summary: str
    steps: tuple[str, ...]
    alternative: str = ""
    note: str = ""

    def searchable_text(self) -> str:
        return " ".join((self.title, *self.keywords, self.summary, *self.steps, self.alternative, self.note))

    def render(self) -> str:
        lines = [self.title, "", self.summary, "", "So gehst du vor:"]
        lines.extend(f"{index}. {step}" for index, step in enumerate(self.steps, start=1))
        if self.alternative:
            lines.extend(("", f"Alternative: {self.alternative}"))
        if self.note:
            lines.extend(("", f"Wichtig: {self.note}"))
        return "\n".join(lines)


def _normalise(value: str) -> str:
    replacements = str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"})
    return " ".join(value.casefold().translate(replacements).split())


HELP_TOPICS: tuple[HelpTopic, ...] = (
    HelpTopic(
        "erste-schritte",
        "Erste Schritte",
        ("start", "anfang", "dashboard", "übersicht", "oeffnen", "module"),
        "Wenn du nicht weißt, wo du anfangen sollst, bleib zuerst im Dashboard. Fertige Bereiche sind direkt nutzbar; geplante Bereiche verändern keine Daten.",
        (
            "Öffne links den Bereich, den du wirklich bearbeiten möchtest.",
            "Nutze Songtexte, Texteditor, Charakterfibel, Vorgaben, Todo oder Kalender nur nacheinander, wenn du den Überblick behalten möchtest.",
            "Achte unten beziehungsweise im Modul auf die Statusmeldung nach dem Speichern.",
            "Bei einer roten Meldung öffne Hilfe & Fehlerhilfe und wechsle zu Fehlermeldungen.",
        ),
        "Mit F1 öffnest du diese Hilfe jederzeit aus dem Dashboard.",
    ),
    HelpTopic(
        "songtexte",
        "Songtexte schreiben und speichern",
        ("song", "songtext", "strophe", "refrain", "speichern", "version", "export"),
        "Der Songeditor speichert strukturierte Songbereiche sicher und legt Versionen an, ohne ältere Stände still zu überschreiben.",
        (
            "Öffne Songtexte und wähle einen vorhandenen Song oder lege einen neuen an.",
            "Schreibe in den gewünschten Bereich; eigene Bereichsnamen sind ebenfalls möglich.",
            "Speichere mit der Schaltfläche oder Strg+S.",
            "Prüfe die sichtbare Rückmeldung. Erst eine erfolgreiche Rückmeldung bedeutet, dass der neue Stand geschrieben wurde.",
        ),
        "Für extern vorbereitete Songtexte gibt es oben die JSON-Importvorlage.",
        "Charaktermarker verwenden absichtlich «…» und nicht [ … ], damit sie nicht mit Songbereichen kollidieren.",
    ),
    HelpTopic(
        "texteditor-charaktere",
        "Texteditor und Charakterfibel",
        ("texteditor", "text", "charakter", "figur", "fibel", "rolle", "referenz"),
        "Charaktere werden zentral in der Charakterfibel verwaltet und können in mehreren Schreibbereichen wiederverwendet werden.",
        (
            "Lege Figuren zuerst in der Charakterfibel an oder bearbeite sie dort.",
            "Öffne anschließend Texteditor oder Songeditor.",
            "Wähle die gewünschte Figur aus der Charakterliste.",
            "Füge die Referenz ein beziehungsweise verknüpfe sie mit dem Text.",
        ),
        "Wenn eine Figur nicht mehr angeboten wird, aktualisiere die Liste und prüfe, ob sie in der Charakterfibel noch vorhanden ist.",
    ),
    HelpTopic(
        "vorgaben-planung",
        "Vorgaben, Todo und Kalender",
        ("genre", "stimmung", "stil", "stimme", "todo", "aufgabe", "kalender", "termin", "erinnerung"),
        "Vorgaben helfen beim Wiederverwenden kreativer Einstellungen; Todo und Kalender halten Aufgaben und Termine getrennt von den Schreibinhalten.",
        (
            "Pflege wiederkehrende Genres, Stimmungen, Stile, Stimmen und Besonderheiten unter Vorgaben.",
            "Lege Aufgaben in der Todo-Liste an und hake sie erst nach Erledigung ab.",
            "Lege Termine im Kalender an; Erinnerungen funktionieren, solange das Hauptprogramm läuft.",
            "Prüfe nach Änderungen die Statusmeldung des jeweiligen Fensters.",
        ),
        "Mehrere Vorgaben können als Komma-Liste eingegeben werden; Dubletten werden nicht still doppelt gespeichert.",
    ),
    HelpTopic(
        "daten-sicherheit",
        "Wo sind meine Daten?",
        ("daten", "ordner", "backup", "sicherung", "speicher", "datei", "versionen", "export"),
        "Provoware trennt Programmdateien, Nutzerdaten, Berichte, Protokolle und Sicherungen. Nutzerdaten liegen im Projektordner unter daten/.",
        (
            "Songtexte findest du unter daten/songtexte/.",
            "Charaktere liegen unter daten/charaktere/, allgemeine Texte unter daten/texte/.",
            "Todo und Kalender liegen in ihren eigenen Unterordnern von daten/.",
            "Berichte, Logs und Backups liegen getrennt in berichte/, logs/ und backups/ und werden nicht als Quellcode versioniert.",
        ),
        "Vor manuellen Änderungen an Datenordnern zuerst ein Backup erstellen.",
        "Das Programm verwendet atomare Schreibwege, damit ein Fehler beim Schreiben nicht einfach den vorherigen gültigen Stand ersetzt.",
    ),
    HelpTopic(
        "fehler-beheben",
        "Fehler verstehen und sicher reagieren",
        ("fehler", "recovery", "problem", "rot", "warnung", "absturz", "meldung", "diagnose"),
        "Bei Problemen zeigt Provoware zuerst eine einfache Erklärung, die Schutzmaßnahme und den empfohlenen nächsten Schritt. Technische Details sind optional.",
        (
            "Wechsle oben auf den Reiter Fehlermeldungen.",
            "Wähle die neueste passende Meldung aus.",
            "Öffne sie und lies zuerst Was wurde geschützt? und Was soll ich jetzt tun?.",
            "Zeige technische Details nur an, wenn du sie für die Fehlersuche oder zum Weitergeben brauchst.",
        ),
        "Mit F5 lädst du die Meldungsliste neu.",
        "Wiederhole riskante Aktionen nicht mehrfach, wenn dieselbe Fehlermeldung erneut erscheint.",
    ),
    HelpTopic(
        "kubuntu-abnahme",
        "Kubuntu 26.04 / Wayland prüfen",
        ("kubuntu", "wayland", "plasma", "abnahme", "zoom", "125", "150", "175", "200", "kontrast"),
        "Die automatische Prüfung testet Qt unter Wayland, ersetzt aber nicht die sichtbare Endabnahme auf deinem echten Kubuntu-Desktop.",
        (
            "Starte im Projektordner ./kubuntu_abnahme.sh.",
            "Prüfe besonders 1366×768 bei 125 % und 150 %.",
            "Prüfe zusätzlich 175 %, 200 % und das Theme Kontrast.",
            "Achte auf abgeschnittene Texte, verdeckte Schaltflächen, Fokus, Menüs und Eingabefelder.",
        ),
        "Wenn die Abnahme X11/XWayland meldet, melde dich ab und starte eine echte Plasma-Wayland-Sitzung.",
    ),
    HelpTopic(
        "tastatur-anzeige",
        "Anzeige, Zoom und Tastatur",
        ("zoom", "schrift", "tastatur", "shortcut", "strg", "mausrad", "f1", "f5", "barrierefrei"),
        "Zoom und Tastaturwege bleiben in allen wichtigen Bereichen verfügbar, damit die Bedienung auch bei großer Schrift praktikabel bleibt.",
        (
            "Strg+Mausrad, Strg++ und Strg+- ändern die Anzeigegröße.",
            "Strg+0 setzt auf 100 % zurück.",
            "F1 öffnet Hilfe & Fehlerhilfe.",
            "F5 aktualisiert Listen beziehungsweise die aktuelle Hilfeansicht, wenn dort Daten neu geladen werden können.",
        ),
        "Unterstützte Zoomstufen sind 100 %, 125 %, 150 %, 175 % und 200 %.",
    ),
)


def help_topics(query: str = "") -> tuple[HelpTopic, ...]:
    """Liefert Hilfethemen in stabiler Reihenfolge; Suchbegriffe werden UND-verknüpft."""

    terms = tuple(term for term in _normalise(query).split(" ") if term)
    if not terms:
        return HELP_TOPICS
    result: list[HelpTopic] = []
    for topic in HELP_TOPICS:
        haystack = _normalise(topic.searchable_text())
        if all(term in haystack for term in terms):
            result.append(topic)
    return tuple(result)


def help_topic_by_key(key: str) -> HelpTopic | None:
    return next((topic for topic in HELP_TOPICS if topic.key == key), None)
