#!/usr/bin/env python3

# Executable to run built-in tests.

warnings = []


def warning(text):
  global warnings
  import sys
  print("Warning:", text, file=sys.stderr)


def tofloat(x, suffixes=[]):
  """Convert a number or number-like string with suffix into float.

  tofloat("3.3k") => 3300.0
  tofloat("20µ") => 20.0e-6
  tofloat(2.2) => 2.2
  tofloat("3mV", ["V"]) => 0.003

  Only one unit suffix is allowed. Suffix is optional.

  Technically these are called SI prefixes, or metric prefixes. Because they are before the
  unit, like, "4 kV", k is a suffix of V. That is k is a unit prefix. That is kV is a unit itself,
  that is equal to 1000 V.

  Some SI unit prefix are intentinally not supported by this function and will
  raise an error. This is to reduce potential mistakes.

  No intervining spaces are allowed. i.e. "1.23 mV" or "1.1m V" will throw exception.
  This restriction might be relaxed (supported by emit a warning) to support
  importing components easier from other systems and formats.

  A leading and trailing spaces will produce a warning, but are supported (i.e. ignored without error).

  TODO: Support underscores, for long values, i.e. 13_512_101, but I doub't it that useful.

  TODO: Warn also about spaces between units and suffixes, i.e. "1.23 mV", or "1.1m V".
  """

  # TODO: Add resistance formats (2R2 = 2.2 Ohm)
  if type(x) is str:
    if x[0].isspace() or x[-1].isspace():
      warning("Leading or trailing whitespace detected in the number / value: '{}'. Please fix.".format(x))
      x = x.strip()
    for suffix in suffixes:
      if x.endswith(suffix):
        x = x[:-len(suffix)]
        break
    if x[-1].isdigit():  # No trailing suffix.
      return float(x)
    n = x[0:-1]
    # ordered for speed
    if x[-1] == "k":  # kilo
      return float(n) * 1.0e3
    if x[-1] == "m":  # milli
      return float(n) * 1.0e-3
    if x[-1] == "u" or x[-1] == "µ":  # micro
      return float(n) * 1.0e-6
    if x[-1] == "M":  # mega
      return float(n) * 1.0e6
    if x[-1] == "n":  # nano
      return float(n) * 1.0e-9
    if x[-1] == "p":  # pico
      return float(n) * 1.0e-12
    if x[-1] == "G":  # giga
      return float(n) * 1.0e9
    if x[-1] == "f":  # femto
      return float(n) * 1.0e-15
    if x[-1] == "a":  # atto
      warning("using atto SI prefix (a = 10^-18) could lead to mistakes. Maybe you meants A (Amperes)?")
      return float(n) * 1.0e-18
    if x[-1] == "T":  # tera
      return float(n) * 1.0e12
    if x[-1] == "z":  # zepto
      assert False, "zepto SI prefix (z = 10^-21) not supported"
    if x[-1] == "y":  # yocto
      assert False, "yocto SI prefix (y = 10^-24) not supported"
    if x[-1] == "Y":  # yotta
      assert False, "yotta SI prefix (Y = 10^23) not supported"
    if x[-1] == "Z":  # zetta
      assert False, "zetta SI prefix (Z = 10^21) not supported"
    if x[-1] == "E":  # exa
      assert False, "exa SI prefix (E = 10^18) not supported"
    if x[-1] == "P":  # peta
      assert False, "peta SI prefix (P = 10^15) not supported"
    if x[-1] == "h":  # hecto
      assert False, "hecto SI prefix (h = 10^2) not supported"
    if x[-1] == "d":  # deci
      assert False, "deci SI prefix (d = 10^-1) not supported"
    if x[-1] == "c":  # centi
      assert False, "centi SI prefix (d = 10^-2) not supported"
    assert False, "unknown suffix or format in tofloat('{}').".format(x)
  return float(x)


# TODO(baryluk): Add helper functions, i.e. nano(5), nano(3) * farad(), 3 * nF, 5 * kOhm, kOhm(5)

# import math
# isclose = lambda a, b: math.isclose(a, b, rel_tol=1e-12)

import unittest


