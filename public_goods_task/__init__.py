import random
import string
import time
from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
from otree.api import Page, WaitPage
from decimal import Decimal


author = "Merve"
doc = """Second part of the study"""


# CONSTANTS AND DEFINITIONS


class C(BaseConstants):
    NAME_IN_URL = "public_goods_task"
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 10
    ENDOWMENT = c(2)
    MULTIPLIER = 1.5
    Likert_1_to_5 = [
        [1, "1 - Strongly disagree"],
        [2, "2 - Disagree"],
        [3, "3 - Neither agree nor disagree"],
        [4, "4 - Agree"],
        [5, "5 - Strongly agree"],
    ]


class Subsession(BaseSubsession):
    def creating_session(self):
        for player in self.get_players():
            player.participant.vars.setdefault("kicked", False)
            player.participant.vars.setdefault("leftover", False)
            player.participant.vars.setdefault("kicked_page_shown", False)
            player.participant.vars.setdefault("leftover_page_shown", False)

            player.participant.vars["grouped"] = False
            player.participant.vars["end_game"] = False
            player.participant.vars["wait_page_arrival"] = None
            player.completion_code = "DS" + "".join(random.choices(string.digits, k=4))
            player.total_task_earnings = 0  # set everyone to zero at the very start
            player.bonus = 0  # set everyone to zero at the very start
            player.final_payoff_total = 0  # set everyone to zero at the very start


class Group(BaseGroup):
    total_contribution = models.CurrencyField(initial=0)
    individual_share = models.CurrencyField(initial=0)


