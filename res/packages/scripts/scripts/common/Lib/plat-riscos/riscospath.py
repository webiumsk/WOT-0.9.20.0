# 2017.08.29 21:59:00 St�edn� Evropa (letn� �as)
# Embedded file name: scripts/common/Lib/plat-riscos/riscospath.py
"""
Instead of importing this module directly, import os and refer to this module
as os.path.
"""
curdir = '@'
pardir = '^'
extsep = '/'
sep = '.'
pathsep = ','
defpath = '<Run$Dir>'
altsep = None
import os, stat, string
try:
    import swi
except ImportError:

    class _swi:

        def swi(*a):
            raise AttributeError, 'This function only available under RISC OS'

        block = swi


    swi = _swi()

_false, _true = range(2)
_roots = ['$',
 '&',
 '%',
 '@',
 '\\']
_allowMOSFSNames = _false

def _split(p):
    """
    split filing system name (including special field) and drive specifier from rest
    of path. This is needed by many riscospath functions.
    """
    dash = _allowMOSFSNames and p[:1] == '-'
    if dash:
        q = string.find(p, '-', 1) + 1
    elif p[:1] == ':':
        q = 0
    else:
        q = string.find(p, ':') + 1
    s = string.find(p, '#')
    if s == -1 or s > q:
        s = q
    else:
        for c in p[dash:s]:
            if c not in string.ascii_letters:
                q = 0
                break

    r = q
    if p[q:q + 1] == ':':
        r = string.find(p, '.', q + 1) + 1
        if r == 0:
            r = len(p)
    return (p[:q], p[q:r], p[r:])


def normcase(p):
    """
    Normalize the case of a pathname. This converts to lowercase as the native RISC
    OS filesystems are case-insensitive. However, not all filesystems have to be,
    and there's no simple way to find out what type an FS is argh.
    """
    return string.lower(p)


def isabs(p):
    """
    Return whether a path is absolute. Under RISC OS, a file system specifier does
    not make a path absolute, but a drive name or number does, and so does using the
    symbol for root, URD, library, CSD or PSD. This means it is perfectly possible
    to have an "absolute" URL dependent on the current working directory, and
    equally you can have a "relative" URL that's on a completely different device to
    the current one argh.
    """
    fs, drive, path = _split(p)
    return drive != '' or path[:1] in _roots


def join(a, *p):
    """
    Join path elements with the directory separator, replacing the entire path when
    an absolute or FS-changing path part is found.
    """
    j = a
    for b in p:
        fs, drive, path = _split(b)
        if j == '' or fs != '' or drive != '' or path[:1] in _roots:
            j = b
        elif j[-1] == ':':
            j = j + b
        else:
            j = j + '.' + b

    return j


def split(p):
    """
    Split a path in head (everything up to the last '.') and tail (the rest). FS
    name must still be dealt with separately since special field may contain '.'.
    """
    fs, drive, path = _split(p)
    q = string.rfind(path, '.')
    if q != -1:
        return (fs + drive + path[:q], path[q + 1:])
    return ('', p)


def splitext(p):
    """
    Split a path in root and extension. This assumes the 'using slash for dot and
    dot for slash with foreign files' convention common in RISC OS is in force.
    """
    tail, head = split(p)
    if '/' in head:
        q = len(head) - string.rfind(head, '/')
        return (p[:-q], p[-q:])
    return (p, '')


def splitdrive(p):
    """
    Split a pathname into a drive specification (including FS name) and the rest of
    the path. The terminating dot of the drive name is included in the drive
    specification.
    """
    fs, drive, path = _split(p)
    return (fs + drive, p)


def basename(p):
    """
    Return the tail (basename) part of a path.
    """
    return split(p)[1]


def dirname(p):
    """
    Return the head (dirname) part of a path.
    """
    return split(p)[0]


def commonprefix(m):
    """Given a list of pathnames, returns the longest common leading component"""
    if not m:
        return ''
    s1 = min(m)
    s2 = max(m)
    n = min(len(s1), len(s2))
    for i in xrange(n):
        if s1[i] != s2[i]:
            return s1[:i]

    return s1[:n]


def getsize(p):
    """
    Return the size of a file, reported by os.stat().
    """
    st = os.stat(p)
    return st[stat.ST_SIZE]


