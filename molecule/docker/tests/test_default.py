# flake8: noqa
import json
import urllib
import os

import testinfra.utils.ansible_runner

RUNNER = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE'])

testinfra_hosts = RUNNER.get_hosts('all')

def test_check_open(host):
    host.run('docker rm -f test')
    assert host.run('docker run -p 80:80 -d --name test nginxdemos/hello:plain-text').rc == 0
    host.run('docker rm -f test')
    # TODO extend verify

def test_rules(host):
    cmd = host.run('iptables -L -n')
    assert cmd.rc == 0
    # TODO improve checks
    assert 'DOCKER' in cmd.stdout.strip()