# MATH 241 · Linear Algebra
## Week 5 · Lecture 3 of 3 · **Friday**
### The Determinant as Volume, and the Product Rule

*“We must admit with humility that, while number is purely a product of our minds, space has a reality outside our minds, so that we cannot completely prescribe its properties a priori.”* — Carl Friedrich Gauss, letter to Friedrich Wilhelm Bessel (1830)

---

**Reading:** Strang §5.1 (the area discussion), §5.3 · **Previous:** L17, cofactors · **Next:** Week 6, eigenvalues

**Coursework:** 📝 **PS 4** due today 17:00 · 📊 **Quiz 6** Tue of Week 6 · 📝 **PS 6** released Wed of Week 6, due Fri of Week 7 17:00 · 💬 **Recitation 5** Thu of Week 6 15:00–15:50

> **PS 4 is due at 17:00 today.** PS 5 was released Wednesday and is due the Friday of Week 6.
>
> **Midterm 1 is next Wednesday**, 18:00–19:15, SSB 110, covering **Weeks 0–5**. This lecture
> completes the examinable material.

---

## 1. What the Three Properties Are Really About

L16's three properties look arbitrary. **They are not: they are the properties of *area*.**

Take the unit square in $\mathbb{R}^2$, with corners $0$, $e_1$, $e_2$, $e_1+e_2$. Apply $A$. The square becomes a **parallelogram** with edges $Ae_1$ and $Ae_2$ — the columns of $A$.

Now read L16's properties as statements about the area of that parallelogram:

| | Property | As a statement about area |
|---|---|---|
| **P1** | $\det I = 1$ | the unit square has area 1 |
| **P2** | swapping rows flips the sign | **orientation** — the sign records whether the plane was flipped |
| **P3** | linear in each row | doubling one edge doubles the area; and areas add when one edge is split |

**Three unremarkable facts about area, and they determine the determinant uniquely.** So:

$$\boxed{\;\lvert\det A\rvert = \text{the factor by which } A \text{ scales area (or volume, in } \mathbb{R}^n)\;}$$