class Test_tofloat(unittest.TestCase):
  def test_all(self):
    self.assertEqual(tofloat(5), 5.0)
    self.assertEqual(tofloat(4.1e-6), 4.1e-6)
    self.assertEqual(tofloat("5k"), 5e3)
    self.assertEqual(tofloat("4M"), 4e6)
    self.assertEqual(tofloat("4M", ["A"]), 4e6)
    self.assertEqual(tofloat("4MA", ["A"]), 4e6)
    self.assertAlmostEqual(tofloat("3.1m"), 3.1e-3)
    self.assertAlmostEqual(tofloat("3.2u"), 3.2e-6)
    self.assertAlmostEqual(tofloat("3.3µ"), 3.3e-6)
    self.assertAlmostEqual(tofloat("3.3µA", ["A"]), 3.3e-6)

    self.assertEqual(tofloat("2"), 2.0e0)
    self.assertEqual(tofloat("2m"), 2.0e-3)
    self.assertEqual(tofloat("2k"), 2.0e3)
    self.assertEqual(tofloat("2M"), 2.0e6)
    self.assertEqual(tofloat("2G"), 2.0e9)
    self.assertEqual(tofloat("2T"), 2.0e12)  # Rear to use, but does happen sometimes.
    self.assertEqual(tofloat("2m"), 2.0e-3)
    self.assertEqual(tofloat("2u"), 2.0e-6)
    self.assertEqual(tofloat("2u"), 2.0e-6)
    self.assertEqual(tofloat("2n"), 2.0e-9)
    self.assertEqual(tofloat("2p"), 2.0e-12)
    self.assertEqual(tofloat("2f"), 2.0e-15)
    # self.assertEqual(tofloat("2a"), 2.0e-18)  # Rear to use. 2aC, or 2aA, silly units a bit.

    with self.assertRaises(Exception):
      tofloat("2kV")  # unknown unit suffix

    with self.assertRaises(Exception):
      tofloat("3c")  # unknown multiplier suffix (centi in SI, but lets not support it)

    with self.assertRaises(Exception):
      tofloat("3e")  # unknown multiplier suffix (not in SI)

    # warns tofloat(" 1 ")
    # warns tofloat(" 3kOhm ")

    with self.assertRaises(Exception):
      tofloat("1.23 mV")
    with self.assertRaises(Exception):
      tofloat("1.1m V")
    with self.assertRaises(Exception):
      tofloat("3 V")
    with self.assertRaises(Exception):
      tofloat("31_123 C")


# Handy shortcuts for common units.
# Some of them can also perform unit conversion, i.e. from F to C, or from A*h to C.

def tofloat_R(x):
  return tofloat(x, ["Ohm", "R", "Ω"])


def tofloat_V(x):
  return tofloat(x, ["V"])


def tofloat_I(x):
  return tofloat(x, ["A", "C/s"])


def tofloat_C(x):
  return tofloat(x, ["F"])


def tofloat_L(x):
  return tofloat(x, ["H"])


def tofloat_P(x):
  return tofloat(x, ["P"])


def tofloat_Energy(x):
  return tofloat(x, ["Wh"])  # Ws, J  (1 J = 1 W*s = 1 N*m).


def tofloat_Charge(x):
  return tofloat(x, ["C", "As", "A*s", "A×s", "A⋅s"])  # Ah


def tofloat_T(x):
  return tofloat(x, ["K"])  # C, F


def tofloat_Hz(x):
  return tofloat(x, ["Hz"])


# Some aliasses. These are non-canonical and can produce a deprecation warnings
# in the future.
tofloat_A = tofloat_I
tofloat_U = tofloat_V


# TODO(baryluk): More tests.
class Test_tofloat_units(unittest.TestCase):
  def test_R(self):
    self.assertEqual(tofloat_R("1.25"), 1.25)
    self.assertEqual(tofloat_R("1.25Ohm"), 1.25)
    self.assertEqual(tofloat_R("1.25M"), 1.25e6)
    self.assertEqual(tofloat_R("1.2kΩ"), 1.2e3)
    self.assertEqual(tofloat_R("1.2kOhm"), 1.2e3)
    with self.assertRaises(Exception):
      tofloat_R("4.2nV")
    with self.assertRaises(Exception):
      tofloat_R("1.2mA")
    with self.assertRaises(Exception):
      tofloat_R("4.2nH")

    with self.assertRaises(Exception):
      tofloat_R("1.20hm")  # 1.20 hm , not 0 (zero), not Ohm.

  def test_V(self):
    self.assertEqual(tofloat_V("31.3uV"), 31.3e-6)
    with self.assertRaises(Exception):
      tofloat_V("1.2kOhm")
    with self.assertRaises(Exception):
      tofloat_V("1.2mA")
    with self.assertRaises(Exception):
      tofloat_V("4.2nH")

  def test_A(self):
    self.assertEqual(tofloat_I("3mA"), 3.0e-3)
    with self.assertRaises(Exception):
      tofloat_I("1.2kOhm")
    with self.assertRaises(Exception):
      tofloat_I("4.2nV")
    with self.assertRaises(Exception):
      tofloat_I("4.2nH")

  def test_L(self):
    self.assertEqual(tofloat_L("4.2nH"), 4.2e-9)
    with self.assertRaises(Exception):
      tofloat_L("1.2kOhm")
    with self.assertRaises(Exception):
      tofloat_L("4.2nV")
    with self.assertRaises(Exception):
      tofloat_V("1.2mA")

  def test_Hz(self):
    self.assertEqual(tofloat_Hz("500kHz"), 500.0e3)
    with self.assertRaises(Exception):
      tofloat_Hz("1.2kOhm")
    with self.assertRaises(Exception):
      tofloat_Hz("4.2nV")
    with self.assertRaises(Exception):
      tofloat_Hz("1.2mA")


