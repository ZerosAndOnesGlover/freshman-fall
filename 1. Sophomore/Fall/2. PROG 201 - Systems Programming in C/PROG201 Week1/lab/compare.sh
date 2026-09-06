#!/bin/sh
# Compare ./pipeline against the shell, on the same commands.
# The shell is the oracle: any line marked DIFFER is a bug in your pipeline.
#
# stdout and the exit status are compared. Error *wording* on stderr is not —
# your "nosuchcommand: No such file or directory" and dash's "not found" are
# both correct, and both must exit 127.

set -u
fail=0

check() {
    desc="$1"; shift
    mine=$(./pipeline "$@" 2>/dev/null);        mine_rc=$?
    shell_cmd=$(printf '%s ' "$@" | sed 's/ : / | /g')
    theirs=$(eval "$shell_cmd" 2>/dev/null);    theirs_rc=$?

    if [ "$mine" = "$theirs" ] && [ "$mine_rc" = "$theirs_rc" ]; then
        printf '  ok      %s\n' "$desc"
    else
        printf '  DIFFER  %s\n    mine  : %s (exit %s)\n    shell : %s (exit %s)\n' \
               "$desc" "$mine" "$mine_rc" "$theirs" "$theirs_rc"
        fail=1
    fi
}

check "one stage"          echo hello
check "two stages"         ls -1 /etc : wc -l
check "three stages"       ls -1 /etc : grep -c host : cat
check "no matches"         ls -1 /etc : grep zzzzz : wc -l
check "big input"          ls -1 /usr/bin : wc -l
check "early exit"         ls -1 /usr/bin : head -3
check "exit status"        true : false
check "command not found"  ls -1 /etc : nosuchcommand

[ $fail = 0 ] && echo "  all checks passed"
exit $fail
