# PHYS 141 — Lecture 11
# Newton's Third Law & Free Body Diagrams

> **Core Principle:** Forces never exist in isolation — they always come in pairs. Newton's Third Law says that whenever object A exerts a force on object B, object B simultaneously exerts an equal and opposite force on object A. These paired forces act on *different* objects, which is why they never cancel. The free body diagram is the tool that keeps this straight.

---


## Where This Fits

**Previously:** **L10** gave us F = ma. Applying it correctly requires accounting for *every* force, which is what a free body diagram enforces.

---

## 1. Newton's Third Law

> **Newton's Third Law:** If object A exerts a force on object B, then object B exerts a force on object A that is equal in magnitude and opposite in direction.

$$\vec{F}_{A \text{ on } B} = -\vec{F}_{B \text{ on } A}$$

### 1.1 The Precise Language

Every statement of the Third Law must identify both objects. The paired forces are called an **action-reaction pair** (though the terms "action" and "reaction" are interchangeable — neither force causes the other; they arise simultaneously).

**Examples of correct Third Law pairs:**

| Action force | Reaction force |
|-------------|---------------|
| Earth pulls you down (gravity) | You pull Earth up (gravity) |
| Floor pushes your feet up (normal) | Your feet push floor down (normal) |
| Rocket expels gas backward (thrust on gas) | Gas pushes rocket forward (thrust on rocket) |
| You push wall rightward | Wall pushes you leftward |
| Bat hits ball forward | Ball hits bat backward |

### 1.2 Why Third Law Pairs Do NOT Cancel

This is the most common misconception in introductory physics. Students see "equal and opposite forces" and conclude they cancel, giving zero net force. **This is wrong** because:

**Third law pairs always act on different objects.**

Newton's second law says ΣF⃗ = ma⃗ for a *single* object. When you draw the free body diagram of object B, you include only forces *on* B — not forces B exerts on others. The reaction force (B on A) acts on A, not on B, so it never appears in B's free body diagram.

**Analogy:** You and a friend each have $10. You give your friend $10 (action: money flows from you to friend). Your friend gives you $10 (reaction: money flows from friend to you). Both transfers are equal. But your net balance changed by +$10 − $10 = $0 only if we add *both* transfers *to you*. If we only look at your account separately, the outgoing $10 reduces your balance — the incoming $10 is a separate transaction.

> **Deep Why:** The Third Law is a consequence of Newton's laws plus the conservation of momentum (Week 5). If A pushes B forward, and B does not push A backward with equal force, then the total momentum of the A+B system would change with no external force — violating momentum conservation. The Third Law is, in a deep sense, what momentum conservation looks like at the level of individual force pairs.

---

## 2. The Free Body Diagram (FBD)

The free body diagram is the single most important problem-solving tool in mechanics. Done correctly, it makes Newton's second law almost mechanical to apply. Done incorrectly or skipped, it is the root cause of most force-problem errors.

### 2.1 Rules for a Correct FBD

1. **Isolate the object.** Represent it as a dot or simple shape. Mentally "cut" all physical connections (strings, surfaces, contacts) and replace them with the forces those connections exert.

2. **Draw every force acting ON the object.** Include:
   - Gravity: always present, always downward, magnitude mg
   - Normal force: whenever the object is in contact with a surface; perpendicular to the surface
   - Tension: whenever a string/rope/cable is attached; along the string, away from the object
   - Friction: whenever there is contact with a surface and relative motion (or tendency of motion) exists; parallel to the surface
   - Any other applied forces given in the problem

