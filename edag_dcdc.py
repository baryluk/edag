#!/usr/bin/env python3

"""A module with various DC/DC converter ICs and ready to use PSU sub-schematics."""

from edag import make_component, tofloat, net, scoped_net
from edag_components import res, cap, ucap, inductor, diode, schottky, voltage_divider_auto
from edag_utils import tofloat_V, tofloat_C, tofloat_R, tofloat_L, tofloat_I, tofloat_Hz


def dcdc_mp2359_full(name:str, *, v_in:'NET', gnd:'NET', v_out:'NET', en:'NET'=None,
                     output_voltage:'V'=3.3,
                     max_output_current:'A'=1.2,
                     min_input_voltage:'V'=12,
                     max_input_voltage:'V'=25,
                     en_pullup:bool=False,
                     package:str="SOT23-6",
                     external_bootstrap_diode=False,
                     opt_d3=False):
  """MP2359 from Monolithic Power aka MPS.

  Adjustable output 1.2A peak current DC/DC converter IC.

  Input 4.5V - 24V required.

  Includes input and output capacitors, feedback resistors, inductor, diode,
  and bootstrap cap. Calculates automatically voltage ratings of caps.

  If `en` net is None, it is tied to v_in via resistor or divider,
  to put make it always enabled. If `en` is not-None, then this
  resistor or divider is not put,  unless en_pullup is also set to True.

  TODO: Calculate voltage divider automatically.

  Datasheet: https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MP2359/document_id/228/

  Warning: Not recommended for new designs.

  Replacement: MPS MP2331H (2A, higher efficiency, lower R_ds(ON) FET,
               configurable soft startup, power good output, SOT583 package).
  """

  assert package in ["TSOT23-6", "SOT23-6"], \
         f"Package {package} is not on a list of supported packages for this part."

  # TODO: Scope(name)

  # X5R or X74 is recommended for their low ESR.
  cap("input_decopul", "10u", p=v_in, n=gnd, voltage="25V")  # TODO: Use max_input_voltage

  if en:
    en_pullup = "100kΩ"
  en = en if en else v_in


  # TODO(baryluk): Factor this (pin_map and make_component) into function.
  pin_map = {
    "in": 5,
    "gnd": 2,
    "en": 4,
    "bst": 1,
    "sw": 6,
    "fb": 3,
  }
  u = make_component("dcdc_mp2359", "MP3259", {
                       "in":v_in, "gnd":gnd, "en":en, "bst":scoped_net(),
                       "sw":scoped_net(), "fb":scoped_net(),
                     }, {"pin_map": pin_map}, [], prefix="U")

  if en_pullup:
    res("en_pullup", en_pullup, v_in, u.pin_nets["en"])

  # According to datasheet, en 

  output_voltage = tofloat_V(output_voltage)
  min_input_voltage = tofloat_V(min_input_voltage)
  max_input_voltage = tofloat_V(max_input_voltage)
  max_current = tofloat_I(max_output_current)

  assert output_voltage >= 0.5  # TODO: To check.

  assert output_voltage + 1.0 <= min_input_voltage  # TODO: To check.

  assert min_input_voltage <= max_input_voltage

  assert max_input_voltage <= 25.0

  if min_input_voltage <= 5.0:
    assert opt_d3, "For input voltage less than 5V, an external diode is required."

  if opt_d3:
    diode("d1??", model="1n4148", a=v_in, c=u.pin_nets["bst"])

  ucap("bst_cap_bulk", "10n", u.pin_nets["bst"], u.pin_nets["sw"],
        voltage=tofloat_V(output_voltage) + 3.0)  # 0.1uF - 1uF recommended
  # or 22nF ?
  schottky("switching_diode", model="B230A-13-F", a=gnd, c=u.pin_nets["sw"])
  inductor("switching_inductor", "4.7u", p1=u.pin_nets["sw"], p2=v_out, current='1.66A')  # TODO: current_rating
  # TODO: Calculate the inductance required


  duty_cycle = tofloat_V(output_voltage) / min_input_voltage
  if tofloat_V(output_voltage) <= 5.0 and duty_cycle > 0.65:
    assert external_bootstrap_diode, ("For output voltage less than 5V and duty cycle above 65%, "
                                      "an external bootstrap diode is required.")

  if external_bootstrap_diode:
    diode("external_bootstrap_diode", "1n1448", a=v_out, c=u.pin_nets["bst"])

  # d2 and d3 are not needed both at the same time.

  # voltage divider examples from datasheet.
  #if voltage == 1.8:
  #  80.6k, 64.9k
  #if voltage == 2.5
  #  49.9k, 23.7k
  #if voltage == 3.3:
  #  49.9, 16.2k
  #if voltage == 5.0:
  #  49.9, 9.53k
  # voltage_divider("feedback_divider", "49.9k", "16.2k", high=v_out, low=gnd, output=u.pin_nets["fb"])
  # feedback current is "0.1uA", calculate rest automatically?
  feedback_voltage = tofloat_V("0.81V")
  voltage_divider_auto("feedback_divider", idle_current="1mA",
                       input_voltage=output_voltage, output_voltage=feedback_voltage,
                       high=v_out, low=gnd, output=u.pin_nets["fb"])

  # X5R or X74 is recommended for their low ESR.
  cap("output_cap", "22uF", p=v_out, n=gnd, voltage=tofloat(output_voltage) + 1.3)

  return {"out":v_out, "en":en}


