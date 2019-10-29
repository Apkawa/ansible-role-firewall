# flake8: noqa
import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_rules(host):
    cmd = host.run('iptables -L -n')
    assert cmd.rc == 0
    assert cmd.stdout.strip() == """
Chain INPUT (policy ACCEPT)
target     prot opt source               destination         
ACCEPT     all  --  0.0.0.0/0            0.0.0.0/0           
ACCEPT     icmp --  0.0.0.0/0            0.0.0.0/0           
ACCEPT     udp  --  0.0.0.0/0            0.0.0.0/0            udp spt:123
ACCEPT     tcp  --  0.0.0.0/0            0.0.0.0/0            tcp dpt:9123
ACCEPT     tcp  --  8.8.8.8              0.0.0.0/0            tcp dpt:1042
DROP       tcp  --  0.0.0.0/0            0.0.0.0/0            tcp dpt:1042
ACCEPT     tcp  --  10.0.0.0/24          0.0.0.0/0            tcp dpt:1043
ACCEPT     tcp  --  10.0.0.0/24          0.0.0.0/0            tcp dpt:1043
DROP       tcp  --  10.0.0.0/24          0.0.0.0/0            tcp dpt:1043
ACCEPT     tcp  --  10.0.0.1             0.0.0.0/0            tcp dpt:1044
DROP       tcp  --  10.0.0.0/24          0.0.0.0/0            tcp dpt:1044
ACCEPT     udp  --  0.0.0.0/0            0.0.0.0/0            udp dpt:9123
ACCEPT     udp  --  8.8.8.8              0.0.0.0/0            udp dpt:1042
DROP       udp  --  0.0.0.0/0            0.0.0.0/0            udp dpt:1042
ACCEPT     udp  --  10.0.0.0/24          0.0.0.0/0            udp dpt:1043
ACCEPT     udp  --  10.0.0.0/24          0.0.0.0/0            udp dpt:1043
DROP       udp  --  10.0.0.0/24          0.0.0.0/0            udp dpt:1043
ACCEPT     udp  --  10.0.0.1             0.0.0.0/0            udp dpt:1044
DROP       udp  --  10.0.0.0/24          0.0.0.0/0            udp dpt:1044
ACCEPT     all  --  0.0.0.0/0            0.0.0.0/0            state RELATED,ESTABLISHED
LOG        all  --  0.0.0.0/0            0.0.0.0/0            limit: avg 15/min burst 5 LOG flags 0 level 7 prefix "Dropped by firewall: "
DROP       all  --  0.0.0.0/0            0.0.0.0/0           

Chain FORWARD (policy ACCEPT)
target     prot opt source               destination         

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination         
ACCEPT     udp  --  0.0.0.0/0            0.0.0.0/0            udp dpt:123

Chain DOCKER-USER (0 references)
target     prot opt source               destination         

Chain FILTERS (0 references)
target     prot opt source               destination   
""".strip()
