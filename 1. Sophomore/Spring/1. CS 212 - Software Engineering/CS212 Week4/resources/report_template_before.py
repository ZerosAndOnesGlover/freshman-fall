# roomsvc/reports.py — extract, lines 12–96, at tag cs212-reference
#
# The Template Method case from L15 §1. Five subclasses exist; two of them
# override generate() itself, which defeats the pattern and is invisible
# unless you read all five. Reproduced so the lecture's claim is checkable.
#
#   UtilisationReport   -- overrides rows(), header()
#   IncomeReport        -- overrides rows(), header(), footer()
#   DeptBreakdown       -- overrides rows()
#   ExamScheduleReport  -- OVERRIDES generate()        <-- (!)
#   AuditExtract        -- OVERRIDES generate()        <-- (!)
#
# Neither of the two calls super().generate(). The hooks they "implement"
# are dead code; git blame dates both overrides to 2022, six months apart,
# by different authors, with the commit messages "quick fix for exams" and
# "audit needs raw rows".


class BaseReport:
    """Renders a report. Subclasses fill in the hooks."""

    def generate(self, start, end):
        # The skeleton. Subclasses depend on this call ORDER, which appears
        # in no signature anywhere -- connascence of execution across a class
        # boundary (W2 L07 section 6).
        self._connect()
        out = []
        out.append(self.header())
        for row in self.rows(start, end):
            out.append(self.format_row(row))
        out.append(self.footer())
        self._disconnect()
        return "\n".join(out)

    def _connect(self):
        self.db = get_connection()          # global, see L14 section 4

    def _disconnect(self):
        self.db.close()

    def header(self):
        raise NotImplementedError

    def rows(self, start, end):
        raise NotImplementedError

    def format_row(self, row):
        return "\t".join(str(c) for c in row)

    def footer(self):
        return ""
