import random
from otree.api import *


author = "Merve"
doc = """Third part of the study: Survey and debriefing"""


# CONSTANTS AND DEFINITIONS 

class C(BaseConstants):
    NAME_IN_URL = 'public_goods_survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    Likert_1_to_5 = [
        [1, "1 - Strongly disagree"],
        [2, "2 - Disagree"],
        [3, "3 - Neither agree nor disagree"],
        [4, "4 - Agree"],
        [5, "5 - Strongly agree"],
    ]
    Likert_1_to_7 = [
        [1, "1 - Strongly disagree"],
        [2, "2 - Disagree"],
        [3, "3 - Somewhat disagree"],
        [4, "4 - Neither agree nor disagree"],
        [5, "5 - Somewhat agree"],
        [6, "6 - Agree"],
        [7, "7 - Strongly agree"],
    ]
    CFC_1_to_7 = [
        [1, "1 - Extremely uncharacteristic of me"],
        [2, "2 - Uncharacteristic of me"],
        [3, "3 - Somewhat uncharacteristic of me"],
        [4, "4 - Neither characteristic nor uncharacteristic"],
        [5, "5 - Somewhat characteristic of me"],
        [6, "6 - Characteristic of me"],
        [7, "7 - Extremely characteristic of me"],
    ]
    # SVO Item Distributions: [ [You, Other], [You, Other] ... ]
    SVO_DISTRIBUTIONS = {
        1: [[85, 85], [85, 76], [85, 68], [85, 59], [85, 50], [85, 41], [85, 33], [85, 24], [85, 15]],
        2: [[85, 15], [87, 19], [89, 24], [91, 28], [93, 33], [94, 37], [96, 41], [98, 46], [100, 50]],
        3: [[50, 100], [54, 98], [59, 96], [63, 94], [68, 93], [72, 91], [76, 89], [81, 87], [85, 85]],
        4: [[50, 100], [54, 89], [59, 79], [63, 68], [68, 58], [72, 47], [76, 36], [81, 26], [85, 15]],
        5: [[100, 50], [94, 56], [88, 63], [81, 69], [75, 75], [69, 81], [63, 88], [56, 94], [50, 100]],
        6: [[100, 50], [98, 54], [96, 59], [94, 63], [93, 68], [91, 72], [89, 76], [87, 81], [85, 85]],
    }

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    t2_con_trust_pred_1 = models.IntegerField(
        label="The other participants will make consistent investments throughout rounds.",	
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    )
    t2_con_trust_pred_2 = models.IntegerField(
        label="The other participants will make investments that clearly show how they want the shared charging infrastructure to develop.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    )
    t2_con_trust_pred_3 = models.IntegerField(
        label="The other participants will use an investment strategy that I can easily predict throughout rounds.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    )
    t2_con_trust_pred_4 = models.IntegerField(
        label="The other participants will each follow a stable approach when making investment decisions throughout rounds.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    ) 
    t2_con_trust_benev_1 = models.IntegerField(
        label="The other participants will be willing to invest for the benefit of the group.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    )    
    t2_con_trust_benev_2 = models.IntegerField(
        label="The other participants will care about how their investments affect the earnings of others.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    )   
    t2_con_trust_benev_3 = models.IntegerField(
        label="The other participants will be willing to invest if I invest as well.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    )   
    t2_con_trust_benev_4 = models.IntegerField(
        label="The other participants will look out for my interests when making investment decisions.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    )  
    svo_1 = models.IntegerField(choices=range(1, 10), widget=widgets.RadioSelectHorizontal)
    svo_2 = models.IntegerField(choices=range(1, 10), widget=widgets.RadioSelectHorizontal)
    svo_3 = models.IntegerField(choices=range(1, 10), widget=widgets.RadioSelectHorizontal)
    svo_4 = models.IntegerField(choices=range(1, 10), widget=widgets.RadioSelectHorizontal)
    svo_5 = models.IntegerField(choices=range(1, 10), widget=widgets.RadioSelectHorizontal)
    svo_6 = models.IntegerField(choices=range(1, 10), widget=widgets.RadioSelectHorizontal)
    hex_3 = models.IntegerField(
        label="I rarely hold a grudge, even against people who have badly wronged me.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    ) 
    hex_6 = models.IntegerField(
        label="I wouldn’t use flattery to get a raise or promotion at work, even if I thought it would succeed.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    ) 
    hex_9 = models.IntegerField(
        label="People sometimes tell me that I am too critical of others.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    ) 
    hex_12 = models.IntegerField(
        label="If I knew that I could never get caught, I would be willing to steal a million dollars.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    ) 
    hex_15 = models.IntegerField(
        label="People sometimes tell me that I’m too stubborn.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    ) 
    hex_18 = models.IntegerField(
        label="Having a lot of money is not especially important to me.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    ) 
    hex_21 = models.IntegerField(
        label="People think of me as someone who has a quick temper.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    )   
    hex_24 = models.IntegerField(
        label="I think that I am entitled to more respect than the average person is.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    )
    hex_27 = models.IntegerField(
        label="My attitude toward people who have treated me badly is “forgive and forget.”",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    )
    hex_30 = models.IntegerField(
        label="If I want something from someone, I will laugh at that person’s worst jokes.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    )
    hex_33 = models.IntegerField(
        label="I tend to be lenient in judging other people.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    )
    hex_36 = models.IntegerField(
        label="I would never accept a bribe, even if it were very large.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    )
    hex_39 = models.IntegerField(
        label="I am usually quite flexible in my opinions when people disagree with me.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    )
    hex_42 = models.IntegerField(
        label="I would get a lot of pleasure from owning expensive luxury goods.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    )
    hex_45 = models.IntegerField(
        label="Most people tend to get angry more quickly than I do.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    )
    hex_48 = models.IntegerField(
        label="I want people to know that I am an important person of high status.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    )
    hex_51 = models.IntegerField(
        label="Even when people make a lot of mistakes, I rarely say anything negative.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    )
    hex_54 = models.IntegerField(
        label="I wouldn’t pretend to like someone just to get that person to do favors for me.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    )
    hex_57 = models.IntegerField(
        label="When people tell me that I’m wrong, my first reaction is to argue with them.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    )
    hex_60 = models.IntegerField(
        label="I’d be tempted to use counterfeit money, if I were sure I could get away with it.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    ) 
    gen_trust_1 = models.IntegerField(
        label="Most people are basically honest.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    )
    gen_trust_2 = models.IntegerField(
        label="Most people are trustworthy.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    )
    gen_trust_3 = models.IntegerField(
        label="Most people are basically good and kind.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    )
    gen_trust_4 = models.IntegerField(
        label="Most people are trustful of others.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    )
    gen_trust_5 = models.IntegerField(
        label="I am trustful.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    )
    gen_trust_6 = models.IntegerField(
        label="Most people will respond in kind when they are trusted by others.",
        choices=C.Likert_1_to_5,
        widget=widgets.RadioSelect,
    )
    env_self_id_1 = models.IntegerField(
        label="Acting environmentally-friendly is an important part of who I am.",
        choices=C.Likert_1_to_7,
        widget=widgets.RadioSelect,
    )
    env_self_id_2 = models.IntegerField(
        label="I am the type of person who acts environmentally-friendly.",
        choices=C.Likert_1_to_7,
        widget=widgets.RadioSelect,
    )
    env_self_id_3 = models.IntegerField(
        label="I see myself as an environmentally-friendly person.",
        choices=C.Likert_1_to_7,
        widget=widgets.RadioSelect,
    )
    CFC_F_1 = models.IntegerField(
        label="I consider how things might be in the future, and try to influence those things with my day to day behavior.",
        choices=C.CFC_1_to_7,
        widget=widgets.RadioSelect,
    )
    CFC_F_2 = models.IntegerField(
        label="Often I engage in a particular behavior in order to achieve outcomes that may not result for many years.",
        choices=C.CFC_1_to_7,
        widget=widgets.RadioSelect,
    )
    CFC_F_3 = models.IntegerField(
        label="I am willing to sacrifice my immediate happiness or wellbeing in order to achieve future outcomes.",
        choices=C.CFC_1_to_7,
        widget=widgets.RadioSelect,
    )
    CFC_F_4 = models.IntegerField(
        label="I think it is important to take warnings about negative outcomes seriously even if the negative outcome will not occur for many years.",
        choices=C.CFC_1_to_7,
        widget=widgets.RadioSelect,
    )
    CFC_F_5 = models.IntegerField(
        label="I think it is more important to perform a behavior with important distant consequences than a behavior with less important immediate consequences.",
        choices=C.CFC_1_to_7,
        widget=widgets.RadioSelect,
    )
    CFC_F_6 = models.IntegerField(
        label="When I make a decision, I think about how it might affect me in the future.",
        choices=C.CFC_1_to_7,
        widget=widgets.RadioSelect,
    )
    CFC_F_7 = models.IntegerField(
        label="My behavior is generally influenced by future consequences.",
        choices=C.CFC_1_to_7,
        widget=widgets.RadioSelect,
    )
    comment = models.StringField(blank=True)
    age = models.IntegerField(label="What is your age?", min=18, max=100)    
    gender = models.IntegerField(
            label="What is your gender?",
            choices=[[0, "Woman"], [1, "Man"], [2, "Other"], [3, "Prefer not to say"]],
            widget=widgets.RadioSelect
        )


# FUNCTIONS 
 
def player_is_kicked(player: Player):
    return player.participant.vars.get("kicked", False)

def player_is_leftover(player: Player):
    return player.participant.vars.get("leftover", False)


# PAGES 

class T2Trust(Page):
    form_model = 'player'
    form_fields = [
        't2_con_trust_pred_1', 't2_con_trust_pred_2', 't2_con_trust_pred_3', 't2_con_trust_pred_4',
        't2_con_trust_benev_1', 't2_con_trust_benev_2', 't2_con_trust_benev_3', 't2_con_trust_benev_4'
    ]
    def is_displayed(player: Player):
        return not player_is_kicked(player) and not player_is_leftover(player)
    
class SVO(Page):
    form_model = 'player'
    form_fields = ['svo_1', 'svo_2', 'svo_3', 'svo_4', 'svo_5', 'svo_6']
    def is_displayed(player: Player):
        # Combined: Not kicked + Not leftover + Randomized order check
        return not player_is_kicked(player) and not player_is_leftover(player)
    def vars_for_template(player: Player):
        return {
            'svo_items': C.SVO_DISTRIBUTIONS,
            'option_list': [1, 2, 3, 4, 5, 6, 7, 8, 9] 
        }
    
class HEXACO(Page):
    form_model = 'player'
    form_fields = [
        'hex_3', 'hex_6', 'hex_9', 'hex_12', 'hex_15', 'hex_18', 
        'hex_21', 'hex_24', 'hex_27', 'hex_30', 'hex_33', 'hex_36', 
        'hex_39', 'hex_42', 'hex_45', 'hex_48', 'hex_51', 'hex_54', 
        'hex_57', 'hex_60'
    ]
    def is_displayed(player: Player):
        return not player_is_kicked(player) and not player_is_leftover(player)
    def vars_for_template(player: Player):
        return {'option_list': [1, 2, 3, 4, 5]}
    
class GenTrust(Page):
    form_model = 'player'
    form_fields = ['gen_trust_1', 'gen_trust_2', 'gen_trust_3', 'gen_trust_4', 'gen_trust_5', 'gen_trust_6']
    def is_displayed(player: Player):
        return not player_is_kicked(player) and not player_is_leftover(player)
    def vars_for_template(player: Player):
        return {'option_list': [1, 2, 3, 4, 5]}
    
class ESI(Page):
    form_model = 'player'
    form_fields = ['env_self_id_1', 'env_self_id_2', 'env_self_id_3']
    def is_displayed(player: Player):
        return not player_is_kicked(player) and not player_is_leftover(player)
    def vars_for_template(player: Player):
        return {'option_list': [1, 2, 3, 4, 5, 6, 7]}   

class CFC(Page):
    form_model = 'player'
    form_fields = ['CFC_F_1', 'CFC_F_2', 'CFC_F_3', 'CFC_F_4', 'CFC_F_5', 'CFC_F_6', 'CFC_F_7']
    def is_displayed(player: Player):
        return not player_is_kicked(player) and not player_is_leftover(player)
    def vars_for_template(player: Player):
        return {'option_list': [1, 2, 3, 4, 5, 6, 7]}
    
class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender']
    def is_displayed(player: Player):
        return not player_is_kicked(player) and not player_is_leftover(player)

class Funnel(Page):
    form_model = 'player'
    form_fields = ['comment']
    def is_displayed(player: Player):
        # Skip this page if they were kicked or left over
        return not player_is_kicked(player) and not player_is_leftover(player)
    
class Debriefing(Page):
    # The final destination for every participant.
    pass


page_sequence = [
    T2Trust,
    SVO,
    HEXACO,
    GenTrust,
    ESI,
    CFC,
    Demographics,
    Funnel,
    Debriefing,
]