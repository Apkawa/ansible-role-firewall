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
    assert host.run('docker run --rm --net=host busybox nc -zvw 1 127.0.0.1 80').rc == 0
    host.run('docker rm -f test')
    # TODO extend verify


def test_rules(host):
    cmd = host.run('iptables -L -n')
    assert cmd.rc == 0
    # TODO improve checks
    assert 'DOCKER' in cmd.stdout.strip()


def test_docker(host):
    cmd = host.run('docker run --rm busybox ping -c 1 -q 8.8.8.8')
    assert cmd.rc == 0, cmd.stdout


def test_access_from_docker_to_host_port(host):
    host.run('docker rm -f echo echo_http')
    assert host.run(
        'docker run --rm -e TCP_PORT=2701 -p 2777:2701 -d --name echo cjimti/go-echo').rc == 0
    assert host.run('docker run --rm busybox nc -zvw 1 172.18.0.1 2777').rc == 0
    host.run('docker rm -f echo echo_http')
