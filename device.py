__author__ = 'karon'

from ncclient import manager
from ncclient.xml_ import *


class Device:
    def __init__(self, name, ip, os, username, password):
        self.name = name
        self.os = os
        self.ip = ip
        self.username = username
        self.password = password

    def get_vlans_xml(self):
        with manager.connect(host=self.ip, port=830, username=self.username, password=self.password,
                             hostkey_verify=False, device_params={'name': self.os}) as conn:
            #Specify Filter
            root_filter = new_ele('filter')
            conf_filter = sub_ele(root_filter, 'configuration')
            sub_ele(conf_filter, 'vlans')

            # Get VLANS out of the running config in XML format
            vlans_xml = conn.get_config(source="running", filter=root_filter)

        return vlans_xml

    def get_vlans_elements(self):
        # Get VLANs out of the running config via XML first
        vlans_xml = self.get_vlans_xml()

        # Get VLANS in a list of elements and subelements
        vlans_elements = vlans_xml.xpath("data/configuration/vlans/vlan")

        return vlans_elements

    def get_groups_xml(self):
        with manager.connect(host=self.ip, port=830, username=self.username, password=self.password,
                             hostkey_verify=False, device_params={'name': self.os}) as conn:
            #Specify Filter
            root_filter = new_ele('filter')
            conf_filter = sub_ele(root_filter, 'configuration')
            sub_ele(conf_filter, 'groups')

            # Get gorups out of the running config in XML format
            groups_xml = conn.get_config(source="running", filter=root_filter)

        return groups_xml

    def get_groups_elements(self):
        # Get Groups out of the running config via XML first
        groups_xml = self.get_groups_xml()

        # Get groups in a list of elements and subelements
        groups_elements = groups_xml.xpath("data/configuration/groups")

        return groups_elements

    def set_vlan(self, name, id, description=None):
        with manager.connect(host=self.ip, port=830, username=self.username, password=self.password,
                             hostkey_verify=False, device_params={'name': self.os}) as conn:
            # Create element view for VLAN
            root = new_ele('config')
            configuration = sub_ele(root, 'configuration')
            vlans = sub_ele(configuration, 'vlans')
            vlan = sub_ele(vlans, 'vlan')
            sub_ele(vlan, 'name').text = name
            sub_ele(vlan, 'vlan-id').text = id
            sub_ele(vlan, 'description').text = description

            # Execute element request on device
            conn.lock()
            conn.edit_config(root)
            conn.commit()
            conn.unlock()

    def del_vlan(self, name):
        with manager.connect(host=self.ip, port=830, username=self.username, password=self.password,
                             hostkey_verify=False, device_params={'name': self.os}) as conn:
            # Create element view for VLAN
            root = new_ele('config')
            configuration = sub_ele(root, 'configuration')
            vlans = sub_ele(configuration, 'vlans')
            vlan = sub_ele(vlans, "vlan")
            vlan.set("delete", "delete")
            sub_ele(vlan, 'name').text = name
            #sub_ele(vlan, 'vlan-id').text = id # DOES NOT WORK!!Probably because Name is the header of the XML object?

            # Execute element request on device
            conn.lock()
            conn.edit_config(root)
            conn.commit()
            conn.unlock()