# PHYS 141 · Week 11 Resources

## Required Textbook Reading

- **HRK:** Ch. 21 (Temperature) — all sections; Ch. 22 (Heat and the First Law) §22.1–22.6 for heat,
  specific heat, and transfer mechanisms; Ch. 23 (Kinetic Theory) §23.1–23.4
- **Serway:** Ch. 19 (Temperature) — all sections; Ch. 20 (First Law of Thermodynamics) §20.1–20.4 and
  §20.7 for heat transfer; Ch. 21 (Kinetic Theory of Gases) §21.1–21.2

## Simulations

- **PhET "States of Matter"** — heat a solid and watch the lattice vibrations grow, then the structure
  break down at melting. The temperature-versus-energy plot reproduces the heating curve of
  Lecture 35 directly, plateaus and all.
- **PhET "Gas Properties"** — vary $P$, $V$, $T$ and $n$ independently. Holding one fixed and watching
  the others makes Boyle's, Charles's, and Gay-Lussac's laws obvious rather than memorised.
- **PhET "Energy Forms and Changes"** — conduction between blocks at different temperatures, with the
  energy flow rendered explicitly.

## Video Demonstration Recommendations

- **The bimetallic strip.** Two metals of different $\alpha$ bonded together; heating makes it curl
  towards the lower-$\alpha$ side. This is the mechanism inside every mechanical thermostat.
- **The ball-and-ring experiment.** A metal ball that just passes through a ring at room temperature
  will not pass when heated — and, crucially, *will* pass if the **ring** is heated instead. The
  second half is the experimental answer to the "does the hole expand?" question of Lecture 34.
- **Boiling water in a paper cup.** The water's high specific heat and the latent heat of vaporisation
  hold the paper below its ignition temperature. Memorable, and entirely explained by this week's
  numbers.
- Any **thermal-camera footage** of a person, a building, or a hot mug — an immediate visualisation of
  the $T^4$ radiation of Lecture 36.

## Deeper Reading

- Feynman, *Feynman Lectures Vol. 1*, Ch. 39 ("The Kinetic Theory of Gases") — derives $PV=nRT$ from
  molecular collisions with unusual clarity, and Ch. 44 for heat engines as a preview of Week 12.
- Atkins, *The Laws of Thermodynamics: A Very Short Introduction* — a genuinely short, genuinely good
  conceptual overview, including a clear discussion of why the Zeroth Law is numbered as it is.
- On **Invar** and low-expansion alloys: Guillaume's 1920 Nobel Prize was awarded for this discovery,
  precisely because precision instrumentation was limited by thermal expansion until then.

## Why Water Is Strange (Enrichment)

Water violates the ordinary rules in several ways at once, and hydrogen bonding is behind all of them:

- **Highest specific heat of any common liquid** (4186 J·kg⁻¹K⁻¹). Oceans therefore act as an enormous
  thermal flywheel, moderating global climate.
- **Very high latent heat of vaporisation** ($2.26\times10^6$ J/kg). Evaporation is an extremely
  effective cooling mechanism — the basis of sweating and of evaporative cooling towers.
- **Densest at 4°C, not at freezing.** Ice floats, lakes freeze from the top, and aquatic life
  survives winter.
- **Anomalously high boiling point** for its molecular mass. Compare H₂O (100°C) with H₂S (−60°C),
  a heavier molecule. Without hydrogen bonding, water would be a gas at room temperature.

**Each of these is a precondition for life as it exists**, which is why the properties of water are
discussed in astrobiology as often as in physics.

## Common Pitfalls This Week

1. **Using Celsius in gas-law or radiation calculations.** $PV = nRT$ and $P = e\sigma AT^4$ both
   require **kelvin**. In the radiation case the error is enormous, since $T$ is raised to the fourth
   power. Celsius is acceptable only for temperature *differences*, where the offset cancels.

2. **Saying an object "contains heat".** It contains internal energy. Heat is energy *crossing a
   boundary*, like work.

3. **Forgetting to check whether all the ice melts.** If the available energy is less than $m_{\text{ice}}L_f$,
   some ice remains and the final temperature is exactly 0°C. Solving blindly produces impossible
   answers such as a final temperature below freezing for a mixture of ice and warm water.

4. **Neglecting the calorimeter.** The container absorbs energy too. Ignoring it biases every measured
   specific heat, and Lab 11 Part 1 is designed to expose this.

5. **Assuming a hole shrinks when a plate is heated.** It expands, in exactly the same proportion as
   the material.

6. **Confusing $\alpha$ and $\beta$.** Linear uses $\alpha$; volume uses $\beta = 3\alpha$. Applying
   $\alpha$ to a volume underestimates the expansion threefold.
