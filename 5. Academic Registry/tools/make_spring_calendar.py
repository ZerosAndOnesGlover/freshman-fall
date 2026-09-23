"""make_spring_calendar.py: print the Year 1 Spring "Graded Work" table for ASSESSMENT CALENDAR.md.

Each row comes from an answer sheet (4. Submissions/...): the date and time are read from the
sheet's source file, the weight is the gradebook component weight / item count. Exams are listed
in EXAMS below. Usage: python3 tools/make_spring_calendar.py > table.md
Same method as make_fall_calendar.py; written 2026-09-23 for the 18 Jan 2027 Spring term.
"""
import re,glob,os,sys,datetime as dt
REG=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEM=os.path.dirname(REG)+"/0. Freshman/Spring"
ROOTS={c:glob.glob(f"{SEM}/*{c} - *")[0] for c in ["CS 102","PROG 102","MATH 142","ECE 110"]}
MON={m:i for i,m in enumerate(["January","February","March","April","May","June","July","August","September","October","November","December"],1)}
DATE=re.compile(r"(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday) (\d{1,2}) (January|February|March|April) 2027\W{1,4}(?:[^0-9\n]{0,20}?)(\d{2}:\d{2}(?:[–-]\d{2}:\d{2})?)")
d0=dt.date(2027,1,18)
def weights(c):
    t=open(f"{REG}/2. Gradebook/Year1 Freshman/Spring/{c}.md").read()
    sec=t.split("## Component Weights")[1].split("\n---\n")[0]
    return {m.group(1).strip():float(m.group(2)) for m in re.finditer(r"^\| ([^|]+?) \| ([\d.]+)% \|",sec,re.M)}
ICON={"Problem Sets":"📝","Labs":"🔬","Laboratory":"🔬","Quizzes":"📊","Project 1":"📋","Project 2":"📋"}
rows=[]
for c,root in ROOTS.items():
    W=weights(c); sheets=[]
    for s in glob.glob(f"{REG}/4. Submissions/Year1 Freshman/Spring/*{c}/week*/*.md"):
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
        day=dt.date(2027,MON[pick.group(3)],int(pick.group(2)))
        wk=(day-d0).days//7
        wt=W.get(comp)
        wtxt=f"≈{wt/count[comp]:.1f}%".replace(".0%","%") if wt and count[comp]>1 else (f"{wt:g}%" if wt else "—")
        rows.append((day,pick.group(4),c,a,wtxt,comp,wk))
EXAMS=[("2027-03-01","18:00–19:15","CS 102","Midterm 1","12.5%","VNC 100 · Weeks 0–4"),
("2027-03-02","18:00–19:30","PROG 102","Midterm 1","12.5%","VNC 100 · Weeks 0–4 · 75-minute paper"),
("2027-03-03","18:00–19:15","MATH 142","Midterm 1","15%","VNC 100 · Weeks 0–4"),
("2027-03-04","18:00–19:15","ECE 110","Midterm","25%","VNC 100 · Weeks 0–5 · ECE 110's only midterm"),
("2027-03-29","18:00–19:15","CS 102","Midterm 2","12.5%","VNC 100 · Weeks 5–9"),
("2027-03-30","18:00–19:30","PROG 102","Midterm 2","12.5%","VNC 100 · Weeks 5–9 · 75-minute paper"),
("2027-03-31","18:00–19:15","MATH 142","Midterm 2","15%","VNC 100 · Weeks 5–9"),
("2027-04-19","08:00–10:00","ECE 110","Final Exam","15%","Comprehensive"),
("2027-04-20","09:00–11:30","MATH 142","Final Exam","20%","Comprehensive"),
("2027-04-21","09:00–11:30","CS 102","Final Exam","20%","Comprehensive · *paper written for 180 min — decide*"),
("2027-04-22","14:00–16:30","PROG 102","Final Exam","15%","Comprehensive · *paper written for 180 min — decide*")]
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
