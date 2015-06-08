__author__ = 'karon'

import sqlite3

database = "junos.db"

conn = sqlite3.connect(database)
#conn.execute('CREATE TABLE Interfaces (interfaceID INTEGER PRIMARY KEY, name TEXT, type TEXT)')
#conn.execute('CREATE TABLE DeviceContainsVlans (ID INTEGER PRIMARY KEY, vlanID NUMERIC, deviceID NUMERIC, FOREIGN KEY(vlanID) REFERENCES Vlans(vlanID), FOREIGN KEY(deviceID) REFERENCES Devices(deviceID))')
#conn.execute('CREATE TABLE GroupContainsVlans (ID INTEGER PRIMARY KEY, vlanID NUMERIC, groupID NUMERIC, FOREIGN KEY(vlanID) REFERENCES Vlans(vlanID), FOREIGN KEY(groupID) REFERENCES Groups(groupID))')
conn.execute('CREATE TABLE DeviceContainsGroups (ID INTEGER PRIMARY KEY, deviceID NUMERIC, groupID NUMERIC, FOREIGN KEY(deviceID) REFERENCES Devices(deviceID), FOREIGN KEY(groupID) REFERENCES Groups(groupID))')
conn.commit()
conn.close()