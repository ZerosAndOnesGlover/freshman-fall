# Lecture Week 3: Ethics in Computing
### The ACM Code of Ethics and Professional Responsibility

---

## 1. Why a Code of Ethics, and Why Now

This is the week CS 190 shifts from contextual background — what the field is, where it came from, how software is built — into its substantive ethical content. Position Papers begin this week, which means the standard changes: you are no longer being asked to understand and discuss. You are being asked to take positions and defend them.

Before engaging with the ACM Code of Ethics itself, it's worth asking a prior question: why do professions develop codes of ethics at all?

The answer is not primarily moral — it's structural. A code of ethics is an institution's answer to a coordination problem. Individual professionals acting in their own interest will sometimes produce outcomes that harm the public they serve. A code of ethics establishes shared standards that: (1) give professionals a basis for resisting organizational pressure to do harmful things ("I can't do that — it violates my professional obligations"); (2) give the public a basis for trust in the profession ("I know this engineer is bound by standards I can rely on"); (3) give the profession a basis for self-governance, including the ability to sanction members who violate the code.

Medicine, law, accounting, and civil/structural engineering all have codes of ethics backed by licensure — you can lose your ability to practice if you violate them. Computing does not have mandatory licensure in most jurisdictions. The ACM Code is voluntary. This creates a genuine tension: voluntary codes provide guidance and professional identity, but they lack enforcement teeth. Whether this is a temporary gap or a fundamental feature of a discipline whose outputs are more diffuse than a building collapse is one of this week's substantive questions.

---

## 2. The ACM Code of Ethics (2018 Revision): Structure and Content

The ACM Code of Ethics and Professional Conduct was most recently revised in 2018. It is organized into four sections:

