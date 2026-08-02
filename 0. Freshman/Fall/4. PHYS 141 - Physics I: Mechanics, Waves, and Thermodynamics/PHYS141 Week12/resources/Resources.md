# PHYS 141 — Week 12 Resources

## Required Textbook Reading

- **HRK:** Ch. 22 (Heat and the First Law) §22.7–22.9; Ch. 24 (Entropy and the Second Law) — all
  sections
- **Serway:** Ch. 20 (First Law) §20.5–20.7; Ch. 22 (Heat Engines, Entropy, and the Second Law) — all
  sections

## Simulations

- **PhET "Gas Properties"** — hold $T$, $P$, or $V$ fixed in turn and drive the system round a cycle.
  Watching the work accumulate as the piston moves makes the $\int P\,dV$ interpretation concrete.
- **PhET "States of Matter"** — useful again this week for the entropy discussion: watching a solid
  melt shows directly why the disordered state has more accessible arrangements.
- Search for an interactive **Carnot cycle** applet where $T_h$ and $T_c$ can be varied. Raising
  $T_h$ against lowering $T_c$ by the same amount, and seeing the asymmetry in the efficiency gain, is
  worth five minutes.

## Video Demonstration Recommendations

- **Fire syringe (adiabatic compression).** Compressing air rapidly in a sealed tube ignites a wisp of
  cotton. No heat is added; the temperature rise comes entirely from work done on the gas — Lecture
  37's adiabatic result in its most dramatic form, and the principle of the diesel engine.
- **Stirling engine demonstration.** A visible external-combustion engine running on a temperature
  difference as small as a hand on a cold plate. It makes the Carnot argument tangible: the smaller
  the temperature difference, the less work available.
- **Rubber band thermodynamics.** Stretch a rubber band against your lip and it warms; let it relax
  and it cools. The entropy explanation — stretching aligns the polymer chains, reducing their
  disorder — is unusual and memorable.

## Deeper Reading

- Feynman, *Feynman Lectures Vol. 1*, Ch. 44 ("The Laws of Thermodynamics") and Ch. 46 ("Ratchet and
  Pawl"). Ch. 46 is the best treatment anywhere of why a microscopic machine cannot cheat the Second
  Law, and it is genuinely entertaining.
- Atkins, *The Second Law* — a book-length treatment aimed at exactly this level.
- Carnot's *Réflexions sur la puissance motrice du feu* (1824) — remarkable for having derived the
  efficiency limit **before** the First Law was formulated, and while still believing in the caloric
  theory of heat. A useful reminder that a correct result can be reached from a wrong model.

## Why Entropy Appears in Computer Science (Enrichment)

Shannon's information entropy,
$$H = -\sum_i p_i\log_2 p_i$$
has the same form as Boltzmann's $S = k_B\ln\Omega$, and the resemblance is not superficial. Both
answer: *how many microscopic configurations are consistent with what I know?*

Consequences you will meet:

- **Data compression.** Shannon's source coding theorem says no lossless compressor can beat the
  entropy of the source. This is the information-theoretic version of "you cannot get something for
  nothing", and it is why ZIP files have a floor.
- **Landauer's principle.** Erasing one bit of information *must* dissipate at least $k_BT\ln2$ of
  energy as heat — about $3\times10^{-21}$ J at room temperature. **Computation has a thermodynamic
  cost**, and it has been measured experimentally.
- **Maxwell's demon.** The 150-year-old paradox of a creature sorting fast and slow molecules to
  violate the Second Law was resolved by noticing that the demon must *record* what it observes — and
  eventually erase those records, paying Landauer's price.

**The link between thermodynamics and information is one of the deepest results of twentieth-century
physics**, and you are now equipped to see why it exists.

## Common Pitfalls This Week

1. **Sign confusion in the First Law.** $\Delta U = Q - W$ with $W$ done *by* the system, or
   $\Delta U = Q + W$ with $W$ done *on* it. Both are correct; mixing them is not. **State your
   convention at the top of every solution.**

2. **Using Celsius in efficiency or entropy formulas.** $e = 1 - T_c/T_h$ requires kelvin. With
   Celsius, an engine between 100°C and 0°C would appear to have efficiency 1.

3. **Assuming an efficient engine can exceed Carnot.** No design, working fluid, or budget can. If a
   calculation gives $e > e_{\text{Carnot}}$, the arithmetic is wrong.

4. **Thinking COP > 1 breaks conservation.** A heat pump *moves* heat, it does not create it. A COP
   of 4 means 3 units come from outside and 1 from the work input.

5. **Computing entropy with $Q/T$ when $T$ changes.** That formula holds only at constant temperature
   — melting, boiling, or a large reservoir. When the temperature varies, you need
   $\Delta S = mc\ln(T_2/T_1)$.

6. **Forgetting that the Second Law applies to the *total*.** A system's entropy can certainly
   decrease — a freezer does it every day. What cannot decrease is the entropy of system plus
   surroundings.

## Final Exam Note

Lecture 39 contains the complete revision plan, the formula summary for all twelve weeks, and the
five most common exam errors. **Start there rather than with these resources.**
