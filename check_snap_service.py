#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" 
    Icinga plugin to check snap services 

    Version 1.0

    Copyright 2018 Florian Köttner

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""

import argparse
import subprocess
import sys

class Snap_service:
    def __init__(self, servicename):
        self.servicename = servicename

    def check(self):
        exitcode = 0
        exitheader = ""
        exitbody = ""

        process = subprocess.Popen(
            [
                '/usr/bin/snap',
                'services',
                self.servicename,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        stdout, stderr = process.communicate()
        if stderr:
            exitcode = 3
            exitheader = 'UNKNOWN - error while executing'
            exitbody = stderr
        else:
            for line in stdout.splitlines()[1:]:
                linevalues = line.split()
                if linevalues[2] != 'active':
                    if exitcode == 0:
                        # something is wrong
                        exitheader = 'CRITICAL - service {0} is not active'.format(linevalues[0])
                        exitcode = 2
                    else:
                        # multiple things are wrong
                        exitheader = 'CRITICAL - multiple services are not active'

            # everything ok
            if exitcode == 0:
                exitheader = 'OK - service {0} is active'.format(self.servicename)
            exitbody = stdout

        print(exitheader)
        print(exitbody)
        return exitcode

def main():
    argp = argparse.ArgumentParser(description=__doc__,
                      formatter_class=argparse.RawTextHelpFormatter,
    )
    argp.add_argument(
        '--service',
        required=True,
        help='Check this service(s)',
    )
    args = argp.parse_args()

    checker = Snap_service(servicename=args.service)
    exitcode = checker.check()
    sys.exit(exitcode)



if __name__ == '__main__':
    main()
