"""make_fall_calendar.py: print the Year 1 Fall "Graded Work" table for ASSESSMENT CALENDAR.md.

Each row comes from an answer sheet (4. Submissions/...): the date and time are read from the
sheet's source file, the weight is the gradebook component weight / item count. Exams are listed
in EXAMS below. Usage: python3 tools/make_fall_calendar.py > table.md
"""
import re,glob,os,sys,datetime as dt
REG=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FALL=os.path.dirname(REG)+"/0. Freshman/Fall"
ROOTS={c:glob.glob(f"{FALL}/*{c} - *")[0] for c in ["CS 101","PROG 101","MATH 141","MATH 151","PHYS 141","CS 190"]}
MON={m:i for i,m in enumerate(["January","February","March","April","May","June","July","August","September","October","November","December"],1)}
DATE=re.compile(r"(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday) (\d{1,2}) (September|October|November|December) 2026\W{1,4}(?:[^0-9\n]{0,20}?)(\d{2}:\d{2}(?:[–-]\d{2}:\d{2})?)")
d0=dt.date(2026,9,21)
def weights(c):
    t=open(f"{REG}/2. Gradebook/Year1 Freshman/Fall/{c}.md").read()
    sec=t.split("## Component Weights")[1].split("\n---\n")[0]
    return {m.group(1).strip():float(m.group(2)) for m in re.finditer(r"^\| ([^|]+?) \| ([\d.]+)% \|",sec,re.M)}
ICON={"Problem Sets":"📝","Labs":"🔬","Laboratory":"🔬","Quizzes":"📊","Projects":"📋"}
rows=[]
for c,root in ROOTS.items():
    W=weights(c); sheets=[]
    for s in glob.glob(f"{REG}/4. Submissions/Year1 Freshman/Fall/*{c}/week*/*.md"):
        t=open(s).read()
        g=lambda k: (re.search(rf"^{k}:\s*\"?(.*?)\"?\s*$",t,re.M) or [None,""])[1]
        sheets.append((int(re.search(r"week(\d+)",s).group(1)),g("assessment"),g("component"),g("source")))
    count={}
    for w,a,comp,src in sheets: count[comp]=count.get(comp,0)+1
    for w,a,comp,src in sheets:
        if not src or src=="---" or re.search(r"Midterm|Final",comp+a): continue
        hits=glob.glob(f"{root}/*Week{w}/**/{src}",recursive=True) or glob.glob(f"{root}/**/{src}",recursive=True)
        if not hits: print("NOSRC",c,a,src,file=sys.stderr); continue
        head="\n".join(open(hits[0]).read().split("\n")[:25])
        due=[l for l in head.split("\n") if re.search(r"Due",l)]
        pick=None
        for l in (due if re.search(r"Problem|Project|Prep|Paper|Reflection|Question|Presentation",comp+a) and due else [])+head.split("\n"):
            if "Due" in l and "|" in l: l=l[l.index("Due"):]
            m=DATE.search(l)
            if m: pick=m; break
        if not pick: print("NODATE",c,a,hits[0].split("/")[-1],file=sys.stderr); continue
        day=dt.date(2026,MON[pick.group(3)],int(pick.group(2)))
        wk=(day-d0).days//7
        wt=W.get(comp)
        wtxt=f"≈{wt/count[comp]:.1f}%".replace(".0%","%") if wt and count[comp]>1 else (f"{wt:g}%" if wt else "—")
        rows.append((day,pick.group(4),c,a,wtxt,comp,wk))
EXAMS=[("2026-11-02","18:00–19:15","CS 101","Midterm 1","15%","VNC 100 · Weeks 0–5"),
("2026-11-04","18:00–19:30","PROG 101","Midterm 1","12.5%","VNC 100 · Weeks 0–5"),
("2026-11-05","18:00–19:15","MATH 141","Midterm 1","15%","VNC 200 · Weeks 0–5"),
("2026-11-06","18:00–19:15","MATH 151","Midterm 1","—","VNC 200 · Weeks 0–5 · *not in the MATH 151 syllabus — decide*"),
("2026-11-30","18:00–19:15","CS 101","Midterm 2","15%","VNC 100 · Weeks 6–9"),
("2026-12-01","18:00–19:30","PROG 101","Midterm 2","12.5%","VNC 100 · Weeks 6–9"),
("2026-12-02","18:00–19:15","MATH 141","Midterm 2","15%","VNC 200 · Weeks 6–9"),
("2026-12-21","08:00–10:00","MATH 151","Final Exam","30%","VNC 200 · Comprehensive · *syllabus says 3 h*"),
("2026-12-22","09:00–11:30","CS 101","Final Exam","20%","VNC 100 · Comprehensive"),
("2026-12-23","09:00–11:30","MATH 141","Final Exam","20%","VNC 200 · Comprehensive"),
("2026-12-24","14:00–16:30","PROG 101","Final Exam","20%","VNC 100 · Comprehensive"),
("2026-12-09","13:00–13:50","CS 190","Presentation","10%","Session A; Sessions B and C not yet timetabled · peer feedback forms due at each session"),
("","","PHYS 141","Midterm","15%","after Week 6 · 90 min · *no date in the registry yet*"),
("","","PHYS 141","Final Exam","20%","finals week · 3 h · *no date in the registry yet*")]
out=[]
undated=[]
for d,tm,c,a,wt,note in EXAMS:
    if not d: undated.append(f"| TBA | — | **{c}** | {'📕' if 'Final' in a else '📘'} {a} | {wt} | {note} |"); continue
    day=dt.date.fromisoformat(d); out.append((day,tm,c,("📕 " if "Final" in a else "📘 ")+a,wt,note,(day-d0).days//7))
for day,tm,c,a,wt,comp,wk in rows:
    icon=ICON.get(comp,"🎤" if c=="CS 190" else "📝")
    out.append((day,tm,c,f"{icon} {a}",wt,"",wk))
out.sort(key=lambda r:(r[0],r[1],r[2]))
lines=["| Week   | Date   | Course       | Assessment                  | Weight | Notes                                   |",
       "| ------ | ------ | ------------ | --------------------------- | ------ | --------------------------------------- |"]
for day,tm,c,a,wt,note,wk in out:
    W=f"W{wk}" if wk<=12 else "Finals"
    lines.append(f"| {W} | {day.strftime('%a %b %d')} | **{c}** | {a} | {wt} | {tm}{(' · '+note) if note else ''} |")
lines+=undated
print("\n".join(lines).replace("📘 Presentation","🎤 Presentation"))
