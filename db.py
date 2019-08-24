#! /usr/bin/python3

from enum import Enum


class Material(Enum):
    PLASTIC = 'plastic'
    METAL = 'metal'


class PaintScheme(Enum):
    UNPAINTED = 'unpainted'
    WOLF_FROM_EBAY = 'wolf_from_ebay'
    GREEN_AND_BLACK_GENCON_2018 = 'green_and_black_gencon_2018'


class Built(Enum):
    YES = 'yes'
    NO = 'NO'


class Error(Exception):
    pass


class Miniature(object):
    def __init__(self, material=None, paint=None, built=None):
        if material is None:
            raise Error('material must be specified')
        self.material = material

        if paint is None:
            raise Error('paint must be specified')
        self.paint = paint

        if built is None:
            raise Error('built must be specified')
        self.built = built

        # Will be set by MiniatureDB later.
        self.kind = None
        self.key = None

    def __str__(self):
        parts = [
            ('kind', '"%s"' % self.kind),
            ('key', self.key),
            ('material', '%s' % self.material),
            ('paint', '%s' % self.paint),
            ('built', '%s' % self.built),
        ]
        parts_strs = ['%s: %s' % x for x in parts]
        return "{ %s }" % '\t'.join(parts_strs)


def _ToSnakeCase(camel_case):
    out = []
    for char in camel_case:
        if char.upper() == char:
            if len(out) > 0:
                out.append('_')
            out.append(char.lower())
        else:
            out.append(char)
    return ''.join(out)


class MiniatureDB(object):
    def MakeMadCat():
        yield Miniature(  # 0
            material=Material.METAL,
            paint=PaintScheme.UNPAINTED,
            built=Built.NO)
        yield Miniature(  # 1
            material=Material.METAL,
            paint=PaintScheme.GREEN_AND_BLACK_GENCON_2018,
            built=Built.YES)

    def MakeVulture():
        yield Miniature(  # 0
            material=Material.METAL,
            paint=PaintScheme.UNPAINTED,
            built=Built.NO)

    def __init__(self):
        self._minis = []
        maker_prefix = 'Make'
        for make_name, make_method in [x for x in MiniatureDB.__dict__.items() if x[0].startswith(maker_prefix)]:
            kind = _ToSnakeCase(make_name[len(maker_prefix):])
            index = 0
            for mini in make_method():
                mini.kind = kind
                mini.key = '%s_%d' % (kind, index)
                self._minis.append(mini)
                self.__dict__[mini.key] = mini
                index += 1


minis = MiniatureDB()
print(minis.mad_cat_0)
print(minis.mad_cat_1)
print(minis.vulture_0)
