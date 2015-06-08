__author__ = 'karon'

# Usefull sites:
# https://github.com/leopoul/ncclient/tree/master/examples
# http://www.juniper.net/techpubs/en_US/junos12.2/information-products/topic-collections/junos-xml-management-protocol-guide/index.html?topic-50312.html
from ncclient import manager
from ncclient.xml_ import *
import sqlite3


def addvlan(name, id, description=None):

    root = new_ele('config')
    configuration = sub_ele(root, 'configuration')
    vlans = sub_ele(configuration, 'vlans')
    vlan = sub_ele(vlans, 'vlan')
    sub_ele(vlan, 'name').text = name
    sub_ele(vlan, 'vlan-id').text = id
    sub_ele(vlan, 'description').text = description

    #vlan = """
    #vlans {
    #    TVLAN2000 {
    #        vlan-id 2000;
    #    }
    #}
    #"""
    #send_config = conn.load_configuration(format='text', config=vlan)

    return root


def addvlan_to_coreuplink(name):

#     configx = """
# <config>
#     <configuration>
#       <groups>
#         <name>uplink-to-core</name>
#         <interfaces>
#           <interface>
#             <name>&lt;ae*&gt;</name>
#             <unit>
#               <name>0</name>
#               <family>
#                 <ethernet-switching>
#                   <vlan>
#                     <members>TVLAN2020</members>
#                   </vlan>
#                 </ethernet-switching>
#               </family>
#             </unit>
#           </interface>
#         </interfaces>
#       </groups>
#     </configuration>
# </config>
#     """
#     confige = to_ele(configx)

    root = new_ele('config')
    configuration = sub_ele(root, 'configuration')
    groups = sub_ele(configuration, 'groups')
    sub_ele(groups, 'name').text = 'uplink-to-core'
    interfaces = sub_ele(groups, 'interfaces')
    interface = sub_ele(interfaces, 'interface')
    sub_ele(interface, 'name').text = '<ae*>'
    unit = sub_ele(interface, 'unit')
    sub_ele(unit, 'name').text = '0'
    family = sub_ele(unit, 'family')
    ethernet_switching = sub_ele(family, 'ethernet-switching')
    vlan = sub_ele(ethernet_switching, 'vlan')
    sub_ele(vlan, 'members').text = name

    return root


def delvlan(name):

    root = new_ele('config')
    configuration = sub_ele(root, 'configuration')
    vlans = sub_ele(configuration, 'vlans')
    vlan = sub_ele(vlans, "vlan")
    vlan.set("delete", "delete")
    sub_ele(vlan, 'name').text = name
    #sub_ele(vlan, 'vlan-id').text = id # DOES NOT WORK!!Probably because Name is the header of the XML object?

#     configx = """
# <config>
#     <configuration>
#       <vlans>
#         <vlan delete="delete">
#           <name>TVLAN2001</name>
#           <vlan-id>2001</vlan-id>
#         </vlan>
#       </vlans>
#     </configuration>
# </config>
#     """
#     confige = to_ele(configx)

    return root


def delvlan_to_coreuplink(name):

    root = new_ele('config')
    configuration = sub_ele(root, 'configuration')
    groups = sub_ele(configuration, 'groups')
    sub_ele(groups, 'name').text = 'uplink-to-core'
    interfaces = sub_ele(groups, 'interfaces')
    interface = sub_ele(interfaces, 'interface')
    sub_ele(interface, 'name').text = '<ae*>'
    unit = sub_ele(interface, 'unit')
    sub_ele(unit, 'name').text = '0'
    family = sub_ele(unit, 'family')
    ethernet_switching = sub_ele(family, 'ethernet-switching')
    vlan = sub_ele(ethernet_switching, 'vlan')
    member = sub_ele(vlan, 'members')
    member.text = name
    member.set("delete", "delete")

    return root


if __name__ == '__main__':
    name = raw_input("Enter VLAN name: ")
    id = raw_input("Enter VLAN ID: ")

    with sqlite3.connect('assets.db') as sql:
        cursor = sql.cursor()
        for row in cursor.execute('SELECT host FROM switches'):
            host = row[0]

            print "\n\nLOGGED IN ON: " + host
            print "=" * 25

            with manager.connect(host=host, port=830, username="DSGadmin", password="Password!", hostkey_verify=False,
                                 device_params={'name':'junos'}) as conn:
                conn.lock()

                #send_config = conn.edit_config(config=addvlan(name, id))
                #send_config = conn.edit_config(config=addvlan_to_coreuplink(name), default_operation="merge")
                send_config = conn.edit_config(config=delvlan(name))
                #send_config = conn.edit_config(config=delvlan_to_coreuplink(name))
                print "\nConfiguration send: " + send_config.xpath("*")[0].tag

                check_config = conn.validate()
                print "\nCheck configuration: "
                print "-" * 20
                routing_engines = check_config.xpath("commit-results/routing-engine")

                for re in routing_engines:
                    print re[0].text + ": " + re[1].tag

                compare_config = conn.compare_configuration()
                print "\nChanges being made: "
                print "-" * 19
                print compare_config.xpath("configuration-information/configuration-output")[0].text

                # Commit changes
                if raw_input("\nCommit changes on " + host + "? (yes/no)") == "yes":
                    commit = conn.commit()
                    print "Configuration commited"
                    print "-" * 22
                    routing_engines = commit.xpath("commit-results/routing-engine")
                    for re in routing_engines:
                        print re[0].text + ": " + re[1].tag
                else:
                    commit = conn.discard_changes()
                    print "Configuration rollback: " + commit.xpath("*")[0].tag

                conn.unlock()