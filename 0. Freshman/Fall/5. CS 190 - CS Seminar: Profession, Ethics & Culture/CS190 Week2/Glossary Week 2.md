# Glossary — Week 2 Additions

---

**Waterfall Model**
A sequential software development methodology in which distinct phases (Requirements → Design → Implementation → Testing → Deployment) are completed in order, with each phase producing a document or artifact that feeds the next. Often misattributed to Royce (1970) as a prescription — Royce's actual paper warned against rigid sequential execution. The model reflects the reasonable intuition that requirements errors are cheaper to fix early; its weakness is the empirical implausibility of complete upfront requirements specification.

**Agile Manifesto**
A 2001 document produced by seventeen software practitioners articulating four value preferences for software development: individuals and interactions over processes and tools; working software over comprehensive documentation; customer collaboration over contract negotiation; responding to change over following a plan. The founding document of the Agile movement.

**Scrum**
The most widely adopted Agile framework. Structures work into fixed-duration sprints (typically 1–2 weeks), defines roles (Product Owner, Scrum Master, development team), and specifies ceremonies (sprint planning, daily standup, sprint review, retrospective). Intended to create short feedback loops between development and users.

**Sprint**
A fixed-duration iteration in Scrum, typically 1–2 weeks, at the end of which the team delivers working software. The sprint boundary creates a regular forcing function for integration, testing, and delivery.

**Product Backlog**
A prioritized list of work items (features, bug fixes, technical improvements) in Scrum, owned by the Product Owner and continuously refined. The backlog is never "done" — it evolves with understanding of the product and market.

**Kanban**
A flow-based development method using a visual board of columns representing work stages, with WIP limits constraining how many items can be in each stage simultaneously. Unlike Scrum, there are no fixed-duration sprints; work flows continuously. Better suited to maintenance and operational work than to feature-driven product development.

**WIP Limit (Work In Progress Limit)**
In Kanban, a constraint on the maximum number of work items allowed in a given stage at once. Forces the team to finish work before starting new work, surfaces bottlenecks, and prevents the accumulation of half-finished tasks.

**Goodhart's Law**
"When a measure becomes a target, it ceases to be a good measure." Named after economist Charles Goodhart; widely applicable in software engineering contexts where productivity metrics (story points, lines of code, coverage percentages) are used for performance evaluation, causing engineers to optimize the metric rather than the underlying goal it was intended to proxy.

**Open Source Software**
Software whose source code is publicly available and which can be inspected, modified, and distributed under the terms of an open source license. Formally defined by the Open Source Initiative's Open Source Definition (ten criteria). Distinguished from "source-available" software, which makes source visible but restricts use.

**Copyleft License**
An open source license that requires any distributed modifications or derivative works to be released under the same license. The "viral" property. Examples: GNU GPL (General Public License), LGPL, AGPL. Designed to prevent open source code from being incorporated into proprietary products without reciprocal contribution. Contrasted with permissive licenses.

**Permissive License**
An open source license that allows modification and redistribution with few restrictions, including incorporation into proprietary software. Examples: MIT, BSD (2-clause and 3-clause), Apache 2.0. Apache 2.0 includes an explicit patent grant absent from MIT/BSD.

**AGPL (GNU Affero General Public License)**
A copyleft license extending the GPL to cover network use: if you run AGPL-licensed software as a web service and users interact with it over a network, you must provide those users access to the source code. Adopted by projects concerned about cloud providers hosting their software without contributing back (e.g., MongoDB, originally; Grafana).

**Dual-Use Research**
Research whose findings or techniques can be applied both for beneficial purposes (defense, safety, understanding) and harmful ones (attack, exploitation, manipulation). A structural challenge in security research, AI capabilities research, and biology. The publication decision for dual-use research involves weighing the benefit of open knowledge against the risk of enabling harm.

**Publish-or-Perish**
The incentive structure in academic research in which researchers are primarily evaluated by their publication record in prestigious venues. Drives research toward demonstrable, publishable results and can discourage replication studies, negative results, and long-horizon projects with uncertain publication outcomes.

**Linus's Law**
Eric Raymond's aphorism from "The Cathedral and the Bazaar": "given enough eyeballs, all bugs are shallow." The claim that open, distributed code review by many contributors tends to surface bugs quickly. Empirically complicated by cases (Heartbleed, xz Utils) where critical vulnerabilities persisted for years in widely-used, publicly-visible code.
