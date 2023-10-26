from flask import (
    Blueprint, render_template
)

import json

blueprint = Blueprint('table', __name__)

@blueprint.route('/table')
def renderTable():
    #get json data from 'back end'
    with open('backEnd/dataSample.json') as f:
        scheduledata = f.read()
    schedule = json.loads(scheduledata) # wouldn't it be simpler to have access to the Staff, and Role objects instead of json string?
    shiftsByStaff = {} #name: list of shifts
    for shift in schedule["shifts"]:
        #if name is already in shiftsByStaff, add shift to the list at that name
        #if name is not in shiftsByStaff, set to empty list
        name = shift["staff"]
        shiftsByStaff.setdefault(name, [])
        shiftsByStaff[name].append(shift)

    data = []
    for staff, shifts in shiftsByStaff.items():
        staffDataDict = {"name": staff, "MONDAY": [], "TUESDAY": [], "WEDNESDAY": [], "THURSDAY": [], "FRIDAY": [], "SATURDAY": [], "SUNDAY": []}
        for shift in shifts:
            staffDataDict[shift["day"]].append(shift["role"])
        staffData = []
        for key, value in staffDataDict.items():
            if key != "name":
                value = ", ".join(value)
            staffData.append(value)
        data.append(staffData)

    return render_template('table/view.html', data=data)