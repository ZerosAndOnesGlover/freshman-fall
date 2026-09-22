# Discussion Questions — Week 5 Seminar

---

## Part 1: What Privacy Actually Protects (~15 min)

1. Solove's taxonomy separates "aggregation" as a distinct harm from "disclosure" or "breach of confidentiality." Construct an example of a system that could cause serious aggregation harm while having excellent data security (no breaches, no unauthorized disclosure). What does this tell you about the limits of "we take security seriously" as a privacy defense?

2. The lecture argues that "it's just metadata" understates privacy risk. Is there a principled line between metadata and content at all, or is the distinction itself not doing useful analytical work? If you think the distinction is still useful, where would you draw it?

3. The "chilling effect" argument holds that surveillance harms people even when the collected data is never misused, because awareness of monitoring changes behavior. Is this a real, measurable harm that should factor into engineering and policy decisions, or is it too speculative and diffuse to weigh against the concrete benefits of a data-collecting system? Argue a position.

## Part 2: Surveillance Capitalism — Testing the Framework (~15 min)

4. Zuboff's framework implies that "free" services are not actually free — users are the raw material, not the customer. Pick a specific free service you use regularly. Does Zuboff's model accurately describe its business logic, in your assessment? What would change your mind either way?

5. Steelman the strongest counterargument to Zuboff: that behavioral advertising is a mutually beneficial, informed exchange — free services for attention/data — and that framing it as "extraction" is a rhetorical choice, not an accurate economic description. Do you find this persuasive?

6. If Zuboff is right that business model, not engineering judgment, primarily determines data collection defaults, what does this imply about the effectiveness of individual engineers trying to advocate for data minimization within their companies? Is this a losing battle, or does individual advocacy still matter, and how?

## Part 3: Law — GDPR vs. Fourth Amendment Traditions (~15 min)

7. GDPR is a comprehensive, ex-ante regulatory framework (rules apply before any harm occurs, as a condition of processing). The US Fourth Amendment tradition is a case-by-case, ex-post judicial framework (courts decide after a specific dispute whether a search was reasonable). What are the tradeoffs of each approach for a fast-moving technology sector? Which do you think produces better outcomes, and under what conditions?

8. *Carpenter* held that the government needed a warrant for cell-site location data despite the third-party doctrine, because of the data's comprehensiveness and its practically unavoidable generation as a byproduct of using a phone. Apply the same reasoning to a different category of data an app you're familiar with collects (browsing history, health data from a wearable, voice assistant recordings). Would *Carpenter*'s logic extend to protect it? Make the argument.

9. The lecture notes *Carpenter* was decided 5-4 and explicitly described as "narrow." Given how quickly technology changes and how slowly courts rule, is case-by-case Fourth Amendment adjudication capable of keeping pace with new data collection technologies at all? What would a better mechanism look like?

## Closing

10. You are designing a new consumer app from scratch. Choose one concrete data minimization practice from Section 6 of the lecture and describe exactly how you would implement it architecturally — not just as a policy statement, but as a specific technical design decision.
