# MATH 241 · Recitation 4 — Solutions and Session Notes
## **INSTRUCTOR ONLY** · Do not distribute

**Session:** Thursday of Week 5, 15:00–15:50, SSB 108 · covers Week 4 · unmarked
**PS 4 is due 17:00 the following day.** **Midterm 1 is the Wednesday of Week 6**, covering Weeks 0–5 — this is the last recitation before that material is complete, so leave five minutes at the end for exam questions even at the cost of §4.

---

## Running the Session

**§2 is the session.** The direction of $M$ is the single error that propagates: a student who has it backwards produces plausible matrices all through Weeks 7, 10 and 11 and never gets a contradiction, because $M$ and $M^{-1}$ are both invertible and both "work". **§2(f) is the check that catches it**, and the point of the section is that they leave with the habit of running it.

| | Section | Budget | If it overruns |
|---|---|---|---|
| §1 | Build, don't recall | 10 min | Cut to 5; keep (e) and (f) |
| §2 | The direction of $M$ | 15 min | **Protect. Cut §4 entirely** |
| §3 | A basis that fits | 10 min | Keep (a),(b),(d) |
| §4 | The machine | 10 min | Drop |
| §5 | Clinic + midterm questions | 5 min | Never drop this week |

---

## §0 / §1 — Build, Don't Recall

**Reflection across $y = -x$ is $(x,y) \mapsto (-y,-x)$.**

$$T(e_1) = (0,-1), \qquad T(e_2) = (-1,0), \qquad A = \begin{bmatrix}0&-1\\-1&0\end{bmatrix}$$

*Students who reach for a formula get the sign wrong. **Make them draw it**: $(1,0)$ reflected in $y=-x$ lands at $(0,-1)$, which is visible in two seconds and memorable.*

**(a)** Rotation by $-90°$: $e_1 \mapsto (0,-1)$, $e_2 \mapsto (1,0)$, so $\begin{bmatrix}0&1\\-1&0\end{bmatrix}$.

**(c)** $(x,y)\mapsto(x,-y)$ is **reflection across the $x$-axis**: $\begin{bmatrix}1&0\\0&-1\end{bmatrix}$.

**(d)** Projection onto the $y$-axis: $e_1 \mapsto (0,0)$, $e_2 \mapsto (0,1)$, so $\begin{bmatrix}0&0\\0&1\end{bmatrix}$.

**(e)** With $R$ = rotate $-90°$ and $F$ = reflect across $y=-x$:

$$RF = \begin{bmatrix}-1&0\\0&1\end{bmatrix} \ \text{(reflect across the } y\text{-axis)}, \qquad FR = \begin{bmatrix}1&0\\0&-1\end{bmatrix}\ \text{(reflect across the } x\text{-axis)}$$

**Different.** Same pair of transformations, opposite order, different answer — and both results are reflections, in perpendicular axes.

**(f)**

- **$A^2 = I$:** the reflections — (b) and (c). **Reflecting twice returns everything to where it started**, so the map is its own inverse. *(Rotation by $-90°$ has $A^2 = $ rotation by $180°$, not $I$; a pair that names it should be asked what $A^4$ is.)*
- **$A^2 = A$:** the projection, (d). **Projecting something already on the $y$-axis does nothing.** L14 §2 and Week 1's L05 exercise 6: idempotent and not the identity forces non-invertibility, and here that is visible — the whole $x$-axis is crushed to $0$.

---

## §2 — The Direction of $M$

$$u_1 = (2,1), \quad u_2 = (1,1), \qquad M = \begin{bmatrix}2&1\\1&1\end{bmatrix}, \quad \det M = 1, \quad M^{-1} = \begin{bmatrix}1&-1\\-1&2\end{bmatrix}$$

*(The determinant is 1, so the inverse is integer — chosen deliberately so the arithmetic never obscures the idea.)*

**(b)** $c_1(2,1) + c_2(1,1) = (5,3)$ gives $2c_1 + c_2 = 5$ and $c_1 + c_2 = 3$, so $c_1 = 2$, $c_2 = 1$:

$$[v]_u = (2,1)$$

**(c)**

$$M\begin{bmatrix}2\\1\end{bmatrix} = \begin{bmatrix}5\\3\end{bmatrix}\ ✓ \qquad\qquad M^{-1}\begin{bmatrix}5\\3\end{bmatrix} = \begin{bmatrix}2\\1\end{bmatrix}\ ✓$$

**$M$ takes new coordinates to old.** Make the room say it.

**(d) — the trap**

The reasoning confuses *what $M$ is built from* with *what $M$ does*. $M$'s columns are the new basis vectors **written in old coordinates**, so multiplying by $M$ forms a combination of those vectors — and a combination of the $u_i$ *is* the vector itself, expressed in the old system.

**Compactly: $M[v]_{\text{new}}$ is "assemble $v$ out of the new basis vectors", and the result is an ordinary old-coordinate vector.** Building *out of* the new basis is not the same as converting *into* it; that is the inverse operation.

*This is the sentence to get from a pair rather than to give them. Ask: "what does $M$ times $(1,0)$ give you, and what basis is that answer written in?"*

**(e)**

$$A = \begin{bmatrix}1&2\\0&3\end{bmatrix}, \qquad B = M^{-1}AM = \begin{bmatrix}1&0\\2&3\end{bmatrix}$$

**(f) — the check**

$$T(u_1) = A\begin{bmatrix}2\\1\end{bmatrix} = \begin{bmatrix}4\\3\end{bmatrix}, \qquad [T(u_1)]_u = M^{-1}\begin{bmatrix}4\\3\end{bmatrix} = \begin{bmatrix}1\\2\end{bmatrix} \;=\; \textbf{column 1 of } B\ ✓$$