def ohm_law(*, r:'Ohm'=None, u:'V'=None, i:'A'=None):
  """Using Ohm's law, given 2 of r, u, i, provide the third."""
  if u and i:
    assert r is None
    u, i = tofloat_V(u), tofloat_I(i)
    r = u / i
    return r
  if u and r:
    assert i is None
    u, r = tofloat_V(u), tofloat_R(r)
    i = u / r
    return i
  if i and r:
    # assert u is None
    i, r = tofloat_I(i), tofloat_R(r)
    u = i * r
    return u
  assert False, "Missing required inputs to ohm_law"


class Test_OhmLaw(unittest.TestCase):
  def test_all(self):
    self.assertEqual(ohm_law(r="1k", u="2V"), 0.002)  # A
    self.assertEqual(ohm_law(u="2V", i="5A"), 0.4)  # Ω
    self.assertEqual(ohm_law(r="3Ω", i="10A"), 30.0)  # V

  def test_toomuch(self):
    with self.assertRaises(Exception):
      a = ohm_law(r="3Ω", i="10A", u='30V')

  def test_toolittle(self):
    with self.assertRaises(Exception):
      a = ohm_law(r="3Ω")
    with self.assertRaises(Exception):
      a = ohm_law(i="10A")
    with self.assertRaises(Exception):
      a = ohm_law(u="30V")


def power(*, r:'Ohm'=None, u:'V'=None, i:'A'=None):
  """Using Ohm'law, given 2 of r, u, i provide the power (p)."""
  if u and i:
    assert r is None
    u, i = tofloat_V(u), tofloat_I(i)
    p = u * i
    return p
  if u and r:
    assert i is None
    u, r = tofloat_V(u), tofloat_R(r)
    p = u*u / r
    return p
  if i and r:
    # assert u is None
    i, r = tofloat_I(i), tofloat_R(r)
    p = i*i * r
    return p
  assert False, "Missing required inputs to power"


class Test_OhmLawPower(unittest.TestCase):
  def test_all(self):
    self.assertEqual(power(r="1k", u="2V"), 0.004)  # W
    self.assertEqual(power(u="2V", i="5A"), 10.0)  # W
    self.assertEqual(power(r="3Ω", i="10A"), 300.0)  # W

  def test_toomuch(self):
    with self.assertRaises(Exception):
      a = power(r="3Ω", i="10A", u='30V')

  def test_toolittle(self):
    with self.assertRaises(Exception):
      a = power(r="3Ω")
    with self.assertRaises(Exception):
      a = power(i="10A")
    with self.assertRaises(Exception):
      a = power(u="30V")


import collections

OhmAll = collections.namedtuple("OhmAll", ['r', 'u', 'i', 'p'])


def ohm_law_all(*, r:'Ohm'=None, u:'V'=None, i:'A'=None, p:'W'=None):
  """Returns a namedtuple, with r, u, i and p.

  TODO: Providing power as input to calculate other paremters is not supported
  at the moment."""
  assert p is None
  if u and i:
    assert r is None
    u, i = tofloat_V(u), tofloat_I(i)
    r = u / i
    p = u * i
    return OhmAll(r, u, i, p)
  if u and r:
    assert i is None
    u, r = tofloat_V(u), tofloat_R(r)
    i = u / r
    p = u*u / r
    return OhmAll(r, u, i, p)
  if i and r:
    assert u is None
    i, r = tofloat_I(i), tofloat_R(r)
    u = i * r
    p = i*i * r
    return OhmAll(r, u, i, p)
  assert False, "Missing required inputs to ohm_law_all"


