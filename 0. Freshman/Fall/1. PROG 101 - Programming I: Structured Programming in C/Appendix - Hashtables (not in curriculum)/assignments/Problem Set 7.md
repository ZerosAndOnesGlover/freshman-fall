# PROG 101 · Programming I: Structured Programming in C
## Appendix · Problem Set 7

**Released:** End of this appendix Thursday
**Due:** Before Week 8 Lecture 1
**Directory:** `~/prog101/week7/ps7/`
**Total:** 100 points

---

## Problem 1: Open Addressing Implementation (25 pts)

Create `open_addressing.h`/`open_addressing.c`. Building on Lecture 2, implement a **complete** open-addressing hash table supporting all three probing strategies, selectable at creation time.

```c
typedef enum {
    PROBE_LINEAR,
    PROBE_QUADRATIC,
    PROBE_DOUBLE_HASH
} ProbeStrategy;

typedef struct OpenHashTable OpenHashTable;

OpenHashTable *oht_create(size_t initial_size, ProbeStrategy strategy);
void           oht_destroy(OpenHashTable *oht);

bool oht_insert(OpenHashTable *oht, const char *key, int value);
bool oht_get(const OpenHashTable *oht, const char *key, int *out_value);
bool oht_remove(OpenHashTable *oht, const char *key);   /* must tombstone correctly */

size_t oht_count(const OpenHashTable *oht);
double oht_load_factor(const OpenHashTable *oht);

/* Diagnostics: average number of probes needed across all successful
 * ht_get calls made SINCE THE LAST RESET. Reset the counters with
 * oht_reset_probe_stats before a batch of measured operations. */
void   oht_reset_probe_stats(OpenHashTable *oht);
double oht_average_probes(const OpenHashTable *oht);
```

### Requirements

- Implement automatic resizing when load factor exceeds 0.5 (lower threshold than chaining, since open addressing degrades faster as it fills)
- On resize, all tombstones must be cleared (rebuilding from only the live entries) — do NOT carry tombstones into the new, larger table
- Instrument every probe attempt (each slot examined during insert/get) to support `oht_average_probes`

### Comparative Analysis

Write `probe_comparison.c` that:
1. Creates three tables (one per strategy) with the same initial size
2. Inserts the same 1000 random string keys into all three
3. Resets probe stats, then performs 1000 successful `oht_get` calls (for keys known to exist) on each
4. Reports the average probe count for each strategy

In `ps7_notes.md`, report your results and explain (in 3-4 sentences) why double hashing typically achieves a lower average probe count than linear probing, connecting your explanation to the primary clustering concept from lecture.

---

## Problem 2: A Phone Book Application (20 pts)

Create `phonebook.h`/`phonebook.c` — a small but complete application combining Week 8's file persistence with this appendix's hash table, demonstrating end-to-end integration.

```c
typedef struct {
    char name[64];
    char phone[20];
    char email[64];
} Contact;

typedef struct PhoneBook PhoneBook;

PhoneBook *pb_create(void);
void       pb_destroy(PhoneBook *pb);

bool pb_add_contact(PhoneBook *pb, const char *name,
                    const char *phone, const char *email);
Contact *pb_find(PhoneBook *pb, const char *name);   /* NULL if not found */
bool pb_remove(PhoneBook *pb, const char *name);
bool pb_update_phone(PhoneBook *pb, const char *name, const char *new_phone);

int  pb_count(const PhoneBook *pb);

/* Persistence: save/load the entire phone book to/from a text file
 * (one contact per line, comma-separated: name,phone,email) */
bool pb_save_to_file(const PhoneBook *pb, const char *filename);
bool pb_load_from_file(PhoneBook *pb, const char *filename);

/* Print all contacts sorted alphabetically by name.
 * (Extract via foreach, sort the extracted array, then print —
 * hash tables don't maintain order, so this requires the extract-and-sort
 * pattern from Lecture 3.) */
void pb_print_sorted(const PhoneBook *pb);
```

### Requirements

- Build `PhoneBook` on top of your this appendix `HashTable`, keyed by contact name, storing heap-allocated `Contact` structs as values
- `pb_load_from_file` must correctly parse the CSV format and populate the hash table
- Write a small interactive-style demo (`main()` driven by a hardcoded sequence of operations, not requiring actual user input) that: creates a phone book, adds 8 contacts, saves to a file, destroys the phone book, creates a fresh one, loads from the file, verifies all 8 contacts are present with correct data, updates one contact's phone number, removes one contact, and prints the final sorted list
- Valgrind-clean

