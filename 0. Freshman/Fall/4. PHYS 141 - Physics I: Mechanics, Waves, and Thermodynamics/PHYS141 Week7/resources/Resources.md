# PHYS 141 · Week 7 Resources

## Required Textbook Reading

- **HRK:** Ch. 12 (Angular Momentum) — all sections; Ch. 13 (Equilibrium of Rigid Bodies) — all sections
- **Serway:** Ch. 11 (Angular Momentum) — all sections; Ch. 12 (Static Equilibrium and Elasticity) — §12.1–12.3

## Simulations

- **PhET "Torque"** (revisit from Week 6) — now focus on the equilibrium tab if available, balancing multiple torques.
- Search for a "gyroscope precession" simulation or video demonstration — seeing a real gyroscope resist tipping over (and instead precess) is far more intuitive than any amount of reading.

## Video Demonstration Recommendation

Search for classic footage of a person on a rotating stool holding a spinning bicycle wheel, flipping it over — one of the most famous and striking demonstrations in physics pedagogy, directly illustrating conceptual question 4 from Lecture 23. Many university physics departments have recorded versions of this demonstration.

## Deeper Reading

- Feynman, *Feynman Lectures Vol. 1*, Ch. 20: "Rotation in Space" — includes Feynman's discussion of gyroscopes and precession, going somewhat beyond this course's scope but very illuminating.
- Kepler's original 1609 statement of his Second Law (in *Astronomia Nova*) is a remarkable historical document — he derived it purely from Tycho Brahe's observational data, decades before Newton showed WHY it must be true (central forces + angular momentum conservation).

## The Neutron Star Connection (Enrichment)

Problem 13 in this week's problem set touches on one of the most spectacular real-world applications of angular momentum conservation: when a massive star's core collapses in a supernova, conservation of angular momentum (combined with the dramatic decrease in radius) can spin up the remnant neutron star to hundreds of rotations per second. The fastest known pulsar (PSR J1748-2446ad) rotates at approximately 716 times per second — a direct astrophysical consequence of exactly the same $I_i\omega_i=I_f\omega_f$ principle used for a spinning skater.

## Common Pitfalls This Week

1. **Forgetting angular momentum depends on the choice of origin/axis.** Unlike mass or moment of inertia about a fixed body-frame axis, L for a particle changes value (in general) if you change your reference point — always state which point/axis you're computing L about.

2. **Assuming angular momentum conservation implies kinetic energy conservation.** These are fully independent — Lecture 23 explicitly shows KE can increase (skater) or decrease (rotational collision) while L stays exactly fixed.

3. **Using τ=Iα when I is changing with time.** The more general and always-valid form is τ=dL/dt=d(Iω)/dt. When I is constant, this reduces to Iα; when I changes, you must account for the full derivative (or, as in this week's conservation problems, simply use L_i=L_f directly, which sidesteps the issue).

4. **Forgetting that equilibrium requires BOTH ΣF=0 and Στ=0.** Students commonly check only one condition — always verify you have enough independent equations (matching your number of unknowns) before declaring a problem solved.

5. **Choosing a pivot point poorly.** Always look for an unknown force acting at some point, and choose your torque pivot exactly there — this single choice can turn a 3-equation, 3-unknown system into a 1-equation, 1-unknown solve for the trickiest variable, then simple substitution for the rest.
