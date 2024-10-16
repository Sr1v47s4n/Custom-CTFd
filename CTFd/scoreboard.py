from flask import Blueprint, render_template

from CTFd.utils import config
from CTFd.utils.config.visibility import scores_visible
from CTFd.utils.decorators.visibility import (
    check_account_visibility,
    check_score_visibility,
)
from CTFd.utils.helpers import get_infos
from CTFd.utils.scores import get_standings
from CTFd.utils.user import is_admin

scoreboard = Blueprint("scoreboard", __name__)


@scoreboard.route("/scoreboard")
@check_account_visibility
@check_score_visibility
def listing():
    infos = get_infos()

    if config.is_scoreboard_frozen():
        infos.append(
            "Hold onto your hats! The scoreboard is frozen! Time to reveal who’s on top!"
        )

    if is_admin() is True and scores_visible() is False:
        infos.append(
            "Looks like the scores are currently snoozing in sleep mode! Don’t worry, they’ll wake up before you find your spots!"
        )

    standings = get_standings()
    return render_template("scoreboard.html", standings=standings, infos=infos)
