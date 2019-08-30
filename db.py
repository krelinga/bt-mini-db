#! /usr/bin/python3

from enum import Enum


class Material(Enum):
    PLASTIC = 'plastic'
    METAL = 'metal'


class PaintScheme(Enum):
    UNPAINTED = 'unpainted'
    WOLF_FROM_EBAY = 'wolf_from_ebay'
    GREEN_AND_BLACK_GENCON_2018 = 'green_and_black_gencon_2018'
    RED_BASIC = 'red_basic'


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
    def MakeAtlas():
        yield Miniature(  # 0
            material=Material.PLASTIC,
            paint=PaintScheme.RED_BASIC,
            built=Built.YES)

    def MakeMadCat():
        yield Miniature(  # 0
            material=Material.METAL,
            paint=PaintScheme.UNPAINTED,
            built=Built.NO)
        yield Miniature(  # 1
            material=Material.METAL,
            paint=PaintScheme.GREEN_AND_BLACK_GENCON_2018,
            built=Built.YES)

    def MakeRaven():
        yield Miniature(  # 0
            material=Material.PLASTIC,
            paint=PaintScheme.UNPAINTED,
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
print(minis.atlas_0)
print(minis.raven_0)


def _FormatOrNone(fmt, value):
    if value is None:
        return None
    return fmt % value


class AlphaStrikeUnitType(Enum):
    BATTLEMECH = 'bm'


class AlphaStrikeUnitTemplate(object):
    def __init__(self, template=None, name=None, model=None, pv=None, tp=None,
                 sz=None, mv=None, mvj=None, role=None, ds=None, dm=None,
                 dl=None, de=None, ov=None, a=None, s=None, specials=None):
        self._template = template

        self._name = name
        self._model = model
        self._pv = pv
        self._tp = tp
        self._sz = sz
        self._mv = mv
        self._mvj = mvj
        self._role = role
        self._ds = ds
#        if dm is not None:
#            self.dm = dm
#        if dl is not None:
#            self.dl = dl
#        if de is not None:
#            self.de = de
#        if ov is not None:
#            self.ov = ov
#        if a is not None:
#            self.a = a
#        if s is not None:
#            self.s = s
#        if specials is not None:
#            self.specials = specials

    def _resolve(self, prop):
        self_val = self.__dict__.get(prop)
        if self_val is not None:
            return self_val
        if self._template is None:
            return None
        return self._template.__dict__.get(prop)

    @property
    def name(self):
        return self._resolve('_name')

    @property
    def model(self):
        return self._resolve('_model')

    @property
    def pv(self):
        return self._resolve('_pv')

    @property
    def tp(self):
        return self._resolve('_tp')

    @property
    def sz(self):
        return self._resolve('_sz')

    @property
    def mv(self):
        return self._resolve('_mv')

    @property
    def mvj(self):
        evaluated = self._resolve('_mvj')
        if evaluated is not None:
            return evaluated
        return 0

    @property
    def role(self):
        return self._resolve('_role')

    @property
    def ds(self):
        return self._resolve('_ds')

    def __str__(self):
        parts = [
            ('name', '"%s"'),
            ('model', '"%s"'),
            ('pv', '%d'),
            ('tp', '%s'),
            ('sz', '%d'),
            ('mv', '%d'),
            ('mvj', '%d'),
            ('role', '%s'),
            ('ds', '%d'),
        ]
        parts_strs = ['%s: %s' % (x[0], _FormatOrNone(x[1], self.__getattribute__(x[0]))) for x in parts]
        return "{ %s }" % '\t'.join(parts_strs)


class AlphaStrikeUnit(AlphaStrikeUnitTemplate):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.name is None:
            raise Error('name must be specified')
        if self.model is None:
            raise Error('model must be specified')
        if self.pv is None:
            raise Error('pv must be specified')
        if self.tp is None or type(self.tp) is not AlphaStrikeUnitType:
            raise Error('tp must be specified and must be of type AlphaStrikeUnitType')
        if self.sz is None:
            raise Error('sz must be specified')
        if self.mv is None:
            raise Error('mv must be specified')
        # self.mvj can be None, it has a default value.
        # self.role can be None, it isn't required.  Or ... even supported for now ;-).
        # self.ds can be None, which would mean no damage in that range bracket.


mad_cat_tmpl = AlphaStrikeUnitTemplate(name="Mad Cat", tp=AlphaStrikeUnitType.BATTLEMECH, sz=3, mv=10)
print('%s' % mad_cat_tmpl)
mad_cat_unit = AlphaStrikeUnit(template=mad_cat_tmpl, model='Prime', pv=54, ds=5)
print('%s' % mad_cat_unit)
