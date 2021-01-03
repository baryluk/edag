#!/usr/bin/env python3

# Executable to run built-in tests and quickly check syntax errors.

# Component values (i.e. resitstance) can be provided as a number
# (i.e. ohms, as float or integer), or as a string with a suffix,
# i.e. "5k", "2u", "2µ".
#
# Where appropiate these values can also have units / suffixes,
# like "5uF", "4MFA", "1.2kΩ", "1MOhm", etc.
#
# Resistance can be expressed also with R suffix, like "1.3R", "0R" or "5kR".
#
# TODO: Support infix-R formats, like "2R2".
#
# TODO: Support tolerances directly in values, i.e. "5k ± 2%".
#
# TODO: Provide functions for decoding cap and resistor values in
# SMD formats. i.e. 1021 means 102 and 1 zero, so 1020 Ohm.
# 1000 means 100 and 0 zeros, so 100 Ohm.  533 means 53 and 3 zeros,
# so 53k. 102 means 10 and 2 zeros, so 1000 or 1k.


from edag import make_component, tofloat, net, scoped_net
from edag_utils import tofloat_V, tofloat_Charge, tofloat_C, tofloat_R, tofloat_L, tofloat_I, tofloat_P, ohm_law, sign_V, abs_V


def battery(name : str,
            voltage:'V' = 1.5,
            *,
            p:'NET', n:'NET',
            capacity:'C'=1000,
            primary:bool=True,
            chemistry:str='LiFePO₄',
            footprint:str='AA'):
  """A simple battery / cell.

  Capacity can be expressed in C (columbs), A*s, As, or Ah. Unit suffixes are supported too.

  TODO: Add energy capacity in Wh or J.
  """
  voltage = tofloat_V(voltage)
  assert voltage > 0.0
  capacity = tofloat_Charge(capacity)
  assert capacity > 0.0
  return make_component(name, "B", [p, n], [], [voltage, capacity])


def cap(name : str,
        capacitance:'F', *,
        p:'NET', n:'NET',
        voltage:'V'=10,
        tolerance_down:'%'=-10, tolerance_up:'%'=15,
        polarized:bool=False, temp_range:'RANGE'=[0, 85]):
  """Capacitor"""
  capacitance = tofloat_C(capacitance)
  assert capacitance > 0.0
  return make_component(name, "C", [p, n], [], capacitance)


def ucap(name : str,
         capacitance:'F',
         a:'NET', b:'NET',
         *,
         voltage:'V'=10,
         tolerance_down:'%'=-10, tolerance_up:'%'=15,
         polarized:bool=False, temp_range:'RANGE'=[0, 85]):
  """Unpolarized Capacitor"""
  capacitance = tofloat_C(capacitance)
  assert capacitance > 0.0
  return make_component(name, "C", [a, b], [], capacitance)


# def res(resistance, a, b, /):
def res(name : str, resistance:'Ω',
        a:'NET', b:'NET',
        *,
        voltage:'V'=None,  # This is just an alternative way to provide power.
        power:'W'=1,
        tolerance:'%'=2,
        temp_range:'RANGE'=[0, 125]):
  """Resistor"""
  resistance = tofloat_R(resistance)
  assert resistance > 0.0
  return make_component(name, "R", [a, b], [], resistance)


def tie(name : str,
        a:'NET', b:'NET',
        *, physical=False):
  """Basically a zero ohm perfect resistor. It is used to connect different nets.
  Often will have no representation on PCB at all. But could be also realized
  as a 0 ohm resistor or jumper, or a link."""
  return make_component(name, "R", [a, b], [], 0.0)


def diode(name : str, *,
          a:'NET', c:'NET',
          model:str="1N4148", current:'A'=2):
  """Diode.

   -----

  """
  current = tofloat_I(current)
  assert current > 0.0
  return make_component(name, "D", [a, c], [], {"model": model})
  # TODO(baryluk): We could maybe add a broad categories, like small
  # signal / power diode, rectifier, Silicon vs Germanium (different
  # voltage drops, costs, and other characteristics), etc


def zener(name : str, *, a:'NET', c:'NET', voltage:'V', model:str=None):
  """Zener diode"""
  voltage = tofloat_V(voltage)
  assert voltage >= 0.1
  return make_component(name, "D_Zener", [a, c], [], {"model": model})


def schottky(name : str, *, a:'NET', c:'NET', model:str=None):
  """Schottky diode"""
  return make_component(name, "D_Schottky", [a, c], [], {"model": model})


