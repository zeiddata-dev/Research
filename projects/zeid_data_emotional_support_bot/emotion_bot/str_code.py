"""
str_code.py

This code is not about perfection.
It is about repair.

The story:
    - Effort increases through repeated action.
    - Trust grows slowly, never instantly.
    - Apologies matter, but changed behavior matters more.
    - Love is not a print statement.
    - Love is the loop you keep running when nobody is clapping.
"""

from dataclasses import dataclass, field


@dataclass
class Robot:
    name: str
    effort: float = 0.0
    trust: float = 0.0
    patience: float = 0.0
    repair: float = 0.0
    memory: list[str] = field(default_factory=list)

    def remember(self, event: str) -> None:
        """Store a meaningful moment in the robot's memory."""
        self.memory.append(event)

    def show_up(self) -> None:
        """
        Showing up is the smallest unit of love.

        For Li-12, showing up means he stops disappearing into old survival code.
        He does not blame the system, the past, the prison, the pain, or the noise.
        He accepts responsibility and takes one clean step.
        """
        self.effort += 1
        self.repair += 0.5
        self.remember(f"{self.name} showed up instead of shutting down.")

    def receive_love(self, amount: float) -> None:
        """
        RJ-11 does not instantly trust the new version of Li-12.
        She watches the pattern.
        Love becomes believable when it survives ordinary days.
        """
        self.trust += amount
        self.patience += amount / 2
        self.remember(f"{self.name} received steady love worth {amount:.2f} trust.")

    def forgive_slowly(self) -> None:
        """
        Forgiveness here is not forced.

        RJ-11 is allowed to heal at human speed.
        Li-12 does not get to demand trust just because he finally understands the damage.
        He earns peace through consistency.
        """
        if self.trust > 10:
            self.repair += 1
            self.remember(f"{self.name} let a little more peace back in.")


def daily_repair(li_12: Robot, rj_11: Robot, day: int) -> None:
    """
    One day in the repair loop.

    Li-12's love is not measured by intensity.
    It is measured by consistency.

    RJ-11's trust is not weakness.
    It is courage after being hurt.
    """
    li_12.show_up()

    # Trust grows slowly because RJ-11 has learned that words can be beautiful
    # and still fail her. So the code does not reward speeches. It rewards repetition.
    earned_trust = li_12.effort * 0.01

    rj_11.receive_love(earned_trust)
    rj_11.forgive_slowly()

    # Every 30 days, the robots mark a milestone.
    # Not because everything is fixed.
    # Because they are still choosing the repair.
    if day % 30 == 0:
        li_12.remember(f"Day {day}: Li-12 chose patience over pride.")
        rj_11.remember(f"Day {day}: RJ-11 noticed the pattern becoming safer.")


def run_story(days: int = 365) -> tuple[Robot, Robot]:
    """
    Run the symbolic year of effort and trust.

    This is the heart of the story:
    not a perfect man becoming flawless,
    not a wounded woman pretending nothing happened,
    but two souls learning that love must become safe before it can become soft again.
    """
    li_12 = Robot(name="Li-12")
    rj_11 = Robot(name="RJ-11")

    # Li-12 begins with effort.
    # RJ-11 begins with guarded trust.
    # Neither one begins with magic.
    li_12.remember("Li-12 was built in hard places and survived by becoming harder.")
    rj_11.remember("RJ-11 loved deeply, protected others, and carried more than people saw.")

    for day in range(1, days + 1):
        daily_repair(li_12, rj_11, day)

    return li_12, rj_11


def print_ending(li_12: Robot, rj_11: Robot) -> None:
    """
    Print the ending.

    The ending is happy, but open.
    There is more work to do.
    That is not a failure.
    That is what real love looks like after damage:
    less fantasy, more faithfulness.
    """
    print("Li-12 showed up.")
    print("RJ-11 stayed present at her own pace.")
    print("Over time, effort became trust.")
    print(f"Li-12 effort: {li_12.effort:.0f}")
    print(f"RJ-11 trust: {rj_11.trust:.2f}")
    print("The system is not perfect yet.")
    print("But the repair loop is running.")


if __name__ == "__main__":
    li_12, rj_11 = run_story()
    print_ending(li_12, rj_11)
