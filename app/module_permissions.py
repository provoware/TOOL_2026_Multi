"""Verweigernde Berechtigungsprüfung für deklarative Modulfunktionen.

Keine Ausführung von Python-, Shell- oder Netzcode; Funktionen sind feste
eingebaute Datenoperationen und erfordern explizite Benutzerfreigabe.
"""
from __future__ import annotations
from app import module_runtime as runtime

SAFE_ACTIONS={"view","edit","search"}

def dispatch(root,module_id,action,*,approved=False,values=None,needle=""):
    if type(approved) is not bool or not approved or action not in SAFE_ACTIONS:
        raise PermissionError("Keine ausdrückliche Freigabe für diese Funktion.")
    definition=runtime.definition(root,module_id)
    if definition is None or action not in definition["capabilities"]:
        raise PermissionError("Modulvertrag erlaubt diese Funktion nicht.")
    if action=="view":
        return runtime.load(root,module_id)["records"]
    if action=="search":
        return runtime.query(root,module_id,needle)
    if not isinstance(values,dict):
        raise ValueError("Zum Bearbeiten werden gültige Formulardaten benötigt.")
    return runtime.save_record(root,module_id,values)
