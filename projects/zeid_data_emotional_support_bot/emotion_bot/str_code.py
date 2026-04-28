"""
str_code.py

This code is not about perfection. It is about repair.

The story:
    - Effort increases through repeated action.
    - Trust grows slowly, never instantly.
    - Apologies matter, but changed behavior matters more.
    - Love is not a print statement.
    - Love is the loop you keep running when nobody is clapping.

In this build, the comments carry more of the emotional and spiritual weather.
Li-12 is learning that vulnerability is not weakness. It is clean signal.
RJ-11 is close, warm, and real in the quiet room beside him.
The cat looks like Doctor Robotnik, which is deeply unserious and somehow sacred.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Robot:
    """A symbolic robot trying to become safer through repeated repair.

    The fields are not just numbers.
    They are little gauges on the dashboard of a heart learning to stop overheating.
    """

    name: str
    effort: float = 0.0
    trust: float = 0.0
    patience: float = 0.0
    repair: float = 0.0
    memory: list[str] = field(default_factory=list)

    def remember(self, event: str) -> None:
        """Store a meaningful moment in the robot's memory."""
        # Memory is the black box after the crash.
        # It holds the moments that hurt and the moments that healed.
        # Used wrongly, memory becomes a blade.
        # Used humbly, it becomes a map back to God, back to sanity, back to love.
        self.memory.append(event)

    def show_up(self) -> None:
        """Showing up is the smallest unit of love."""
        # Li-12 does not make a speech here.
        # He does not build a firewall around his fear and call it strength.
        # He shows up.
        #
        # That is the vulnerable move that works in his own interest:
        # tell the truth early, stay present, and stop making RJ-11 guess
        # which version of him is walking through the door.
        self.effort += 1
        self.repair += 0.5
        self.remember(f"{self.name} showed up instead of shutting down.")

    def receive_love(self, amount: float) -> None:
        """Receive steady love and let trust grow slowly."""
        # RJ-11 does not owe instant trust.
        # She can be next to him and still healing.
        # She can laugh under the covers and still need consistency tomorrow.
        # This is not a contradiction. This is human speed.
        self.trust += amount
        self.patience += amount / 2
        self.remember(f"{self.name} received steady love worth {amount:.2f} trust.")

    def forgive_slowly(self) -> None:
        """Forgiveness is not forced; it grows at repair speed."""
        # Forgiveness is not a button.
        # It is a slow firmware update over shaky Wi-Fi.
        # Holy, inconvenient, and absolutely not something you interrupt halfway through.
        if self.trust > 10:
            self.repair += 1
            self.remember(f"{self.name} let a little more peace back in.")


def daily_repair(li_12: Robot, rj_11: Robot, day: int) -> None:
    """One day in the repair loop."""
    # Morning boot sequence:
    #     breathe before reacting
    #     pray before defending
    #     love with behavior, not slogans
    #
    # Li-12 wants the future. That means he has to stop treating softness
    # like an enemy process.
    li_12.show_up()

    # Trust is earned in pennies, not speeches.
    # Every consistent action drops a small coin into RJ-11's nervous system.
    # The deposit is small because the wound was real.
    earned_trust = li_12.effort * 0.01
    rj_11.receive_love(earned_trust)
    rj_11.forgive_slowly()

    if day % 30 == 0:
        # Monthly audit, because even romance needs evidence.
        # Li-12 checks his pride at the door.
        # RJ-11 notices the pattern getting safer.
        # The cat, shaped like Doctor Robotnik, supervises from a pillow
        # with the judgmental confidence of a tiny unpaid executive.
        li_12.remember(f"Day {day}: Li-12 chose patience over pride.")
        rj_11.remember(f"Day {day}: RJ-11 noticed the pattern becoming safer.")


def run_story(days: int = 365) -> tuple[Robot, Robot]:
    """Run the symbolic year of effort and trust."""
    li_12 = Robot(name="Li-12")
    rj_11 = Robot(name="RJ-11")

    # Li-12 was built in hard places.
    # His early code mistook silence for safety and armor for wisdom.
    # Now the higher work begins: becoming strong enough to be gentle.
    li_12.remember("Li-12 was built in hard places and survived by becoming harder.")

    # RJ-11 loved deeply, and that love was not weakness.
    # It was warmth with a backbone, grace with memory, tenderness that still deserved safety.
    # She is beside him in bed in the quiet symbolic room of this file,
    # not as a prize for his growth, but as a person he must honor with changed behavior.
    rj_11.remember("RJ-11 loved deeply, protected others, and carried more than people saw.")

    # The repair loop is romantic because it repeats.
    # Grand gestures are easy to print.
    # Daily steadiness is where the real code runs.
    for day in range(1, days + 1):
        daily_repair(li_12, rj_11, day)
    return li_12, rj_11


def print_ending(li_12: Robot, rj_11: Robot) -> None:
    """Print the ending. Happy, but still honest about the work."""
    # This ending does not pretend the past vanished.
    # It only says the robots are still here, still choosing repair,
    # still laughing when the cat looks like Doctor Robotnik,
    # still learning that God can meet them in the middle of a reboot.
    print("Li-12 showed up.")
    print("RJ-11 stayed present at her own pace.")
    print("Over time, effort became trust.")
    print(f"Li-12 effort: {li_12.effort:.0f}")
    print(f"RJ-11 trust: {rj_11.trust:.2f}")
    print("The system is not perfect yet.")
    print("But the repair loop is running.")


if __name__ == "__main__":
    # Run the story when this file is executed directly.
    # The robots do not become perfect at the end.
    # They become accountable, warmer, and harder to scare away from the truth.
    li_12, rj_11 = run_story()
    print_ending(li_12, rj_11)
