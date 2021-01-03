#!/usr/bin/env python3

"""Linear regulators"""

from edag_components import make_component
from edag_utils import tofloat_V

import functools

# Accurate is for "A" variants, like LM7805ACT from Fairchild, with ±2% accuracy over 0°C - 125°C.
# Otherwise ±4% accfuracy over -40°C to 125°C
#
# Usually speced for 1.5A continues max recommended current.
#
# Usually they are in TO-220 package. Sometimes others, like TO-92 for smaller power variants. Also available in high power TO-3 version (uA78P05), or TO-252 (DPAK), (like 78M05), or SO-8 (STMicroelectronic 78L05A), or isolated TO-220 (like TS7805).
def regulator_class(type:str = "lm7805", voltage:'V' = 5, accurate:bool = False):
  voltage = tofloat_V(voltage)
  assert voltage >= 0.1
  # @functools.wraps(func)
  def fn(name : str, *, input : 'NET', gnd : 'NET', output : 'NET'):
    """A {type} voltage regulator for {voltage} V, from LM78xx series."""
    return make_component(name, type, {"in": input, "gnd":gnd, "out":output}, [], {'voltage': voltage}, prefix="U")
  # functools.update_wrapper(make_component, fn, assigned={}, updated)
  fn.__name__ = type
  fn.__doc__ = fn.__doc__.format(type=type.upper(), voltage=voltage)
  fn.__qualname__ = type
  return fn

# print(regulator_class)

# Not all manufacturers provide all the variants.
lm7805 = regulator_class("lm7805", 5)
lm7806 = regulator_class("lm7806", 6)
lm7808 = regulator_class("lm7808", 8)
lm7809 = regulator_class("lm7809", 9)
lm7810 = regulator_class("lm7810", 10)
lm7812 = regulator_class("lm7812", 12)
lm7815 = regulator_class("lm7815", 15)
lm7818 = regulator_class("lm7818", 18)
lm7824 = regulator_class("lm7824", 24)

#print(lm7824)
#help(lm7824)

# Other linear regulators:

# BL1117-33 3.3V fixed, from Shanghai Belling. LDO, 1V.
# BL1117-33
# BL1117-.. has also fixed versions for 1.2V, 1.5V, 1.8V, 2.5V, 3.3V, 5V, and 12V.
# BL1117 (no suffixes) is an adjustable one, between 1.25V and 12V.
# Available in SOT-223 (20°C/W) and TO-252 (10°C/W) power package.
# 2mA standby current.
# 1.3V dropout at 1A load current.
# Suffix A - ±1% accuracy, Suffix C - ±2% accuracy.
# Suffix X - SOT-223. Suffix Y - TO-252.
# pinout: SOT-223 and TO-252:  pin 1 - GND (or adjustement), pin 2 - Vout, pin 3 - Vin.
# https://datasheet.lcsc.com/szlcsc/1811021608_BL-Shanghai-Belling-BL1117-33CX_C5400.pdf
# Max input 15V. The BL1117-12V max input 20V.
# Adjustable version: minimum load current 6-10mA.
# Data sheet also mentions TO-220 (4.5°C/W) in one place, but that is probably a mistake.
#
# Adjustable one provides a 1.25V reference voltage.
# The output voltage of adjustable version followstheequation: Vout=1.25(1+R2/R1)+IAdjR2. We can ignore +IAdj because IAdj(about 50uA) is much less than the current of R1(about 2~10mA). 
# R1 between Vout and Adj pin, R2 between Adj and shared ground.

bl1117_12 = regulator_class("bl1117-12", 1.2)
bl1117_15 = regulator_class("bl1117-15", 1.5)
bl1117_18 = regulator_class("bl1117-18", 1.8)
bl1117_25 = regulator_class("bl1117-25", 2.5)
bl1117_33 = regulator_class("bl1117-33", 3.3)
bl1117_50 = regulator_class("bl1117-50", 5)
bl1117_12 = regulator_class("bl1117-12", 12)
#bl1117 = regulator_class("bl1117", 0)


#  XC6206P332MR - 3.3V fixed  , max 200mA ?
# Texas Instruments uA79M05  # Negative voltage, 500mA, 5V.   uA79M00 series.
# Texas Instruments LM317  , # adjustable positive linear voltage regulator
"LM317T"
"LM337"  # adjustable negative linear voltage regulator

