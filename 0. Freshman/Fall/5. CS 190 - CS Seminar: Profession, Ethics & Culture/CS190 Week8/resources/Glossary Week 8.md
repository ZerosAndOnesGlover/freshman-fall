# Glossary — Week 8 Additions

---

**Bug bounty** — A programme under which a vendor pays researchers for vulnerability reports. Converts
an adversarial relationship into a transactional one, but the vendor sets the scope and the price, and
both are typically far below what an exploit brokerage offers.

**CERT/CC** — The Computer Emergency Response Team Coordination Center at Carnegie Mellon. A neutral
coordinator for disclosures spanning multiple vendors, useful precisely because it has no product to
defend.

**CFAA (Computer Fraud and Abuse Act, 1986)** — The principal US anti-hacking statute. Its key
phrases — accessing a computer "without authorization" or in a way that "exceeds authorized access" —
predate the web and have been the central source of legal risk for security researchers.

**Coordinated disclosure** — Reporting a vulnerability privately to the vendor, agreeing a timeline,
and publishing after a patch is available. The current professional norm. Often called *responsible
disclosure*, a term many researchers avoid because it prejudges the argument.

**CSIRT** — Computer Security Incident Response Team. National CSIRTs act as coordinators and points
of contact for disclosures affecting a country's infrastructure.

**CVE (Common Vulnerabilities and Exposures)** — A public identifier assigned to a specific
vulnerability, so that vendors, researchers and defenders can refer unambiguously to the same flaw.

**CVSS (Common Vulnerability Scoring System)** — A numerical severity score. Widely used, widely
criticised, and useful chiefly as a shared vocabulary rather than as a precise measure.

**DMCA § 1201** — The anti-circumvention provision of the Digital Millennium Copyright Act, which
prohibits bypassing access controls. Because security research frequently requires exactly that, the
Copyright Office grants a **security-research exemption** — narrow, conditional, and requiring renewal
every three years.

**Embargo** — An agreed period during which parties who have been told about a vulnerability refrain
from disclosing it. Necessary for flaws spanning many vendors; increasingly leaky as the number of
informed parties grows.

**Exploit brokerage** — A firm that buys vulnerabilities and sells them, typically to government
customers. Distinguished from a bug bounty not by the presence of money but by the outcome: the flaw
is **preserved rather than fixed**.

**Full disclosure** — Publishing vulnerability details immediately and publicly, without prior notice
to the vendor. Historically a response to vendors who ignored private reports.

**Hacktivism** — Computer intrusion or disruption undertaken to advance a political cause. Borrows the
moral structure of civil disobedience while typically lacking its defining feature: open action with
acceptance of the penalty.

**ISO/IEC 29147** — International standard on **vulnerability disclosure**: how an organisation should
receive and respond to reports.

**ISO/IEC 30111** — Companion standard on **vulnerability handling**: the internal process for
investigating and remediating a report once received.

**Non-disclosure** — Declining to reveal a vulnerability to anyone. May be a defensible judgement
about safety-critical systems with no available patch, or a commercial decision to preserve the flaw.

**Responsible disclosure** — See *coordinated disclosure*. The adjective is contested: it implies the
alternatives are irresponsible, which is the very question under debate.

**Safe harbour** — A vendor's published commitment not to pursue legal action against researchers
acting in good faith within stated bounds. **Not a law**: it is one company's promise, revocable, and
it does not bind prosecutors or third parties.

**Van Buren v. United States (2021)** — Supreme Court decision narrowing the CFAA. Held that
"exceeds authorized access" means obtaining information from areas one is not entitled to reach, not
misusing information one is entitled to access. Removed the broadest reading without creating a
research exemption.

**Vulnerability lifecycle** — The sequence *introduced → discovered → disclosed → patched → deployed*,
with exploitation possible at any point after discovery. The window between discovery and deployment
is where disclosure policy does its work.

**Whistleblowing** — Revealing wrongdoing encountered through **authorised** access. Ethically and
legally distinct from intrusion, though the two are frequently conflated in public debate; many
jurisdictions protect the first and none protect the second.

**Zero-day** — A vulnerability for which no patch exists. So called because defenders have had zero
days to prepare.
