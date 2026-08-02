# Reading Guide — Week 8
### Cybersecurity Ethics: Responsible Disclosure and Hacktivism

---

## Required Reading

### 1. *Van Buren v. United States*, 593 U.S. \_\_\_ (2021) — Majority Opinion (Barrett, J.)

The Supreme Court's narrowing of the Computer Fraud and Abuse Act. A police officer with legitimate
database access used it for an improper purpose; the question was whether that "exceeds authorized
access" under the CFAA.

**Read for:** the "gates-up-or-down" reasoning — the Court's distinction between accessing areas you
are not entitled to reach, and misusing information you *are* entitled to obtain.

**Guiding questions:**
- Why did the Court find the government's broader reading untenable? What ordinary conduct would it
  have criminalised?
- The majority notes the statute was written in 1986. How much interpretive work should a court do to
  update a statute that has not kept pace with technology, and how much should it leave to Congress?
- The decision narrows the CFAA but does not create a research exemption. What is still unclear for a
  researcher who scans systems they do not own?

---

### 2. ISO/IEC 29147 — *Vulnerability Disclosure* (overview sections)

The international standard describing how organisations should receive and handle vulnerability
reports. Read the scope and the description of the disclosure process; you do not need the full
normative text.

**Read for:** what a well-run disclosure process actually looks like from the vendor's side — the part
researchers rarely see.

**Guiding questions:**
- The standard specifies that vendors should provide a means of receiving reports. Why is this
  apparently trivial requirement so frequently unmet in practice?
- What does the standard say, and decline to say, about timelines?

---

### 3. Google Project Zero — "Policy and Disclosure" (current version of the team's published policy)

The most consequential unilateral disclosure policy in the industry: 90 days, then publication,
with defined exceptions.

**Read for:** the reasoning offered for a fixed deadline, and for the exceptions the team has found
necessary to add over time.

**Guiding questions:**
- What is the argument that a *fixed* deadline serves users better than a negotiated one?
- The policy has been revised repeatedly since its introduction. What does the pattern of revisions
  suggest about how well the original theory survived contact with practice?
- Would a 90-day deadline have been appropriate for Meltdown and Spectre? If not, does that refute the
  policy or merely bound it?

---

## Optional / Enrichment Reading

### 4. Electronic Frontier Foundation — "Coders' Rights Project" resources on security research and the law

A practitioner-facing summary of the legal exposure security researchers face in the United States,
including CFAA and DMCA § 1201 issues. Useful as orientation rather than as legal advice.

### 5. Anderson, R. — *Security Engineering*, 3rd ed., chapter on economics and assurance

Anderson's central argument is that security failures are usually **economic** failures rather than
technical ones — systems fail because the party who could fix a flaw is not the party who bears the
cost of it. This reframes disclosure as an incentive problem.

### 6. Coleman, G. — *Hacker, Hoaxer, Whistleblower, Spy: The Many Faces of Anonymous* (2014), introduction and one case chapter

An anthropologist's study of Anonymous, written from close observation. Read as ethnography, not
endorsement: the value is in understanding how participants reasoned about what they were doing, which
is difficult to reconstruct from news coverage.

---

## A Note on Reading Legal Material

You are not lawyers and are not expected to read cases as lawyers do. Read the **majority opinion's
statement of facts** and its **central reasoning**, and skip the procedural history and the discussion
of precedent unless it interests you.

What matters for this seminar is the *structure of the argument* — what the Court thought the statute
was for, and why the alternative reading was rejected. That is a form of reasoning you can assess
without legal training, and it is the part that bears on your professional life.