# LM317 can also be used as a constant current source easily. A variable resistor around 1 Ohm (1.5W usually) to sense current, it can support often 1A.

# Texas Instruments TL780 series, pinout like A7800 series, improved version of A7800 series. A precision (±1% at 25°C, ±2% over whole temp range) 1.5A regulator.
"TL780-05"  # in 4 packages
"TL780-12" # in 2 packages
"TL780-15" # in 2 packages


# Texas Instruments uA7800 series. Fixed linear regulators (±4% at 25°C, ±5% over whole temp range).
# 1.5A recommended continues max current. Peak 2.2A, 2.1A for higher voltage ones. 2V dropout @ 1A.
# All in 4 or 5 packages. KC (TO-220), and KTE (PowerFLEX) are obsolete. Use KCS or KCT (TO-220) or KTT (TO-263).
"uA7805"
"uA7808"
"uA7810"
"uA7812"
"uA7815"
"uA7824"


"LM1084TI-5.0"  # Fixed +5V 5A LDO voltage regulator.
"LM2937ET-5.0"
"LDO HTC LM1117S-5V"
"L7912CV"
"LT1085CT-5"
"LM350K" # a big can

# Advanced Monolithic Systems, Inc.  AMS1117 series (fixed and adjustable).
"AMS1117-T33"  # Fixed +3.3V 1A LDO voltage regulator, in TO-252 (DPAK?), SOT-223, SOIC-8L. Line regulation: 0.2% max. Load regulation: 0.4% max. 1V dropout.  Output offset (accuracy)  ~ ±1.5% at 25°C, ±3% over whole temp range..
# Versions: 1.5V, 1.8V, 2.5V, 2.85V, 3.3V, 5.0V
"AMS1117"  # Adjustable. Might require extra capacitor to improve stability.

"LM1117" # LDO
"LM2940L" # LDO
"XC6206"  # Torex, 3.3V LDO, in SOT23-3.

"LT3042"  # Low noise linear voltage regulator. Low noise? 7805 is probably better..

"LT1761"  # Linear Technology (now Analog Devices). 100mA, Low Noise, LDO Micropower Regulators in TSOT-23-5. 1.2V, 1.5V, 1.8V, 2.0V, 2.5V, 2.8V, 3.0V, 3.3V, 5.0V, and adjustable (1.22V-20.0V). 300mV drop at 100mA. Three pin variants -BYP, -SD, -X with reordered pins, or ~SHDN pin available.
"LT1761-5"  # 5V LDO.

"LT1120"  # 125mA LDO voltage regulator with 20uA I_Q. Includes 2.5V reference and comperator.
"LT1121"  # 150mA micropower LDO voltage regulator. 30uA I_Q. SOT-223.
"LT1129"  # 700mA micropower LDO voltage regulator. 50uA I_Q.
"LT1175"  # 500mA negative LDO voltage regulator. Micropower. 45uA I_Q. 0.26V dropout. SOT-223
"LT1521"  # 300mA LDO voltage regulator with shutdown. Micropower. 15uA I_Q. Reverse-battery protection.
"LT1529"  # 3A LDO voltage regulator with 50uA I_Q. 500mV dropout.
"LT1762 series"  # 150mA, Low Noise, LDO voltage regulator, micropower. 25uA I_Q. 20uV_{RMS} noise.
"LT1763 series"  # 500mA, Low Noise, LDO voltage regulator, micropower. 30uA I_Q. 20uV_{RMS} noise.
"LTC1929"  # Doubler Charge Pump with Low Noise Linear Regulator. Low output noise: 60uV_{RMS} (100kHz BW).
"LT1962 series"  # 300mA, Low Noise, LDO voltage regulator, micropower. 30uA I_Q. 20uV_{RMS} noise.
"LT1963"  # 1.5A, Low Noise, LDO voltage regulator. Fast transient Response. 40uV_{RMS} noise. SOT-223.
"LT1764"  # 3A, Low Noise, LDO voltage regulator. Fast transient response. 40uV_{RMS} noise. 340mV dropout.
