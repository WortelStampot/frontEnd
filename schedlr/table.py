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
    schedule = json.loads(scheduledata)
    shifts = schedule['shifts']

    return render_template('table/view.html', shifts=shifts)