def led(name : str, *, a:'NET', c:'NET', color="red"):
  """LED (Light-emitting diode)"""
  assert color in ["red", "green", "yellow", "orange",
                   "blue", "white", "amber", "pink", "uv"]
  # red orange
  # yellow orange
  # super red
  # amber yellow
  return make_component(name, "D", [a, c], [], [])

# multi-color LEDs, i.e. 2, 3 or 4 in one package, with common cathode,
# common anode or independent pins. some multi-color LEDs are also
# bidirectional. That is passing current opposite way passes it via other
# diode. pretty common for 2 color LEDs (often green + red, or blue + red).
# There are also somteimes LEDs with two same diodes connected
# anti-parallel. so they can be driven in both direction, but give same
# color.


def bulb(name : str, *, a:'NET', b:'NET'):
  """This is basically a resistor. No polarity.

  Most bulbs are specified by voltage and power, not by resistance or current.

  Most bulbs also have strongly temperature dependent resistance.
  """
  todo


def variable_resistor():
  """Aka potentiometer."""
  todo


def ac_source():
  """AC voltage source."""
  todo


def dc_source():
  """Abstract perfect DC voltage source."""
  todo


def current_source():
  """Abstract perfect DC current source."""
  todo


def inductor(name : str,
             inductance:'H',
             *,
             p1:'NET', p2:'NET',
             power:'W'=1, current:'A'=1):
  """Inductor"""
  inductance = tofloat_L(inductance)
  assert inductance > 0.0
  assert tofloat_P(power) > 0.0
  assert tofloat_I(current) > 0.0
  return make_component(name, "L", [p1, p2], [], inductance)


def bead(name:str, *,
         resistance:'Ohm' = "100Ohm",
         frequency:'Hz' = "100MHz",
         max_current:'A'="200mA"):
  """Basically a small inductor, but calculate parameters based on desired
  resistance and frequency.
  """
  pass


def led_with_resistor(name : str,
                      *,
                      a:'NET', c:'NET',
                      current:'A'="5m",
                      voltage:'V'=3.3,
                      color="red"):
  """Automaticaly calculates proper current limiting resistor.

  This takes into account the color, as well non-linearities at low currents.
  """
  current = tofloat_I(current)
  assert current > 0.0
  voltage = tofloat_V(voltage)
  assert voltage > 0.0
  pass


def switch(name : str,
           a:'NET', b:'NET',
           *,
           omentary:bool=True):
  """Switch"""
  return make_component(name, "SW", [a, b], [], {"momentary": momentary})


GND = net("GND")


def switch_with_pullup(name : str, *,
                       sw:'NET', gnd:'NET'=GND,
                       momentary:bool=True,
                       resistance:'Ohm'="5k"):
  """Switch with a pullup resistor"""
  voltage = tofloat_R(resistance)
  assert voltage > 0.0
  pass


def fuse(name : str,
         a:'NET', b:'NET',
         *,
         current:'A'=1, type="polyfuse"):
  return make_component(name, "F", [a, b], [], {"current": current, "type":type})


def reverse_polarity_protection(name : str,
                                *,
                                input:'NET', output:'NET', gnd:'NET',
                                current:'A'=1, max_voltage:'V'=30, fancy=True):
  """A reverse polarity protection based on diode or p-channel MOSFET"""
  mosfet = "Alpha-Omega Semicon AO3401A"  # 30V, 4A, SOT23.. gate-source voltage: -12V to 12V.  If the input is higher, a zener + resistor would work.
  current = tofloat_I(current)
  max_voltage = tofloat_I(max_voltage)
  pass


# def zener_reference(name : str, *, input:'NET', output:'NET', gnd:'NET'=GND(), voltage:'V'=5.2, min_input_voltage:'V'=10, max_input_voltage:'V'=12, max_load_current:'A'=0.020, jfet_constant_current:bool=False):
#   """A simple zener based voltage references with input diode, current limit. A constant current source is an option."""
#   TODO: Add max zener current.
#   pass


# Provide tools to compute things like power / current ratings from other paremeters, like current and/or voltage.

