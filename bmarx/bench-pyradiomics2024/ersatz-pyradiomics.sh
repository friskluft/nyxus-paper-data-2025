#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re
import sys
from radiomics.scripts.__init__ import parse_args
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(parse_args())

