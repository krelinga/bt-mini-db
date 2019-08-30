#! /usr/bin/python3

from enum import Enum


import specials


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
                 dl=None, de=None, ov=None, a=None, s=None, specials=()):
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
        self._dm = dm
        self._dl = dl
        self._de = de
        self._ov = ov
        self._a = a
        self._s = s
        self._specials = specials

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

    @property
    def dm(self):
        return self._resolve('_dm')

    @property
    def dl(self):
        return self._resolve('_dl')

    @property
    def de(self):
        return self._resolve('_de')

    @property
    def ov(self):
        evaluated = self._resolve('_ov')
        if evaluated is not None:
            return evaluated
        return 0

    @property
    def a(self):
        return self._resolve('_a')

    @property
    def s(self):
        return self._resolve('_s')

    @property
    def specials(self):
        found = []
        if self._template is not None:
            found.extend(self._template._specials)
        if self._specials is not None:
            found.extend(self._specials)
        return found

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
            ('dm', '%d'),
            ('dl', '%d'),
            ('de', '%d'),
            ('ov', '%d'),
            ('a', '%d'),
            ('s', '%d'),
            ('specials', '%s'),
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
        # self.dm can be None, which would mean no damage in that range bracket.
        # self.dl can be None, which would mean no damage in that range bracket.
        # self.de can be None, which would mean no damage in that range bracket.
        # self.ov can be None, it has a default value.
        if self.a is None:
            raise Error('a must be specified')
        if self.s is None:
            raise Error('s must be specified')
        # self.specials can be None, it has a default value.


mad_cat_tmpl = AlphaStrikeUnitTemplate(name="Mad Cat", tp=AlphaStrikeUnitType.BATTLEMECH, sz=3, mv=10, a=8, s=4, specials=(specials.CASE, specials.OMNI))
print('%s' % mad_cat_tmpl)
mad_cat_unit = AlphaStrikeUnit(template=mad_cat_tmpl, model='Prime', pv=54, ds=5, dm=5, dl=4, ov=1, specials=(specials.IF(2), specials.LRM(1,1,2)))
print('%s' % mad_cat_unit)
print('%s' % AlphaStrikeUnit(template=mad_cat_tmpl, model='A', pv=59, ds=7, dm=7, dl=3, ov=1))
print('%s' % AlphaStrikeUnit(template=mad_cat_tmpl, model='B', pv=48, ds=4, dm=4, dl=4, specials=(specials.IF(1), )))
print('%s' % AlphaStrikeUnit(template=mad_cat_tmpl, model='C', pv=50, ds=4, dm=4, dl=4, specials=(specials.AMS, specials.IF(1), specials.LRM(1,1,1), specials.OVL)))
print('%s' % AlphaStrikeUnit(template=mad_cat_tmpl, model='D', pv=51, ds=5, dm=5, dl=3, specials=(specials.REAR(2, 2, None), )))
print('%s' % AlphaStrikeUnit(template=mad_cat_tmpl, model='E', pv=53, ds=7, dm=5, dl=4, specials=(specials.LTAG, )))
print('%s' % AlphaStrikeUnit(template=mad_cat_tmpl, model='F', pv=54, ds=5, dm=5, dl=4, ov=2, specials=(specials.IF(2), specials.LRM(1,1,2))))
print('%s' % AlphaStrikeUnit(template=mad_cat_tmpl, model='H', pv=59, ds=6, dm=6, dl=4, ov=1, specials=(specials.IF(3), )))
print('%s' % AlphaStrikeUnit(template=mad_cat_tmpl, model='S', pv=54, ds=6, dm=6, dl=2, ov=1, specials=(specials.SRM(3, 3), )))
