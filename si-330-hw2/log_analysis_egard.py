__author__ = 'emmagardiner'
# -*- coding: utf-8 -*-
#!/usr/bin/python -tt

# SI 330 HW 2 Filtering text files with regular expressions
#
# Your goal is to create two files:
#
# (a) A summary file that contains the counts of all valid daily visits to each top-level domain.
# The rows should be ordered in chronological order, and the columns should be sorted in alphabetical
# order of top-level domains.  The file should be tab-delimited.
#
# (b) A ‘suspicious entries’ file with the actual invalid access rows filtered from the original log,
# according to the criteria below

# For example, this line in the log counts as a valid visit to the ‘hu’ top-level domain.
#
# 195.82.31.125 - - [09/Mar/2004:22:03:09 -0500] "GET http://www.goldengate.hu/cgi-bin/top/topsites.cgi?an12 HTTP/1.0" 200 558 "http://Afrique" "Mozilla/4.0 (compatible; MSIE 5.5; Windows 98)"
#
# The 'hu' part in the hostname www.goldengate.hu is the top-level domain (representing the country of Hungary).
# The status code of '200' tells us that the visit was successful. So the line should be counted as a valid visit
# for the 'hu' domain on 09/Mar/2004.  Note that the top-level domain for a hostname like www.cocegas.com.br
# (Links to an external site.) is .br, not .com.
#
# Use the following rules to determine if a line should be as a valid line.  A line in the log file represents
# a valid visit only if these conditions are true:
#
# (1) The HTTP verb is GET or POST
# (2) AND the status code is 200
# (3) AND the URL being accessed starts with http:// or https://, followed by one or more alphabetic characters
# (i.e. not a digit or a symbol). For example, the URL should NOT start with 'http:///', which is an error.
# (4) AND the top-level domain consists of only letters. This is to say, if the host name is actually
# a numerical IP address like '202.96.254.200', we don’t count it. If the whole domain name is just '.com' as in
# http://.com/blah or does not even contain a dot as in http://c/blah, we do not count it.
# (5) AND the URL does not specify a username or password, i.e. it is not of the following form -
# http://user:password@www.example.com (Links to an external site.).
# An example of this would be - GET http://z0z0n1:XXXXXXXX@www.amkingdom.com/protected/mea1x.htm HTTP/1.0"
#
# As an example, note that we do not count lines like the following as valid:
#
# 68.48.142.117 - - [09/Mar/2004:22:41:42 -0500] "GET /scripts/..%c1%9c../winnt/system32/cmd.exe?/c+dir HTTP/1.0" 200 566 "-" "-"
#
# This is because /scripts/ obviously doesn't look like a web address since it does not start with http:// or https:// )
# This is a prime example of an attempt to get a file stored locally on that proxy server to exploit vulnerabilities.
#
# Important Details (to check after getting your basic code working):
#
# Be aware that some rows use multiple spaces as a separator between fields, so make sure to use [\s]+
# if you split the line’s fields using whitespace (and not just [\s]).
# Be sure to handle the case where the hostname part of the URL contains a port number delimited by a colon,
# i.e. like 'abcde.com:8080', the 8080 part is called the port number. The port number is not part of the
# top-level domain and should be ignored: The top-level domain of 'abcde.com:8080' should be counted as 'com'.
# You should convert case-sensitive variants of top-level domain strings like ‘CoM’ or ‘cOm’ into the
# lower-case version (‘com’).
# A small number of valid lines are missing the ‘HTTP/1.x’ after the URL and just have the three-digit
# HTTP status code. So having the HTTP/1.x field after the URL is not a requirement to have a valid line.

import re

#access_log_file = open('access_log_first1000_lines.txt', 'r')

#re.findall(r'.*[^"](GET|POST)[\s]+(http://|https://)\w+.', )

#^https?://\w.*?\.(\w+)[^/]$'

def get_toplevel_domain(url):
    match = re.search(r'http[s]?://[a-zA-Z][^/:]+\.([a-zA-Z]+)[/:]?', url)# your code: some re call with a regular expression
    if match == None:
        return None
    return match.group(1) # your code: the match string (in lowercase)

#x = '195.82.31.125 - - [09/Mar/2004:22:03:15 -0500] "GET http://toplist.goldengate.hu/ HTTP/1.0" 200 992 "http://www.goldengate.hu/cgi-bin/top/topsites.cgi?an12" "Mozilla/4.0 (compatible; MSIE 5.5; Windows 98)"'

#print get_toplevel_domain(x)

#f = open('access_log_first1000_lines.txt', 'rU')
#for line in f:
#    print get_toplevel_domain(line)

def read_log_file(filename):
    valid_entries = []
    invalid_entries = []

    f = open(filename, 'rU')
    for line in f:
        line = line.strip()

        # extract fields
        fields = re.split(r'\s+', line)

        # extract URL
        # extract toplevel_domain from URL
        for x in fields:
            url = re.search(r'http[s]?://[a-zA-Z][^/:]+\.[a-zA-Z]+', x)
            if url == None:
                continue
            else:
                TLD = get_toplevel_domain(url.group().lower())
        #print fields

        # check for missing HTTP version
        # ???????

        # extract valid date
        for x in fields:
            search = re.search(r'([0-9]{2}/[a-zA-Z]{3}/[1-9]{1}[0-9]{3})', x)
            if search == None:
                continue
            else:
                date = search.group()

        # form record: date, TLD, line

        record = [date, TLD, line]
        #print record

        # checks:

        #verb must be GET or POST
        verb = re.match(r'["](GET|POST)', fields[5])

        status = re.match(r'200', fields[8])

        http = re.match(r'http[s]?://', fields[6])

        if verb == None or status == None or http == None:
            invalid_entries.append(record)
        else:
            valid_entries.append(record)
        # if any of these tests fail
        #   append the line to the invalid list and continue
        #    invalid_entries.append(record)
        #    continue

        # otherwise if we get here, it's a valid record

    f.close()
    # for line in invalid_entries:
    #     print line
    return (valid_entries, invalid_entries)

#read_log_file('access_log_first1000_lines.txt')

valid_rows, invalid_rows = read_log_file(r'access_log.txt')

dict = {}
for r in valid_rows:
    date = r[0]
    TLD = r[1]
    if date in dict:
        if TLD in dict[date]:
            dict[date][TLD] += 1
        else:
            dict[date][TLD] = 1
    else:
        dict[date] = {TLD: 1}


f = open('valid_log_summary_egard.txt', 'w')
for key in sorted(dict.keys()):
    i = dict[key]
    f.write(key)
    f.write("\t")
    for k in sorted(i.keys()):
        h = i[k]
        f.write(k + ":" + str(h))
        f.write("\t")
    f.write("\n")

f.close()

f = open('invalid_access_log_egard.txt', 'w')
for r in invalid_rows:
    r.remove(r[0])
    r.remove(r[0])
    f.write(str(r))
    f.write("\n")
f.close()