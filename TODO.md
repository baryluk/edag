Duplicate function. i.e. capture subschematic using sub, or subschematic
capture, then duplicate all the components and scoped sub-nets to form
new ones. Handling of the scoped nets from current scope and parents,
should be defineable, i.e. current scope re-use, parent re-use, or
current scope rename, by parent re-use. duplicate should basically have
same effect as calling the function that produce it being called second
time. In fact that can be used for testing too, and maybe serialization.

Merge networks.

"tie" componenent. basically a zero ohm resistor.

Connect pins. create anonymous network or tie, to connect pins after the fact.

Better support for circular graphs of connections.

Support multi-unit LEDs.


TODO: Handling of multi-unit components, and chips with multiple
independent components. We can just diode, then have a property to assign
it to a IC type or specific IC. Similar thing for dual transistor
packages, or resistor arrays, or inverters in 74xx series, NAND gates,
etc. In schematic or simulation we treat them independent, but for PCB we
might need specific chip with multiple units, and we want to be able to
quickly swap which pins we use for easier / better layout.

Similarly for microcontrollers and FPGA, we probably want to use pin
names and nets that follow a function, then assign physical pins to
functions. Preferably synchronized with some programming tools, header
file generation, etc.

