#!/usr/bin/env python3
"""
turing_machine_simulator.py
CS 101 — Week 0, Lab 0 Bonus Exercise

A simple Turing Machine simulator in Python.

A Turing Machine consists of:
  - An infinite tape of cells, each holding a symbol
  - A read/write head that scans the current cell
  - A finite set of states
  - A transition function: (state, symbol) → (new_state, write_symbol, direction)

This simulator lets you define a Turing Machine and watch it run.

HOW TO USE:
  1. Read through the code and understand the structure
  2. Run the provided examples
  3. Try the exercises at the bottom

This is the theoretical foundation of everything in CS 101.
"""

class TuringMachine:
    """
    A simple Turing Machine simulator.
    
    Tape: Represented as a dictionary {position: symbol}
          Positions not in the dict are treated as BLANK ('_')
    Head: An integer position (starts at 0)
    State: The current machine state
    """
    
    BLANK = '_'
    LEFT = 'L'
    RIGHT = 'R'
    HALT = 'HALT'
    
    def __init__(self, transitions, initial_state, accept_states, reject_states=None):
        """
        Initialize the Turing Machine.
        
        Args:
            transitions: dict mapping (state, symbol) → (new_state, write_symbol, direction)
            initial_state: The starting state
            accept_states: Set of accepting states
            reject_states: Set of rejecting states (optional)
        """
        self.transitions = transitions
        self.initial_state = initial_state
        self.accept_states = set(accept_states)
        self.reject_states = set(reject_states) if reject_states else set()
    
    def run(self, input_string, max_steps=1000, verbose=True):
        """
        Run the Turing Machine on an input string.
        
        Args:
            input_string: The input to process (string)
            max_steps: Maximum number of steps before declaring it might not halt
            verbose: If True, print each step
        
        Returns:
            'accept', 'reject', or 'timeout'
        """
        # Initialize tape
        tape = {}
        for i, symbol in enumerate(input_string):
            tape[i] = symbol
        
        head = 0
        state = self.initial_state
        steps = 0
        
        if verbose:
            print(f"Input: '{input_string}'")
            print(f"Starting in state: {state}")
            print("-" * 50)
        
        while steps < max_steps:
            # Read current symbol
            current_symbol = tape.get(head, self.BLANK)
            
            if verbose:
                self._print_configuration(tape, head, state, steps)
            
            # Check for halting states
            if state in self.accept_states:
                if verbose:
                    print(f"\n✓ ACCEPTED after {steps} steps")
                return 'accept'
            
            if state in self.reject_states:
                if verbose:
                    print(f"\n✗ REJECTED after {steps} steps")
                return 'reject'
            
            if state == self.HALT:
                if verbose:
                    print(f"\n■ HALTED after {steps} steps")
                return 'accept'  # Treat HALT as accept for these examples
            
            # Look up transition
            key = (state, current_symbol)
            if key not in self.transitions:
                if verbose:
                    print(f"\n✗ NO TRANSITION for ({state}, '{current_symbol}') — REJECTING")
                return 'reject'
            
            # Apply transition
            new_state, write_symbol, direction = self.transitions[key]
            tape[head] = write_symbol
            
            if direction == self.RIGHT:
                head += 1
            elif direction == self.LEFT:
                head -= 1
            
            state = new_state
            steps += 1
        
        if verbose:
            print(f"\n⏱ TIMEOUT: Did not halt after {max_steps} steps")
            print("   This might mean the machine loops forever on this input.")
        return 'timeout'
    
    def _print_configuration(self, tape, head, state, step):
        """Print the current tape configuration."""
        if not tape:
            tape_str = "_"
        else:
            min_pos = min(min(tape.keys()), head) - 1
            max_pos = max(max(tape.keys()), head) + 1
            
            tape_chars = []
            head_markers = []
            
            for pos in range(min_pos, max_pos + 1):
                symbol = tape.get(pos, '_')
                tape_chars.append(f" {symbol} ")
                if pos == head:
                    head_markers.append(" ^ ")
                else:
                    head_markers.append("   ")
            
            tape_str = "|".join(tape_chars)
            head_str = " ".join(head_markers)
            
        print(f"Step {step:3d} | State: {state:10s} | Tape: [{tape_str}]")


# =============================================================================
# EXAMPLE 1: Accept strings with an even number of 1s over alphabet {0, 1}
# =============================================================================

def example_even_ones():
    """
    This TM accepts binary strings where the number of 1s is even (including 0).
    
    States:
        q0: Even number of 1s seen so far (initial and accepting)
        q1: Odd number of 1s seen so far
    
    Strategy:
        - Start in q0 (0 ones seen = even)
        - On reading '1': toggle between q0 and q1
        - On reading '0': stay in current state
        - On reading blank (_): halt (accept if in q0, reject if in q1)
    """
    transitions = {
        # (state, symbol): (new_state, write, direction)
        ('q0', '0'): ('q0', '0', 'R'),   # Even ones, see 0 → still even
        ('q0', '1'): ('q1', '1', 'R'),   # Even ones, see 1 → now odd
        ('q0', '_'): ('ACCEPT', '_', 'R'), # Even ones, end of input → ACCEPT
        
        ('q1', '0'): ('q1', '0', 'R'),   # Odd ones, see 0 → still odd
        ('q1', '1'): ('q0', '1', 'R'),   # Odd ones, see 1 → now even
        ('q1', '_'): ('REJECT', '_', 'R'), # Odd ones, end of input → REJECT
    }
    
    tm = TuringMachine(
        transitions=transitions,
        initial_state='q0',
        accept_states=['ACCEPT'],
        reject_states=['REJECT']
    )
    
    print("=" * 60)
    print("EXAMPLE 1: Even number of 1s")
    print("=" * 60)
    
    test_cases = [
        ("110",   True,  "Two 1s (even) → accept"),
        ("1",     False, "One 1 (odd) → reject"),
        ("0000",  True,  "Zero 1s (even) → accept"),
        ("11011", True,  "Four 1s (even) → accept"),
        ("1010",  True,  "Two 1s (even) → accept"),
        ("101",   False, "Three 1s (odd) → reject"),
    ]
    
    print("\nRunning tests (verbose=False for brevity):")
    for input_str, should_accept, description in test_cases:
        result = tm.run(input_str, verbose=False)
        actual_accept = (result == 'accept')
        status = "✓" if actual_accept == should_accept else "✗ WRONG"
        print(f"  {status} Input '{input_str}': {description}")
    
    print("\n--- Verbose trace for '110' ---")
    tm.run("110", verbose=True)


