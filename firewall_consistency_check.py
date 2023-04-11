from netmiko import ConnectHandler
'''

Script to check firewall rulesets, verify if they are there and update if not

To add:
1. rules abstraction either through  napalm for routing or others to translate to intent
2. command abstraction or device selection
2. input/output to external files or prompt to do so
3. 

'''

push_check = True
question = "Do you want to proceed with pushing changes to devices?"

# Define the dictionary of rules to check
rules_dict = {
    "allow-http": "permit tcp any any eq 80",
    "allow-https": "permit tcp any any eq 443",
    "allow-ssh": "permit tcp any any eq 22",
}

# Define the list of firewalls to connect to
firewalls = [
    {"device_type": "cisco_asa", "ip": "192.168.1.1", "username": "admin", "password": "password"},
    {"device_type": "cisco_asa", "ip": "192.168.1.2", "username": "admin", "password": "password"},
    {"device_type": "cisco_asa", "ip": "192.168.1.3", "username": "admin", "password": "password"},
]

# Loop through each firewall
for fw in firewalls:
    # Create Netmiko SSH client object
    ssh = ConnectHandler(**fw)

    # Loop through each rule in the dictionary
    for rule_name, rule_command in rules_dict.items():
        # Check if the rule already exists in the firewall
        output = ssh.send_command(f"show access-list | include {rule_command}")
        if output:
            print(f"Rule '{rule_name}' already exists on {fw['ip']}")
        else:
            # Push the missing rule to the firewall
            while push_check == True:
                answer = input(f"{question} (y/n) [default y]: ").lower().strip()
                # if answer is no yes, also check length to make sure there is some input
                if len(answer) != 0 and answer[0] != 'y':
                    # if answer is n/ no/ etc
                    if answer[0] == 'n':
                        push_check = False
                        break

                #push changes assuming above loop doesn't stop it
                ssh.send_config_set([f"access-list 1 {rule_command}", "write memory"])
                print(f"Pushed rule '{rule_name}' to {fw['ip']}")

    # Close the SSH connection
    ssh.disconnect()