**1. General Ethical Principles** (what every computing professional should do)
**2. Professional Responsibilities** (how to act in one's professional role)
**3. Professional Leadership Principles** (for those in positions of authority)
**4. Compliance with the Code**

We will work through the most important principles in each section.

---

### 2.1 Section 1: General Ethical Principles

**1.1 Contribute to society and to human well-being, acknowledging that all people are stakeholders in computing.**

The opening principle establishes the profession's fundamental orientation: the public interest, not the client's or employer's interest, is the primary obligation. The phrase "all people are stakeholders" is doing real work here — it extends the engineer's responsibility beyond direct users to *everyone affected* by the system, including those who never interact with it directly.

The code elaborates: "Those who design and implement systems that have a wide-scale impact on individuals or society bear a special responsibility to act in the public interest." This is a direct statement that scale creates obligation — building a system used by a billion people is not the same as building one used by a hundred.

**1.2 Avoid harm.**

This principle defines harm broadly: "unnecessary personal injury; financial loss; damage to property; loss of information; theft; unauthorized access to computing systems; and harm to society and the environment." The word "unnecessary" is important — it acknowledges that some harm may be an unavoidable byproduct of beneficial systems, and the professional obligation is to minimize it rather than pretend it doesn't exist.

The code also assigns responsibility for foreseeable harms: "If harm is suspected, it must be reported to a responsible party." This is a positive obligation to act, not merely a negative obligation to avoid.

**1.3 Be honest and trustworthy.**

The code interprets honesty to include being forthright about uncertainties: a professional should "not misrepresent technical matters to customers, employers, or the public." The obligation extends to not deliberately creating false impressions through technically true but misleading statements — a distinction that matters significantly in marketing, security communications, and AI capability claims.

**1.4 Be fair and take action not to discriminate.**

The code explicitly addresses algorithmic systems: "The values of equality, tolerance, respect for others, and the principles of equal justice govern this principle." It names "age, color, disability, ethnicity, family status, gender identity, labor union membership, military status, nationality, race, religion or belief, sex, sexual orientation, and any other unjustified characteristic" as protected attributes.

Note: the code says "unjustified" discrimination, not all differential treatment. A medical dosing algorithm that produces different outputs based on weight is not discriminatory in the relevant sense. An algorithm that produces different loan approval rates based on race — even without race as an explicit input, through proxy variables — is exactly the kind of discrimination this principle addresses. The question of *how* to detect and remedy such disparities is Week 4's territory.

**1.5 Respect the work required to produce new ideas, inventions, creative works, and computing artifacts.**

This is the intellectual property principle — covering copyright, patents, and trade secrets. The code notes that this includes respecting open-source licenses, not just proprietary ones. Violating a GPL license by incorporating GPL code into proprietary software without disclosure is a professional ethics violation under this framework, not just a legal risk.

**1.6 Respect privacy.**

"The responsibility of respecting privacy applies to computing professionals in a particularly profound way" — the code acknowledges that computing professionals have both unusual access to personal data and unusual ability to surveil, aggregate, and exploit it. The obligations include: collecting only data that is necessary for the purpose, retaining it only as long as needed, and protecting it from unauthorized access and use.

**1.7 Honor confidentiality.**

Confidentiality obligations to employers and clients are real and important — but the code is explicit that they do not override obligations to public safety. "This duty to honor confidentiality of information does not apply when the professional is asked to keep something secret that would endanger health or safety, acts unethically, or is contrary to law."

---

### 2.2 Section 2: Professional Responsibilities

**2.1 Strive to achieve high quality in both the processes and products of professional work.**

This principle connects technical quality to ethics: shipping knowingly buggy, insecure, or unreliable software is not just an engineering failure but an ethical violation when that software has real consequences for real people. The code calls for ongoing professional education — staying current with the field is an ethical obligation, not merely a career strategy.

**2.2 Maintain high standards of professional competence, conduct, and ethical practice.**

Closely related: you should not take on work for which you lack the competence to do it safely. This is a harder constraint than it appears — there is constant organizational pressure to accept projects, agree to timelines, and make promises about capabilities. The code gives professionals a basis to push back.

**2.3 Know and respect existing rules pertaining to professional work.**

Laws and regulations provide minimum standards. The code frames professional ethics as often requiring *more* than legal compliance — the law is a floor, not a ceiling. An action can be legal and still violate professional ethics.

**2.4 Accept and provide appropriate professional review.**

Code review, security audits, ethical review — the principle establishes that accepting review of one's work is an obligation, not a personal choice. It also establishes an obligation to provide honest review rather than cursory approval.

**2.6 Perform work only in areas of competence.**

If asked to work on a system in a domain where you lack expertise — medical devices, avionics, financial systems under complex regulations — you have an obligation to disclose your limitations and either acquire the needed expertise or refer the work to someone who has it.

**2.7 Foster public awareness and understanding of computing, related technologies, and their consequences.**

This is the public communication obligation. Computing professionals have specialized knowledge the public generally lacks; the code establishes a responsibility to use that knowledge to inform public understanding rather than exploit the information asymmetry.

**2.8 Access computing and communication resources only when authorized or when compelled by the public good.**

The "unauthorized access" prohibition is absolute for systems you have no right to access. The "compelled by the public good" carve-out is deliberately narrow and demanding — it addresses situations like a security researcher discovering a critical vulnerability through a means that technically exceeded authorized access. The code does not sanction general hacking for beneficial purposes; it acknowledges that there are extreme situations where the calculus is genuinely complicated.

---

### 2.3 Section 3: Professional Leadership Principles

Section 3 is directed at computing professionals in management, executive, and policy roles — but its principles are useful for any engineer who will eventually be in a position of influence over others, which is most of them.

**3.1 Ensure that the public good is the central concern during all professional computing work.**

Leaders have greater responsibility because they shape systems for others. An engineering manager who does not create conditions for their team to raise ethical concerns is failing this principle even if they personally never act unethically.

**3.2 Articulate, encourage acceptance of, and evaluate fulfillment of social responsibilities by members of the organization or group.**

This is the institutional ethics principle: leaders are responsible not just for their own conduct but for creating cultures where ethical concerns can be raised and acted on. A culture where raising ethical concerns is penalized is an ethics violation by leadership, not just a management failure.

**3.4 Ensure that users and those who will be affected by a system have their needs fully addressed.**

User advocacy from a leadership position. This principle requires that leaders represent user interests in system design, not just efficiency and profit — and that "users who will be affected by a system" is interpreted broadly, as in principle 1.1.

**3.6 Use care when modifying or retiring systems.**

Systems on which people depend — medical records systems, tax systems, public transit scheduling — cannot be migrated, modified, or decommissioned without attention to impact on users who depend on them. The engineers who build and maintain such systems bear responsibility for managing transitions safely.

---

### 2.4 Section 4: Compliance with the Code

**4.1 Uphold, promote, and respect the principles of the Code.**

Not merely comply personally, but actively advocate within professional contexts. This is a positive obligation.

**4.2 Treat violations of the Code as inconsistent with membership in the ACM.**

The code explicitly calls on members to report violations. This is the teeth of a voluntary code — social accountability, even without legal accountability.

---

## 3. What the Code Does Not Resolve

A code of ethics is not a decision procedure. It cannot tell you exactly what to do in most hard cases. What it provides is a set of considerations that must be taken seriously — a checklist of values to weigh, not an algorithm for resolving conflicts among them.

The code does not resolve:

**The tension between employer loyalty and public interest.** You work for a company that has built a system you believe is causing harm. The company's legal team says the system is compliant with all applicable law. Your manager says shipping is more important than your concerns. What do you do? The code tells you that public interest takes priority over employer loyalty — but it does not tell you how to act on that priority without losing your job or being sued for breach of confidentiality.

**The problem of uncertainty.** Harm must be "reasonably foreseeable" to trigger the obligation to avoid it. But foreseeable by whom, with what prior knowledge? An engineer in 2005 building a social media recommendation system could not have foreseen its role in polarizing political discourse in 2016. Is that lack of foresight a moral failing? The code does not say.

**The diffusion of responsibility problem.** In a large organization building a harmful system, no single engineer built the whole system. Each individual contributed a component that seemed innocuous in isolation. The harm was emergent. Who is responsible? The code implies that anyone who understood the system's operation bore an obligation to raise concerns — but in a 2,000-person engineering organization, understanding the system as a whole is itself impossible.

These unresolved tensions are not a criticism of the code — they reflect the genuine difficulty of applied ethics in complex organizations. They are, however, exactly the territory that CS 190's position papers will ask you to navigate.

---

## 4. The Argument for Mandatory Licensure

The ACM Code is voluntary. The strongest argument for mandatory computing licensure (analogous to PE — Professional Engineer — licensure in civil/mechanical/electrical engineering) runs as follows:

1. Computing systems now mediate access to healthcare, credit, employment, criminal justice, democratic participation, and physical safety.
2. Failures in these systems can cause serious harm at large scale.
3. No individual computing professional can be held professionally accountable for harms caused by systems they worked on, because there is no license to revoke.
4. Therefore, the profession lacks a structural mechanism for enforcing professional responsibility.
5. Therefore, mandatory licensure — or equivalent mandatory accountability mechanisms — is warranted.

The strongest arguments against:

- Software changes too fast for licensure curricula to remain relevant; licensed engineers would be practicing on outdated credentials within years of receiving them.
- The field's heterogeneity makes a universal license ill-fitting — a machine learning engineer and a systems programmer and a web developer do not share enough common practice for a single credential to be meaningful.
- Licensure creates barriers to entry that reduce labor supply and can disadvantage self-taught programmers and international talent.
- The PE model requires professional sign-off on designs before construction; software's continuous deployment model is structurally incompatible with pre-deployment professional sign-off.

This debate is unresolved in the profession and in policy, and it is directly relevant to how computing professionals think about their own accountability — which makes it good territory for a position paper.

---

## 5. The Code in Practice: Three Scenarios

These scenarios are introduced here and will reappear in the Week 3 discussion. Come with a view on each.

**Scenario A:** You are an engineer at a company building a facial recognition system for law enforcement use. Internal testing shows the system's error rate for identifying women with dark skin is 34%, compared to 1% for light-skinned men. Your manager has told you the contract is critical to the company's revenue and the system ships in two weeks regardless. Which ACM principles apply? What are your obligations under the code? What would you actually do?

**Scenario B:** You are maintaining a legacy system for a hospital. You discover a security vulnerability that could allow unauthorized access to patient medical records — potentially affecting hundreds of thousands of patients. Fixing it properly requires a six-month refactor the hospital has not budgeted for. Disclosing the vulnerability publicly would likely force the hospital to fund the fix, but could also expose it to exploitation before the fix is deployed. What does the code say you should do? Do you agree?

**Scenario C:** You work at a company that operates a platform used by millions of people. You discover that a recommendation algorithm your team built is being used in a way its designers did not intend — to surface increasingly extreme political content to users who engage with political content. You were not told about this deployment. You didn't work on this specific configuration. The harm is real but diffuse. What are your obligations?

---

## 6. Key Terms Introduced This Week

See `Glossary Week 3.md`. New terms: *code of ethics*, *licensure*, *foreseeable harm*, *public interest*, *diffusion of responsibility*, *confidentiality (professional)*, *whistleblowing*.