class Test_OhmLawAll(unittest.TestCase):
  def test_ru(self):
    a = ohm_law_all(r="1k", u="2V")
    self.assertEqual(a.i, 0.002)  # A
    self.assertEqual(a.p, 0.004)  # W
    self.assertEqual(a.r, 1.0e3)  # input
    self.assertEqual(a.u, 2.0)  # input

  def test_ui(self):
    a = ohm_law_all(u="2V", i="5A")
    self.assertEqual(a.r, 0.4)  # Ω
    self.assertEqual(a.p, 10.0)  # W
    self.assertEqual(a.u, 2.0)  # input
    self.assertEqual(a.i, 5.0)  # input

  def test_ri(self):
    a = ohm_law_all(r="3Ω", i="10A")
    self.assertEqual(a.u, 30.0)  # V
    self.assertEqual(a.p, 300.0)  # W
    self.assertEqual(a.r, 3.0)  # input
    self.assertEqual(a.i, 10.0)  # input

  def test_toomuch(self):
    with self.assertRaises(Exception):
      a = ohm_law_all(r="3Ω", i="10A", u='30V')

  def test_toolittle(self):
    with self.assertRaises(Exception):
      a = ohm_law_all(r="3Ω")
    with self.assertRaises(Exception):
      a = ohm_law_all(i="10A")
    with self.assertRaises(Exception):
      a = ohm_law_all(u="30V")


def sign(value):
  """Resturns +1 or -1, depending on a sign of value.

  Value can be in a format accepted by the `tofloat` function.

  This is useful for parametric components and sub-schematics, that can operate
  on negative values of some paremters, like for example voltage divider dividing
  -10V to -5V, or a voltage regulator factory, to produce -5V and +5V regulators
  (referenced to ground).

  A bidiractional buck-boost converted might have limits depending on a
  direction, and these often will be expressed in signed form.
  """
  value = tofloat(value)
  if value >= 0.0:
    return 1
  else:
    return -1


assert sign(5.0) == 1.0
assert sign(-7.0) == -1.0
assert sign(0.0) >= 0.0

def sign_V(value):
  value = tofloat_V(value)
  if value >= 0.0:
    return 1
  else:
    return -1

def abs_V(value):
  return abs(tofloat_V(value))

_eia_96_codes = {
  '00': 0,
  '01': 100,
  '02': 102,
  '03': 105,
  '04': 107,
  '05': 110,
  '06': 113,
  '07': 115,
  '08': 118,
  '09': 121,
  '10': 124,
  '11': 127,
  '12': 130,
  '13': 133,
  '14': 137,
  '15': 140,
  '16': 143,
  '17': 147,
  '18': 150,
  '19': 154,
  '20': 158,
  '21': 162,
  '22': 165,
  '23': 169,
  '24': 174,
  '25': 178,
  '26': 182,
  '27': 187,
  '28': 191,
  '29': 196,
  '30': 200,
  '31': 205,
  '32': 210,
  '33': 215,
  '34': 221,
  '35': 226,
  '36': 232,
  '37': 237,
  '38': 243,
  '39': 249,
  '40': 255,
  '41': 261,
  '42': 267,
  '43': 274,
  '44': 280,
  '45': 287,
  '46': 294,
  '47': 301,
  '48': 309,
  '49': 316,
  '50': 324,
  '51': 332,
  '52': 340,
  '53': 348,
  '54': 357,
  '55': 365,
  '56': 374,
  '57': 383,
  '58': 392,
  '59': 402,
  '60': 412,
  '61': 422,
  '62': 432,
  '63': 442,
  '64': 453,
  '65': 464,
  '66': 475,
  '67': 487,
  '68': 499,
  '69': 511,
  '70': 523,
  '71': 536,
  '72': 549,
  '73': 562,
  '74': 576,
  '75': 590,
  '76': 604,
  '77': 619,
  '78': 634,
  '79': 649,
  '80': 665,
  '81': 681,
  '82': 698,
  '83': 715,
  '84': 732,
  '85': 750,
  '86': 768,
  '87': 787,
  '88': 806,
  '89': 825,
  '90': 845,
  '91': 866,
  '92': 887,
  '93': 909,
  '94': 931,
  '95': 953,
  '96': 976,
}

_eia_96_multipliers = {
  'Z': 0.001,
  'Y': 0.01,
  'R': 0.01,
  'X': 0.1,
  'S': 0.1,
  'A': 1.0,
  'B': 10.0,
  'H': 10.0,
  'C': 100.0,
  'D': 1000.0,
  'E': 10000.0,
  'F': 100000.0,
}