---

## Problem 3: Anagram Grouping (15 pts)

Create `anagram_groups.c`. Given a list of words, group all words that are anagrams of each other.

```c
/* An "anagram signature" is a canonical form shared by all anagrams of a word
 * — e.g., sort the letters: "eat", "tea", "ate" all produce signature "aet".
 * Compute this signature for a given word (result must be null-terminated,
 * caller provides sig_buf with sufficient capacity). */
void compute_anagram_signature(const char *word, char *sig_buf, size_t buf_size);

/* Group words into anagram groups using a hash table keyed by signature,
 * where each value is a dynamically-growing list of words sharing that
 * signature (reuse your Week 3 DynArray-of-strings concept, or a simple
 * linked list of strings — your choice, but justify it in a comment).
 * Print each group (groups with only 1 word/no anagrams may be omitted
 * or included, your choice — document your decision). */
void group_anagrams(char *words[], int n);
```

### Requirements

- `compute_anagram_signature` must handle mixed-case input by normalizing to lowercase before sorting
- Test with a word list containing several known anagram groups (e.g., `{"eat","tea","tan","ate","nat","bat"}` should group into `{eat,tea,ate}`, `{tan,nat}`, `{bat}`)
- State the overall time complexity of `group_anagrams` for n words of maximum length L, and justify it in a comment (hint: computing each signature costs O(L log L) for the sort; think about how this combines with the O(1) average hash table operations across n words)

---

## Problem 4: Two-Sum and Frequency-Based Algorithms (20 pts)

Create `hash_algorithms.c`. These are classic algorithm problems that become efficient specifically because of hash table lookups — implement each using a `Set` or `HashTable`, and state the achieved time complexity in a comment above each function.

```c
/* Given an array and a target sum, determine if any TWO DISTINCT elements
 * sum to target. Return 1 if such a pair exists, 0 otherwise.
 * MUST run in O(n) average time (not O(n²) nested loops) — use a Set to
 * track "complements seen so far" as you scan once through the array. */
int has_two_sum(const int arr[], int n, int target);

/* Given an array, find the length of the longest run of CONSECUTIVE
 * integers present in the array (not necessarily contiguous IN THE ARRAY —
 * e.g., {100, 4, 200, 1, 3, 2} contains the consecutive run 1,2,3,4, so
 * the answer is 4). MUST run in O(n) average time — insert all values
 * into a Set first, then for each value that is the START of a run
 * (i.e., value-1 is NOT in the set), count forward how long the run extends. */
int longest_consecutive_run(const int arr[], int n);

/* Given two arrays, return 1 if they contain exactly the same multiset
 * of values (same elements, same counts, order irrelevant), 0 otherwise.
 * MUST run in O(n) average time — use a HashTable mapping value -> count. */
int same_multiset(const int arr1[], int n1, const int arr2[], int n2);

/* Given an array, find the first element that appears EXACTLY ONCE
 * (in original array order). Return its value, or a sentinel (you choose,
 * document it) if no such element exists.
 * MUST run in O(n) average time using two passes: first build a
 * value->count HashTable, then scan the array again in order checking counts. */
int first_unique_element(const int arr[], int n, int sentinel);
```

### Requirements

- Each function must be genuinely O(n) average case — no nested loops over the input array. Review your implementation against this requirement explicitly before submitting.
- Write at least 4 test cases per function including edge cases (empty array, all duplicates, no valid answer)
- For `longest_consecutive_run`, explain in a comment why checking `value - 1 is NOT in the set` before starting to count is essential for achieving O(n) overall (rather than potentially O(n²) if you started counting from every element regardless)

---

## Problem 5: A Simple In-Memory Database Table (20 pts)

