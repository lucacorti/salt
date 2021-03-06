# -*- coding: utf-8 -*-

# Import python libs
from __future__ import absolute_import
import sys

# Import salt libs
from salt.utils.winservice import Service, instart
import salt
import salt.defaults.exitcodes

# Import third party libs
import win32serviceutil
import win32service
import winerror


class MinionService(Service):

    def start(self):
        self.runflag = True
        self.log("Starting the Salt Minion")
        minion = salt.Minion()
        minion.start()
        while self.runflag:
            pass
            #self.sleep(10)
            #self.log("I'm alive ...")

    def stop(self):
        self.runflag = False
        self.log("Shutting down the Salt Minion")


def _main():
    servicename = 'salt-minion'
    try:
        status = win32serviceutil.QueryServiceStatus(servicename)
    except win32service.error as details:
        if details[0] == winerror.ERROR_SERVICE_DOES_NOT_EXIST:
            instart(MinionService, servicename, 'Salt Minion')
            sys.exit(salt.defaults.exitcodes.EX_OK)
    if status[1] == win32service.SERVICE_RUNNING:
        win32serviceutil.StopServiceWithDeps(servicename)
        win32serviceutil.StartService(servicename)
    else:
        win32serviceutil.StartService(servicename)


if __name__ == '__main__':
    _main()
