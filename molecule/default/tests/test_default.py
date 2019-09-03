# flake8: noqa
import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_rules(host):
    cmd = host.run('iptables -L')
    assert cmd.rc == 0
    assert cmd.stdout.strip() == """
Chain INPUT (policy ACCEPT)
target     prot opt source               destination         
ACCEPT     all  --  anywhere             anywhere            
ACCEPT     tcp  --  anywhere             anywhere             tcp dpt:grcp
ACCEPT     tcp  --  dns.google           anywhere             tcp dpt:afrog
DROP       tcp  --  anywhere             anywhere             tcp dpt:afrog
ACCEPT     tcp  --  10.0.0.0/24          anywhere             tcp dpt:boinc-client
ACCEPT     tcp  --  10.0.0.0/24          anywhere             tcp dpt:boinc-client
DROP       tcp  --  10.0.0.0/24          anywhere             tcp dpt:boinc-client
ACCEPT     tcp  --  10.0.0.1             anywhere             tcp dpt:dcutility
DROP       tcp  --  10.0.0.0/24          anywhere             tcp dpt:dcutility
ACCEPT     udp  --  anywhere             anywhere             udp dpt:9123
ACCEPT     udp  --  dns.google           anywhere             udp dpt:afrog
DROP       udp  --  anywhere             anywhere             udp dpt:afrog
ACCEPT     udp  --  10.0.0.0/24          anywhere             udp dpt:boinc-client
ACCEPT     udp  --  10.0.0.0/24          anywhere             udp dpt:boinc-client
DROP       udp  --  10.0.0.0/24          anywhere             udp dpt:boinc-client
ACCEPT     udp  --  10.0.0.1             anywhere             udp dpt:dcutility
DROP       udp  --  10.0.0.0/24          anywhere             udp dpt:dcutility
ACCEPT     icmp --  anywhere             anywhere            
ACCEPT     udp  --  anywhere             anywhere             udp spt:ntp
ACCEPT     all  --  anywhere             anywhere             state RELATED,ESTABLISHED
LOG        all  --  anywhere             anywhere             limit: avg 15/min burst 5 LOG level debug prefix "Dropped by firewall: "
DROP       all  --  anywhere             anywhere            

Chain FORWARD (policy ACCEPT)
target     prot opt source               destination         

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination         
ACCEPT     udp  --  anywhere             anywhere             udp dpt:ntp
""".strip()
