# 2017.08.29 21:58:59 St�edn� Evropa (letn� �as)
# Embedded file name: scripts/common/Lib/plat-os2emx/grp.py
"""Replacement for grp standard extension module, intended for use on
OS/2 and similar systems which don't normally have an /etc/group file.

The standard Unix group database is an ASCII text file with 4 fields per
record (line), separated by a colon:
  - group name (string)
  - group password (optional encrypted string)
  - group id (integer)
  - group members (comma delimited list of userids, with no spaces)

Note that members are only included in the group file for groups that
aren't their primary groups.
(see the section 8.2 of the Python Library Reference)

This implementation differs from the standard Unix implementation by
allowing use of the platform's native path separator character - ';' on OS/2,
DOS and MS-Windows - as the field separator in addition to the Unix
standard ":".

The module looks for the group database at the following locations
(in order first to last):
  - ${ETC_GROUP}              (or %ETC_GROUP%)
  - ${ETC}/group              (or %ETC%/group)
  - ${PYTHONHOME}/Etc/group   (or %PYTHONHOME%/Etc/group)

Classes
-------

None

Functions
---------

getgrgid(gid) -  return the record for group-id gid as a 4-tuple

getgrnam(name) - return the record for group 'name' as a 4-tuple

getgrall() -     return a list of 4-tuples, each tuple being one record
                 (NOTE: the order is arbitrary)

Attributes
----------

group_file -     the path of the group database file

"""
import os
__group_path = []
if os.environ.has_key('ETC_GROUP'):
    __group_path.append(os.environ['ETC_GROUP'])
if os.environ.has_key('ETC'):
    __group_path.append('%s/group' % os.environ['ETC'])
if os.environ.has_key('PYTHONHOME'):
    __group_path.append('%s/Etc/group' % os.environ['PYTHONHOME'])
group_file = None
for __i in __group_path:
    try:
        __f = open(__i, 'r')
        __f.close()
        group_file = __i
        break
    except:
        pass

__field_sep = [':']
if os.pathsep:
    if os.pathsep != ':':
        __field_sep.append(os.pathsep)

def __get_field_sep(record):
    fs = None
    for c in __field_sep:
        if record.count(c) == 3:
            fs = c
            break

    if fs:
        return fs
    else:
        raise KeyError, '>> group database fields not delimited <<'
        return


class Group:

    def __init__(self, name, passwd, gid, mem):
        self.__dict__['gr_name'] = name
        self.__dict__['gr_passwd'] = passwd
        self.__dict__['gr_gid'] = gid
        self.__dict__['gr_mem'] = mem
        self.__dict__['_record'] = (self.gr_name,
         self.gr_passwd,
         self.gr_gid,
         self.gr_mem)

    def __len__(self):
        return 4

    def __getitem__(self, key):
        return self._record[key]

    def __setattr__(self, name, value):
        raise AttributeError('attribute read-only: %s' % name)

    def __repr__(self):
        return str(self._record)

    def __cmp__(self, other):
        this = str(self._record)
        if this == other:
            return 0
        elif this < other:
            return -1
        else:
            return 1


def __read_group_file():
    if group_file:
        group = open(group_file, 'r')
    else:
        raise KeyError, '>> no group database <<'
    gidx = {}
    namx = {}
    sep = None
    while 1:
        entry = group.readline().strip()
        if len(entry) > 3:
            if sep is None:
                sep = __get_field_sep(entry)
            fields = entry.split(sep)
            fields[2] = int(fields[2])
            fields[3] = [ f.strip() for f in fields[3].split(',') ]
            record = Group(*fields)
            if not gidx.has_key(fields[2]):
                gidx[fields[2]] = record
            if not namx.has_key(fields[0]):
                namx[fields[0]] = record
        elif len(entry) > 0:
            pass
        else:
            break

    group.close()
    if len(gidx) == 0:
        raise KeyError
    return (gidx, namx)


def getgrgid(gid):
    g, n = __read_group_file()
    return g[gid]


def getgrnam(name):
    g, n = __read_group_file()
    return n[name]


def getgrall():
    g, n = __read_group_file()
    return g.values()


if __name__ == '__main__':
    getgrall()
# okay decompyling c:\Users\PC\wotmods\files\originals\res\packages\scripts\scripts\common\Lib\plat-os2emx\grp.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2017.08.29 21:58:59 St�edn� Evropa (letn� �as)
