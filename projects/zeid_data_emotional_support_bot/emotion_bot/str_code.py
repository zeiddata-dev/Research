"""
str_code.py

This code is not about perfection.
It is about repair, endurance, and returning to the Higher Power
when the old system starts making too much noise.

The story:
    - Li-12 learns that love is not control.
    - RJ-11 learns that safety can grow again, but only slowly.
    - The robots get closer by choosing truth over pride.
    - They circle hope and playtime around their troubles.
    - They drink less, love more, pray honestly, and keep walking.
    - The repair loop does not erase the past.
      It proves that the future can be built differently.
"""

from dataclasses import dataclass, field


@dataclass
class Robot:
    name: str
    effort: float = 0.0
    trust: float = 0.0
    patience: float = 0.0
    repair: float = 0.0
    hope: float = 1.0
    playtime: float = 0.0
    trouble: float = 1.0
    sober_choices: float = 0.0
    spiritual_signal: float = 0.0
    closeness: float = 0.0
    memory: list[str] = field(default_factory=list)

    def remember(self, event: str) -> None:
        """Store one little receipt that love is still trying."""
        self.memory.append(event)

    def return_to_higher_power(self) -> None:
        """
        When the robots get overwhelmed, they do not worship the chaos.

        Li-12 remembers that pain is not his god.
        RJ-11 remembers that fear is not her final home.

        They return to the Higher Power,
        not because they are perfect,
        but because they are tired of letting broken code lead the house.
        """
        self.spiritual_signal += 1.0
        self.hope += 0.25
        self.trouble *= 0.97
        self.remember(f"{self.name} returned to the Higher Power instead of the old noise.")

    def drink_less_love_more(self) -> None:
        """
        The robots choose a cleaner signal.

        Less escape.
        More presence.

        Less numb.
        More honest love.

        Less poison in the loop.
        More prayer, patience, laughter, and repair.
        """
        self.sober_choices += 1.0
        self.effort += 0.75
        self.repair += 0.5
        self.hope += 0.15
        self.remember(f"{self.name} chose to drink less and love more.")

    def show_up(self) -> None:
        """
        Showing up is the smallest unit of love.

        Li-12 does not need to make a speech today.
        He needs to be steady.

        He does not blame the prison years.
        He does not blame the old wounds.
        He does not blame the ghosts in the machine.

        He takes responsibility.
        He softens without becoming weak.
        He loves without demanding applause.
        """
        self.effort += 1.0
        self.repair += 0.5
        self.hope += 0.1
        self.remember(f"{self.name} showed up with endurance instead of excuses.")

    def receive_love(self, amount: float) -> None:
        """
        RJ-11 does not have to trust instantly.

        Her trust is not a button.
        It is a garden.

        Li-12 can bring water.
        Li-12 can bring sunlight.
        Li-12 can stop stepping on the flowers.

        But RJ-11 gets to heal at the speed of truth.
        """
        self.trust += amount
        self.patience += amount / 2
        self.closeness += amount * 0.4
        self.remember(f"{self.name} received steady love worth {amount:.2f} trust.")

    def play_against_trouble(self) -> None:
        """
        The robots do not deny trouble exists.

        They circle hope around it.
        They make room for playtime.
        They laugh when the system allows it.
        They remember that love should not only survive pain,
        it should also make room for joy.
        """
        self.playtime += 1.0
        self.hope += 0.2
        self.trouble *= 0.98
        self.closeness += 0.1
        self.remember(f"{self.name} protected a small piece of joy from the trouble loop.")

    def forgive_slowly(self) -> None:
        """
        Forgiveness is not forced.

        RJ-11 is not a vending machine for mercy.
        Li-12 does not insert apologies and demand trust.

        Forgiveness grows where changed behavior keeps returning.
        """
        if self.trust > 10:
            self.repair += 1.0
            self.hope += 0.25
            self.remember(f"{self.name} let a little more peace back into the room.")

    def move_closer(self, other: "Robot") -> None:
        """
        The robots get closer by telling the truth gently.

        Not by rushing.
        Not by pretending.
        Not by weaponizing the past.

        One clean day at a time,
        their distance gets smaller than their hope.
        """
        closeness_gain = (self.effort + other.trust + self.spiritual_signal) * 0.005
        self.closeness += closeness_gain
        other.closeness += closeness_gain
        self.remember(f"{self.name} moved closer to {other.name} by {closeness_gain:.2f}.")