def smd_tofloat(x:str):
  """It should be passed as string, but integer is also ok, it will be converted to decimal string."""
  if type(x) is int:
    x = str(x)

  # EIA-96 system (2 digit + 1 letter).
  if len(x) == 3 and x[0:1].isdigit() and x[2].isalpha():  # aka "11A format"
     # EIA-96 system. For 1% SMD resistors.
     value = _eia_96_codes[x[0:2]]
     # Note, We also have '00' in the table to handle 00R, but it also allows things like 00D, etc.
     # Technically 00R is 0 * 0.01, but it will end up as 0 anyway, and float, which is nice.
     # Technically EIA-96 doesn't support 00R, or other 00 things, like 00Z, 00X, etc.
     if x[2] == 'R' and value != 0:  # Allow 00R.
       warning(f"Using R suffix in '{x}' with EIE-96 codes (2 digit + 1 leter) is not recommended "
               "and deprecated. I.e. '17R' is 1.47Ω, not 17Ω. Use Y to clarify.")
     if x[2] == 'S':
       warning(f"Using S suffix in '{x}' with EIE-96 codes (2 digit + 1 leter) is not deprecated, "
               "use X instead.")
     if x[2] == 'H':
       warning(f"Using H suffix in '{x}' with EIE-96 codes (2 digit + 1 leter) is not deprecated, "
               "use B instead.")
     if value == 0 and x[2] != 'R':
       warning(f"Using non-R suffix in '{x}' with EIE-96 codes (2 digit + 1 letter) for non-zero values, "
               "is not recommended. Use '00R'.")
     multiplier = _eia_96_multipliers[x[2]]
     return value * multiplier

  # if len(x) == 3 and x[0].isalpha() and x[1:3].isdigit():  # aka "A11 format"
    # 2%, 5%, 10% SMD resistors.

  # Support 'R' in 3 digit codes, assuming it is not at the end. I.e. '17R',
  # is the EIA-96 format. 17R itself deprecated, and 17Y should be used, but still.
  if len(x) == 3 and 'R' in x:
    assert x[2] != 'R'
    assert x.count('R') == 1
    x = x.replace('R', '.')
    return float(x)

  # Normal 3 digit codes.
  if len(x) == 3 and x.isdigit():
    value = int(x[0:2])
    multiplier = 10 ** int(x[2])
    if value == 0 and multiplier != 1:
      warning(f"Using non-zero last digit in 3-digit SMD code, with 00 at the start, is not recommended, "
              f"use '000' instead of '{x}'.")
    return value * multiplier

  # Support 'R' in 4 digit codes.
  #
  # If R is used to point to decimal digit, the last digit no longer is
  # a multiplier, but part of a resistance.
  # i.e. 0R75 is 0.750 Ω, not 0.7*10^5.
  # 0R01, is 0.010 Ω, not 0 Ω.
  # Also R can be at the start, to mean 0., so R531, means 0.531 Ω
  #
  # We allow 'R' at any position, including last. Because that is not a ambigouity.
  if len(x) == 4 and 'R' in x:
    assert x.count('R') == 1
    if x[-1] == 'R':
      warning(f"Avoid using 'R' at the end of 4-digit SMD codes, prefer '0'. "
              f"I.e. '123R', use '1230' instead. Found when parsing: '{x}'.")
    x = x.replace('R', '.')
    # Note, float function, will handle also things like '.123', so 'R123',
    # converted to '.123' will convert to 0.123. Which is correct.
    # Similarly 'R123' will be converted to '123.', which will convert to
    # 123.0, which is correct.
    return float(x)

  # sub-milliΩ resolution. ie. 5L12 is 5.12 mΩ.
  # We only allow this in 4-digit codes.
  if len(x) == 4 and 'L' in x:
    assert x.count('L') == 1
    x = x.replace('L', '.')
    # float is smart, so 'L123', will be 0.123e-3, and '789L' will be 789e-3
    # return float(x) * 1.0e-3
    return float(x + "e-3")  # Should be slightly more accurate.

  # Normal 4 digit codes.
  if len(x) == 4 and x.isdigit():
    value = int(x[0:3])
    multiplier = 10 ** int(x[3])
    if value == 0 and multiplier != 1:
      warning(f"Using non-zero last digit in 4-digit SMD code, with 00 at the start, "
              f"is not recommended, use '0000' instead of '{x}'.")
    # TODO: Using float(str(value) + "e{x[3]}") might be more accurate,
    # as some multipliers are not exact in floating points.
    return value * multiplier

  # Handle common zero formats not handled by code above.
  if x == "0":
    return 0.0
  if x == "00":
    return 0.0
  # 3 and 4 digit (000, 0000) should be already handled above.

  assert False, (f"Unknown format when parsing '{x}'. EIE-96 system (2 digits + letter), "
                 "or 3 or 4 digits SMD formats, with last digit for multiplier supported only.")
  # TODO: Underline formats, i.e. _101_ means 0.101 Ω, _068_ is same
  # as R068, or 0.068Ω, aka 69 mΩ.

