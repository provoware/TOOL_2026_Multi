#!/usr/bin/env python3
"""PySide6-Startanzeige mit atomar gespeicherten Checkpoints und Konsolenfallback."""
from __future__ import annotations
import json,os,sys
from pathlib import Path
STEPS=["Python prüfen","Umgebung vorbereiten","Abhängigkeiten prüfen","Projekt prüfen","Headless-Start prüfen","Anwendung unter Prozesswache starten"]
COLORS={"pending":"#708396","running":"#FFD166","ok":"#3DE783","failed":"#FF6475"}; SYMBOLS={"pending":"●","running":"●","ok":"●","failed":"●"}
def initial_state(): return {"schema_version":1,"phase":"running","progress":0,"message":"Start wird vorbereitet …","steps":[{"label":x,"status":"pending"} for x in STEPS]}
def read_state(path):
    try:
        data=json.loads(path.read_text(encoding="utf-8"))
        if data.get("schema_version")==1 and len(data.get("steps",[]))==len(STEPS):return data
    except (FileNotFoundError,json.JSONDecodeError,OSError,AttributeError):pass
    return initial_state()
def write_state(path,state): path.parent.mkdir(parents=True,exist_ok=True); tmp=path.with_suffix(path.suffix+".tmp"); tmp.write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding="utf-8"); os.replace(tmp,path)
def set_step(path,step_number,status,message):
    if not 1<=step_number<=len(STEPS):raise ValueError("Ungültige Checkpoint-Nummer")
    if status not in COLORS:raise ValueError("Ungültiger Checkpoint-Status")
    state=read_state(path); state["steps"][step_number-1]["status"]=status; state["message"]=message; state["progress"]=int(sum(i["status"]=="ok" for i in state["steps"])*100/len(STEPS)); state["phase"]="failed" if status=="failed" else state["phase"]; write_state(path,state)
def finish(path,message):
    state=read_state(path)
    for step in state["steps"]:
        if step["status"]!="failed":step["status"]="ok"
    state.update({"phase":"done","progress":100,"message":message}); write_state(path,state)
def gui(path):
    try:
        from PySide6.QtCore import QTimer
        from PySide6.QtWidgets import QApplication,QFrame,QLabel,QProgressBar,QVBoxLayout,QWidget
    except ImportError:return 0
    app=QApplication.instance() or QApplication([]); win=QWidget(); win.setWindowTitle("Provoware – sicherer Start"); win.setFixedSize(680,430)
    win.setStyleSheet("QWidget{background:#06111D;color:#F4F8FC;font-size:10pt} QFrame{background:#0B1A28;border:1px solid #27425A;border-radius:6px} QProgressBar{background:#102538;border:1px solid #27425A;border-radius:5px;text-align:center} QProgressBar::chunk{background:#FF9800;border-radius:4px}")
    layout=QVBoxLayout(win); layout.setContentsMargins(28,24,28,24); title=QLabel("Provoware-Datenbank-Dashboard 2026"); title.setStyleSheet("font-size:19pt;font-weight:700"); layout.addWidget(title); sub=QLabel("Vollautomatischer Start · echte Checkpoints · PySide6"); sub.setStyleSheet("color:#9DB0C4"); layout.addWidget(sub)
    card=QFrame(); cl=QVBoxLayout(card); labels=[]
    for _ in STEPS: q=QLabel(); cl.addWidget(q); labels.append(q)
    layout.addWidget(card); progress=QProgressBar(); progress.setRange(0,100); layout.addWidget(progress); message=QLabel(); layout.addWidget(message)
    timer=QTimer(win)
    def refresh():
        state=read_state(path)
        for idx,item in enumerate(state["steps"]):
            status=item.get("status","pending"); labels[idx].setText(f"{SYMBOLS.get(status,'●')}  {item['label']}"); labels[idx].setStyleSheet(f"color:{COLORS.get(status,'#9DB0C4')}")
        progress.setValue(int(state.get("progress",0))); message.setText(state.get("message",""))
        if state.get("phase")=="done": timer.stop(); QTimer.singleShot(800,win.close)
        elif state.get("phase")=="failed": timer.stop(); QTimer.singleShot(8000,win.close)
    timer.timeout.connect(refresh); timer.start(180); refresh(); win.show(); return app.exec()
def main(argv):
    if len(argv)<3: print("Nutzung: start_status.py <init|set|finish|gui> <statusdatei> [...]",file=sys.stderr); return 2
    command,path=argv[1],Path(argv[2])
    if command=="init":write_state(path,initial_state())
    elif command=="set" and len(argv)>=6:set_step(path,int(argv[3]),argv[4]," ".join(argv[5:]))
    elif command=="finish" and len(argv)>=4:finish(path," ".join(argv[3:]))
    elif command=="gui":return gui(path)
    else:print("Ungültiger Aufruf.",file=sys.stderr); return 2
    return 0
if __name__=="__main__":raise SystemExit(main(sys.argv))
