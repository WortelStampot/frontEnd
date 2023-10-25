from flask import (
    Blueprint, render_template
)

import json

blueprint = Blueprint('table', __name__)

@blueprint.route('/table')
def renderTable():
    #get json data from 'back end'
    with open('backEnd/schedule_5_1.json') as f:
        scheduledata = f.read()
    schedule = json.loads(scheduledata) # wouldn't it be simpler to have access to the Staff, and Role objects instead of json string?
    shifts = sorted(schedule['shifts'], key= lambda shift: shift['staff']) # sort shifts by staff name
    staff = set(shift['staff'] for shift in shifts)

    return render_template('table/view.html', shifts=shifts, staff=staff)