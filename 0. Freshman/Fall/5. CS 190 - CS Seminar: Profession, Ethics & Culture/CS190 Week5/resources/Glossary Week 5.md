# Glossary — Week 5 Additions

---

**Solove's Taxonomy of Privacy**
Daniel Solove's framework (2006) categorizing privacy harms into four groups by the activity that causes them — information collection (surveillance, interrogation), information processing (aggregation, identification, insecurity, secondary use, exclusion), information dissemination (breach of confidentiality, disclosure, exposure, blackmail, appropriation, distortion), and invasion (intrusion, decisional interference) — rather than treating privacy as a single unified concept.

**Aggregation (Privacy Harm)**
The privacy harm arising when disparate, individually low-sensitivity pieces of information are combined to create a profile or inference more revealing than any single piece of information alone. Not addressed by data security measures alone, since aggregation harm can occur with zero unauthorized access or breach.

**Chilling Effect**
The phenomenon in which awareness of surveillance or monitoring causes people to alter their behavior (self-censoring speech, avoiding certain associations or reading material) even absent any specific misuse of the collected information. Recognized in First Amendment jurisprudence as an independent harm to open discourse and dissent.

**Surveillance Capitalism**
A term coined by Shoshana Zuboff (2019) describing an economic logic in which human experience is extracted as behavioral data ("behavioral surplus"), processed into predictions about future behavior, and sold in a market for behavioral futures — primarily to advertisers. Contested framework; critics argue it overstates manipulative power and understates genuine value exchange in "free" digital services.

**GDPR (General Data Protection Regulation)**
The European Union's comprehensive data protection law, effective May 2018, applying extraterritorially to any organization processing the personal data of EU residents regardless of the organization's location. Establishes core principles (lawfulness, purpose limitation, data minimization, accuracy, storage limitation, integrity/confidentiality, accountability) and individual rights (access, rectification, erasure, portability, objection, rights regarding automated decision-making).

**Data Controller / Data Processor**
Under GDPR, the data controller is the entity that determines the purposes and means of processing personal data; the data processor processes data on the controller's behalf (e.g., a cloud hosting provider). Different compliance obligations attach to each role.

**Data Minimization**
A GDPR principle (Article 5) requiring that only data "adequate, relevant, and limited to what is necessary" for a stated purpose be collected — a direct legal constraint against "collect everything, you might need it later" data collection defaults.

**Right to Be Forgotten (Right to Erasure)**
A GDPR-granted right (Article 17) allowing individuals to require deletion of their personal data under specified conditions. Carries significant systems engineering implications for architectures where data is replicated across downstream pipelines, backups, and third-party integrations.

**Privacy by Design / Privacy by Default**
GDPR principles (Article 25) requiring that data protection measures be built into system architecture from inception (by design) and that the most privacy-protective configuration be the default setting, requiring active opt-in for less protective options (by default).

**Fourth Amendment**
The US constitutional provision protecting against "unreasonable searches and seizures," originally targeting physical searches of homes and papers, later extended via judicial interpretation to non-physical contexts.

**Reasonable Expectation of Privacy**
The test established in *Katz v. United States* (1967) for determining whether government conduct constitutes a Fourth Amendment "search": whether a person has an actual, subjective expectation of privacy that society recognizes as objectively reasonable.

**Third-Party Doctrine**
The Fourth Amendment doctrine, established in *Smith v. Maryland* (1979), holding that information voluntarily shared with a third party (e.g., a phone company) carries no reasonable expectation of privacy, allowing the government to obtain it from that third party without a warrant. Highly consequential for modern digital services, since nearly all digital activity technically involves sharing data with some third-party provider.

**Carpenter v. United States (2018)**
A Supreme Court decision holding that the government's warrantless acquisition of historical cell-site location data violated the Fourth Amendment, distinguishing this data from prior third-party doctrine cases due to its comprehensiveness and the practical unavoidability of its generation as a byproduct of simply using a cell phone. Explicitly described by the majority as a narrow ruling, leaving open how far its reasoning extends to other data categories.

**CCPA / CPRA**
The California Consumer Privacy Act (2018) and its successor, the California Privacy Rights Act (2020), the most influential US state-level privacy laws, often described as the closest US analogue to GDPR, though narrower in scope and enforcement mechanism.