*(P3's additivity is the one that repays a picture: two parallelograms sharing an edge, with the other edges adding, have areas that add. Draw it once.)*

---

## 2. Measured, on Week 4's Transformations

| Transformation | $\det$ | Area factor | |
|---|---:|---:|---|
| identity | $1$ | $1$ | |
| scale $x$ by 3 | $3$ | $3$ | one direction stretched |
| scale both by 2 | $4$ | $4$ | $2^2$ — **not** $2$ |
| shear $\begin{bmatrix}1&2\\0&1\end{bmatrix}$ | $1$ | $1$ | **area-preserving** |
| rotate $90°$ | $1$ | $1$ | rigid |
| reflect across $y=x$ | $-1$ | $1$ | rigid, **orientation reversed** |
| project onto $y=x$ | $0$ | $0$ | **the plane collapses to a line** |

**Three of these deserve a sentence.**

**The shear has determinant 1.** It slides the unit square sideways into a parallelogram with the same base and the same height — **and area is base times height**, so nothing changes. This is L16 §3(c) made visible: *adding a multiple of one row to another does not change the determinant*, because it is a shear.

**The reflection has determinant $-1$.** The area is unchanged and the sign is not. **The sign is orientation**: a reflection turns an anticlockwise circuit of the square into a clockwise one, and no rotation can do that. *(In $\mathbb{R}^3$ this is handedness — a reflection turns a right-handed coordinate frame into a left-handed one, which is why CS 321 cares about the sign of a transformation's determinant and why a negative-determinant model matrix makes surface normals point inwards.)*

**The projection has determinant 0.** It squashes the plane onto a line, and a line has zero area. **This is $\det = 0 \iff$ singular, seen rather than proved** — the map destroys a dimension, so no inverse can restore it.

---

## 3. The Product Rule

> $$\det(AB) = \det(A)\det(B)$$

**Given §1, this is almost obvious:** applying $B$ scales volume by $\det B$, then applying $A$ scales it by $\det A$, so the composite scales by the product. *(A proof from the properties alone is available and is Strang §5.3; the volume argument is the one to remember.)*

**Verified:** $\det A = 24$, $\det C = 13$, and $\det(AC) = 312 = 24 \times 13$ ✓

**Three consequences, all immediate:**

**(a) $\det(A^{-1}) = 1/\det A$.** From $AA^{-1} = I$: $\det A \cdot \det(A^{-1}) = 1$. *(And this re-proves that a singular matrix has no inverse — you cannot divide by zero.)*

**(b) $\det(A^k) = (\det A)^k$.**

**(c) $\det(AB) = \det(BA)$**, even though $AB \ne BA$. **Verified: both are 312.** The determinant is blind to the order, because multiplication of numbers is commutative even when multiplication of matrices is not.

### And the transpose

$$\det(A^\mathsf{T}) = \det A$$

**Verified: both 24.** *(It follows from the $n!$ formula, where transposing merely re-indexes the same $n!$ products.)*

**The consequence is a labour-saving one: every statement about rows is automatically a statement about columns.** L16's P2 and P3 were about rows; they hold for columns too, and L17's expansion works along any row *or* column, for this reason.

---

## 4. Similarity Invariance — the Debt from Week 4

Week 4's L15 §6 asserted that similar matrices have the same determinant and pointed at Week 5. **Here it is, in one line:**

$$\det(M^{-1}AM) = \det(M^{-1})\det(A)\det(M) = \frac{1}{\det M}\det(A)\det(M) = \det(A) \qquad \square$$

**Verified:** with $M$ of determinant 2, $B = M^{-1}AM$ came out as a completely different matrix, and $\det B = 24 = \det A$ ✓

> **So the determinant belongs to the transformation, not to the basis** — which is exactly what
> §1 says it should, since *the factor by which volume is scaled* is a fact about the map and cannot
> depend on which coordinates you describe it in.
>
> **This is the first of Week 4's three invariants to be properly explained.** Rank was easy — it is
> $\dim(\text{range})$. Trace has a one-line proof and no obvious meaning yet. **The determinant now
> has both a proof and a reason**, and Week 6 will give the trace its reason too, when both turn out
> to be functions of the eigenvalues.

---

## 5. The Sign, and Where You Have Met It Before

$\det A > 0$ means $A$ **preserves orientation**; $\det A < 0$ means it **reverses** it.

In $\mathbb{R}^2$: does an anticlockwise circuit stay anticlockwise? In $\mathbb{R}^3$: does a right-handed frame stay right-handed? **Rotations preserve; reflections reverse; and no continuous family of rotations can ever produce a reflection**, because the determinant would have to pass through $0$ on the way from $+1$ to $-1$, and a rigid motion is never singular.

> **The Jacobian.** In MATH 142's change of variables,
> $$\iint_R f(x,y)\,dx\,dy = \iint_{R'} f\big(x(u,v), y(u,v)\big)\,\Big\lvert\det J\Big\rvert\,du\,dv$$
> and the factor $\lvert\det J\rvert$ is **exactly §1**: the local area-scaling factor of the
> coordinate change, linearised at each point. **The absolute value is there because area is
> positive and orientation is not the integral's business.**
>
> **Polar coordinates' mysterious $r$ is a determinant.** With $x = r\cos\theta$, $y = r\sin\theta$,
> $$\det J = \det\begin{bmatrix}\cos\theta & -r\sin\theta\\ \sin\theta & r\cos\theta\end{bmatrix} = r\cos^2\theta + r\sin^2\theta = r$$
> **You have been using this lecture's theorem since MATH 142 without a derivation for it.**

---

## 6. The Standing Warning, Renewed

Everything above is exact mathematics. **None of it makes $\det$ a good numerical test.**

- **$\det$ is not scale-invariant.** $\det(cA) = c^n\det A$, so a $1000\times1000$ matrix of entries around $0.1$ has a determinant near $10^{-1000}$ and underflows to zero — while being perfectly well conditioned.
- **Week 0's L03 §6 measured it:** $\det H_{10} = 2.2\times10^{-53}$, and scaling $H_{10}$ by 10 multiplies that by $10^{10}$ while changing the accuracy of a solve not at all.
- **PS 0 Q5(b) built both failures:** determinant $10^{-8}$ with condition number $1$, and determinant $1$ with condition number $10^{12}$.

> **The rule, one last time.** Use $\det A \ne 0$ in proofs and in $2\times2$ work by hand. **To ask
> a machine whether a system can be trusted, compute $\operatorname{cond}(A)$** — which is
> scale-invariant, and which is the number Weeks 8 to 11 keep returning to.

---

## 7. What to Take Away

1. **L16's three properties are the properties of area**, which is why they determine a unique function.
2. **$\lvert\det A\rvert$ is the volume-scaling factor**, and $\det A = 0$ means a dimension was destroyed.
3. **A shear has determinant 1** — base times height — which is L16 §3(c) made visible.
4. **$\det(AB) = \det A \det B$**, hence $\det(A^{-1}) = 1/\det A$ and $\det(AB) = \det(BA)$ even though $AB \ne BA$.
5. **$\det(A^\mathsf{T}) = \det A$**, so every row fact is a column fact for free.
6. **$\det(M^{-1}AM) = \det A$** — Week 4's debt paid, and the determinant belongs to the transformation.
7. **The sign is orientation**, and $\lvert\det J\rvert$ in MATH 142's change of variables is this lecture. **Polar coordinates' $r$ is a determinant.**
8. **Still not a numerical test.** $\det$ is not scale-invariant; $\operatorname{cond}$ is.

---

## Exercises

*(Not assessed. PS 5 is due Friday of Week 6 — the week of the midterm.)*

1. Find the area of the parallelogram with edges $(3,1)$ and $(1,4)$. Then with edges $(1,4)$ and $(3,1)$ — **what changed, and what did not?**
2. $A$ is $3\times3$ with $\det A = -2$. Find $\det(A^\mathsf{T})$, $\det(A^{-1})$, $\det(3A)$, $\det(A^3)$, $\det(-A)$.
3. Show that an orthogonal matrix ($Q^\mathsf{T}Q = I$) has $\det Q = \pm1$. **What does each sign mean geometrically?** *(Week 8's matrices, and Week 3's $P^{-1} = P^\mathsf{T}$ was the first example.)*
4. Compute the Jacobian determinant for spherical coordinates $x = \rho\sin\phi\cos\theta$, $y = \rho\sin\phi\sin\theta$, $z = \rho\cos\phi$. *(You should get $\rho^2\sin\phi$ — the factor MATH 142 gave you without explanation.)*
5. **True or false:** if $\det A = \det B$ then $A$ and $B$ are similar. Give a counterexample. *(Week 4's PS 4 Q5(d) has one to hand.)*
6. A $1000\times1000$ matrix has every entry about $0.1$ and is perfectly well conditioned. Estimate its determinant. **What happens when a `double` tries to hold it, and what should you have computed instead?**

---

*MATH 241 · Week 5 · L18 · © CSE Department*
