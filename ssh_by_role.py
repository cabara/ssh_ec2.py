#! /usr/bin/python3

import argparse
import os
import subprocess
import json

def print_with_indexes(items):
    print('\n'.join(
        [
            "%s: --> %s" % (number, item)
            for number, item in
            zip(
                range(len(items)),
                items
            )
        ]
    ))

home_path = os.environ['HOME']
inventory_script = os.path.join(home_path, '.scripts/ssh_by_role/inventory.py')

parser = argparse.ArgumentParser()
parser.add_argument('word')
parser.add_argument('--no-ssh', action='store_true', help="won't ssh just print out the host dns")
parser.add_argument('--tag', default="role", help="what EC2 tag to search")
parser.add_argument('--ssh-key', default="~/.ssh/keypair.pem", help="path to the ssh key")
parser.add_argument('--remote-user-name', default='ubuntu', help="the remote machine user name")
parser.add_argument('--inventory-script', default=inventory_script, help="path to EC2 inventory script")

args = parser.parse_args()

command = [args.inventory_script, '--tag-name', args.tag]
run_inventory = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
string_inventory, error= run_inventory.communicate('S\nL\n')
inventory = json.loads(string_inventory.decode('utf-8'))

tags = list(filter(lambda role: args.word in role, inventory.keys()))

print_with_indexes(tags)

print('enter number of %s (defualt 0):' % args.tag)
index = input()
index = int(index) if index else 0

tag = tags[index]

hosts = inventory[tag].get('hosts')
host = hosts[0]

if not args.no_ssh:
    os.system('ssh -i %s %s@%s' % (args.ssh_key, args.remote_user_name, host))
else:
    print(host)
