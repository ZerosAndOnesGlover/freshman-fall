# CS 190 · CS Seminar: Profession, Ethics & Culture
## Lecture · Week 7: Intellectual Property in Computing
### Copyright, Patents, Trade Secrets, and the DMCA

**Date:** Wednesday 11 November 2026 · 13:00–13:50 · Week 7

---

## 1. Why Software Doesn't Fit Cleanly Into Any IP Category

Intellectual property law developed over centuries to protect distinct kinds of creative and inventive output: copyright for literary and artistic expression, patents for functional inventions, trade secrets for confidential business information. Software is unusual because it plausibly fits into all three categories simultaneously, and the law has struggled — across decades of litigation — to settle where the boundaries actually lie.

Source code is text, expressive in the way a novel is expressive, which points toward copyright. A novel algorithm can be a functional, useful process, which points toward patent protection. The specific way a company implements a system internally is often kept confidential precisely because competitors would benefit from knowing it, which points toward trade secret protection. Unlike a novel (clearly copyright) or a mechanical invention (clearly patent-eligible), software sits at the overlap, and which protection regime applies — sometimes more than one simultaneously — has been litigated extensively and remains genuinely unsettled in several areas. This week works through each regime and the specific frictions software creates within it.

---

## 2. Copyright

### 2.1 What Copyright Protects, and What It Doesn't

Copyright protects **original expression** fixed in a tangible medium. It does not protect **ideas, procedures, processes, systems, methods of operation, concepts, or principles** — this is the **idea/expression dichotomy**, codified in US law at 17 U.S.C. § 102(b), and it is the single most important concept for understanding how copyright applies to software.

For source code, this means: your specific arrangement of code — variable names, comments, exact structure, specific expression of logic — is protected. The *underlying algorithm* the code implements is not protected by copyright at all (it may be patentable — see Section 3). This is why two independently written implementations of, say, quicksort are not copyright infringements of each other, even if functionally identical, provided neither copied the other's actual code — the algorithm is an unprotectable idea; only a specific expression of it is protected.

### 2.2 Automatic Protection and Registration

Copyright protection in the US (and under the Berne Convention, internationally) attaches automatically upon creation and fixation — you do not need to register or include a copyright notice for a work to be protected. Registration with the US Copyright Office is not required for protection to exist, but it is a prerequisite for filing an infringement lawsuit in the US and provides access to statutory damages and attorney's fees that are unavailable for unregistered works. This matters practically: nearly all code you write, including code you never publish, is automatically copyrighted the moment you write it — this is the legal foundation that makes open source licensing possible at all. A license is only meaningful because the licensor holds a right to grant in the first place.

### 2.3 Copyright Term and Software's Awkward Fit

US copyright for works created after 1978 lasts for the life of the author plus 70 years (or 95 years from publication for corporate/work-for-hire authorship). This term length was calibrated for literary and artistic works with long cultural lifespans (novels, films, music) — it produces a genuinely strange result for software, where a piece of code from a 95-year corporate copyright term will remain legally protected roughly nine decades after the hardware it ran on is a museum piece and long after any commercial or even historical interest in the specific code exists. This mismatch between copyright's original calibration and software's actual useful lifespan is a recurring critique from legal scholars and a contributing factor to why software preservation and abandonware present ongoing legal complications for archivists.

### 2.4 Fair Use and Software

The fair use doctrine (17 U.S.C. § 107) permits certain unlicensed uses of copyrighted work, evaluated via a four-factor balancing test: (1) the purpose and character of the use (commercial vs. non-profit/educational; transformative vs. not), (2) the nature of the copyrighted work, (3) the amount and substantiality of the portion used, and (4) the effect on the market for the original work.

**Google v. Oracle (2021)** is the single most important fair use case for software engineers to know. Google had copied approximately 11,500 lines of Oracle's Java API declaring code (the method signatures and class structure needed for interoperability — not the underlying implementation, which Google wrote independently) into the Android platform, to allow Java developers to use familiar APIs. Oracle sued for copyright infringement, and after nearly a decade of litigation across multiple trials and appeals, the Supreme Court held (6-2, with Justice Barrett not participating) that Google's use was fair use.

The Court's reasoning is important beyond the specific outcome: it treated API declaring code as, at most, thinly protected by copyright given its functional nature (echoing the idea/expression dichotomy — an API is closer to a "method of operation," which § 102(b) explicitly excludes from protection, than to creative literary expression), and found Google's use highly transformative because it enabled a new platform (mobile) rather than merely substituting for Oracle's existing market (enterprise/desktop Java). Notably, the Court explicitly declined to decide whether API declaring code is copyrightable at all — it assumed copyrightability for the sake of argument and ruled on fair use grounds instead, leaving the underlying copyrightability question technically unresolved even after this landmark case, a good illustration of how narrowly courts sometimes rule even in landmark decisions (recall *Carpenter* from Week 5).

