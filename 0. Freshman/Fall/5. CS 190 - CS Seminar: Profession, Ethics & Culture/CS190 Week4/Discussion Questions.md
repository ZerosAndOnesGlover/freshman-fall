# Discussion Questions: Week 4 Seminar

---

## Part 1: Mechanisms (~15 min)

1. The lecture distinguishes four mechanisms of algorithmic bias: biased training data, proxy variables, objective function mismatch, and non-representative sampling. Which mechanism was primarily responsible in each of the three case studies (Amazon hiring, lending/ECOA, Gender Shades)? Are any of the cases actually a mix of more than one mechanism?

2. Amazon's engineers patched specific gendered terms the model was found to penalize, and the model found new proxies. Why does patching individual features fail as a general strategy? What would a genuine fix have required instead?

3. "We didn't include race as an input feature, so our model can't be racially biased." Explain precisely why this claim is false, using the proxy variable mechanism. Can you think of a proxy variable, other than ZIP code, that might carry demographic signal in a domain you're interested in (e.g., a hiring model, a healthcare model, a criminal justice model)?

## Part 2: Law and Measurement (~15 min)

4. Disparate treatment requires intent; disparate impact does not. Why does this distinction matter specifically for algorithmic systems, as opposed to human decision-makers? Is it harder or easier to prove intent for an algorithm than for a human loan officer?

5. Gender Shades' key methodological contribution was disaggregated, intersectional reporting rather than aggregate accuracy. Pick a system you're familiar with (a service you use, or a hypothetical one) and describe what subgroups you'd want to see disaggregated performance for, and why aggregate accuracy alone would be misleading.

6. The lecture states that reporting a single aggregate accuracy number "hides" subgroup disparities. Is this always true, or can you construct a case where aggregate accuracy is actually the right metric to report, and disaggregation would be misleading or unnecessary? (Think about this carefully — it's not a rhetorical question.)

## Part 3: The Impossibility Result (~15 min)

7. Walk through, in your own words, why demographic parity and predictive parity conflict when base rates differ between groups. Use a concrete numerical example if it helps (you can construct a simple one with made-up numbers).

8. If fairness metrics are mathematically incompatible with each other under realistic conditions, does that mean "fairness" is an incoherent goal for algorithmic systems? Or does it mean something more specific — that fairness requires an explicit, contestable choice among genuinely different notions of what fairness means? Argue for one of these positions.

9. Who should make the choice of which fairness metric to optimize for in a given deployed system — the engineering team, company leadership, affected communities, regulators, courts? Does your answer depend on the domain (hiring vs. lending vs. criminal justice vs. medical diagnosis)?

## Closing

10. The lecture argues Gender Shades is a case where rigorous technical research produced a measurable real-world policy outcome (IBM's decision, municipal bans). Is this a representative example, or is it a case study selected because it worked? What conditions made it effective that might not generalize to other cases of harmful algorithmic systems?