class Player(BasePlayer):
    completion_code = models.StringField()
    contribution = models.CurrencyField(
        min=0,
        # max=C.ENDOWMENT,
        doc="""The amount contributed by the player""",
        initial=0,
    )
    budget = models.CurrencyField(initial=C.ENDOWMENT)
    total_task_earnings = models.CurrencyField()
    bonus = models.CurrencyField()
    final_payoff_total = models.FloatField()
    # --- T1 TRUST MEASURES ---
    t1_con_trust_pred_1 = models.IntegerField(
        label="The other participants will make consistent investments throughout rounds.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    )
    t1_con_trust_pred_2 = models.IntegerField(
        label="The other participants will make investments that clearly show how they want the shared charging infrastructure to develop.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    )
    t1_con_trust_pred_3 = models.IntegerField(
        label="The other participants will use an investment strategy that I can easily predict throughout rounds.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    )
    t1_con_trust_pred_4 = models.IntegerField(
        label="The other participants will each follow a stable approach when making investment decisions throughout rounds.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    )
    t1_con_trust_benev_1 = models.IntegerField(
        label="The other participants will be willing to invest for the benefit of the group.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    )
    t1_con_trust_benev_2 = models.IntegerField(
        label="The other participants will care about how their investments affect the earnings of others.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    )
    t1_con_trust_benev_3 = models.IntegerField(
        label="The other participants will be willing to invest if I invest as well.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    )
    t1_con_trust_benev_4 = models.IntegerField(
        label="The other participants will look out for my interests when making investment decisions.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    )


# FUNCTIONS


def player_is_kicked(
    player: Player,
):  # A helper function, making it easier to check whether a player is kicked.
    return player.participant.vars.get(
        "kicked", False
    )  # Returns whether a player is marked as "kicked."


# Instead of writing player.participant.vars.get("kicked", False) everywhere, we just call player_is_kicked(player).


def player_is_leftover(player: Player):  #  A helper function for "leftover" players.
    return player.participant.vars.get("leftover", False)


def contribution_max(player: Player):

    if player.round_number == 1:
        return player.budget
    else:
        return player.in_round(player.round_number - 1).budget


def contribution_error_message(player, value):

    current_budget = 0
    if player.round_number == 1:
        current_budget = player.budget
    else:
        current_budget = player.in_round(player.round_number - 1).budget

    # Raise an error if value is outside the range
    if value > current_budget:
        return f"Cannot offer more than your remaining budget: {current_budget}"
    else:
        pass


def vars_for_template(player: Player):
    session = player.session
    subsession = player.subsession
    timeout_time = session.config["timeout_time"]
    timeout_time_minutes = timeout_time / 60
    timers = session.config.get("timers", False)
    incentives = session.config["incentives"]
    base_fee = session.config["base_fee"]
    payoff_conversion = session.config["payoff_conversion"]

    return {
        "timeout_time": timeout_time,
        "timeout_time_minutes": timeout_time_minutes,
        "timers": timers,
        "incentives": incentives,
        "base_fee": base_fee,
        "payoff_conversion": payoff_conversion,
    }


def set_payoffs(group: Group):
    group.total_contribution = sum([p.contribution for p in group.get_players()])
    group.individual_share = (
        group.total_contribution * C.MULTIPLIER
    ) / C.PLAYERS_PER_GROUP

    # Mode 1: Fresh endowment of 2 euros each round
    for p in group.get_players():
        p.payoff = group.individual_share + (C.ENDOWMENT - p.contribution)
        p.budget = C.ENDOWMENT  # Each round starts fresh with 2 euros

    # # Mode 2: Carryover budget from previous rounds
    # for p in group.get_players():
    #     if group.round_number == 1:
    #         previous_budget = C.ENDOWMENT
    #     else:
    #         previous_budget = p.in_round(group.round_number - 1).budget
    #     p.payoff = group.individual_share + (previous_budget - p.contribution)
    #     p.budget = previous_budget - p.contribution + group.individual_share


def leftover_check(player: Player):
    participant = player.participant
    group = player.group
    other_players = player.get_others_in_group()

    for p in other_players:
        # Use `p.participant.vars.get("kicked", False)` instead of `p.participant.kicked`
        if p.participant.vars.get("kicked", False):
            participant.vars["leftover"] = True
            break  # Stop checking once confirmed

        # Also check if a player left before finishing the game
        if p.round_number < C.NUM_ROUNDS and p.participant._current_page_name in [
            "Funnel",
            "Debriefing",
            "Kicked",
        ]:
            participant.vars["leftover"] = True
            break  # Stop checking once confirmed


def waiting_too_long(player):
    # Get wait page arrival time
    arrival_time = player.participant.vars.get("wait_page_arrival")
    if arrival_time is None:
        return False
    return (time.time() - arrival_time) > 5 * 60


def group_by_arrival_time_method(subsession, waiting_players):

    # 1. Initialize arrival time for newly arrived players
    current_time = time.time()
    for player in waiting_players:
        if (
            "wait_page_arrival" not in player.participant.vars
            or player.participant.vars["wait_page_arrival"] is None
        ):
            # Set the clock exactly when they first appear in 'waiting_players'
            player.participant.vars["wait_page_arrival"] = current_time

    # 2. Check for timeouts
    for player in waiting_players:
        arrival_time = player.participant.vars["wait_page_arrival"]
        if (current_time - arrival_time) > 300:
            player.participant.vars["leftover"] = True
            # Return them solo to force them forward
            return [player]

    # 3. If no timeouts, try to form a full group
    if len(waiting_players) >= 4:
        return waiting_players[:4]


# PAGES


class Waitforgroup(WaitPage):
    title_text = "Pairing with participants"

    body_text = """
        Please wait while we match you with other participants. 
        <br><br>
        If a full group cannot be formed within <strong>5 minutes</strong>, 
        the session will end. In that case, <strong>you will still receive your base participation fee</strong> 
        for your time. You will be automatically redirected to the debriefing page to complete your submission.
        <br><br>
        <strong>Only participants who remain active on this page for the full 5-minute duration 
        will be eligible for the base participation fee.</strong>
        <br><br>
        <i>This page will refresh automatically, but you may also 
        <strong>reload the page manually</strong> after 5 minutes to 
        check your status.</i>
        
        <script>
            setTimeout(function() {
                window.location.reload();
            }, 302000); // 5 minutes + 2 seconds buffer
        </script>
    """

    group_by_arrival_time = True  # Enable automatic grouping

    def is_displayed(player: Player):
        return (
            not player_is_kicked(player)
            and not player_is_leftover(player)
            and player.round_number == 1
            and not player.participant.vars.get("end_game", False)
        )


class GroupingConfirmation(Page):
    def vars_for_template(player: Player):
        return {
            "num_other_participants": player.session.config.get("group_size", 4) - 1
        }

    def is_displayed(player: Player):
        return (
            not player_is_kicked(player)
            and not player_is_leftover(player)
            and player.round_number == 1
            and not player.participant.vars.get("end_game", False)
        )

    def get_timeout_seconds(player: Player):
        return player.session.config["timeout_time"]

    def before_next_page(player: Player, timeout_happened):
        participant = player.participant

        if timeout_happened:
            participant.vars["kicked"] = True

        if not player_is_leftover(player):
            participant.vars["grouped"] = True

        leftover_check(player)


class T1Trust(Page):
    form_model = "player"
    form_fields = [
        "t1_con_trust_pred_1",
        "t1_con_trust_pred_2",
        "t1_con_trust_pred_3",
        "t1_con_trust_pred_4",
        "t1_con_trust_benev_1",
        "t1_con_trust_benev_2",
        "t1_con_trust_benev_3",
        "t1_con_trust_benev_4",
    ]

    def is_displayed(player: Player):
        # Only show in the very first round, right after grouping, assuming they aren't kicked/leftovers
        return (
            player.round_number == 1
            and not player_is_kicked(player)
            and not player_is_leftover(player)
        )

    def get_timeout_seconds(player: Player):
        return player.session.config.get("timeout_time")

    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if timeout_happened:
            participant.vars["kicked"] = True
        leftover_check(player)


class Contribute(Page):
    form_model = "player"
    form_fields = ["contribution"]

    def is_displayed(player: Player):
        return not player_is_kicked(player) and not player_is_leftover(player)

    def vars_for_template(player: Player):
        # Retrieve last round's budget for rounds after the first round
        if player.round_number > 1:
            player.budget = player.in_round(player.round_number - 1).budget

        return {
            "num_rounds": C.NUM_ROUNDS,
            "num_other_participants": (C.PLAYERS_PER_GROUP) - 1,
            "multiplier": C.MULTIPLIER,
            "endowment": float(C.ENDOWMENT),
            "player_budget": player.budget,
        }

    def get_timeout_seconds(player: Player):
        return player.session.config.get("timeout_time")

    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        if timeout_happened:
            participant.vars["kicked"] = True
        leftover_check(player)


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = "set_payoffs"

    def is_displayed(player: Player):
        return not player_is_kicked(player) and not player_is_leftover(player)

    def before_next_page(player: Player, timeout_happened):
        participant = player.participant

        if timeout_happened:
            participant.vars["kicked"] = True

        leftover_check(player)


class Results(Page):
    def is_displayed(player: Player):
        return not player_is_kicked(player) and not player_is_leftover(player)

    def vars_for_template(player: Player):
        players = player.group.get_players()

        contributions = []
        for p in players:
            label = f"Player {p.id_in_group}"
            is_you = p == player  # Check if this is the current player

            money_kept = C.ENDOWMENT - p.contribution

            contributions.append(
                {
                    "index": p.id_in_group,  # Needed for assigning positions in HTML
                    "label": label,
                    "contribution": p.contribution,
                    "money_kept": money_kept,
                    "payoff": p.payoff,
                    "is_you": is_you,  # Boolean to check if it's the participant
                }
            )

        return {
            "contributions": contributions,
            "prev_budget": (
                player.in_round(player.round_number - 1).budget
                if player.round_number > 1
                else C.ENDOWMENT
            ),
            "incentives": player.session.config.get("incentives", False),
        }

    def get_timeout_seconds(player: Player):
        # If it's the last round, disable the timer (return None)
        if player.round_number == C.NUM_ROUNDS:
            return None
        return player.session.config.get("timeout_time")

    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        # Only process timeout if it's NOT the last round
        if timeout_happened and player.round_number < C.NUM_ROUNDS:
            participant.vars["kicked"] = True
            leftover_check(player)


class Payoff(Page):
    def is_displayed(player: Player):
        return (
            not player_is_kicked(player)
            and not player_is_leftover(player)
            and player.round_number == C.NUM_ROUNDS
        )

    def vars_for_template(player: Player):
        players = player.group.get_players()

        # Create a structured list of final payoffs, not needed for now
        # final_results = []
        # for p in players:
        #     label = f"Player {p.id_in_group}"
        #     if p == player:
        #         label += " (This is you)"
        #     final_results.append({
        #         "label": label,
        #         "payoff": round(p.payoff, 2)
        #     })

        # Retrieve and round values
        incentives = player.session.config["incentives"]
        base_fee = round(Decimal(player.session.config["base_fee"]), 2)
        payoff_conversion = Decimal(str(player.session.config["payoff_conversion"]))
        timers = player.session.config.get("timers", False)

        all_rounds = player.in_all_rounds()
        total_earnings = round(sum(p.payoff for p in all_rounds), 2)
        # average_earnings = round(total_earnings / C.NUM_ROUNDS, 2)
        bonus = (
            round(total_earnings * payoff_conversion, 2)
            if incentives
            else Decimal("0.00")
        )
        final_payoff_total = round(base_fee + bonus, 2)

        player.total_task_earnings = total_earnings  # so they show up in data
        player.bonus = bonus  # so they show up in data
        player.final_payoff_total = float(final_payoff_total)  # so they show up in data

        return {
            "incentives": incentives,
            "base_fee": base_fee,
            "payoff_conversion": payoff_conversion,
            "total_earnings": total_earnings,
            # "average_earnings": average_earnings,
            "bonus": bonus,
            "final_payoff_total": final_payoff_total,
            # "final_results": final_results,
            "num_rounds": C.NUM_ROUNDS,
            "timers": timers,
        }


class Leftover(Page):
    def is_displayed(player: Player):
        participant = player.participant

        # 1. First, keep your 'kicked' protection
        if player_is_kicked(player):
            return False

        # 2. Define the "Leftover Condition" using your exact logic
        is_leftover_now = not participant.vars.get("grouped", False) or (
            participant.vars.get("leftover", False)
            and not participant.vars.get("end_game", False)
        )

        # 3. Only show if they are a leftover
        # AND they haven't seen this message yet.
        return is_leftover_now and not participant.vars.get(
            "leftover_page_shown", False
        )

    def vars_for_template(player: Player):
        # Keeps your variables for the HTML to show the right message
        return {
            "was_never_grouped": not player.participant.vars.get("grouped", False),
        }

    def before_next_page(player: Player, timeout_happened):
        # Mark as leftover (if not already)
        if not player_is_kicked(player):
            # 1. Mark as leftover
            player.participant.vars["leftover"] = True
            # 2. APPLY RULE: Leftover after grouping = Base only (£3.00)
            base_fee = player.session.config.get("base_fee", 3.00)
            player.total_task_earnings = 0
            player.bonus = 0
            player.final_payoff_total = float(base_fee)
            # 3. Lock the door so they skip the rest of the game
            player.participant.vars["leftover_page_shown"] = True


class Kicked(Page):
    def is_displayed(player: Player):
        """
        Show this page ONLY if the player was kicked during the Task app.
        And only show it ONCE.
        """
        participant = player.participant
        is_kicked = participant.vars.get("kicked", False)
        already_handled_in_intro = participant.vars.get("kicked_in_intro", False)

        # Show ONLY if kicked, not already handled, and hasn't been shown yet in this app
        return (
            is_kicked
            and not already_handled_in_intro
            and not participant.vars.get("kicked_page_shown", False)
        )

    def vars_for_template(player: Player):
        session = player.session
        timeout_time = session.config.get("timeout_time", 0)
        timeout_time_minutes = int(timeout_time / 60)

        return {
            "timeout_time_minutes": timeout_time_minutes,
            "round_number": player.round_number,
            "total_rounds": C.NUM_ROUNDS,
        }

    def before_next_page(player: Player, timeout_happened):
        # APPLY RULE: Leftover after grouping = Base only (£3.00)
        base_fee = player.session.config.get("base_fee", 3.00)
        player.total_task_earnings = 0
        player.bonus = 0
        player.final_payoff_total = float(base_fee)
        # Mark as shown so they skip rounds 2-10 instantly
        player.participant.vars["kicked_page_shown"] = True


page_sequence = [
    Waitforgroup,
    GroupingConfirmation,
    T1Trust,
    Contribute,
    ResultsWaitPage,
    Results,
    Payoff,
    Leftover,
    Kicked,
]
