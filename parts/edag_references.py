#!/usr/bin/env python3

# References.

"TL431"  # Precision Programmable Reference.  SOT-23-3 (3 pin), SOT-23-5 (5 pin), SOIC-8, PDIP-8, SOP-8, and some more (13 different packages).  0.5%, 1%, 2% grades.
"TL432"  # ditto. same device, just different pinout in the packages.
"TL431LI"  # a newer beter version.
"TL432LI"  # ditto.
"LT6657"  # from Linear Technologies. Low Noise, Buffered Reference, 1.5ppm/°C (A grade).
"MAX6009"  # From Maxim Integrated. Precision Shunt Voltage Reference, ultra low power (1uA to 2mA). SOT-23-3, SO-8. MAX6006, MAX6007, MAX6008, MAX6009. 1.25V, 2.048V, 2.5V, 3.0V respectively. Various grades available. 0.2% and 0.5% available. 30ppm/°C and 75ppm/°C.
"ADR4550" # from Analog Devices
"ICL8069"
"LM385"
"LT1004"
"LM4040"
"LM285"
"LTZ1000"  # Ultra precision refrence.  H8 package TO-5 metal can, with 8 pins. Integrated heater element.  Temperature drive of better than 0.03ppm/°C and long-term stability of 1uV per month can be achived. Noise 0.15ppm can be achived. Required special thermal handling of PCB to make sure zener and transistor leads to the package are at the same temperature (otherwise thermocouple forms), including sizing of traces should be same. Even air currents and convection can influence precission. Single point grounding is suggested. See application notes AN-82 and AN-86 for additional help. And AN124f.
"LTZ1000A"  # Ultra precision refernce. A higher thermal resistance (400°C/W) than LTZ1000 (80°C/W) for higher precision.
"LT1006"
"LM199"   # Old design from Linear Technology?

"LT1021"  # Linear Technology. 2ppm/°C. 5V, 7V, 10V precision reference. Available in TO-5, -55°C - 125°C, Series or Shunt Operation
"LM339A"  # Linear Technology. 1ppm/°C.
"LM399"  # 7V Precision Shunt Reference. 0.2% accuracy, 0.5ppm/°C drift, 20uV_{RMS} noise.
"LT1236"  # 5V and 10V Low Drift Precision Reference. 0.05% accuracy, 5ppm/°C drift, Series or Shunt Operation
"LT1389"  # 1.25V, 2.5V, 4V and 5V nanopower shunt reference. 800nA, 0.05% accuracy, 10ppm/°C drift.
"LT1634"  # 1.25V and 2.5V micropower shunt reference. 0.05% accuracy, 10ppm/°C drift, 10uA current.
"LTC6655"  # Precision Low Noise reference family. 2ppm/°C, maximum drift (?), 650nV_{p-p} Noise (0.1Hz to 10Hz).


# Other voltage references, ordered by noise.

"2DW233"  # some chineese reference. 0.05ppm p-p sometimes.  Diamond brand by Shanghai 17th Radio Factory. Some other can be 20uV_{pp} to 100uV_{pp} which is not very precise.
"4910AV"  # some reference, 0.10 ppm p-pm often.
"LTZ1000A"
"7000"
"4910-CH1"
"731B"
"732A"
"AD587LN"
"LT1021BMH-7"
"AD587KR"
"LTC6655-2.5"
"LTC6655-1.25"
"732B"
"LM329"
"LM369BH"
"LM399"
"AD780AN"
"AD584LH-10"   # ~1.68ppm p-p.


"2DW232", "2DW233", "2DW234", "2DW235"   # Previously known as 2DW7C (around a year 2006 changed name to 2DW23x). zero tempco current:  For 2DW232, its 5mA. 2DW233 is 7.5mA. 2DW234 is 10mA.

"LT1031"  # Zener reference. max 6uV_{p-p} noise.


"ADR421"  # Analog Devices. Ultraprecision, Low Noise, 2.500 V XFET® Voltage References. 1.75uV_{p-p}.  Available in SOIC_N-8 and MSOP-8.
"ADR420"  # 1.75uV_{p-p} noise. Wider input voltage range.
"ADR423"  # 2.0uV_{p-p} noise.
"ADR425"  # 3.4uV_{p-p} noise.


"LT1021"  # Precision Reference. 5ppm/°C. 1ppm p-p noise.   5-lead Can, N8 (PDIP-8) and S8 (SOIC-8 ?)  packages. H package (8-lead TO-5). 
"LT1021"
"LT1021-7"  # highest long term stability. non-adjustable. no trip pin.
"LT1021-5"  # 5V  . LT1021C-5 has highest precission at 25°C. But LT1021B-5 has lowest temperature sensitivity.
"LT1021-10"

"Ref 01."
"Ref 02."
"LM368"
"MC1400"
"MC1404"


"LM334"  # current source


"LT1019"  # Precision Bandgap reference. 0.05%, 5ppm/°C
"LT1027"  # Precision 5V reference. 0.02%, 2ppm/°C
"LT1236"  # Precision reference. SO-8, 5V and 10V, 0.05%, 5ppm/°C
"LTC1258"  # Micropower reference. 200mV dropout. MSOP.
"LT1389"  # Nanopower shunt reference. 800nA operating current.
"LT1460"  # Micropower reference. SOT-23. 2.5V, 5V, 10V.
"LT1634"  # Micropower shunt reference. 0.05%, 10ppm/°C, MSOP.