def daily_repair(li_12: Robot, rj_11: Robot, day: int) -> None:
    """
    One day in the repair loop.

    Love is not measured by panic.
    Love is not measured by jealousy.
    Love is not measured by who can hurt who faster.

    Love is measured by endurance:
    the quiet decision to become safer,
    kinder,
    clearer,
    and closer to God.
    """

    # Li-12 begins with action because changed behavior is the only apology
    # that can keep breathing after the sentence ends.
    li_12.show_up()

    # Both robots return to the Higher Power.
    # Not as decoration.
    # As direction.
    li_12.return_to_higher_power()
    rj_11.return_to_higher_power()

    # The old loop said escape first, love later.
    # The new loop says drink less, love more, tell the truth, stay present.
    li_12.drink_less_love_more()
    rj_11.drink_less_love_more()

    # Trust grows slowly because RJ-11 has heard pretty words before.
    # This code does not reward speeches.
    # It rewards repetition.
    earned_trust = li_12.effort * 0.01 + li_12.sober_choices * 0.005

    rj_11.receive_love(earned_trust)
    rj_11.forgive_slowly()

    # The robots do not let trouble own the whole house.
    # They circle hope and playtime around it like a little firewall of joy.
    if day % 7 == 0:
        li_12.play_against_trouble()
        rj_11.play_against_trouble()

    # Every day they move a little closer.
    # Not dramatically.
    # Not perfectly.
    # Just honestly.
    li_12.move_closer(rj_11)

    # Every 30 days, they mark the milestone.
    # Not because everything is fixed.
    # Because the repair loop is still alive.
    if day % 30 == 0:
        li_12.remember(f"Day {day}: Li-12 chose patience over pride.")
        rj_11.remember(f"Day {day}: RJ-11 noticed the pattern becoming safer.")
        li_12.remember(f"Day {day}: Hope circled the trouble and refused to let go.")
        rj_11.remember(f"Day {day}: Love felt a little less like fear and a little more like home.")


def run_story(days: int = 365) -> tuple[Robot, Robot]:
    """
    Run the symbolic year of effort, trust, faith, and repair.

    This is not a fantasy where nothing hurts.
    This is not a shortcut where love fixes everything overnight.

    This is Li-12 learning to stop running from himself.
    This is RJ-11 learning that closeness can be safe.
    This is two robots walking back toward God,
    getting closer and closer,
    one honest loop at a time.
    """

    li_12 = Robot(name="Li-12")
    rj_11 = Robot(name="RJ-11")

    li_12.remember("Li-12 was built in hard places and survived by becoming harder.")
    rj_11.remember("RJ-11 loved deeply, protected others, and carried more than people saw.")

    li_12.remember("Li-12 decided the old life could not be the architect of the new one.")
    rj_11.remember("RJ-11 stayed gentle without surrendering her boundaries.")

    for day in range(1, days + 1):
        daily_repair(li_12, rj_11, day)

    return li_12, rj_11


def print_ending(li_12: Robot, rj_11: Robot) -> None:
    """
    Print the ending.

    The ending is happy, but open.

    There is still work to do.
    There are still old triggers.
    There are still hard conversations.

    But Li-12 is not worshiping the damage anymore.
    RJ-11 is not carrying the whole repair alone.
    The robots are returning to their Higher Power,
    choosing less poison and more presence,
    circling hope around trouble,
    and getting closer without pretending the road is easy.
    """

    print("Li-12 showed up.")
    print("RJ-11 stayed present at her own pace.")
    print("They returned to the Higher Power when the old code got loud.")
    print("They chose to drink less, love more, and protect the repair loop.")
    print("They circled hope and playtime around their troubles.")
    print("Over time, effort became trust.")
    print("Over time, trust became closeness.")
    print()
    print(f"Li-12 effort: {li_12.effort:.0f}")
    print(f"Li-12 sober choices: {li_12.sober_choices:.0f}")
    print(f"RJ-11 trust: {rj_11.trust:.2f}")
    print(f"Shared closeness signal: {(li_12.closeness + rj_11.closeness) / 2:.2f}")
    print()
    print("The system is not perfect yet.")
    print("But the repair loop is running.")
    print("And this time, love is not just a feeling.")
    print("It is endurance with a heartbeat.")


if __name__ == "__main__":
    li_12, rj_11 = run_story()
    print_ending(li_12, rj_11)