def _mp2359_test():
  dcdc_mp2359_full("3.3V regulator", v_in=net(), gnd=net(), v_out=net())


#_mp2359_test()


def dcdc_tps543x_full(name:str, *,
                      v_in:'NET', gnd:'NET', v_out:'NET', en:'NET'=None,
                      output_voltage:'V'=5.0,
                      output_ripple:'V'="30mV",
                      max_current:'A'=3.0,
                      min_input_voltage:'V'=12,
                      max_input_voltage:'V'=36,
                      inductance:'H'='15µH',  # Output indoctor inductance.
                      en_pullup:bool=False,
                      package:str="HSOP-8",  #  (SOIC-8 with Thermal Pad)
                      catch_diode:str = "B340A",  # from Diodes, Inc.
                      V_diode:'V'="0.5V",  # Forward voltage drop of used catch diode (i.e. B340A has 0.5V).
                      external_bootstrap_diode=False,
                      opt_d3=False,
                      all_ceramic_output_filter_caps=True):
  """TPS5430 or TPS5431 from Texas Instruments.

  3.0A continuous (4.0A peak) current step-down converter.

  Input 5.5 to 36.0V (TPS5430), 5.5 to 23.0V (TPS5431).

  So:
    TPS5431 is intended if the input is nominal 12V (10.8 - 19.8V for example, might be limited by preceading capacitors or reverse polarity protection devices).
    TPS5430 is intended if the input is nominal 24V.

  Switching frequency about 500kHz typical (400kHz-600kHz).

  Efficiency is around 88%, but can be smaller or higher, depending on input
  voltage, and output current (85% - 93% over interesting range).

  If `all_ceramic_output_filter_caps` is False, use a single output capacitor.
  If it is True use more complex all-ceramic output for output
  filtering and voltage sensing.
  By default all_ceramic_output_filter_caps is True, if
  output_voltage <= 3.3V, and False if output_voltage > 3.3V

  Includes input and output capacitors, feedback resistors, inductor, diode,
  and bootstrap cap. Calculates automatically voltage ratings of caps.

  If `en` net is None, it is tied to v_in via resistor or divider,
  to put make it always enabled. If `en` is not-None, then this
  resistor or divider is not put,  unless en_pullup is also set to True.

  TODO: Calculate voltage divider automatically.

  Datasheet: https://www.ti.com/lit/ds/symlink/tps5430.pdf
  """

  assert package in ["SOIC-8", "HSOP-8"], \
         f"Package {package} is not on a list of supported packages for this part."

  # Catch diode forward voltage
  V_diode = 0.5  # V, B340A. Forward current 3A, forward voltage drop 0.5V. Reverse voltage of 40V.

  # Output inductor series resistance.
  R_inductor = tofloat_R("37mOhm")  # Typical.
  # Example: Sumida CDRH10RNP-150N, 15uH ± 30% (at 100kHz/1V),
  # 50mOhm max DCR (37mOhm typ), saturation 3.60A, Temperature rise current 3.10A.

  # Minimum and maximum output load current.
  I_out_min = 0.001
  I_out_max = 3.000

  assert R_inductor * I_out_max <= 1, \
         "Voltage drop over the output inductor at maximum load exceeds 1V"

  V_in_min = tofloat_V(min_input_voltage)
  V_in_max = tofloat_V(max_input_voltage)

  assert V_in_min >= 5.5
  assert V_in_max <= 36.0

  assert tofloat_V(output_voltage) >= 1.23
  assert tofloat_V(output_voltage) <= 31.0
  assert tofloat_V(output_voltage) <= V_in_min - 0.5  # Rough approximation.

  K_inductor = 0.25  # Should be between 0.2 and 0.3 usually.

  assert tofloat_L('10µH') <= tofloat_L(inductance), \
         "Output inductor inductance should be bigger then 10µH."
  assert tofloat_L(inductance) <= tofloat_L('100µH'), \
         "Output inductor inductance should be smaller than 100µH."

  F_sw = tofloat_Hz("500kHz")

  V_out = tofloat_V(output_voltage)
  V_out_max = tofloat_V(output_voltage) + tofloat_V(output_ripple)
  I_out = tofloat_I(max_current)

  # Section 8.2.1.2.4.1, equation 4.
  L_inductor_min = V_out_max * (V_in_max - V_out) / (V_in_max * K_inductor * I_out * F_sw)
  assert tofloat_L(inductance) >= L_inductor_min, f"Requsted inductance {inductance} should be >= {L_inductor_min}"

  assert tofloat_V(V_diode) >= 0.2, \
         "Catch diode voltage drop unrealistically low or negative."
  V_diode_min = tofloat_V(V_diode) * 0.99
  V_diode_max = tofloat_V(V_diode) * 1.01

  # Section 8.2.1.2.8.1, equation 13.
  # Minimum maximum duty cycle of 87%. Typical maximum duty cycle is 89%.
  # This assumes a worst case scenario of high resistence of the internal high side FET.
  # In practice the voltage can be slightly higher depending on a specific die quality.
  # Typical R_DS(on) is 0.110 Ω, maximum R_DS(on) is 0.230Ω.
  # With V_in = 5.5 V, the typical R_DS(on) is 150 mΩ.
  V_out_max = 0.87 * ((V_in_min - I_out_max * 0.230) + V_diode_max) - I_out_max * R_inductor - V_diode_min
  # Equation 14.
  # Constrained by minimum current, input voltage, and minimum switch on time
  # (which can be as high as 200ns). Typical minimum controllable on time is 150ns.
  V_out_min = 0.12 * ((V_in_max - I_out_min * 0.110) + V_diode_min) - I_out_min * R_inductor - V_diode_max

  assert tofloat_V(output_voltage) < V_out_max, \
         f"Condition fail: {output_voltage} < {V_out_max} failed"
  assert V_out_min < tofloat_V(output_voltage), \
         f"Condition fail: {V_out_min} < {output_voltage} failed"
  if __debug__:
    print(f"Desired output voltage: {output_voltage} within design limits: {V_out_min} - {V_out_max}")

  # Low ESR recommended. 4.7uF minimum recommended. X5R or X7R recommended.
  C1 = cap("input_bypass_cap", "10uF", n=gnd, p=v_in)  # C1
  # If the input supply is more than few inches from TPS543x additional bulk
  # capacitance using electrolitic capacitor (i.e. 100uF) is recommended.

  if en:
    en_pullup = "100kΩ"
  en = en if en else v_in
  # Note, TPS543x ENA pin has an internal pull-up current source, so the ENA pin can be floated.
  # Otherwise, use open drain or open collector output logic to interface witht the pin.
  # Bringing ENA to ground or below 0.5V, will disable the regulator and activate the shutdown mode.
  # Quiescent current in shutdown mode is typically 18 uA.
  # When the ENA pin is made high again (>0.5V ?), the slow startup brings
  # voltage from 0 V to final value, linearly in about 8ms. This is to limit the
  # start-up inrush current.

  # TODO(baryluk): Factor this (pin_map and make_component) into function.
  pin_map = {
    "vin": 7,
    "ena": 5,
    "nc": [2,3],
    "gnd": 6,
    "PowerPAD": 9,  # Power Pad. Must be connected to GND pin (6) for proper operation.
                    # 6 thermal vias for it should be enough. Device PowerPad must be
                    # soldered down to PCB for correct performance. Not just thermally bounded!
    "boot": 1,
    "ph": 8,
    "vsense": 4,  # Feedback
  }
  u = make_component("dcdc_tps5430", "TPS5430", {
                       "vin":v_in, "gnd":gnd,
                       "ena":en, "boot":scoped_net(),
                       "ph":scoped_net(), "vsense":scoped_net(),
                       "PowerPAD": gnd, "nc":net(),
                     }, {"pin_map": pin_map}, [], prefix="U")  # U1

  ucap("bootstrap_cap", "0.01uF", a=u.pin_nets["boot"], b=u.pin_nets["ph"])  # C3  # TODO(baryluk): Voltage
  if all_ceramic_output_filter_caps:
    schottky("switching_diode", model="B340A", a=gnd, c=u.pin_nets["ph"])  # D1
  else:
    schottky("switching_diode", model="MRBS340", a=gnd, c=u.pin_nets["ph"])  # D1

  # TODO(baryluk): 22uH for wider input range?
  # TODO(baryluk): Automatically calculate the minimum value.

  # TODO(baryluk): Max current.
  L1 = inductor("switching_inductor", "15uH", p1=u.pin_nets["ph"], p2=v_out, current='4.0A')  # L1

  # Example: For 5V output voltage, 10kΩ + 3.24kΩ ?  About 0.38mA idle current.
  # The voltage on VSENSE pin should be 1.221 V.
  # Voltage reference accuracy is min=1.202V, typ=1.221V, max=1.239V.
  # Over whole output current range is min=1.196V, typ=1.221V, max=1.245V.
  # For 3.3V output, use 10kΩ + 5.9kΩ
  #
  # 10kΩ + 3.3kΩ is also reasonable and gives 4.92V output voltage.
  vsense = u.pin_nets["vsense"]
  vsense_voltage = tofloat_V("1.221V")
  _output = voltage_divider_auto("feedback_divider", idle_current="0.4mA",
                                 input_voltage=output_voltage, output_voltage=vsense_voltage,
                                 high=v_out, low=gnd, output=vsense)  # R1, R2
  assert _output is vsense

  if all_ceramic_output_filter_caps:
    # Use smaller output cap. The output might have higher ripple.

    # TODO(baryluk): Automatically calculate based on the L1, and take into
    # account output_voltage, as at higher voltages the ceramic capacitors do
    # have lower effective capacitance.
    # X5R or X74 is recommended for their low ESR.
    C3 = cap("output_cap", "100uF", p=v_out, n=gnd, voltage=tofloat_V(output_voltage) + 1.3)

    # But use two stage filtering for the VSENSE to ensure stability and good average voltage.

    # TODO(baryluk): Automatically compute the external compensation network
    # based on L1, R1, R2, C3, effective capacitance of C3 at output_voltage,
    # and equations from 8.2.3.2.1, 8.2.3.2.2 sections.

    # C6 voltage rating can be smaller than the full output voltage, because of voltage divider.
    # Here we give it a 0.5V headroom above (output_voltage - vsense_voltage).
    C6 = cap("vsense_filter_high", "1500pF", n=vsense, p=v_out, voltage=tofloat_V(output_voltage) - vsense_voltage + 0.5)
    # C4 voltage rating can be smaller than the full output voltage, because of voltage divider.
    # Here we give it a 0.5V headroom above vsense_voltage.
    C4 = cap("vsense_filter_low", "150pF", n=gnd, p=vsense, voltage=vsense_voltage + 0.5)
    # C4 is optional, but is to improve the load regulation performance.
    # Ct should be less than 1/10 of C6.

    C7 = cap("vsense_filter_low2_cap", "0.1uF", p=vsense, n=net(), voltage=vsense_voltage + 0.5)
    R3 = res("vsense_filter_low2_res", "549Ω", a=C7.pin_nets[1], b=gnd, voltage=vsense_voltage + 0.5)

    # See the datasheet as well TI SLVA237 for additional information.
  else:
    C3 = cap("output_cap", "220uF", p=v_out, n=gnd, voltage=tofloat_V(output_voltage) + 1.3)

  return {"out":v_out, "en":en}


