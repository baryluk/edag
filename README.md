Prototype of creating electric nets / schematics, without visual
schematic.

The scripts generate nets for KiCad pcbnew so it can be layed down. It can also
output dot format for graphviz, and netlists for spice simulations. It can
probably also be used for IC design, and other complex designs, but I have zero
expirience in this area, or the tools used to do that.

Nets and components can be created programatically, so you can reuse
sub-circuits, make parametrized parts (i.e. filters, various other
blocks), do iteration, recursion, etc.

The tricky part is keeping the designators stable between runs, even if
new components are added, or some are removed from the middle of the code
stream. The naive sequential numbering will not work, as it will disrupt
all desginators (annotations), which is a problem, because if the output
netlist is used for doing PCB layout (i.e. in pcbnew), person starts
doing a layout, then one changes the schematic in edag program (i.e. adds
a bunch of resistors in the middle of the program), and then regenerate a
net net list, all subsequent resistors would get new designators, which
can seriously screw things up, or make the previous work almost ruined.

So this library tracks a lot of details, like type, name, sub-schematic,
backtrace, nominal value, scope, and other user defined features, to make
component designators as stable as possible.

During export the extra file with all the details is written, and during next
runs it is read back and analyzed during new export.

The naming of nets is less important, but the program tries to keep net names and
their indexes stable too.

Check test.py for example of using various features.

Components and other functions (including decorators) do have extensive
documentation that can be accessed from python using help() command.

Simple generic components are available in `edag_components.py`.

More complex or non-generic parts are in `parts/` directory.

Only functions and classes with explicit documentations are considered a
public API of this library.

The other stuff is internal and subject to change in name, functionality,
semantics, etc. In particular all definition starting with underscore,
are private and should not be used by users.