### 2.5 Copyright and AI Training Data: The Live Litigation Frontier

As of this writing, one of the most consequential open copyright questions in computing is whether training a machine learning model on copyrighted text, images, code, or other media constitutes infringement, or whether it is protected as fair use (in the US) or falls under a specific text-and-data-mining exception (in the EU and UK, which have more explicit statutory provisions for this than the US's judge-made fair use doctrine).

Multiple ongoing lawsuits (authors and publishers against LLM developers; visual artists and Getty Images against image-generation model developers; and a significant case involving GitHub Copilot and open-source code licensing obligations) are actively litigating this question, with no definitive appellate resolution as of this writing. The core legal arguments echo Google v. Oracle's fair use framework directly: model developers argue training is highly transformative (the model does not reproduce specific works but learns statistical patterns across a vast corpus, similar in kind — proponents argue — to how a human author "trains" on a lifetime of reading without each subsequent work infringing everything they've read) and does not substitute for the market of any individual work; plaintiffs argue the copying involved in creating training datasets is wholesale and the resulting models can, in some documented cases, be prompted to reproduce substantial verbatim or near-verbatim portions of specific training examples (a phenomenon called "memorization"), which would look much less transformative and much more like straightforward copying if proven common and significant.

This is genuinely unresolved law that will likely be substantially clarified during your professional career, and it is a live example of "capability outpacing governance" from last week's unifying frame — the technology (large-scale generative model training) developed faster than copyright law's application to it could be settled.

---

## 3. Patents

### 3.1 What a Patent Protects, and the Bargain It Represents

A patent grants its holder an exclusive right to make, use, sell, or import the patented invention for a limited term (20 years from filing in the US), in exchange for public disclosure of how the invention works, sufficient to enable a person skilled in the relevant art to reproduce it. This is the fundamental patent bargain: society gets a public, detailed disclosure of a working invention (unlike a trade secret, which relies on non-disclosure) in exchange for a temporary government-enforced monopoly on its commercial exploitation. Unlike copyright, patent protection requires an application and formal examination process by a patent office (the USPTO in the US) — it is not automatic.

### 3.2 Patentability Requirements

To be patentable, an invention must be: **novel** (not previously disclosed anywhere in the world — "prior art" defeats novelty), **non-obvious** (not a trivial or predictable combination of existing known techniques to a person of ordinary skill in the field), and constitute **patent-eligible subject matter**. This last requirement is where software patents become genuinely contested.

### 3.3 The Software Patent Eligibility Problem

US patent law (35 U.S.C. § 101) excludes abstract ideas, laws of nature, and natural phenomena from patent eligibility — an algorithm, standing alone, is generally treated as an abstract idea (mathematics), not a patentable invention, echoing copyright's idea/expression dichotomy in a parallel but distinct doctrinal form. The difficult question, litigated extensively, is when a software-implemented process crosses the line from "abstract idea merely implemented on a generic computer" (not patentable) to a genuinely patent-eligible application of that idea (patentable).