$$T(u_2) = A\begin{bmatrix}1\\1\end{bmatrix} = \begin{bmatrix}3\\3\end{bmatrix}, \qquad [T(u_2)]_u = M^{-1}\begin{bmatrix}3\\3\end{bmatrix} = \begin{bmatrix}0\\3\end{bmatrix} \;=\; \textbf{column 2 of } B\ ✓$$

> **Insist that every pair runs this check.** It is the only self-contained way to catch a reversed
> $M$. Computing $MAM^{-1}$ instead of $M^{-1}AM$ gives
> $\begin{bmatrix}-5&12\\ -4&9\end{bmatrix}$ — a perfectly respectable matrix, and wrong.
>
> **And it has trace 4 and determinant 3, exactly like $B$.** That is not luck: $MAM^{-1}$ is
> *also* similar to $A$, so every similarity invariant agrees. **The invariants are structurally
> incapable of detecting a reversed $M$**, and checking $B$'s columns against $T(u_1)$ and $T(u_2)$
> is the only test that works.

---

## §3 — A Basis That Fits the Map

$$A = \begin{bmatrix}5&-2\\-2&5\end{bmatrix}$$

**(a)** $A(1,1) = (3,3) = \mathbf{3}(1,1)$ and $A(1,-1) = (7,-7) = \mathbf{7}(1,-1)$.

**(b)** $B = \begin{bmatrix}3&0\\0&7\end{bmatrix}$, **read straight off (a)** — the images are multiples of the basis vectors themselves, so the coordinate columns are $(3,0)$ and $(0,7)$.

**(c)** $\operatorname{trace}A = 10 = 3 + 7$ ✓ · $\det A = 25 - 4 = 21 = 3 \times 7$ ✓

*(Worth pointing out: the trace is the **sum** of the two multiples and the determinant their **product**. That is not a coincidence, and Week 6 explains it.)*

**(d) — the argument**

**Only the description has been simplified.** The transformation is whatever it is; $A$ and $B$ describe the same one.

**A statement visible in $B$ and not in $A$:** *there are two perpendicular directions that this map does not rotate at all — it merely stretches one by 3 and the other by 7.* True of the map, invisible in $\begin{bmatrix}5&-2\\-2&5\end{bmatrix}$, and the first thing you read off $\operatorname{diag}(3,7)$.

**A physical version, if a pair wants one:** a material with different stiffness along two axes. In the natural axes the stress–strain relation is two independent numbers; in any rotated frame it is a full matrix describing the same material.

*Accept any correct statement. **Push back on "the map became simpler"** — that is the misconception the section exists to correct.*

**(e)** They should describe: *look for directions $v$ with $Av$ parallel to $v$* — that is, nonzero $v$ and a scalar $\lambda$ with $Av = \lambda v$.

**A pair that produces that equation has written down the eigenvalue problem**, two weeks early. Tell them so, and tell them the method to solve it is Week 6's, because it needs the determinant, which is Week 5's.

---

## §4 — The Machine

**(a)** Adding entries to the `maps` dictionary should reproduce §1's four matrices exactly.

**(b)** **They do not commute.** $R_{30}F$ and $FR_{30}$ differ — a rotation and a reflection almost never commute. *(Rotations commute with each other, which is L14 §3's remark and is special.)* The prediction is the exercise; most rooms guess wrong after seeing the rotations commute.

**(c)** $D^3$ has the single entry $6$ in position $(1,4)$, and $\frac{d^3}{dx^3}x^3 = 6$ ✓

**(d)** Any $M^{-1}\operatorname{diag}(2,5)M$ works; with $M = \begin{bmatrix}1&1\\0&1\end{bmatrix}$ they get $\begin{bmatrix}2&3\\0&5\end{bmatrix}$ — trace 7, determinant 10, rank 2, matching. *(A pair that picks $M$ with determinant other than 1 will get fractions and should be told that is fine and not a mistake.)*

---

## §5 — Clinic and Midterm Notes

**Q4(c).** §2. Refuse to re-derive; ask them to run §2(f)'s check on their own answer.

**Q3(c), $DJ$ against $JD$.** The unstick: *"which basis vector does the differing entry correspond to, and what does $D$ do to it?"* Do **not** say "the constant"; that is the answer.

**Q5(d).** *"What is $M^{-1}IM$, for any $M$ at all?"* One line, nothing more.

### Midterm 1 — questions to expect this week

The paper covers **Weeks 0–5** and is sat **Wednesday of Week 6, 18:00–19:15, SSB 110**. Week 5 (determinants) will not have happened when this session runs, so the honest answer to "what is on it" is: everything through Friday of Week 5.

**The three things worth saying if asked:**

1. **Weeks 2–4 are cumulative in a way Weeks 0–1 were not.** The four subspaces are used throughout Week 4 and will be used on the paper.
2. **One handwritten sheet, one side.** Put the four-subspace diagram on it, and the change-of-basis direction.
3. **The most common lost marks in past years are $\mathbf{C}$ and $\mathbf{N}$ placed in the wrong $\mathbb{R}^k$, and $M$ reversed.** Both are checkable in seconds and neither is a matter of understanding.

---

## What to Report Back

| Signal | What it means for Week 5 |
|---|---|
| §2(d) needed the answer given | The direction is memorised, not understood. **It will reverse under exam pressure**; flag for the Week 5 recap |
| §3(d) answered "the map got simpler" | The map/description distinction has not landed. **Week 7 is unreadable without it** |
| §3(e) produced $Av = \lambda v$ | Excellent. Tell them Week 6, and that Week 5's determinant is the tool |

---

*MATH 241 · Week 4 · Recitation 4 Solutions · © CSE Department*