3. **Do NOT draw:**
   - Forces the object exerts on other things (those go on the other object's FBD)
   - Velocity or acceleration vectors (these are not forces)
   - Internal forces if treating the object as a rigid body

4. **Label every force** with its symbol (N, T, f, mg, F_app, etc.)

5. **Draw arrows from the point of application** (or from the center of mass for gravity), pointing in the correct direction.

6. **Establish a coordinate system** on the FBD. Mark x and y axes. If acceleration is known to be along a particular direction (e.g., down an incline), align an axis with it.

### 2.2 Common FBD Mistakes

| Mistake | Consequence |
|---------|-------------|
| Including both halves of a Newton's 3rd Law pair on one FBD | Double-counting forces; wrong equations |
| Drawing acceleration as a force | Fictitious extra force in equations |
| Wrong direction for normal force (not perpendicular to surface) | Wrong component decomposition |
| Omitting gravity | Missing a force entirely |
| Drawing tension pointing toward the object (into it) instead of away | Wrong sign in equations |

---

## 3. Normal Force — Not Always Equal to mg

A common error: automatically setting N = mg. This is only true when:
- The surface is horizontal AND
- There is no vertical acceleration AND
- No other vertical forces act

**When N ≠ mg:**

| Situation | Normal force |
|-----------|-------------|
| Object on horizontal surface, no other vertical forces | N = mg |
| Elevator accelerating upward at a | N = m(g + a) |
| Elevator accelerating downward at a | N = m(g − a) |
| Object on incline at angle θ | N = mg cosθ |
| Person in a car going over a hill (centripetal acceleration downward) | N = m(g − v²/r) |
| Object pressed against ceiling by upward force | N acts downward on object |

The normal force is always the force required to prevent the object from passing through the surface — it is determined by the equations of motion, not assumed.

---

## 4. Tension in Ropes and Strings

**Assumptions we make this semester (unless stated otherwise):**
- Strings and ropes are **massless** (zero mass) and **inextensible** (don't stretch)
- Pulleys are **massless and frictionless** (they only redirect tension)

Under these assumptions:
- The tension magnitude is the same throughout a continuous string
- A pulley reverses the direction of the tension force but does not change its magnitude

**Why massless strings?** From ΣF = ma for the string: F_on_string = m_string × a. If m_string = 0, then ΣF = 0 even if a ≠ 0. This means the forces at both ends of the string must be equal in magnitude — hence uniform tension throughout.

---

## 5. Worked Examples

### Example 11.1 — Block on frictionless surface with horizontal string

A 4.0 kg block sits on a frictionless horizontal surface. A horizontal string pulls it to the right with tension T = 12 N. Find the acceleration and the normal force.

**FBD on block:**
- W = mg = 39.2 N downward
- N upward (normal from surface)
- T = 12 N rightward (tension)

**x:** ΣFₓ = T = ma → 12 = 4.0 · a → **a = 3.0 m/s² (rightward)**

**y:** ΣFᵧ = N − mg = 0 → **N = 39.2 N**

---

### Example 11.2 — Two blocks connected by a string (horizontal, frictionless)

Block A (mass 3.0 kg) is connected by a string to Block B (mass 5.0 kg). An external force F = 16 N pulls Block B to the right. Both blocks are on a frictionless surface. Find the acceleration of the system and the tension in the string.

**Strategy:** Treat the two-block system as a whole first to find acceleration, then isolate one block to find tension.

**System (A+B together):**
Only external horizontal force = 16 N. Total mass = 8.0 kg.
$$a = \frac{F}{m_{total}} = \frac{16}{8.0} = 2.0 \text{ m/s}^2$$

**Isolate Block A (only force on it horizontally is tension T from string):**
$$T = m_A \cdot a = 3.0 \times 2.0 = \mathbf{6.0 \text{ N}}$$

**Verify with Block B** (forces: F forward, T backward):
$$F - T = m_B \cdot a \implies 16 - 6.0 = 5.0 \times 2.0 = 10 \checkmark$$

---

### Example 11.3 — Identifying Third Law pairs

A book rests on a table.

**Identify all Third Law pairs:**

Pair 1: Earth pulls book downward (gravity) ↔ Book pulls Earth upward (gravity)
Pair 2: Table pushes book upward (normal) ↔ Book pushes table downward (normal)
Pair 3: Earth pulls table downward (gravity) ↔ Table pulls Earth upward (gravity)
Pair 4: Floor pushes table upward (normal) ↔ Table pushes floor downward (normal)

**What forces act on the book?**
- Earth's gravity on book (downward)
- Table's normal force on book (upward)

These two are NOT a Third Law pair (they act on the same object — the book). They happen to be equal because the book is in equilibrium (ΣF = 0). If you placed the book on a scale in an accelerating elevator, gravity and normal force would no longer be equal — but they would still not be a Third Law pair.

**What is the Third Law pair of Earth's gravity on the book?**
The book's gravity on Earth — pulling Earth upward. This force exists and is real, but Earth's mass is so enormous (6×10²⁴ kg) that the resulting acceleration of Earth is ~10⁻²⁵ m/s² — completely unmeasurable.

---

### Example 11.4 — FBD on an incline

A 6.0 kg block sits on a frictionless incline at 30°. Find the acceleration and the normal force.

**FBD:** Weight mg = 58.9 N straight down. Normal force N perpendicular to incline surface (at 30° from vertical, or 60° from horizontal).

**Coordinate system:** x along the incline (positive down the slope), y perpendicular to incline (positive away from surface).

**Decompose gravity:**
- Along incline (x): mg sin30° = 58.9 × 0.5 = 29.4 N (down the slope)
- Perpendicular to incline (y): mg cos30° = 58.9 × 0.866 = 51.0 N (into the slope)

**x:** ΣFₓ = mg sinθ = ma → **a = g sin30° = 4.90 m/s²** (down the slope)

**y:** ΣFᵧ = N − mg cosθ = 0 → **N = mg cos30° = 51.0 N**

Note: N < mg (51.0 N < 58.9 N). The surface supports only the component of gravity perpendicular to it.

---

## 6. Summary

| Concept | Key Point |
|---------|-----------|
| Newton's 3rd Law | F_{A on B} = −F_{B on A}; equal magnitude, opposite direction |
| Action-reaction pairs | Always on *different* objects; never cancel |
| Free body diagram | Isolate one object; draw all forces ON it; nothing else |
| Normal force | Always ⊥ to surface; NOT always equal to mg — determined by equations |
| Tension | Same throughout a massless, inextensible string; pulls away from object |
| Incline decomposition | mg sinθ along slope; mg cosθ perpendicular to slope |

---


---

## CS Connection — Free Body Diagrams as Interface Boundaries

Drawing a free body diagram means choosing a system boundary and enumerating everything crossing it. That is precisely what defining a module interface does — decide what is inside, then account for every interaction with the outside. Third-law pairs act on different bodies and therefore never appear in the same diagram, which is the physical version of the rule that a function's internal state is not its caller's concern.

---

## Looking Ahead

**L12** puts the method to work on the standard hard cases: friction, inclines, and connected systems.

## Conceptual Questions

1. A horse pulls a cart forward. By Newton's Third Law, the cart pulls the horse backward with equal force. So why does the horse-cart system accelerate at all?

2. You stand on a bathroom scale in an elevator. The scale reads your "weight." Explain what the scale actually measures (hint: it's not gravitational force). What does the scale read when the elevator is in free fall?

3. A book is pushed against a vertical wall by a horizontal force F. List all the forces on the book and identify which are Third Law pairs with forces on other objects.

4. On a frictionless incline at angle θ, a block accelerates at g sinθ. At θ = 0° (horizontal surface), what should the formula give? At θ = 90° (vertical drop), what does it give? Do both limits make physical sense?