# import math
# isclose = lambda a, b: math.isclose(a, b, rel_tol=1e-12)


class Test_SMD_tofloat(unittest.TestCase):
  # EIE-96 formats.
  def test_eie96(self):
    self.assertEqual(smd_tofloat("01Y"), 1.0)
    self.assertAlmostEqual(smd_tofloat("68X"), 49.9)
    self.assertAlmostEqual(smd_tofloat("76X"), 60.4)
    self.assertEqual(smd_tofloat("01A"), 100.0)
    self.assertEqual(smd_tofloat("29B"), 1.96e3)
    self.assertEqual(smd_tofloat("01C"), 10e3)
    self.assertNotEqual(smd_tofloat("17R"), 17.0)  # warns
    self.assertEqual(smd_tofloat("17R"), 1.47)  # warns

  # 3 digit formats.
  def test_3digit(self):
    self.assertEqual(smd_tofloat("220"), 22.0)
    self.assertEqual(smd_tofloat("471"), 470.0)
    self.assertEqual(smd_tofloat("102"), 1000.0)

  def test_3digit_with_R(self):
    self.assertEqual(smd_tofloat("1R4"), 1.4)
    self.assertEqual(smd_tofloat("3R3"), 3.3)
    self.assertEqual(smd_tofloat("3R0"), 3.0)
    self.assertEqual(smd_tofloat("0R3"), 0.3)
    self.assertEqual(smd_tofloat("136"), 13.0e6)

    with self.assertRaises(Exception):
      smd_tofloat("99R")

  # 4 digit formats.
  def test_4digit(self):
    self.assertEqual(smd_tofloat("4700"), 470.0)
    self.assertEqual(smd_tofloat("2001"), 2000.0)
    self.assertEqual(smd_tofloat("1002"), 10000.0)

  def test_4digit_with_R(self):
    self.assertEqual(smd_tofloat("15R0"), 15.0)
    self.assertEqual(smd_tofloat("0R20"), 0.200)
    self.assertEqual(smd_tofloat("0R75"), 0.750)
    self.assertEqual(smd_tofloat("0R01"), 0.010)

    self.assertEqual(smd_tofloat("R105"), 0.105)
    self.assertEqual(smd_tofloat("R133"), 0.133)
    self.assertEqual(smd_tofloat("14R7"), 14.7)

  # Technically 150R, is same as 1500, aka 150Ω. But I doubt it is used on real parts.
  # It is supported tho.
  def test_3digit_trailing_R(self):
    self.assertEqual(smd_tofloat("150R"), 150.0)
    self.assertEqual(smd_tofloat("123R"), 123.0)

  # 4 digit L codes.
  def test_4digit_with_L(self):
    self.assertEqual(smd_tofloat("5L12"), 5.12e-3)
    self.assertEqual(smd_tofloat("L123"), 0.123e-3)
    self.assertEqual(smd_tofloat("789L"), 789e-3)

  # Zeros
  def test_zeros(self):
    # This one works by accident. Not sure if it is technically allowed by EIA-96.
    self.assertEqual(smd_tofloat("00R"), 0.0)

    self.assertEqual(smd_tofloat("0R0"), 0.0)
    self.assertEqual(smd_tofloat("R00"), 0.0)
    self.assertEqual(smd_tofloat("R000"), 0.0)
    self.assertEqual(smd_tofloat("000R"), 0.0)  # Technically probably not allowed.

    self.assertEqual(smd_tofloat("0000"), 0.0)
    self.assertEqual(smd_tofloat("000"), 0.0)
    self.assertEqual(smd_tofloat("00"), 0.0)
    self.assertEqual(smd_tofloat("0"), 0.0)

  def test_other(self):
    # self.assertEqual(smd_tofloat("14R"), 14.0)
    pass


# Some resistors for current sensing below ohm, have marks like 1M50 = 1.50mΩ, 2M2 = 2.2mΩ, 5L00 = 5mΩ.
# Current sensing resistors can also be marked with a long bar over number, i.e. 1m5 = 1.5mΩ, R001 = 1mΩ.
# Or long under line, in which case the R is omitted. i.e. underlined 101 means 0.101Ω, underlined 047 means 0.047Ohm.
# So R068 is same as _068_

# We can add also a decoder for resistor colors. Just for completness.

