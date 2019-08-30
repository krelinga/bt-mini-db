def _FormatNumber(x):
    if x is None:
        return '-'
    return '%d' % x


AMS = 'AMS'


CASE = 'CASE'


def IF(num):
    return 'IF%d' % num


def LRM(s, m, l):
    return 'LRM%s/%s/%s' % (_FormatNumber(s), _FormatNumber(m), _FormatNumber(l))


LTAG = 'LTAG'


OMNI = 'OMNI'


OVL = 'OVL'


def REAR(s, m, l):
    return 'REAR%s/%s/%s' % (_FormatNumber(s), _FormatNumber(m), _FormatNumber(l))


def SRM(s, m):
    return 'SRM%s/%s' % (_FormatNumber(s), _FormatNumber(m))
