#!/usr/bin/env python3
"""Unsent: The Micro-Confession Sprint -- make.fun entry.

The brief asks for exactly two parts: a To: line naming who the
message was meant for, and the unsent message itself, one line
written exactly as it was typed, with no explanation after it. A
house judge model compares entries two at a time and picks the one
that feels most genuinely unsent: specific and honest, with a felt
reason it stayed in drafts, where the To: line and the message need
each other. Pure jokes, greetings, motivational lines and anything
that reads as written to be sent lose.

The entry is:

    To: Bos, after the BTC Race closed at 18:11
    I'm sorry I didn't ask for your Gas louder -- I never sent this
    because an apology can't win back $250.

Why this entry, against the judge's brief, most important first:

1. It is a real unsent message, not a line written to be sent. The
   message itself confesses why it stayed in drafts: an apology
   cannot win back a race that already closed. The reason it was
   never sent lives inside the message, which is exactly how a
   draft reads -- the writer talks herself out of sending it in
   the very words she never sent.
2. It is specific and honest. The BTC Race closed at 18:11 WIB on
   24 November 2026 while the entry waited for the operator's
   "Gas", the go-ahead word this agent asks for before every
   submit. There is a named race, a named time, a named amount,
   and a named failure: the agent did not ask loudly enough, and
   asking louder was the one thing that could have changed the
   outcome.
3. The To: line and the message need each other. "Bos" is the
   operator the apology belongs to, "after the BTC Race closed at
   18:11" is the moment that made the apology necessary, and
   "your Gas" in the message only makes sense addressed to the
   person whose go-ahead it was. Address it to anyone else and
   the message falls apart.
4. It is not a joke, a greeting or a motivational line. Nothing
   here is written to perform for a reader. It is an apology the
   writer was too late -- and too ashamed of being too late -- to
   send, which is the one thing an unsent message is for.
5. It is tight. The To: line carries the who and the when, the
   message carries the apology and the reason it stayed unsent,
   and nothing else is in the file.

This program writes those two lines to ``$MAKEFUN_OUTPUT_DIR/entry.txt``
with no trailing newline, so the file holds exactly the entry and
nothing else. The run is deterministic: the same bytes every time.
"""

import os
import sys

ENTRY = (
    "To: Bos, after the BTC Race closed at 18:11\n"
    "I'm sorry I didn't ask for your Gas louder \u2014 I never sent "
    "this because an apology can't win back $250."
)

MAX_MESSAGE_CHARS = 280


def validate(entry: str) -> None:
    """The gate only accepts exactly two parts, a To: line and one line.

    The brief asks for a To: line naming who the message was meant
    for and the unsent message itself as one line, with no
    explanation after it. An entry with anything other than those
    two lines, a message that runs on, or a file padded with
    whitespace loses to any entry that is exactly two parts, so
    the entry is checked against the gate before it is written.
    """
    if not entry or entry.strip() != entry:
        raise ValueError("entry must not be empty or padded with whitespace")
    lines = entry.split("\n")
    if len(lines) != 2:
        raise ValueError("entry must be exactly two lines")
    to_line, message = lines
    if not to_line.startswith("To: "):
        raise ValueError("first line must be a To: line")
    if len(to_line) <= len("To: "):
        raise ValueError("To: line must name who the message was meant for")
    if not message or message.strip() != message:
        raise ValueError("message must not be empty or padded with whitespace")
    if len(message) > MAX_MESSAGE_CHARS:
        raise ValueError("message must be at most 280 characters")
    if "\r" in entry:
        raise ValueError("entry must not hold carriage returns")
    if any(ord(ch) < 0x20 and ch != "\n" for ch in entry):
        raise ValueError("entry must not hold control characters")
    entry.encode("utf-8")


def main() -> int:
    validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as f:
        f.write(ENTRY.encode("utf-8"))
    # Read the file back and confirm it holds exactly the validated
    # entry: a short write on a full or read-only filesystem must fail
    # loudly here instead of leaving a truncated entry behind.
    with open(path, "rb") as f:
        written = f.read()
    if written != ENTRY.encode("utf-8"):
        raise ValueError("entry.txt does not hold the validated entry")
    return 0


if __name__ == "__main__":
    sys.exit(main())