# Color band for digits. Shared by resistor and inductor coding (only for digits!).
_resistor_colors = {
  "black": 0,
  "brown": 1,
  "red": 2,
  "orange": 3,
  "yellow": 4,
  "green": 5,
  "blue": 6,
  "violet": 7,
  "gray": 8,
  "white": 9,
}
_resistor_multipliers = {}
for color, value in _resistor_colors.items():
  _resistor_multipliers[color] = 10 ** value  # black (value == 0) => multiplier 10^0 => 1x.
_resistor_multipliers["gold"] = 0.1
_resistor_multipliers["silver"] = 0.01


assert _resistor_multipliers["black"] == 1.0
assert _resistor_multipliers["blue"] == 1.0e6
assert _resistor_multipliers["white"] == 1.0e9

# For 4, 5 and 6 color band formats.
# in %.  20 => +/- 20%, +/- 0.2 of nominal value.
_resistor_tolerances_pct = {
  "black": 20,    # "M". Usually not present at all on resistor. Because lack of 4th band means +/- 20%.
  "brown": 1,     # "F"
  "red": 2,       # "G"
  "orange": 3,    # non-standard
  "yellow": 5,    # shouldn't be used, but is same as gold (similar color).
  "green": 0.5,   # "D"
  "blue": 0.25,   # "C"
  "violet": 0.1,  # "B"
  "gray": 0.05,   # "A"
  "white": 10,    # shouldn't be used, but is same as silver (similar color).
  "gold": 5,      # "J". same as yellow.
  "silver": 10,   # "K". same as white
}

# in ppm/K
_resistor_temp_coef = {
  "black": 250,  # standard, same as no 5th bar. Essentially.   "U"
  "brown": 100,  # standard.  "S"
  "red": 50,     # "R"
  "orange": 15,  # "P"
  "yellow": 25,  # "Q"
  "green": 20,   # "Z"    # rearly used.
  "blue": 10,    # "Z" ?
  "violet": 5,   # "M"
  "gray": 1,     # "K"   # similar to white, so same value. Not sure which one is canonical. My guess white?
  "white": 1,    # apparently. Shouldn't appear really tho.
}


ResistorValue = collections.namedtuple('ResistorValue', ['r', 'tolerance_pct', 'temp_coef'])


def resistor_colors_to_float(colors:list):
  """3, 4, 5, 6 color bands support.

  On resistor if bands are grouped on one side, make sure to have a group
  of closely-spaced band on the left side of the resistor, then read left
  to right.

  Like this:

         +----------------+
  -------| | | |          |---------
         +----------------+
         +----------------+
  -------| | | |       |  |---------
         +----------------+
           ^ 1st digit ^tolerance
             ^2nd digit
               ^multiplier

         +----------------+
  -------| |   | |   |    |---------
         +----------------+
           ^1st^2nd  ^tolerance  (often gold or silver)
                 ^multiplier

         +----------------+
  -------| |   | | | |    |---------
         +----------------+
           ^1st^2nd^multiplier
                 ^3rd^tolerance

         +----------------+
  -------| |   | | | |  | |---------   (ouch).
         +----------------+
           ^1st  ^3rd   ^temp coef
               ^2nd^multiplier
                     ^tolerance

         +--------------------+
  -------| |   | | |     |  | |---------
         +--------------------+
           ^1st  ^3rd       ^temp coef
               ^2nd^multiplier
                         ^tolerance

         +-----------------+
  -------| | | | |    |  | |---------
         +-----------------+
           ^1st^3rd    ^temp coef
             ^2nd^multiplier
                      ^tolerance

  One of the hint for ordering. The first band can't be silver or gold.
  However, there might be yellow (which is similar to gold) or white
  (which is similar to silver).

  For 5% and 10% resistor, simply make sure the silver or gold band are
  on the right.

  5% resistors often will have yellow / brown casing, or beige.
  1% and 2% resistors often will have blue casing.

  Usually blue and dark brown resistor are using metal-oxide film
  elements.

  Usually beige and green bodied resistor will use carbon film.

  TODO: If the resistor is uncommon value, give a warning, maybe it is
  reversed reading?
  """
  tolerance_pct = 5
  temp_coef = 250

  # in 3 colors: 1st digit, 2nd digit, multiplier
  # in 4 colors: 1st digit, 2nd digit, multiplier, tolerance
  # in 5 colors: 1st digit, 2nd digit, 3rd digit, multiplier, tolerance
  # in 6 colors: 1st digit, 2nd digit, 3rd digit, multiplier, tolerance, temperature_coefficient

  if len(colors) == 3 or len(colors) == 4:
    if colors[0] == "black":  # 0
      assert colors[1] == "black"  # 0
      assert colors[2] == "black"  # x1
    value = 10 * _resistor_colors[colors[0]] + _resistor_colors[colors[1]]
    multiplier = _resistor_multipliers[colors[2]]
    if len(colors) == 4:
      tolerance_pct = _resistor_tolerances_pct[colors[3]]
    return ResistorValue(value * multiplier, tolerance_pct, temp_coef)

  if len(colors) == 5 or len(colors) == 6:
    if colors[0] == "black":  # 0
      assert colors[1] == "black"  # 0
      assert colors[2] == "black"  # 0
      assert colors[3] == "black"  # x1
    value = 100 * _resistor_colors[colors[0]] + 10 * _resistor_colors[colors[1]] + _resistor_colors[colors[2]]
    multiplier = _resistor_multipliers[colors[3]]
    tolerance_pct = _resistor_tolerances_pct[colors[4]]
    if len(colors) == 6:
      temp_coef = _resistor_temp_coef[colors[5]]
    return ResistorValue(value * multiplier, tolerance_pct, temp_coef)

  # a 7th band is for reliability:
  #  brown 1% failure rate
  #  red 0.1% failure rate
  #  orange 0.01% failure rate
  #  yellow 0.001% failure rate

  # There are some resistors that have 4 bands like normal, and 5th to indicate the failure rate.


