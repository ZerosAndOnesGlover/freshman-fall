#!/usr/bin/env bash
# CS 212 Week 11 -- every metric in L34-L36, as one script.
#
#   ./metrics.sh            # your own project
#   ./metrics.sh ~/roomsvc  # or the reference codebase
#
# Nothing here is marked. It exists so that A 11 Q1 and Q4 are twenty minutes
# of reading output rather than an evening of assembling commands.
#
# Requires: git, radon, coverage (all in the course toolchain).

set -uo pipefail
REPO="${1:-.}"
SINCE="${SINCE:-10 weeks ago}"
SRC="${SRC:-src}"
cd "$REPO" || exit 1

hr() { printf '\n== %s ==\n' "$1"; }

hr "Integration frequency  (W8 L25 s1 -- the ten-second CI test)"
printf 'commits to main, last 7 days: %s\n' \
  "$(git log --oneline main --since='7 days ago' 2>/dev/null | wc -l | tr -d ' ')"
echo 'open branches, oldest first:'
git for-each-ref --sort=committerdate --format='  %(committerdate:relative)  %(refname:short)' \
  refs/heads/ | head -8
echo '  (a branch older than three days is too big -- semantic drift, W8 L25 s3)'

hr "Hotspots: change frequency  (L35 s3)"
git log --since="$SINCE" --name-only --format='' \
  | grep -E '\.py$' | sort | uniq -c | sort -rn | head -12

hr "Hotspots: complexity"
command -v radon >/dev/null && radon cc -s -n C "$SRC" 2>/dev/null | head -20 \
  || echo '  radon not installed: pip install radon'

hr "Maintainability index  (L35 s2 -- a smell, not an action)"
command -v radon >/dev/null && radon mi -s "$SRC" 2>/dev/null | sort -t'(' -k2 -n | head -8

hr "Coverage, ascending  (W6 L19 s5 -- read the TOP, cross-referenced with change)"
if command -v coverage >/dev/null && [ -f .coverage ]; then
  coverage report --precision=1 --sort=cover 2>/dev/null | head -14
  echo '  BrPart is the most valuable column: reachable, exercised, half-checked.'
else
  echo '  no .coverage file: coverage run -m pytest && rerun this'
fi

hr "Change coupling  (L35 s3 -- couplings that exist in NO import graph)"
git log --since="$SINCE" --name-only --format='@' \
  | awk '
      /^@/ { for (i=1;i<=n;i++) for (j=i+1;j<=n;j++) {
               a=f[i]; b=f[j]; if (a>b) {t=a;a=b;b=t}; pair[a" + "b]++ }
             n=0; next }
      /\.py$/ { f[++n]=$0 }
      END { for (p in pair) if (pair[p] > 2) printf "%6d  %s\n", pair[p], p }' \
  | sort -rn | head -10
echo '  If neither file imports the other, the coupling is in the DOMAIN --'
echo '  which means a boundary is in the wrong place (A 11 Q1b).'

hr "Knowledge distribution / bus factor  (L35 s3)"
TOP=$(git log --since="$SINCE" --name-only --format='' \
      | grep -E '\.py$' | sort | uniq -c | sort -rn | head -1 | awk '{print $2}')
if [ -n "${TOP:-}" ] && [ -f "$TOP" ]; then
  echo "surviving lines in the hotspot ($TOP), by author:"
  git blame --line-porcelain "$TOP" 2>/dev/null | grep '^author ' \
    | sort | uniq -c | sort -rn \
    | awk -v t="$(git blame "$TOP" 2>/dev/null | wc -l)" \
        '{printf "  %5.1f%%  %s\n", 100*$1/t, substr($0, index($0,$3))}'
  echo '  One author above ~70% is a bus factor of 1 on your most-changed file.'
fi

hr "Traceability  (W1 L04 s6 -- roomsvc manages 14%)"
TOTAL=$(git log --oneline | wc -l | tr -d ' ')
LINKED=$(git log --format='%s%n%b' | grep -cE '#[0-9]+' || true)
awk -v l="$LINKED" -v t="$TOTAL" \
  'BEGIN{printf "  %d of %d commits reference an issue (%.0f%%)\n", l, t, 100*l/t}'

hr "Deprecations  (W10 L33 s1 -- roomsvc has 17, oldest March 2021)"
grep -rIn --include='*.py' -iE 'deprecat' "$SRC" 2>/dev/null | head -10
echo '  A deprecation without a usage metric and a date is a comment.'

hr "Next"
cat <<'MSG'
  Read these as TRENDS, not scores (L35 s5). A trend is robust to a bad
  measure, implies a direction, and catches deterioration that a threshold
  hides. Record today's values in docs/debt.md's trend table.

  And remember what none of this can see (L35 s6): whether you built the
  right thing, whether anyone can understand it, whether the team works --
  or whether your invariant is enforced. Eleven weeks of measurement, and
  that last one was one line of DDL.
MSG