def voltage_divider(name : str, *,
                    r_high:'Ohm', r_low:'Ohm',
                    high:'NET', low:'NET', output:'NET'=None,
                    accuracy:'%'=1):
  """Accuracy is used to select standard series resistors for the divider.

  If better accuracy is needed, a combinations of resistors will be used.

  TODO(baryluk): Quantize to R24, R48, R92 series.
  """
  # TODO: Scope(name)
  assert accuracy > 0.0

  output = output if output else net()
  res("r_high", r_high, a=high, b=output)
  res("r_low", r_low, a=output, b=low)
  return output


def voltage_divider_auto(name : str, *,
                         idle_current:'A'="1mA",
                         input_voltage:'V'=10,
                         output_voltage:'V'=3.3,
                         high:'NET', low:'NET', output:'NET'=None,
                         accuracy:'%'=1, load_current:'A'="1uA"):
  assert accuracy > 0.0

  assert sign_V(input_voltage) == sign_V(output_voltage), f"Sign of input and output voltage must match, got: {input_voltage} and {output_voltage}"
  assert abs_V(output_voltage) <= abs_V(input_voltage), f"(absolute) output voltage must be smaller than (absolute) input voltage, got: {input_voltage} and {output_voltage}"
  # TODO: Scoped(name)
  total_resistance = ohm_law(u=input_voltage, i=idle_current)
  # r_high + r_low = total_resistance
  # r_low / total_resistance = output_voltage / input_voltage
  r_low = total_resistance * tofloat_V(output_voltage) / tofloat_V(input_voltage)
  assert r_low >= 0.0
  assert r_low <= total_resistance
  r_high = total_resistance - r_low
  # print(f"voltage divider: {input_voltage} -> {output_voltage}: {total_resistance}Ohm total, with {r_high} + {r_low}")
  assert r_high >= 0.0
  assert r_high <= total_resistance
  # TODO: Quantize to accuracy using R6, R12, R24, R48, series,
  # or not quantizing for very high accuracies.
  return voltage_divider(name,
                         r_high=r_high, r_low=r_low,
                         high=high, low=low, output=output,
                         accuracy=accuracy)


def voltage_divider_test():
  # voltage divider examples from datasheet.
  #if voltage == 1.8:
  #  80.6k, 64.9k
  #if voltage == 2.5
  #  49.9k, 23.7k
  #if voltage == 3.3:
  #  49.9, 16.2k
  #if voltage == 5.0:
  #  49.9, 9.53k
  # voltage_divider("feedback_divider", "49.9k", "16.2k", high=v_out, low=gnd, output=u.pin_nets["fb"])    # feedback current is "0.1uA", calculate rest automatically?

  gnd = scoped_net("gnd")

  voltage_divider_auto("feedback_divider", idle_current="0.05m", input_voltage=3.3, output_voltage=0.81, high=net(), low=gnd, output=scoped_net("output"))
  assert False

  # About: 10kΩ + 3.24kΩ
  voltage_divider_auto("feedback_divider", idle_current="0.4m", input_voltage=5, output_voltage=1.221, high=net(), low=gnd, output=scoped_net("output"))
  assert False


# voltage_divider_test()


"""
scr, D   (silicon controlled rectifier)
diac, D  (diode for alternating current)
varicap, D (variable capacitance diode, varicap, varactor)
photo, D (photo diode, opto)
radiation, D (semiconductor radiation detector)
dtemperature, D (temperature dependent diode, temperature sensor diode)
tunnel  (Esaki diode)
tvs (bidirectional transient-voltage-supression diode, tvs, thyrector)
unitunnel (unitunnel diode)

ujt, Q (unijunction transistor), i.e. 2N2646
npn, Q (NPN transistor, BJT, bipolar junction transistor)
pnp, Q

npn_double, Q  (Double NPN transistor, Current mirror configuration)
pnp_double, Q  (Double PNP transistor, Current mirror configuration)
npn_darlington
pnp_darlington
digital PNP transistor (i.e. DTA1D3R)
dual NPN input resistor transistor (i.e. ROHM IMH3A)

dual_npn_npn  (just two separate transistor in common package)
dual_npn_pnp  (i.e. OnSemi FMB3946, FMB2227A)
dual_pnp_pnp

n_jfet
p_jfet
nmos
pmos
p_mosfet
n_mosfet

bridge

n_mosfet_gan (with 4 leads, i.e. Panasonic PGA26E19BA, PGA26E07BA - separate drain pin for load and for gate driving)

mnmos (for simulation, with G, D, S, B)
mpmos (for simulation, with G, D, S, B)


opamp

igbt

igbt_gate_driver

mosfet_gate_driver


mosfet_gate_driver_optoisolated
"""