class Test_ResistorColors(unittest.TestCase):
  def test_all(self):
    self.assertEqual(resistor_colors_to_float(["green", "blue", "black"]).r, 56.0)
    self.assertEqual(resistor_colors_to_float(["yellow", "gray", "silver"]).r, 0.48)
    self.assertEqual(resistor_colors_to_float(["green", "blue", "black", "brown"]), ResistorValue(56.0, 1.0, 250))
    self.assertEqual(resistor_colors_to_float(["yellow", "gray", "silver", "green"]), ResistorValue(0.48, 0.5, 250))
    self.assertEqual(resistor_colors_to_float(["orange", "white", "violet", "gold", "brown"]),
                     ResistorValue(39.7, 1.0, 250))
    self.assertEqual(resistor_colors_to_float(["brown", "black", "green", "orange", "gray"]),
                     ResistorValue(105e3, 0.05, 250))
    self.assertEqual(resistor_colors_to_float(["yellow", "orange", "red", "green", "blue", "violet"]),
                     ResistorValue(43.2e6, 0.25, 5))  # value, tolerance, temp_coef


def capacitor_code_to_float(code:str):
  # Code: 1st digit (1-9), 2nd digit (0-9), multiplier (0-9).
  # 100 => 10 pF
  # 101 => 100 pF
  # 102 => 1 nF
  # 103 => 10 nF
  # 104 => 100 nF
  # 105 => 1 uF
  # 106 => 10 uF
  # 107 => 100 uF
  # 108 => 0.1 pF
  # 109 => 1 pF
  pass


def inductor_colors_to_float_uH(colors:list):
  # 4 colors: 1st digit, 2nd digit, multiplier, tolerance
  # noqa  # E241
  _multipliers = {
    "black":       1.0,   #       1x uH
    "brown":      10.0,   #      10x uH
    "red":       100.0,   #     100x uH
    "orange":   1000.0,   #    1000x uH
    "yellow":  10000.0,   #   10000x uH
    "green":  100000.0,   #  100000x uH
    "blue":  1000000.0,   # 1000000x uH
    "gold":        0.1,   #       0.1x uH
    "silver":      0.01,  #       0.01x uH
  }
  _tolerances_pct = {
    "black": 20,
    "brown": 1,
    "red": 2,
    "orange": 3,
    "yellow": 4,  # different than for resistor (5%) which uses same for yellow and gold.
    "gold": 5,
    "silver": 10,
  }
  value = 10 * _resistor_colors[colors[0]] + _resistor_colors[colors[1]]
  multiplier = _multipliers[colors[2]]
  tolerance_pct = _tolerances_pct[colors[3]]  # lookup even if not used to make sure it is correct / exists.
  return value * multiplier


class Test_InductorColors(unittest.TestCase):
  def test_all(self):
    self.assertEqual(inductor_colors_to_float_uH(["black", "blue", "red", "black"]), 600)  # 600 uH, +/- 20%
    self.assertEqual(inductor_colors_to_float_uH(["green", "orange", "yellow", "gold"]), 530.0e3)  # 530 mH, +/- 5%


if __name__ == '__main__':
  unittest.main(verbosity=0)
