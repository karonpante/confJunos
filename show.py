__author__ = 'karon'

from ncclient import manager
from ncclient.xml_ import *


def get_vlans_xml():
    conn = manager.connect(host="10.1.11.75", port=830, username="DSGadmin", password="Password!", hostkey_verify=False,
                           device_params={'name': 'junos'})
    #Specify Filter
    root_filter = new_ele('filter')
    conf_filter = sub_ele(root_filter, 'configuration')
    sub_ele(conf_filter, 'vlans')

    # Get VLANS out of the running config in XML format
    vlans_xml = conn.get_config(source="running", filter=root_filter)

    return vlans_xml


def get_vlans_elements():
    vlans_xml = get_vlans_elements()

    # Get VLANS out of the running config in a list of elements and subelements
    vlans_elements = vlans_xml.xpath("data/configuration/vlans/vlan")

    return vlans_elements


def show_groups():
    conn = manager.connect(host="10.1.11.75", port=830, username="DSGadmin", password="Password!", hostkey_verify=False,
                           device_params={'name': 'junos'})
    #Specify Filter
    root_filter = new_ele('filter')
    conf_filter = sub_ele(root_filter, 'configuration')
    sub_ele(conf_filter, 'groups')

    # Get VLANS out of the running config in XML format
    vlans_xml = conn.get_config(source="running", filter=root_filter)

    # Get VLANS out of the running config in a list of elements and subelements
    vlans_list = vlans_xml.xpath("data/configuration/groups")
    print vlans_xml

    for element in vlans_list:
        element_list = list(element)
        print element_list


if __name__ == '__main__':
    #with manager.connect(host="10.1.11.75", port=830, username="DSGadmin", password="Password!", hostkey_verify=False, device_params={'name':'junos'}) as conn:
        #show_groups(conn)
        print get_vlans_xml()