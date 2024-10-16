from flask import Blueprint, redirect, render_template, request, url_for

from CTFd.constants.config import ChallengeVisibilityTypes, Configs
from CTFd.utils.config import is_teams_mode
from CTFd.utils.dates import ctf_ended, ctf_paused, ctf_started
from CTFd.utils.decorators import (
    during_ctf_time_only,
    require_complete_profile,
    require_verified_emails,
)
from CTFd.utils.decorators.visibility import check_challenge_visibility
from CTFd.utils.helpers import get_errors, get_infos
from CTFd.utils.user import authed, get_current_team

challenges = Blueprint("challenges", __name__)


@challenges.route("/challenges", methods=["GET"])
@require_complete_profile
@during_ctf_time_only
@require_verified_emails
@check_challenge_visibility
def listing():
    if (
        Configs.challenge_visibility == ChallengeVisibilityTypes.PUBLIC
        and authed() is False
    ):
        pass
    else:
        if is_teams_mode() and get_current_team() is None:
            return redirect(url_for("teams.private", next=request.full_path))

    infos = get_infos()
    errors = get_errors()

    if Configs.challenge_visibility == ChallengeVisibilityTypes.ADMINS:
        infos.append(
            "Whoop! The challenges are yet to see the light. Can you wait a bit for the sunrise?"
        )

    if ctf_started() is False:
        errors.append(
            f"Oops! Hold up your horses, the runway isn’t cleared for takeoff just yet!"
        )

    if ctf_paused() is True:
        infos.append(
            f"Just like in the movies... we’ll be right back after this short break!"
        )

    if ctf_ended() is True:
        infos.append(
            "That’s a wrap, everyone! Thanks for joining us today! We hope you had a blast! \n"
            "Until next time, keep smiling and stay awesome!"
        ) 

    return render_template("challenges.html", infos=infos, errors=errors)