# =============================================================================
# EXAMPLE 2: Unary increment (add 1 to a unary number)
# =============================================================================

def example_unary_increment():
    """
    Unary representation: n is represented as n consecutive 1s.
    Example: 3 = "111", 5 = "11111"
    
    This TM adds 1 to a unary number by appending a '1' at the end.
    
    Strategy:
        - Move right until we find a blank
        - Write a '1' there
        - Halt
    """
    transitions = {
        ('q0', '1'): ('q0', '1', 'R'),   # Keep moving right over 1s
        ('q0', '_'): ('HALT', '1', 'R'), # Found end: write 1 and halt
    }
    
    tm = TuringMachine(
        transitions=transitions,
        initial_state='q0',
        accept_states=['HALT']
    )
    
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Unary increment (add 1 to a unary number)")
    print("=" * 60)
    
    print("\n--- Incrementing 3 (\"111\") ---")
    tm.run("111", verbose=True)


# =============================================================================
# EXERCISES FOR STUDENTS
# =============================================================================

def exercise_template():
    """
    EXERCISE: Build a TM that accepts palindromes over {a, b}.
    
    A palindrome reads the same forwards and backwards.
    Examples: "aba", "abba", "a", "" (empty), "aabaa"
    Non-examples: "ab", "abb", "abab"
    
    This is harder than the examples above. Think about the strategy:
    
    Strategy hint:
        1. Read the first character. Remember it in the state.
        2. Move all the way to the end (past all remaining characters).
        3. Read the last character. Does it match the first?
        4. If yes: mark both as 'done', move inward, repeat.
        5. If no: reject.
        6. If we reach the middle (or empty tape): accept.
    
    States you might need:
        - 'start': initial state — read first char
        - 'seeking_end_a': read 'a' first, moving to end to check
        - 'seeking_end_b': read 'b' first, moving to end to check
        - 'found_a': at right end, found matching 'a', moving back
        - 'found_b': at right end, found matching 'b', moving back
        - 'return': moving left back to first unprocessed character
        - 'accept': accept state
        - 'reject': reject state
    
    Fill in the transitions dict below and test your machine.
    """
    
    transitions = {
        # TODO: Fill in transitions
        # Format: ('state', 'symbol'): ('new_state', 'write', 'direction')
        #
        # You will need transitions for:
        #   - Reading the first character and marking it
        #   - Scanning to the end
        #   - Checking the last character
        #   - Returning to the left
        #   - Handling the base cases (empty or single character)
    }
    
    tm = TuringMachine(
        transitions=transitions,
        initial_state='start',
        accept_states=['accept'],
        reject_states=['reject']
    )
    
    test_cases = [
        ("",     True,  "Empty string is a palindrome"),
        ("a",    True,  "Single character is a palindrome"),
        ("aa",   True,  "aa is a palindrome"),
        ("ab",   False, "ab is not a palindrome"),
        ("aba",  True,  "aba is a palindrome"),
        ("abba", True,  "abba is a palindrome"),
        ("abab", False, "abab is not a palindrome"),
        ("aabaa",True,  "aabaa is a palindrome"),
    ]
    
    print("\n" + "=" * 60)
    print("EXERCISE: Palindrome Checker")
    print("=" * 60)
    
    if not transitions:
        print("⚠ No transitions defined yet. Build the TM!")
        return
    
    all_correct = True
    for input_str, should_accept, description in test_cases:
        result = tm.run(input_str, verbose=False)
        actual_accept = (result == 'accept')
        status = "✓" if actual_accept == should_accept else "✗ WRONG"
        if actual_accept != should_accept:
            all_correct = False
        print(f"  {status} Input '{input_str}': {description}")
    
    if all_correct:
        print("\n🎉 All test cases passed! Your TM is correct.")
    else:
        print("\n⚠ Some test cases failed. Keep debugging!")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("CS 101 — Week 0: Turing Machine Simulator")
    print("This is the theoretical foundation of all computation.\n")
    
    example_even_ones()
    example_unary_increment()
    
    print("\n" + "=" * 60)
    print("YOUR TURN: Complete the palindrome exercise above")
    print("=" * 60)
    exercise_template()
    
    print("\n" + "=" * 60)
    print("REFLECTION QUESTIONS:")
    print("=" * 60)
    print("""
1. The TuringMachine class above is itself a Python program.
   It *simulates* a Turing Machine. But Python itself runs on
   a real computer, which IS (in theory) a Turing Machine.
   So we have: Turing Machine simulating Turing Machine.
   What does this tell you about the universality of computation?

2. The 'timeout' case in the run() method represents what 
   theoretical concept? Why can't we always know in advance
   whether a TM will halt?

3. How many states does the even-ones TM have? How many
   different inputs does it accept? What does this tell you
   about the relationship between finite automata and infinite languages?
""")
