__author__ = 'karon'

# imports
from flask import Flask, render_template, request, session, flash, redirect, url_for, g
import sqlite3
from device import Device

#
# Configuration
#
DATABASE='junos.db'

# Declare Flask application
app = Flask(__name__)

# Pulls in app configuration by looking for UPPERCASE variables
app.config.from_object(__name__)


# Function to connect to DB
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

# Routes
@app.route('/')
def main():
    return render_template('main.xhtml')

@app.route('/vlans', methods=['POST', 'GET'])
def vlans():
    devvlans = None
    devgroups = None
    g.db = connect_db()

    if request.method == 'POST':
        dev1 = Device("EALABSW00002", "10.1.11.75", "junos", "DSGadmin", "Password!")

        if request.form['btn_vlans'] == "check":
            devvlans = dev1.get_vlans_xml()
            devgroups = dev1.get_groups_xml()

        elif request.form['btn_vlans'] == "vlanadd":
            # Declare VLAN variables
            vlan_id = request.form['vlans_id']
            vlan_description = request.form['vlans_description']
            vlan_name = "VLAN"+vlan_id

            # Adjust database
            g.db.execute('insert into vlans (id, description) values (?, ?)', [vlan_id, vlan_description])
            g.db.commit()

            # Adjust device
            dev1.set_vlan(vlan_name, vlan_id, vlan_description)

        elif request.form['btn_vlans'] == "vlanedit":
            # Declare VLAN variables
            vlan_id = request.form['vlans_id']
            vlan_description = request.form['vlans_description']
            vlan_name = "VLAN"+vlan_id

            # Adjust database
            g.db.execute('update vlans set description = ? where id is ?', [vlan_description, vlan_id])
            g.db.commit()

            # Adjust device
            dev1.set_vlan(vlan_name, vlan_id, vlan_description)

        elif request.form['btn_vlans'] == "vlanremove":
            # Declare VLAN variables
            vlan_id = request.form['vlans_id']
            vlan_name = "VLAN"+vlan_id

            # Adjust database
            g.db.execute('delete from vlans where id is ?', [vlan_id])
            g.db.commit()

            # Adjust device
            dev1.del_vlan(vlan_name)

    cur = g.db.execute('select * from vlans')
    dbvlans = [dict(id=row[1], vlan=row[2]) for row in cur.fetchall()]
    g.db.close()
    return render_template('vlans.xhtml', vlans=dbvlans, devvlans=devvlans, devgroups=devgroups)

if __name__ == '__main__':
    app.run(debug=True)