def getmtime(p):
    """
    Return the last modification time of a file, reported by os.stat().
    """
    st = os.stat(p)
    return st[stat.ST_MTIME]


getatime = getmtime

def exists(p):
    """
    Test whether a path exists.
    """
    try:
        return swi.swi('OS_File', '5s;i', p) != 0
    except swi.error:
        return 0


lexists = exists

def isdir(p):
    """
    Is a path a directory? Includes image files.
    """
    try:
        return swi.swi('OS_File', '5s;i', p) in (2, 3)
    except swi.error:
        return 0


def isfile(p):
    """
    Test whether a path is a file, including image files.
    """
    try:
        return swi.swi('OS_File', '5s;i', p) in (1, 3)
    except swi.error:
        return 0


def islink(p):
    """
    RISC OS has no links or mounts.
    """
    return _false


ismount = islink

def samefile(fa, fb):
    """
    Test whether two pathnames reference the same actual file.
    """
    l = 512
    b = swi.block(l)
    swi.swi('OS_FSControl', 'isb..i', 37, fa, b, l)
    fa = b.ctrlstring()
    swi.swi('OS_FSControl', 'isb..i', 37, fb, b, l)
    fb = b.ctrlstring()
    return fa == fb


def sameopenfile(a, b):
    """
    Test whether two open file objects reference the same file.
    """
    return os.fstat(a)[stat.ST_INO] == os.fstat(b)[stat.ST_INO]


def expanduser(p):
    fs, drive, path = _split(p)
    l = 512
    b = swi.block(l)
    if path[:1] != '@':
        return p
    if fs == '':
        fsno = swi.swi('OS_Args', '00;i')
        swi.swi('OS_FSControl', 'iibi', 33, fsno, b, l)
        fsname = b.ctrlstring()
    else:
        if fs[:1] == '-':
            fsname = fs[1:-1]
        else:
            fsname = fs[:-1]
        fsname = string.split(fsname, '#', 1)[0]
    x = swi.swi('OS_FSControl', 'ib2s.i;.....i', 54, b, fsname, l)
    if x < l:
        urd = b.tostring(0, l - x - 1)
    else:
        x = swi.swi('OS_FSControl', 'ib0s.i;.....i', 54, b, fsname, l)
        if x < l:
            urd = b.tostring(0, l - x - 1)
        else:
            urd = '$'
    return fsname + ':' + urd + path[1:]


def expandvars(p):
    """
    Expand environment variables using OS_GSTrans.
    """
    l = 512
    b = swi.block(l)
    return b.tostring(0, swi.swi('OS_GSTrans', 'sbi;..i', p, b, l))


abspath = os.expand
realpath = abspath

def normpath(p):
    """
    Normalize path, eliminating up-directory ^s.
    """
    fs, drive, path = _split(p)
    rhs = ''
    ups = 0
    while path != '':
        path, el = split(path)
        if el == '^':
            ups = ups + 1
        elif ups > 0:
            ups = ups - 1
        elif rhs == '':
            rhs = el
        else:
            rhs = el + '.' + rhs

    while ups > 0:
        ups = ups - 1
        rhs = '^.' + rhs

    return fs + drive + rhs


def walk(top, func, arg):
    """Directory tree walk with callback function.
    
    For each directory in the directory tree rooted at top (including top
    itself, but excluding '.' and '..'), call func(arg, dirname, fnames).
    dirname is the name of the directory, and fnames a list of the names of
    the files and subdirectories in dirname (excluding '.' and '..').  func
    may modify the fnames list in-place (e.g. via del or slice assignment),
    and walk will only recurse into the subdirectories whose names remain in
    fnames; this can be used to implement a filter, or to impose a specific
    order of visiting.  No semantics are defined for, or required of, arg,
    beyond that arg is always passed to func.  It can be used, e.g., to pass
    a filename pattern, or a mutable object designed to accumulate
    statistics.  Passing None for arg is common."""
    try:
        names = os.listdir(top)
    except os.error:
        return

    func(arg, top, names)
    for name in names:
        name = join(top, name)
        if isdir(name) and not islink(name):
            walk(name, func, arg)
# okay decompyling c:\Users\PC\wotmods\files\originals\res\packages\scripts\scripts\common\Lib\plat-riscos\riscospath.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2017.08.29 21:59:00 St�edn� Evropa (letn� �as)