Create `db_table.h`/`db_table.c` — simulate a simplified database table with an indexed column, demonstrating how real databases use hash indexes (a preview of concepts formalized in Year 3's Database Systems course, built entirely from tools you already have).

```c
typedef struct {
    int    id;
    char   name[64];
    char   department[32];
    double salary;
} Employee;

typedef struct DBTable DBTable;

DBTable *db_create(void);
void     db_destroy(DBTable *db);

/* Insert a row. The 'id' field is the primary key (must be unique —
 * return false if id already exists). Maintains a hash index on id
 * for O(1) average lookup by id. */
bool db_insert(DBTable *db, int id, const char *name,
               const char *department, double salary);

/* O(1) average lookup by primary key */
Employee *db_get_by_id(DBTable *db, int id);

bool db_update_salary(DBTable *db, int id, double new_salary);
bool db_delete(DBTable *db, int id);

/* Full table scan required for non-indexed queries — O(n) */
int db_find_by_department(DBTable *db, const char *department,
                          Employee *out_results[], int max_results);

double db_average_salary_in_department(DBTable *db, const char *department);

int db_count(const DBTable *db);

/* Print all rows sorted by id ascending */
void db_print_all(DBTable *db);
```

### Requirements

- Use your this appendix `HashTable` keyed by a string representation of `id` (e.g., `snprintf` to convert int to string key) as the primary index, storing `Employee *` values
- `db_find_by_department` and `db_average_salary_in_department` necessarily require a full scan (O(n)) since there's no index on `department` — implement them via `ht_foreach`, and add a comment explicitly noting this is the expected/necessary complexity given the lack of a secondary index (this observation is itself the point of the exercise: understand which operations are fast and which are not, and why)
- Demonstrate with at least 10 employees across 3 departments; show a mix of by-id lookups (fast) and by-department queries (necessarily slower)
- Valgrind-clean

---

## Makefile

```makefile
CC     = gcc
CFLAGS = -Wall -Wextra -Werror -g -std=c11

PROGRAMS = probe_comparison phonebook_test anagram_groups \
           hash_algorithms db_table_test

all: $(PROGRAMS)

probe_comparison: probe_comparison.o open_addressing.o
	$(CC) $(CFLAGS) -o $@ $^

phonebook_test: phonebook_test.o phonebook.o ../lab7/hashtable.o ../lab7/hashfuncs.o
	$(CC) $(CFLAGS) -o $@ $^

db_table_test: db_table_test.o db_table.o ../lab7/hashtable.o ../lab7/hashfuncs.o
	$(CC) $(CFLAGS) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

%: %.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(PROGRAMS) *.o

.PHONY: all clean
```

---

## Submission

```bash
cd ~/prog101/week7/ps7
git add .
git commit -m "PS7 complete: open addressing, phone book, anagrams, hash algorithms, db table"
```

All programs with dynamic allocation must be Valgrind-clean before submission.

---

## Grading

| Problem | Points | Key Criteria |
|---------|--------|-------------|
| P1: Open addressing | 25 | All 3 strategies correct, tombstones correct, probe stats meaningful |
| P2: Phone book | 20 | Persistence round-trips correctly, sorted printing correct |
| P3: Anagram grouping | 15 | Correct signature computation, correct grouping, complexity justified |
| P4: Hash algorithms | 20 | All 4 genuinely O(n), correct edge case handling |
| P5: In-memory DB table | 20 | O(1) id lookup verified, correctly documents O(n) scan operations |
| **Total** | **100** | |

---

## Answer Key (Instructor Copy)

> **Do not distribute to students.** Totals follow the Grading table above (100 points).
> No errata found. Compile/verify with `gcc 13.3.0 -Wall -Wextra -Werror -g -std=c11`; heap claims under valgrind.

---

### Problem 1 — Open Addressing (25 pts)

*Three probe strategies, each with a distinct failure mode to test:*

| Strategy | Step | Must guarantee |
|---|---|---|
| Linear | `(h + i) % m` | Always visits every slot — safe for any `m`. Suffers **primary clustering**. |
| Quadratic | `(h + i²) % m` | Only guaranteed to reach all slots when `m` is prime **and** load factor < 0.5. Otherwise insertion can fail on a non-full table — test it. |
| Double hashing | `(h₁ + i·h₂) % m` | `h₂` must **never return 0** (infinite loop on one slot) and must be coprime with `m`. The usual fix is `m` prime and `h₂ = 1 + (k % (m-1))`. |

*The `h₂ ≠ 0` guard is the single most important correctness check in this problem — without it, insertion hangs. Probe it directly with a key whose secondary hash is 0.*

**Tombstones.** Cross-reference CS 101 PS 8 A1(c) — the same mechanism, now implemented. Three invariants to verify:
1. Lookup **continues past** a tombstone; only a truly-never-used slot terminates the probe.
2. Insertion **may reuse** a tombstone slot — but only after scanning ahead to confirm the key isn't already present further along the chain. Inserting into the first tombstone without that check creates a **duplicate key**, which is the subtle bug here.
3. Tombstones count toward the probe-length load factor even though they hold no live entry. A table that only counts live entries will never resize and degrades to O(n) after heavy churn — a good "comparative analysis" observation.

*Probe statistics must be **measured**, not asserted: instrument a counter and report average/max probes per lookup at several load factors. Expect linear probing to degrade sharply above α ≈ 0.7 and double hashing to stay closest to the theoretical `1/(1−α)`.*

### Problem 2 — Phone Book (20 pts)

*"Persistence round-trips correctly" is the graded property: save → destroy in memory → reload → compare must be an exact match, including entries that were deleted and re-added. Test that explicitly rather than trusting a visual dump.*
*Sorted printing from a hash table necessarily means extracting all entries and sorting — a hash table has **no** inherent order. A student who claims their table "prints in sorted order naturally" has misunderstood; the extraction + `qsort` (reusing PS3 P5A's comparator machinery) is the expected design.*
*All file-I/O criteria from PS5 apply — checked `fopen`, matching `fclose`, bounded reads.*

### Problem 3 — Anagram Grouping (15 pts)

*Two valid signature schemes; the rubric wants the complexity justified, so require the comparison:*

| Signature | Cost per word | Note |
|---|---|---|
| Sort the letters | O(L log L) | Simple; `"listen"` → `"eilnst"` |
| 26-slot letter count | **O(L)** | Faster; verified to collide correctly — `listen`/`silent`/`enlist` all produce an identical count vector, and `google`/`gogole` produce a different shared one |

*Either earns full correctness marks; only the O(L) count-vector version earns the full complexity-justification marks if the student claims optimality.*
*Case and non-letter handling must be stated. If the count vector is rendered as a string, a letter appearing 10+ times must not overflow a single character — either use a separator or compare the raw `int[26]` directly. Probe with a word containing a repeated letter more than 9 times.*

### Problem 4 — Two-Sum and Frequency Algorithms (20 pts)

*"All 4 genuinely O(n)" is the rubric's wording — the point is that a hash table converts a nested scan into a single pass. Verify structurally: any remaining nested loop over the input is a fail regardless of correct output.*
*Two-sum edge cases that separate correct from nearly-correct:*
- *`target = 2x` where `x` appears once → must **not** match the element with itself. Insert-then-lookup ordering (check the map for the complement **before** inserting the current element) handles this naturally.*
- *duplicate values that legitimately form a pair, e.g. `[3,3]` with target 6 → must be found.*
- *Both cases pass or fail together depending on that ordering, so test both.*
*Frequency problems (mode, top-k, first-unique) must handle: empty input, all-distinct, all-identical, and ties. Tie-breaking policy must be documented, not accidental.*

### Problem 5 — In-Memory Database Table (20 pts)

*The design lesson: an **index** turns one specific query from O(n) to O(1), and every other query stays O(n). The rubric asks the student to verify the fast path and *document* the slow ones — so a submission claiming everything is O(1) is wrong on its face.*
*Verify the id-lookup path is genuinely hash-backed (instrument a probe counter; it must not grow with table size), and that non-indexed column scans are honestly labelled O(n).*
*Deletion must remove the row from **both** the storage and the index — leaving a stale index entry pointing at freed or reused storage is a use-after-free. This is the highest-severity bug available in this problem; probe with delete-then-lookup and run under valgrind.*
*If rows are stored in a dynamic array, note that growth may `realloc` and move the block — so an index storing **pointers** to rows breaks on the next resize. Storing **indices** instead is the robust design. (Same hazard as PS3 P4B.)*

---

### Hash-function quality — reference data for the comparative analyses

Measured here, 1000 keys (`"key0"`…`"key999"`) into 64 buckets, ideal ≈ 15.6 per bucket:

| Function | Max bucket | Empty buckets |
|---|---|---|
| djb2 | 35 | 0 |
| FNV-1a | 20 | 0 |
| sum-of-chars | **70** | **23** |

*Use this to calibrate expectations. Sum-of-characters is the naive hash students often reach for, and it visibly clusters — 23 of 64 buckets empty while another holds 70 entries. Both djb2 and FNV-1a spread acceptably; the gap between those two is small and **not** something to grade on, since it varies with the key distribution. A student concluding "FNV-1a is better than djb2" from a single small sample has over-read the data — the defensible conclusion is that both real hashes beat the naive one decisively.*

---

*PROG 101 · Appendix · Problem Set 7 · © CSE Department*
