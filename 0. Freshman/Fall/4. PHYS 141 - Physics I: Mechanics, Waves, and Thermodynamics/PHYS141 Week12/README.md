# PHYS 141 · Physics I: Mechanics, Waves & Thermodynamics
## Week 12: Thermodynamics II — Laws, Entropy & Heat Engines

**Semester:** Fall | **Credits:** 4 | **Lab:** Weekly 3-hr lab session

---

## Week 12 Contents

| File | Description |
|------|-------------|
| [[L37 The First Law of Thermodynamics]] | Internal energy; $\Delta U = Q-W$; the four standard processes; cycles; why perpetual motion is impossible |
| [[L38 The Second Law Entropy and Heat Engines]] | Clausius and Kelvin–Planck; engine efficiency; the Carnot limit; refrigerators and heat pumps; entropy |
| [[L39 Review and the Road Ahead]] | Course synthesis: the structural analogies, the five ideas worth keeping, exam preparation |
| [[LAB 12 Heat Engines and Thermal Efficiency]] | Gas laws and absolute zero by extrapolation; work from a $PV$ cycle; engine efficiency vs Carnot; heat-pump COP and entropy |
| [[PS 12 Laws of Thermodynamics Entropy and Heat Engines]] | 10 problems on the First and Second Laws, engines, and entropy |
| [[QUIZ 12 Laws of Thermodynamics Entropy and Heat Engines]] | 10-question quiz (administered Monday of Finals Week) |
| [[PHYS141 Week12/resources/Resources\|Resources]] | Textbook references, simulations, deeper reading, final-exam guidance |
| [[PHYS141 Week12/solutions_instructor/PS 12 Solutions\|PS 12 Solutions]] | Full worked solutions (instructor only) |
| [[PHYS141 Week12/solutions_instructor/LAB 12 Solutions\|LAB 12 Solutions]] | Expected data, analysis answers, systematic errors to look for |

---

## Learning Objectives

By the end of Week 12, you will be able to:

1. Define internal energy and explain why it is a state function while $Q$ and $W$ are not
2. Apply $\Delta U = Q - W$ with a consistently stated sign convention
3. Compute the work done by a gas as the area under a $PV$ curve
4. Analyse isothermal, isobaric, isochoric, and adiabatic processes and identify which quantity vanishes in each
5. Explain why an adiabatically expanding gas cools
6. Show that $Q_{\text{net}} = W_{\text{net}}$ for any cycle, and read net work as the enclosed $PV$ area
7. State both forms of the Second Law and explain why they are equivalent
8. Compute heat-engine efficiency and the Carnot limit, and explain why a cold reservoir is unavoidable
9. Compute refrigerator and heat-pump COPs and explain why COP > 1 conserves energy
10. Compute entropy changes for phase changes, isothermal expansions, and heat flow between reservoirs
11. Use $\Delta S_{\text{total}} \ge 0$ to determine whether a process can occur
12. Explain $S = k_B\ln\Omega$ and why the Second Law is statistical

---

## Schedule

| Day | Activity |
|-----|----------|
| Mon 14 Dec, 14:00 | Lecture 37 — The First Law of Thermodynamics |
| Tue 15 Dec, 14:00 | Lecture 38 — The Second Law, Entropy, and Heat Engines |
| Thu 17 Dec, 14:00–17:00 | Lab 12 — Heat Engines and Thermal Efficiency (3 hrs) |
| Fri 18 Dec, 14:00 | Lecture 39 — Review and the Road Ahead |
| Fri 18 Dec, 15:00 | Problem Set 12 released — due Wed 23 Dec, 17:00 (finals week) |

---

## Key Results

| | |
|---|---|
| Internal energy | $U = \tfrac32nRT$ (monatomic); **state function** |
| First Law | $\Delta U = Q - W$ |
| Work | area under the $PV$ curve |
| Isothermal | $\Delta U = 0$, $Q = W = nRT\ln(V_2/V_1)$ |
| Isobaric | $W = P\Delta V$ |
| Isochoric | $W = 0$ |
| Adiabatic | $Q = 0$, $\Delta U = -W$; **expansion cools** |
| Cycle | $Q_{\text{net}} = W_{\text{net}}$ = enclosed area |
| Clausius | no spontaneous cold → hot heat flow |
| Kelvin–Planck | heat cannot be **fully** converted to work |
| Efficiency | $e = 1 - Q_c/Q_h$ |
| **Carnot limit** | $e = 1 - T_c/T_h$ — substance-independent |
| Raising $T_h$ | helps more than lowering $T_c$ |
| COP fridge / heat pump | $T_c/(T_h-T_c)$ / $T_h/(T_h-T_c)$; **differ by exactly 1** |
| Entropy | $\Delta S = \int dQ_{\text{rev}}/T$; state function |
| Second Law | $\Delta S_{\text{total}} \ge 0$ |
| Statistical form | $S = k_B\ln\Omega$ |

---

## Connections

**Back:** Week 4's conservation of energy becomes the First Law once heat is admitted as a transfer
mechanism. Week 11's ideal gas is the working substance throughout, and its kinetic theory is what
makes $U = \tfrac32nRT$ more than a definition.

**Forward:** PHYS 320 derives every result of this week from statistical mechanics — counting
microstates rather than postulating laws. ECE and mechanical engineering courses apply the Carnot
limit to real cycles: Otto, Diesel, Rankine, Brayton.

**Sideways:** Shannon's information entropy in CS 350 has the same functional form as
$S = k_B\ln\Omega$, and for the same reason — both count the microstates consistent with what is
known. That correspondence is not an analogy but an identity of structure.

---

*This concludes PHYS 141.*
