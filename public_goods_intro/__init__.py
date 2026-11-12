from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from otree.api import Page
from otree.api import *

author = "Merve"
doc = """First part of the study""" 


# CONSTANTS AND DEFINITIONS 

class C(BaseConstants):
    NAME_IN_URL = 'public_goods_intro'
    PLAYERS_PER_GROUP = None 
    NUM_ROUNDS = 1 
    ENDOWMENT = c(2)  # Each unit represents 1 million €
    MULTIPLIER = 1.5

class Subsession(BaseSubsession):
    def creating_session(self):
        for player in self.get_players():
            player.participant.vars["kicked"] = False # This means no one is "kicked" when the game starts. Set to False (default state).
            player.participant.vars["no_consent_clicks"] = 0

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    consent = models.BooleanField(
        choices=[[True, "Yes"], [False, "No"]],
        widget=widgets.RadioSelect,
        blank=True  
    )
    comprehension1 = models.IntegerField(
        label="If all four companies invest €1M each, what is the boosted total after the 50% boost?",
        choices=[
            [0, "€5M"],
            [1, "€6M"],
            [2, "€7M"],
        ],
        widget=widgets.RadioSelect(),
    )
    comprehension2 = models.BooleanField(
        label="Do you receive a share from the boosted total even if you invest nothing?",
        choices=[[True, "Yes"], [False, "No"]]
    )
    comprehension3 = models.IntegerField(
        label="What happens to the boosted total when companies invest more money overall?",
        choices=[
            [0, "It stays the same."],
            [1, "It increases."],
            [2, "It decreases."],
        ],
        widget=widgets.RadioSelect(),
    )


# FUNCTIONS 

def vars_for_template(player: Player):
    session = player.session
    subsession = player.subsession
    comprehension_check = session.config.get("comprehension_check", False)
    timeout_time = session.config["timeout_time"]
    timeout_time_minutes = timeout_time / 60
    timers = session.config.get("timers", False)
    incentives = session.config["incentives"]

    return {

        "comprehension_check": comprehension_check,
        "timeout_time": timeout_time,
        "timeout_time_minutes": timeout_time_minutes,
        "incentives": incentives,
        "timers": timers,
        
    }

def player_is_kicked(player: Player):
    return player.participant.vars.get("kicked", False) # Returns whether a player is marked as "kicked."
# Instead of writing player.participant.vars.get("kicked", False) everywhere, we just call player_is_kicked(player).


# PAGES 

class InformedConsent(Page):
    form_model = 'player'
    form_fields = ['consent']

    def is_displayed(player: Player):
        """ Show informed consent only in the first round. """
        return player.round_number == 1

    def vars_for_template(player: Player):
        # Keeps all existing variables (Incentives, Timeouts, etc.)
        return vars_for_template(player)

    def error_message(player: Player, values):
        consent_choice = values.get('consent')

        if consent_choice is None:
            return "Please select an option to proceed."

        # If they chose 'No'
        if consent_choice is False:
            # Check how many times they've clicked 'Next' with 'No' selected
            if player.participant.vars.get("no_consent_clicks", 0) == 0:
                # This is the first click. Increment the counter and show the warning.
                player.participant.vars["no_consent_clicks"] = 1
                return (
                    "You have selected 'No'. This means that the study will end now. If you still want to participate, please select 'Yes'. " 
                    "If you do not wish to participate, click 'Next' again to proceed to the exit page."
                )
            
        # If it's the second click (counter is 1) or they chose 'Yes', 
        # oTree returns None and proceeds.

    def before_next_page(player: Player, timeout_happened):
        if player.consent is False:
            # Mark them as kicked so they skip the game
            player.participant.vars['kicked'] = True
            # Mark specifically for the NoConsent page
            player.participant.vars['no_consent'] = True

class NoConsent(Page):
    def is_displayed(player: Player):
        # Only shows if they explicitly submitted 'No'
        return player.participant.vars.get('no_consent', False)

class Overview(Page):
    def vars_for_template(player: Player):
        session = player.session
        return {
            "num_other_participants": 3,
            "timeout_time_minutes": session.config["timeout_time"] // 60,
            "incentives": session.config.get("incentives", False),
            "timers": session.config.get("timers", False),
            "comprehension_check": session.config.get("comprehension_check", False), 
        }

    def is_displayed(player: Player):
        return not player_is_kicked(player) # If returns True, the page will not be displayed.


    def get_timeout_seconds(player: Player):
        return player.session.config["timeout_time"]

    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.participant.vars["kicked"] = True # Once times out, marked as "kicked".
            player.participant.vars["kicked_in_intro"] = True  