def _tps543x_test():
  dcdc_tps543x_full("5.0V regulator", v_in=net(), gnd=net(), v_out=net())


_tps543x_test()


def dcdc_tps65131_full(name:str, *,
                       v_in:'NET', gnd:'NET', v_out:'NET', en:'NET'=None,
                       output_voltage_positive:'V'=12.0,
                       output_voltage_negative:'V'=-12.0,
                       max_current:'A'=0.750,  # Per output.
                       min_input_voltage:'V'=2.7,
                       max_input_voltage:'V'=5.5,
                       en_pullup:bool=False,
                       package:str="VQFN-24 with PowerPad",
                       external_bootstrap_diode=False,
                       opt_d3=False,
                       all_ceramic_output_filter_caps=True):
  """Positive and Negative back-boost DC/DC converter using Texas Instruments TPS6513x.

  TPS65130 has 800mA typical switch current limit.
  TPS65131 has 2000mA typical switch current limit.

  The positive rail can go up to 15V.

  The negative rail can go down to -15V.

  Up to 89% efficiency at positive output voltage rail.
  Up to 81% efficiency at negative output voltage rail.

  Minimum 1.25MHz fixed frequency PWM operation.
  """

  # Current into feedback (FBP) pin, is about 0.05uA,
  # and voltage across divider should be 1.213V (internal reference).
  # The divider "idle" current should 100 times more, so about 5uA or more.
  # So R2 should be lower than 200kΩ. R1 adjusted depending on desired output voltage.
  # Example: V_POS = 10.5V => R2 = 130kΩ, R1 = 1.0MΩ
  #          V_NEG = -10V => R4 = 121.2kΩ, R3 = 1.0MΩ
  pass
