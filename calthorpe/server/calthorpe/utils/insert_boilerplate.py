# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
# 
# Copyright (C) 2012 Calthorpe Associates
# 
# This program is free software: you can redistribute it and/or modify it under the terms of the
 # GNU General Public License as published by the Free Software Foundation, version 3 of the License.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
# 
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates.
# Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709.
# Phone: (510) 548-6800. Web: www.calthorpe.com

import glob
import sys, fileinput
import re

def pre_append(line, file_name):
    fobj = fileinput.FileInput(file_name, inplace=1)
    first_line = fobj.readline()
    sys.stdout.write("%s\n%s" % (line, first_line))
    for line in fobj:
        sys.stdout.write("%s" % line)
    fobj.close()

boilerplate_file = open('../LICENSE', 'r')
boilerplate = boilerplate_file.read()
boilerplate_file.close()
def sub_py(boilerplate):
    text = re.sub(r'^', '# ', boilerplate, 0, re.M)
    return re.sub(r'$', '\n', text, 1)
def sub_js(boilerplate):
    text = re.sub(r'^', '* ', boilerplate, 0, re.M)
    text = re.sub(r'^', '/* \n', text, 1)
    return re.sub(r'$', '\n */\n', text, 1)
def sub_html(boilerplate):
    text = re.sub(r'^', '<!-- \n', boilerplate, 1)
    return re.sub(r'$', '\n -->\n', text, 1)
format_dict =  {
    'py': sub_py(boilerplate),
    'js': sub_js(boilerplate),
    'css': sub_js(boilerplate),
    'html': sub_html(boilerplate)
}
for path in glob.glob(sys.argv[1]):
    ext = re.match(r'.*\.(\w+)$', path).group(1)
    if format_dict.get(ext):
        print path
        pre_append(format_dict[ext], path)
