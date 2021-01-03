#!/usr/bin/env -S PYTHONDEVMODE=1 PYTHONWARNINGS=error python3 -X dev -W error

from edag import process, GND, net, scoped_net, sub, Scope, make_component
from edag_components import cap, res, diode, ucap
from parts.edag_linear import lm7805, lm7809
from edag_notes import note, warning
from edag_dcdc import dcdc_tps543x_full, dcdc_mp2359_full


# TODO: Move to utils
def export_nets(**kwargs):
  return dict(kwargs)


@Scope()
@note("psu")
def psu(regulator = lm7805, gnd=None):
  gnd = gnd if gnd else GND()

  input, output = scoped_net("input"), scoped_net("output")

  with note("psu"):
    with warning("capacitors at least 5mm way from regulator for heat reasons"):
      cap("input_cap", "50m", p=input, n=gnd)

      regulator("voltage regulator", input=input, gnd=gnd, output=output)

      cap("output cap1", "50m", p=output, n=gnd)

      for caps in range(3):
        cap("output cap2", "2n", p=output, n=gnd)

  with note("load"):
    r = res("load", "1k", a=output, b=net())
    diode("load", a=r.pin_nets[1], c=gnd)

  return export_nets(gnd=gnd, input=input, output=output)


def crystal(name = "crystal", value:'HZ'="16M", *, gnd:'NET', a:'NET', b:'NET', footprint:'FOOTPRINT'="SMD-3225_4P"):
  return make_component(name, "X", [gnd, a, b], [], value, prefix="Y")


@Scope()
def oscilator(frequency:'HZ'="16M", /, load_capacitors:'F'="12p", feed_resistance:'Ohm'=47, gnd=None):
  gnd = gnd if gnd else GND()
  with note("oscilator_" + str(frequency)):
      # with Scope() as scope:
      a = scoped_net()  # same as net(), if there is no name provided
      b = scoped_net()
      load_capacitance = load_capacitors
      crystal("crystal", value=frequency, gnd=gnd, a=a, b=b)
      ucap("load_cap_1", load_capacitance, a=a, b=gnd)
      ucap("load_cap_2", load_capacitance, a=b, b=gnd)
      r = res("feed_resistor", feed_resistance, a=b, b=net())

      return export_nets(input=a, output=r.pin_nets[1])


@note("myschematic")
def myschematic():
  psu1 = sub(psu, lm7805)
  psu2 = sub(psu, lm7809)

  v_in = net("v_in_20V")  # 20V nominal
  gnd = GND()

  # Parametrically create a DC-DC converter circuit, automatically computing all
  # paramters from requirements, and placing auxilary components.
  dc1 = sub(dcdc_mp2359_full, "dcdc3.3V", v_in=v_in, gnd=gnd, v_out=net(),
                              output_voltage="3.3V",
                              max_output_current="1.2A",
                              min_input_voltage="12V",
                              max_input_voltage="25V",
                              en_pullup=True,
                              external_bootstrap_diode=False,
                              opt_d3=True)

  dc2 = sub(dcdc_tps543x_full, "dcdc5V", v_in=v_in, gnd=gnd, v_out=net(),
                               output_voltage="5V", max_current="2A",
                               min_input_voltage="10V", max_input_voltage="24V",
                               en_pullup=True, external_bootstrap_diode=True,
                               all_ceramic_output_filter_caps=True,
                               inductance="16µH")  # Default of 15µH is a bit too low, causes assert.

  #print(dc2.nets["v_out"])

  # whatever, do something silly with the sub-components.
  #ucap("silly_capacitor", "1uF", dc1.out, dc2.out)

  osc = oscilator("16M")
  # osc["input"]
  # osc["output"]


process(myschematic)