**Alice Corp. v. CLS Bank International (2014)** is the landmark Supreme Court case establishing the current test (the "Alice/Mayo two-step framework," building on the Court's earlier *Mayo* decision in a biotech context). Step one: is the patent claim directed to an abstract idea (or law of nature/natural phenomenon)? Step two, if yes: does the claim include an "inventive concept" sufficient to transform the abstract idea into a patent-eligible application — something significantly more than simply instructing that the abstract idea be implemented "on a computer" using conventional, generic computer functions?

*Alice* invalidated a patent on a computerized method for mitigating settlement risk in financial transactions, holding that using a computer to implement a well-known economic practice (an intermediary holding funds in escrow — a concept far older than computers) did not transform an abstract idea into a patentable invention merely by adding "on a generic computer" to the claim.

The practical consequence for the software industry has been substantial: *Alice* has been used to invalidate a very large number of previously granted software patents in subsequent litigation and has made obtaining new software patents significantly more difficult for claims that closely resemble "do [abstract business or mathematical concept] using a generic computer," while leaving room for patents on claims involving genuine technical improvements to computer functionality itself (e.g., a specific technical improvement to how a database indexes data, a specific technical improvement to network routing efficiency) — the line between these two categories remains actively litigated and is not always predictable in advance, which is itself a significant practical problem for patent applicants and their attorneys.

### 3.4 Software Patents: The Policy Debate

**The case for software patents:** Encourage disclosure and investment in software R&D by providing a period of exclusivity to recoup development costs, analogous to the justification for patents generally; without them, competitors could freely copy novel technical approaches the moment they're released, undermining incentives to invest in developing them.

**The case against, specific to software:** Software development, unlike pharmaceutical development (patents' traditional stronghold, where a single patent may represent a decade and billions of dollars of R&D), often produces valuable innovations through much shorter, cheaper, more incremental development cycles, meaning the patent bargain's core justification (encouraging investment that wouldn't otherwise happen) is weaker for much of software. Software patents have also been widely criticized as enabling **patent trolling** — entities that acquire broad, vague software patents not to practice the invention themselves but to extract licensing fees or settlements from operating companies through litigation threats, imposing a substantial tax on genuine innovation without contributing to it. The **patent thicket** problem — modern software and hardware products (a single smartphone, famously) may implicate thousands of individual patents held by dozens of different entities, making it practically impossible for any single engineer or company to verify non-infringement before shipping a product — is a further structural critique specific to software and hardware's componentized, cumulative nature.

---

## 4. Trade Secrets

### 4.1 What a Trade Secret Protects

A trade secret is confidential business information that provides a competitive advantage and is subject to reasonable efforts to maintain its secrecy — a formula, process, method, technique, or compilation of information not generally known and not readily ascertainable by proper means. Unlike copyright and patents, trade secret protection has **no fixed term** — it lasts as long as the secrecy is maintained, potentially indefinitely (the formula for Coca-Cola, famously never patented, is the classic non-software example of an indefinitely maintained trade secret).

### 4.2 The Fundamental Tradeoff Against Patents

Trade secret protection requires *not* disclosing the invention (the opposite of the patent bargain) and provides no protection against **independent discovery** or **reverse engineering** by lawful means — if a competitor legitimately figures out your trade secret independently, or legally reverse-engineers it from a publicly available product, trade secret law provides no recourse (unlike patent law, which protects against independent invention of the same claimed invention during the patent term regardless of how the infringer arrived at it). Trade secret protection *does* provide recourse against **misappropriation** — theft, breach of a confidentiality agreement, or other improper means of acquiring the secret.

This produces a genuine strategic choice for a company with a novel technical approach: patent it (public disclosure, but strong protection including against independent invention, for a fixed term) or keep it as a trade secret (no disclosure required, potentially indefinite protection, but no protection against reverse engineering or independent discovery, and no protection at all if the secret leaks). Many companies' core algorithms (search ranking algorithms, recommendation system internals, specific trading strategies) are maintained as trade secrets rather than patented specifically because patenting would require public disclosure of the algorithm's workings, while a trade secret requires only that reasonable security and confidentiality measures be maintained — a tradeoff most large technology companies make deliberately and explicitly for their most commercially sensitive algorithms.

### 4.3 Trade Secrets and Employee Mobility

Trade secret law creates significant tension with employee mobility and knowledge transfer — an engineer who worked on a trade-secret-protected system and then leaves for a competitor inevitably carries general knowledge, skills, and understanding developed during that employment, which is not itself a trade secret violation (an employee's general skill and knowledge is understood to belong to the employee, not the employer), but carrying and using *specific* confidential information (source code, specific algorithmic parameters, customer lists) to a new employer would constitute misappropriation. The line between "general skill and knowledge I carry in my head" and "specific confidential information I'm not permitted to use" is genuinely difficult to draw in practice and is a recurring subject of trade secret litigation between technology companies, particularly in cases involving employees moving between direct competitors.

---

## 5. The DMCA and Anti-Circumvention

### 5.1 The Digital Millennium Copyright Act (1998)

The DMCA is a US federal law with two provisions of particular relevance to software engineers, both distinct from ordinary copyright infringement liability.

### 5.2 The Safe Harbor Provisions (§ 512)

The DMCA's safe harbor provisions protect online service providers (platforms hosting user-generated content — video platforms, code repositories, social media, cloud storage) from copyright liability for infringing content uploaded by their users, provided the platform complies with a **notice-and-takedown** process: promptly removing content upon receiving a valid infringement notice from a rights holder, and providing a counter-notice mechanism for users who believe their content was wrongly removed. This safe harbor is the legal foundation that makes user-generated content platforms viable at all — without it, a platform could face crushing liability for every instance of user-uploaded infringing content, making the business model of platforms like YouTube, GitHub, or any service hosting user content essentially unworkable at scale.

The system has well-documented problems in practice: automated takedown systems (deployed by platforms to handle the enormous volume of notices at scale) generate significant **false positives** — legitimate, non-infringing content (including fair use content, and in some documented cases entirely original content misidentified by automated matching systems) removed based on automated or bad-faith notices, with the burden falling on the user to file a counter-notice and potentially face litigation to restore their own legitimate content. This dynamic — automated enforcement at scale producing systematic over-removal, with recourse burden placed on the affected party rather than the entity issuing the (sometimes erroneous) notice — is a recurring structural pattern worth comparing to the algorithmic bias content from Week 4: an automated system optimized for one goal (efficient rights enforcement at platform scale) producing predictable, disparately distributed harm (erroneous removal of legitimate content) as a side effect, with limited built-in mechanism for those affected to contest it efficiently.

### 5.3 Anti-Circumvention (§ 1201)

Separately, and more directly consequential for a working engineer, the DMCA's anti-circumvention provisions make it illegal to circumvent **technological protection measures** (DRM — digital rights management) that control access to copyrighted works, and separately illegal to manufacture or distribute tools primarily designed to circumvent such measures — **regardless of whether the underlying use of the copyrighted work would itself be lawful** (e.g., fair use). This is the provision's most legally distinctive and most criticized feature: § 1201 liability for circumvention is analytically separate from ordinary copyright infringement, meaning a use that would be entirely lawful under fair use doctrine can still trigger DMCA anti-circumvention liability if accomplishing it required bypassing a technical protection measure.

This has produced significant, well-documented friction with legitimate security research, accessibility engineering, and interoperability work: security researchers who circumvent DRM or access controls to identify and responsibly disclose vulnerabilities have faced § 1201 liability exposure for the circumvention itself, independent of the legitimate and often beneficial purpose of the research (a direct connection to next week's cybersecurity ethics and responsible disclosure content). The US Copyright Office conducts a triennial rulemaking process that grants specific, temporary exemptions to § 1201 for particular categories of use (including, in various rulemaking cycles, exemptions for good-faith security research, for accessibility purposes for people with disabilities, and for repair and diagnosis of certain consumer devices) — but this exemption process is narrow, must be renewed and re-litigated every three years, and does not provide the kind of general, durable legal certainty that fair use doctrine provides for ordinary copyright infringement claims.

### 5.4 Right to Repair

A closely related and currently very active policy area: § 1201's anti-circumvention provisions have been used by manufacturers of everything from tractors to smartphones to medical devices to restrict independent repair, by treating the diagnostic software and firmware access needed for repair as protected by technical measures whose circumvention is independently illegal, regardless of the underlying repair activity's legality. This has driven the **right to repair** movement and resulting state-level legislation (several US states have passed right-to-repair laws in recent years covering electronics, agricultural equipment, and other categories) specifically to carve out repair-related circumvention from liability, illustrating another instance of a copyright-adjacent legal mechanism (DRM anti-circumvention, originally justified as protecting creative works from piracy) being used for a purpose — restricting repair markets — quite far from its original stated justification.

---

## 6. Synthesis: What This Means for You as a Future Engineer

1. **Copying code, even functionally trivial code, without a license is copyright infringement** unless a specific exception (fair use, an applicable open source license) applies — and "I only copied a small amount" is not itself a defense; *Google v. Oracle*'s outcome turned on transformative purpose and market effect, not merely on the quantity copied (11,500 lines is not small in absolute terms, but the Court found the use transformative regardless).

2. **The algorithm itself is generally not copyrightable, but may be patentable** if it clears the *Alice* two-step test — meaning independent reimplementation of a known algorithm is not copyright infringement, but could still infringe an existing patent regardless of independent development, which is a meaningfully different and often underappreciated risk.

3. **Reverse engineering for interoperability is legally significant and contested territory** — lawful in some circumstances and jurisdictions (particularly for achieving interoperability, under some fair use and other statutory carve-outs), but potentially exposing you to DMCA § 1201 liability if it requires circumventing a technical protection measure, independent of whether the underlying purpose was legitimate.

4. **Respecting open source license terms is a legal obligation, not merely good etiquette** — as established in Week 2, copyleft license violations (using GPL code in proprietary software without complying with its terms) constitute copyright infringement, actionable by the license holder.

5. **The legal status of AI training on copyrighted data is currently unresolved** — building or working on generative AI systems currently involves operating in a genuinely unsettled legal area, which is a different and more uncertain position than working in most other areas of software development where the applicable IP law, whatever its complexities, is at least settled.

---

## Key Terms Introduced This Week

See [[Glossary Week 7]]. New terms: *idea/expression dichotomy*, *fair use (four-factor test)*, *Google v. Oracle*, *patent eligibility*, *Alice/Mayo framework*, *patent troll*, *patent thicket*, *trade secret*, *misappropriation*, *DMCA safe harbor*, *notice-and-takedown*, *anti-circumvention (§ 1201)*, *right to repair*.
