#!/usr/bin/env python
from paramiko import (AuthenticationException, AutoAddPolicy,
                      BadHostKeyException, SSHException)
from paramiko.client import SSHClient


def main():
    try:
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy)
        client.connect("localhost", port=31042,
                       username="admin", password="passwd")
    except (BadHostKeyException, AuthenticationException,
            SSHException):
        return 1
    return 0


if __name__ == '__main__':
    exit(main())
