"""Compatibility wrapper for the symbolic repair loop story.

This file keeps the old import path alive.
That matters because repair is not only about writing new promises.
It is also about not breaking the paths people already rely on.

The real story lives in ``str_code``.
This module simply holds the door open and says:
come in, the robots are still trying, and yes, the cat still looks like Doctor Robotnik.
"""

from __future__ import annotations

# Re-export the story objects from str_code.
# A wrapper is humble infrastructure: not flashy, but loyal.
# RJ-11 would respect that. Li-12 is learning to.
from .str_code import Robot, daily_repair, print_ending, run_story

# Public names kept stable for callers.
# Stability is its own love language when people depend on your code.
__all__ = ["Robot", "daily_repair", "print_ending", "run_story"]
