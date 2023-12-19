import requests
from ncclient import manager
import xml.dom.minidom

# Connect to the NETCONF device
m = manager.connect(
    host="192.168.56.119",
    port=830,
    username="cisco",
    password="cisco123!",
    hostkey_verify=False
)

# Verify the current running-config
print("# Current Running Configuration:")
netconf_reply = m.get_config(source="running")
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

# Make three changes to the configuration

# Change 1: Update the hostname
netconf_hostname = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
     <hostname>CSR1kv_updated</hostname>
  </native>
</config>
"""
netconf_reply = m.edit_config(target="running", config=netconf_hostname)
print("# Change 1 - Updated Hostname:")
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

# Change 2: Add a new Loopback interface
netconf_newloop = """
<config>
 <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
  <interface>
   <Loopback>
    <name>2</name>
    <description>My second NETCONF loopback</description>
    <ip>
     <address>
      <primary>
       <address>10.1.1.2</address>
       <mask>255.255.255.0</mask>
      </primary>
     </address>
    </ip>
   </Loopback>
  </interface>
 </native>
</config>
"""
netconf_reply = m.edit_config(target="running", config=netconf_newloop)
print("# Change 2 - Added New Loopback:")
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

# Change 3: Modify Loopback 1 description
netconf_loopback_update = """
<config>
 <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
  <interface>
   <Loopback>
    <name>1</name>
    <description>Updated description for Loopback 1</description>
   </Loopback>
  </interface>
 </native>
</config>
"""
netconf_reply = m.edit_config(target="running", config=netconf_loopback_update)
print("# Change 3 - Updated Loopback 1 Description:")
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

# Verify the changes
print("# Updated Running Configuration:")
netconf_reply = m.get_config(source="running")
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())


# List Webex Teams Rooms
access_token = "NDliNWM0MmYtNjZlOS00OTM3LTg0NTQtZjFlOWFiMTQzZGJlMzA1YTgzZTctMzQ4_P0A1_d0b19fc5-a717-4064-90e2-8d88b3acad9c"  # Replace with your actual access token
webex_api_url = "https://api.ciscospark.com/v1/rooms"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}

response = requests.get(webex_api_url, headers=headers)
rooms = response.json()["items"]

# Specify the Webex Teams room IDs where you want to send notifications
target_room_ids = ["Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vOWNmOTJjYTAtOWU3Mi0xMWVlLWIzMzEtOWRhNDAzZWQwNGU0", "Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vNTk0MmI4NDAtOWU2ZS0xMWVlLWJiZjMtNjM5MjNmODVmMGQ4"]  # Replace with the actual room IDs

# Send a notification to each specified room
for room_id in target_room_ids:
    webex_message = """
    Configuration Update:
    - Hostname changed to CSR1kv_updated
    - Added a new Loopback interface (Loopback 2)
    - Updated description for Loopback 1
    """

    payload = {
        "roomId": room_id,
        "markdown": webex_message,
        "title": "Configuration Update"
    }

    response = requests.post(webex_api_url, headers=headers, json=payload)

    # Check the response status
    if response.status_code == 200:
        print(f"Notification sent successfully to WebEx Teams room {room_id}!")
    else:
        print(f"Failed to send notification to WebEx Teams room {room_id}. Status code: {response.status_code}")
        print(response.text)

# Close the NETCONF session
m.close_session()