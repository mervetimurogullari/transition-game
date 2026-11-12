from os import environ

SESSION_CONFIGS = [
    dict(
        name="transition_game",
        display_name="Public Goods Decision Study",
        app_sequence=["public_goods_intro", "public_goods_task", "public_goods_survey"],
        num_demo_participants=100,
        timeout_time=5 * 60,
        incentives=True,
        base_fee=3.00,
        payoff_conversion=0.10,  # Conversion Rule: £0.10 for every €1 Million earned in-task
        timers=True,
        comprehension_check=True,
        prolific_redirect_url="[prolific link here]",
        use_browser_bots=False,
    ),
]

# if set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = [
    "no_consent",
    "no_consent_clicks",
    "end_game",
    "leftover",
    "kicked",
    "grouped",
    "kicked_in_intro",
    "wait_page_arrival",
    "kicked_page_shown",
    "leftover_page_shown",
]

SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = "en"

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = "EUR"
USE_POINTS = False

ROOMS = [
    dict(name="prolific_study", display_name="Prolific Data Collection"),
]

ADMIN_USERNAME = "[placeholder]"
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get("OTREE_ADMIN_PASSWORD")

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""

SECRET_KEY = "8863634709909"

INSTALLED_APPS = ["otree"]
