"""Lesbare Auswertung ausschließlich aus den erlaubten lokalen Leistungsaggregaten."""
from app.performance import BUCKETS, validate

OP_LABELS = {'app.start': 'Dashboard-Start', 'module.open': 'Modul öffnen',
             'archive.load': 'Modulbestand lesen', 'file.write': 'Text/JSON schreiben',
             'save.attempt': 'Gültiger Speicherversuch'}
AREA_LABELS = {'app': 'Programm', 'books': 'Bücher', 'snippets': 'Textbuttons',
               'songs': 'Songtexte', 'texts': 'Texteditor', 'profiles': 'Profile',
               'todo': 'Aufgaben', 'calendar': 'Kalender', 'characters': 'Figuren',
               'diagnostics': 'Diagnose', 'exports': 'Ausgabe', 'other': 'Sonstiges'}


def percentile_bucket(row, fraction):
    goal = max(1, int(row['count'] * fraction + 0.999999))
    total = 0
    for index, count in enumerate(row['buckets']):
        total += count
        if total >= goal:
            return f'≤ {BUCKETS[index]} ms' if index < len(BUCKETS) else '> 10000 ms'
    return 'nicht ermittelt'


def report(payload):
    data = validate(payload)
    lines = ['Leistung & Verbesserung · lokale Tagesübersicht',
             'Laufzeiten in Millisekunden; Bytes sind logische Nutzdaten, keine SSD-Schreibmengen.',
             'Keine Texte, Titel, Zwischenablageinhalte oder Dateipfade enthalten.', '']
    if not data['days']:
        lines.append('Für diese Auswahl sind noch keine Messwerte vorhanden.')
    for day, rows in sorted(data['days'].items(), reverse=True):
        lines.extend([day, ''])
        for key, row in sorted(rows.items()):
            version, operation, area = key.split('|')
            lines.append(f"{OP_LABELS[operation]} · {AREA_LABELS[area]} · Version {version}")
            lines.append(f"  Anzahl: {row['count']} · Fehler: {row['errors']} · Unverändert: {row['unchanged']} · Bytes: {row['bytes']}")
            if operation != 'save.attempt' and row['count']:
                lines.append(f"  Mittel: {row['total_ms'] / row['count']:.2f} ms · Maximum: {row['max_ms']:.2f} ms")
                if row['count'] >= 20:
                    lines.append(f"  Grobe Median-Grenze: {percentile_bucket(row, .5)} · Grobe 95%-Grenze: {percentile_bucket(row, .95)}")
                else:
                    lines.append('  Weniger als 20 Messungen: noch keine belastbare Verteilungsbewertung.')
        lines.append('')
    lines.extend(['Hinweise:',
                  'Ein Speicherversuch kann mehrere Dateischreibvorgänge einschließlich Versionen auslösen.',
                  'Unverändert wird bei Büchern, Textbuttons und dem Texteditor vor dem Schreiben erkannt.',
                  'Ein Modul wird bis zum Rücksprung aus seinem Öffnen-Aufruf gemessen; vollständiger Bildaufbau kann länger dauern.',
                  'Caches, physische Datenträgerzugriffe und CPU/RAM werden in dieser Ausbaustufe nicht ermittelt.',
                  'Vergleiche nur ähnliche Datenmengen und Kalt-/Warmzustände; diese werden noch nicht automatisch getrennt.'])
    return '\n'.join(lines)
