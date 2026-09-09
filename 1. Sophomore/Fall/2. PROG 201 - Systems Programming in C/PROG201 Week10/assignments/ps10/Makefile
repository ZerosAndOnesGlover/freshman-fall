# The vulnerable target. Protections removed deliberately; it exists to be
# attacked in the sandbox. Always run it under `setarch -R` (ASLR off, one
# process only -- the machine-wide setting is never changed).
all: vuln vuln_pie vuln_canary

vuln: vuln.c
	gcc -fno-stack-protector -no-pie -z noexecstack -o $@ vuln.c

# for Part D: the same source with each protection put back
vuln_pie: vuln.c
	gcc -fno-stack-protector -pie -fPIE -z noexecstack -o $@ vuln.c
vuln_canary: vuln.c
	gcc -no-pie -z noexecstack -o $@ vuln.c

clean:
	rm -f vuln vuln_pie vuln_canary
.PHONY: all clean