class GeneralInstructions1(Page):
    def is_displayed(player: Player):
        return not player_is_kicked(player) # If returns True, the page will not be displayed.

    def get_timeout_seconds(player: Player):
        return player.session.config.get("timeout_time")

    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.participant.vars["kicked"] = True # Once times out, marked as "kicked".
            player.participant.vars["kicked_in_intro"] = True 

class GeneralInstructions2(Page):
    def is_displayed(player: Player):
        return not player_is_kicked(player) # If returns True, the page will not be displayed.
 
    def vars_for_template(player: Player):
        return {
            "num_rounds": player.session.config.get("NUM_ROUNDS", 10),
            "num_other_participants": 3,
            "multiplier": player.session.config.get("MULTIPLIER", 1.5),
            "endowment": player.session.config.get("ENDOWMENT", 2),
        }

    def get_timeout_seconds(player: Player):
        return player.session.config.get("timeout_time")

    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.participant.vars["kicked"] = True # Once times out, marked as "kicked".
            player.participant.vars["kicked_in_intro"] = True 

class Example(Page):
    def is_displayed(player: Player):
        return not player_is_kicked(player) # If returns True, the page will not be displayed.

    def get_timeout_seconds(player: Player):
        return player.session.config.get("timeout_time")

    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.participant.vars["kicked"] = True # Once times out, marked as "kicked".
            player.participant.vars["kicked_in_intro"] = True 

class ComprehensionCheck(Page):
    form_model = 'player'
    form_fields = ['comprehension1', 'comprehension2', 'comprehension3']

    def is_displayed(player: Player):
        return (
            player.session.config.get("comprehension_check", False)
            and player.round_number == 1
            and not player_is_kicked(player) # If returns True, the page will not be displayed.
        )
    
    def vars_for_template(player: Player):
        return {
            "endowment": player.session.config.get("ENDOWMENT", 2),
        }
    
    def get_timeout_seconds(player: Player):
        return player.session.config.get("timeout_time")

    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.participant.vars["kicked"] = True # Once times out, marked as "kicked".
            player.participant.vars["kicked_in_intro"] = True 

    def error_message(player, values):
        errors = {}

        if values.get('comprehension1') != 1:
            errors['comprehension1'] = "This is not correct. The four companies together invest €4M. The total group investment is increased by 50%, which adds €2M. This results in a boosted total of €6M in the shared fund."

        if values.get('comprehension2') is not True:
            errors['comprehension2'] = "This is not correct. The boosted total is shared equally among all four companies, even if a company did not invest."

        if values.get('comprehension3') != 1:
            errors['comprehension3'] = "This is not correct. When companies invest more money, the boosted total becomes larger because the combined investment is increased by 50%."
        return errors if errors else None

class Earnings(Page):
    def is_displayed(player: Player):
        return not player_is_kicked(player) # If returns True, the page will not be displayed.

    def get_timeout_seconds(player: Player):
        return player.session.config.get("timeout_time")

    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.participant.vars["kicked"] = True # Once times out, marked as "kicked".
            player.participant.vars["kicked_in_intro"] = True 

class GroupAssignment(Page):
    def is_displayed(player: Player):
        return not player_is_kicked(player) # If returns True, the page will not be displayed.

    def vars_for_template(player: Player):
        return {
            "num_other_participants": player.session.config.get("group_size", 4) - 1
        }

    def get_timeout_seconds(player: Player):
        return player.session.config.get("timeout_time")

    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.participant.vars["kicked"] = True # Once times out, marked as "kicked".
            player.participant.vars["kicked_in_intro"] = True 

class Kicked(Page):
    def is_displayed(player: Player):
        return player_is_kicked(player)  # If returns True, the page will be displayed.


page_sequence = [
    InformedConsent,
    NoConsent,
    Overview,
    GeneralInstructions1,
    GeneralInstructions2,
    Example,
    ComprehensionCheck,
    Earnings,
    GroupAssignment,
    Kicked,
]

