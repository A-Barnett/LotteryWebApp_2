# IMPORTS
import logging
import re
from wtforms.validators import DataRequired, ValidationError, Length, Email, EqualTo
from flask import Blueprint, render_template, request, flash, redirect, url_for
import bcrypt
import secrets
from app import db
from models import Draw, decrypt
from flask_login import login_required
# CONFIG
lottery_blueprint = Blueprint('lottery', __name__, template_folder='templates')


from flask_login import current_user
# VIEWS
# view lottery page
@lottery_blueprint.route('/lottery')
@login_required
def lottery():
    if current_user.role == 'user':
        return render_template('lottery/lottery.html')
    else:
        logging.warning('SECURITY -  Invalid access [%s, %s, %s, %s]’,current_user.id,current_user.username,'
                        'current_user.role,request.remote_addr')



def validate_numbers(numbers):
    num = numbers.split(" ")
    num = list(filter(None, num))
    if len(num) != 6:
        flash("Must submit 6 numbers")
        return False
    for n in num:
        n = int(n)
        if n > 60 or n < 1:
            flash("Numbers must be between 1 - 60")
            return False
    return True


@lottery_blueprint.route('/add_draw', methods=['POST'])
def add_draw():
    submitted_draw = ''
    for i in range(6):
        submitted_draw += request.form.get('no' + str(i + 1)) + ' '
    submitted_draw.strip()
    check = validate_numbers(submitted_draw)
    # create a new draw with the form data.
    if check:
        new_draw = Draw(user_id=current_user.id, numbers=submitted_draw, master_draw=False,
                        lottery_round=0)  # TODO: update user_id [user_id=1 is a placeholder]
        # add the new draw to the database
        db.session.add(new_draw)
        db.session.commit()
        # re-render lottery.page
        flash('Draw %s submitted.' % submitted_draw)
    return lottery()


# view all draws that have not been played
@lottery_blueprint.route('/view_draws', methods=['POST'])
def view_draws():
    # get all draws that have not been played [played=0]
    playable_draws = Draw.query.filter_by(been_played=False,
                                          user_id=current_user.id).all()  # TODO: filter playable draws for current user
    playable_draws_de = []
    # if playable draws exist
    for d in playable_draws:
        playable_draws_de.append(decrypt(d.numbers, current_user.postkey))

    if len(playable_draws) != 0:
        # re-render lottery page with playable draws
        print(playable_draws_de)
        return render_template('lottery/lottery.html', playable_draws=playable_draws_de)
    else:
        flash('No playable draws.')
        return lottery()


# view lottery results
@lottery_blueprint.route('/check_draws', methods=['POST'])
def check_draws():
    # get played draws
    played_draws = Draw.query.filter_by(been_played=True,
                                        id=current_user.id).all()  # TODO: filter played draws for current user

    # if played draws exist
    if len(played_draws) != 0:
        return render_template('lottery/lottery.html', results=played_draws, played=True)

    # if no played draws exist [all draw entries have been played therefore wait for next lottery round]
    else:
        flash("Next round of lottery yet to play. Check you have playable draws.")
        return lottery()


# delete all played draws
@lottery_blueprint.route('/play_again', methods=['POST'])
def play_again():
    Draw.query.filter_by(been_played=True, master_draw=False, id=current_user.id).delete(synchronize_session=False)
    db.session.commit()

    flash("All played draws deleted.")
    return lottery()
