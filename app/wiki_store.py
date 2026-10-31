"""Lokale Wissenssammlungen mit geprüften Querverweisen und Versionsschutz."""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from uuid import uuid4

from app import module_archive as archive

MODULE, COLLECTION = "wiki", "articles"
MAX_ARTICLES = 2000
MAX_BASES = 100


def _tags(values):
    if not isinstance(values, list) or len(values) > 60:
        raise ValueError("Ungültige Anzahl Schlagworte.")
    for entry in values:
        archive.text(entry, "Schlagwort", required=True, limit=80)
    if len(set(tag.casefold() for tag in values)) != len(values):
        raise ValueError("Doppelte Schlagworte.")
    return values


def validate_record(raw):
    keys = {"id", "base", "title", "content", "tags", "links", "revisions"}
    if not isinstance(raw, dict) or set(raw) != keys:
        raise ValueError("Wissensartikel hat eine ungültige Struktur.")
    archive.identifier(raw["id"])
    archive.text(raw["base"], "Wissenssammlung", required=True, limit=100)
    archive.text(raw["title"], "Artikeltitel", required=True, limit=200)
    archive.text(raw["content"], "Artikelinhalt")
    _tags(raw["tags"])
    links = raw["links"]
    if not isinstance(links, list) or len(links) > 100:
        raise ValueError("Ungültige Artikelverknüpfungen.")
    for ident in links:
        archive.identifier(ident)
    if len(set(links)) != len(links):
        raise ValueError("Ungültige Artikelverknüpfungen.")
    revisions = raw["revisions"]
    if not isinstance(revisions, list) or len(revisions) > 20:
        raise ValueError("Höchstens 20 frühere Fassungen.")
    for revision in revisions:
        if not isinstance(revision, dict) or set(revision) != {"time", "content"}:
            raise ValueError("Ungültige ältere Textfassung.")
        archive.text(revision["time"], "Zeitpunkt", required=True, limit=40)
        archive.text(revision["content"], "Frühere Textfassung")
    return deepcopy(raw)


def validate(raw):
    if not isinstance(raw, dict) or set(raw) != {"schema_version", "bases", "articles"} or raw["schema_version"] != 1:
        raise ValueError("Wissensarchiv hat ein unbekanntes Format.")
    bases = raw["bases"]
    if (not isinstance(bases, list) or not bases or len(bases) > MAX_BASES):
        raise ValueError("Mindestens eine, höchstens 100 Wissenssammlungen.")
    for base in bases:
        archive.text(base, "Sammlung", required=True, limit=100)
    if len(set(value.casefold() for value in bases)) != len(bases):
        raise ValueError("Doppelte Wissenssammlungen.")
    articles = raw["articles"]
    if not isinstance(articles, list) or len(articles) > MAX_ARTICLES:
        raise ValueError("Höchstens 2000 Wissensartikel.")
    clean = [validate_record(article) for article in articles]
    by_id = {item["id"]: item for item in clean}
    if len(by_id) != len(clean):
        raise ValueError("Doppelte Artikelkennung.")
    titles = set()
    for item in clean:
        if item["base"] not in bases:
            raise ValueError("Artikel verweist auf eine fehlende Sammlung.")
        key = (item["base"].casefold(), item["title"].casefold())
        if key in titles:
            raise ValueError("Doppelter Titel in derselben Sammlung.")
        titles.add(key)
        if item["id"] in item["links"] or any(link not in by_id for link in item["links"]):
            raise ValueError("Artikelverweis ist ungültig.")
    return {"schema_version": 1, "bases": list(bases), "articles": clean}


def load(root):
    return archive.load(root, MODULE, validate,
                        lambda: {"schema_version": 1, "bases": ["Allgemein"], "articles": []})


def add_base(root, name):
    name = archive.text(name.strip(), "Sammlung", required=True, limit=100)
    state = load(root)
    if name.casefold() in {value.casefold() for value in state["bases"]}:
        raise ValueError("Sammlung ist bereits vorhanden.")
    state["bases"].append(name)
    archive.save(root, MODULE, state, validate)
    return name


def put(root, record):
    record = validate_record(record)
    state = load(root)
    if record["base"] not in state["bases"]:
        raise ValueError("Wissenssammlung ist unbekannt.")
    articles = state["articles"]
    found = next((i for i, item in enumerate(articles) if item["id"] == record["id"]), None)
    if found is not None:
        previous = articles[found]
        # Vergangene Fassungen werden nur im Speicherbestand des Editors geführt;
        # mitgelieferte, abweichende Versionslisten dürfen sie nicht löschen.
        record["revisions"] = deepcopy(previous["revisions"])
        if previous["content"] != record["content"]:
            record["revisions"] = (record["revisions"] + [{
                "time": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "content": previous["content"],
            }])[-20:]
        articles[found] = record
    else:
        if record["revisions"]:
            raise ValueError("Neue Artikel dürfen keine erfundene Versionshistorie haben.")
        articles.append(record)
    archive.save(root, MODULE, state, validate)
    return deepcopy(record)


def remove(root, article_id):
    state = load(root)
    archive.identifier(article_id)
    if any(article_id in a["links"] for a in state["articles"]):
        raise ValueError("Artikel ist noch mit anderen Artikeln verknüpft.")
    count = len(state["articles"])
    state["articles"] = [a for a in state["articles"] if a["id"] != article_id]
    if len(state["articles"]) == count:
        raise ValueError("Artikel existiert nicht.")
    archive.save(root, MODULE, state, validate)


def import_copies(root, raw):
    imported = validate(raw)
    state = load(root)
    for base in imported["bases"]:
        if base.casefold() not in {name.casefold() for name in state["bases"]}:
            state["bases"].append(base)
    base_lookup = {name.casefold(): name for name in state["bases"]}
    new_ids = {item["id"]: uuid4().hex for item in imported["articles"]}
    titles = {(a["base"].casefold(), a["title"].casefold()) for a in state["articles"]}
    for entry in imported["articles"]:
        article = deepcopy(entry)
        article["id"] = new_ids[entry["id"]]
        article["base"] = base_lookup[entry["base"].casefold()]
        article["links"] = [new_ids[link] for link in entry["links"]]
        desired = article["title"]
        counter = 2
        while (article["base"].casefold(), article["title"].casefold()) in titles:
            suffix = f" (Kopie {counter})"
            article["title"] = desired[:200-len(suffix)] + suffix
            counter += 1
        titles.add((article["base"].casefold(), article["title"].casefold()))
        state["articles"].append(article)
    archive.save(root, MODULE, state, validate)
    return len(imported["articles"])


def search(root, query="", base=None):
    state = load(root)
    needle = query.casefold().strip()
    return [deepcopy(a) for a in state["articles"]
            if (base is None or a["base"] == base)
            and needle in " ".join((a["title"], a["content"], " ".join(a["tags"]))).casefold()]
