#!/usr/bin/env python3

# Only functions and classes with explicit documentations are considered
# a public API of this library.
#
# The other stuff is internal and subject to change in name, functionality,
# semantics, etc. In particular all definition starting with underscore,
# are private and should not be used by users.


from collections import namedtuple, defaultdict, Counter
import traceback

import edag_utils

Net = namedtuple("net", ["name"])


class Schematic(object):
  def __init__(self):
    self.anonymous_nets = []

    # This is a stack of scopes. The current scope is at the end.
    self.scopes = []
    # This is a tree of scopes. Each scope is persistently stored here, even
    # after exiting the scope. Tree only is extended on right sides of each
    # level.
    self.scopes_tree = []
    # This is a path in the tree to the current scope.
    self.scopes_path = [0]

    # This really is a tree, not a stack, because we want to remember all used nets.
    self.scoped_nets_stack = []

    # This is a list of strings, designating a scope path.
    # NewScope object will store a snapshot of it, as well
    # pre-computed string for the full path.
    self.scoped_nets_stack_path = []

    # Initialize the bottom (and current top) of the stack.
    self.scoped_nets_stack_path.append("root")

    # Components within a current scope, possibly with scoped nets.
    # Used by SubschematicCapture
    self.current_scope = None  # To properly set 'parent'.
    self.current_scope = self.new_scope(node_i=0)
    print(self.current_scope)

    self.scopes.append(self.current_scope)
    assert self.scopes[0] is self.current_scope

    self.scoped_nets_stack.append([])  # Empty root.

    # Insert as a root scope.
    self.scopes_tree.append(self.current_scope)

    # All components in a schematic, from all scopes.
    self.registered_components = []

    # Various ids used within a schematic for designators and referencing.
    self.global_id = 0
    self.component_id = defaultdict(int)
    self.stable_component_ids = defaultdict(lambda: defaultdict(int))
    self.stable_net_ids = {}

  class _NewScope(object):
    def __init__(self, path:str, parent:'_NewScope_or_None', node_i:int):
      self.path = list(path)   # Make a copy!
      self.path_string = "/".join(path)
      # self.registered_components = []
      self.own_nets = {}
      self.sub_scopes = []
      # Index with-in nodes (sub_scopes) of the parent of this scope.
      self.node_i = 0
      self.parent = parent  # Could be None for the top of scopes
      # if parent:
      #   assert self.parent.sub_scopes[self.node_i] is self

  def new_scope(self, node_i):
    s = self._NewScope(self.scoped_nets_stack_path, self.current_scope, node_i)
    # assert s.parent.sub_scopes[s.node_i] is s
    # assert self.current_scope is s.parent
    return s

  def net(self, name:str = None):
    if name:
      assert "/" not in name
      return Net(name)
    l = len(self.anonymous_nets)
    new_net = Net(f"anon_{l}")
    self.anonymous_nets.append(new_net)
    return new_net

  def register_component(self, component):
    self.registered_components.append(component)

  def Scope(self, scope_args = None):
    def decer(func):
      def dec(*args, **kwargs):
        print("BEFORE current scopes stack:", self.scopes)
        print("BEFORE current scopes tree:", self.scopes_tree)
        print("BEFORE current scopes path:", self.scopes_path)

        depth = 0
        node_i = self.scopes_path[depth]
        node = self.scopes_tree[node_i]
        # print(f"node_i = {node_i}")
        print(f"{self.scopes_path}")
        # This is not super, efficient, but entering new scope shouldn't be too
        # frequent, and the scopes_tree depth is small, so should be ok.
        while depth < len(self.scopes_path) - 1:
          node_i = self.scopes_path[depth]
          node = node.sub_scopes[node_i]
          depth += 1

        self.scopes_path.append(len(node.sub_scopes))
        self.scoped_nets_stack_path.append(f"scope_{node_i}")

        prev_scope = self.current_scope
        new_scope_ = self.new_scope(node_i)  # NewScope(self.scoped_nets_stack_path)
        self.current_scope = new_scope_

        self.scopes.append(new_scope_)

        print("DURING current scopes stack:", self.scopes)
        print("DURING current scopes tree:", self.scopes_tree)
        print("DURING current scopes path:", self.scopes_path)

        print("running scoped function")
        r = func(*args, **kwargs)
        print("finishing scoped function")

        popped_scope = self.scopes.pop()
        node.sub_scopes.append(popped_scope)
        self.scopes_path.pop()
        self.scoped_nets_stack_path.pop()

        self.current_scope = prev_scope
        print(prev_scope)
        if __debug__:
          assert self.current_scope.path_string == "/".join(self.scoped_nets_stack_path)
          assert len(self.current_scope.path) == len(self.scoped_nets_stack_path)
          assert self.current_scope.path == self.scoped_nets_stack_path
          # assert self.current_scope.path is self.scoped_nets_stack_path

        print("AFTER  current scopes stack:", self.scopes)
        print("AFTER  current scopes tree:", self.scopes_tree)
        print("AFTER  current scopes path:", self.scopes_path)
        return r
      return dec
    decer.__doc__ = Scope.__doc__  # Self reference
    return decer

  def scoped_net(self, name:str = None):
    path = self.current_scope.path_string
    if name:
      assert "/" not in name
      return Net(f"{path}/{name}")
    l = len(self.scoped_nets_stack[-1])
    new_net = Net(f"{path}/anon_{l}")
    self.scoped_nets_stack[-1].append(new_net)
    return new_net

  # TODO: We might want a functionality to lookup nets up the scopes.
  # To basically provide nested net name resolution.
  # I.e. access some named nets from the parent scopes, but creat new ones
  # locally only (or for own sub-scopes).
  def lookup_net(self, name:str):
    pass

  def load_stable_ids(self):
    pass

  def save_stable_ids(self):
    print(dict(self.stable_component_ids))


# The top of the stack is the schematic we are working with now.
# All component, global and scoped nets will work on it implicitly.
# If a new schematic is created and pushed on the stack,
# it will have own namespace created from scratch.
_schematic_stack = []

# Alias to the top of the stack, to speed up operations.
_current_schematic = None


def NewGlobalScope():
  """This create a completly new global schematic scope.

  This can be created inside currently captured schematic,
  to create a new workspace, i.e. for optimisation processes,
  which might be exploring automatically various variants of a some electronic
  module, but should not be captured in the final output schematic.

  The schematics in this new global scope are in its own universe,
  and can't interact with each other or the parent global scope.

  At the end of the scope, one has an option to copy it back,
  and store somewhere, and if needed actually use ("emit").

  Global scopes can be nested. Each one is new and created from scratch.

  To pass some common circuits, they need to be recreated at the moment,
  which can be done easily via a factory function.
  """
  global _schematic_stack, _current_schematic
  new_schematic = Schematic()
  _schematic_stack.append(new_schematic)
  _current_schematic = _schematic_stack[-1]
  return new_schematic


# Initiailize default schematic.
NewGlobalScope()


def net(name:str = None):
  """Create a (global) net reference.

  If no name is given a new unique net is created, that can be used for
  components (or merging into other net if you really want to).

  If name is given create a net refernce that reference a global net of this
  net. To create local net, use scoped_net(name).
  """
  global _current_schematic
  return _current_schematic.net(name)


"""Global ground"""
GND = lambda: Net("GND")


def Scope(scope_args = None):
  """A decorator to make a function define a new schematic scope.

  Example:
    @Scope()
    def psu():
      output = scoped_net("output")
      gnd = scoped_net("gnd")
      lm7805("regulator", input=net(), gnd=gnd, output=output)
      with note("load"):
         res("load_resistor", 100, a=output, b=gnd)

  The gnd and output are scoped net, that are unique only in the current scope.
  Using them again anywhere else in a schematic again, including other calls
  to `psu` function, will use different nets.

  scoped nets can be accessed by caller, and if appropriate merged.
  scoped net can also be passed around to other components and sub-scopes,
  both by the current scope, sub-scopes, or by the caller.

  Scopes are also used for documentation and for ensuring stable net
  names / designators, and component designators. Otherwise adding or removing
  a single component, could renumerate annotations / designators of a lot
  of other components, which would make incremental work on the output
  (i.e. PCB layout) extreamlly hard.

  Scope path (together with component type, name, and scoped net names, and
  sometimes component nominal value or comment, and order within a scope)
  usually provides means to ensure the designators are the same as in previous
  runs.

  Backtrace during component creation, filename and line, can also be used for
  ensuring designator stability, but they are less reliable than explicit scopes
  and names.
  """
  global _current_schematic
  return _current_schematic.Scope(scope_args)


"""
BEFORE current scopes stack: []
BEFORE current scopes tree: []
BEFORE current scopes path: [0]
DURING current scopes stack: [{}]
DURING current scopes tree: []
DURING current scopes path: [0, 0]
running scoped function
finishing scoped function
AFTER  current scopes stack: []
AFTER  current scopes tree: [{}]
AFTER  current scopes path: [0]
BEFORE current scopes stack: []
BEFORE current scopes tree: [{}]
BEFORE current scopes path: [0]
DURING current scopes stack: [{}]
DURING current scopes tree: [{}]
DURING current scopes path: [0, 1]
running scoped function
finishing scoped function
AFTER  current scopes stack: []
AFTER  current scopes tree: [{}, {}]
AFTER  current scopes path: [0]
"""

# TODO(baryluk): Add tests for this.


def scoped_net(name=None):
  """Create a scoped net reference.

  Scoped net will only be valid for a specific scope, and same name
  can be used in different scopes, referncing different physical nets.

  For clairy, the 'name' should not conflict with any global net,
  but it is supported. The scoped and global net will be referencing
  different physical nets.

  If the name is not given, it will create an anonymous new unique net,
  just like net(), but capturing extra trace information from the scope,
  which might be useful when referncing things manually.
  """
  global _current_schematic
  return _current_schematic.scoped_net(name)


# pin_nets is either list or dict.
# common_properties is a dict.
# own_properties is of component defined type, i.e. for capacitor it can be capacitance,
# for a resistor it can be a tuple of resistance and rated power,
# for a ac voltage source it can be frequency and amplitude, etc.

Component = namedtuple("Component", ["name",
                                     "type",
                                     "id",
                                     "global_id",
                                     "pin_nets",
                                     "common_properties",
                                     "own_properties",
                                     "notes"])


import edag_notes

# Public: Default number of digits in the numeric part of a designator. i.e. 3 => "C001"
designator_digits = 1


def make_component(name:str,
                   type:str,
                   pin_nets:'DICT_OR_LIST',
                   common_properties:'DICT_OR_LIST',
                   own_properties:'ANY',
                   *,
                   prefix:str = None,
                   notes = [],
                   nopop:bool = False,
                   simonly:bool = False):
  """Create an instance of a component.

  This function can be used by user directly, or by component libraries.
  Most users will wrap this function into handy helper, or autogenerate these
  helpers for a big class of similar components.

  Note that this doesn't create a component class or type. It actually creates
  a singular specific component.

  The function itself is a component class.

  Call to the function resturns a specific instance of a component belonging to
  this class.

  Calling this function twice with exactly same parameters, will return new
  component instance.

  This function will automatically assign a designator based on various factors,
  like type, name, value, scope, backtrace, prefix, sequential order within a
  program or scope.

  Example:
    name: "5v regulator"
    type: "lm7805"
    pin_nets: dict or list
    common_properties: list or dict, things like comment, datasheet URL, package
                       type, footprint, power rating, voltage rating, tolerance
    own_properties: per-type properties. arbitrary type, value, list, dict,
                    etc. i.e. for capacitor it is capacitance.
    prefix: "M"
    notes: ["Place close to the edge of board for heatsink attachment"]
    nopop: False; If true, place a footprint, but don't put a component during
                  assembly.
    simonly: False; If true, don't create footprint for PCB, only create a
                    reference for simulation (i.e. voltage probe between two
                    nets).

    TODO: Current measurements in simonly. I.e. in simulation we want a current
    sensor with name, but during layout we want a short, with same net name on
    both sides.

  package type and footprint are separate. I.e. same cap can be in many
  different packages, same package can have many different footprints, i.e.
  high density vs low density, universal vs specialized, hand soldered vs pick
  and place.

  Other common_properties: layout_notes (i.e. placement hints), bom_notes
  (i.e. sourcing restrictions for things like capacitors, resistors, etc),
  mechanical_notes, assembly_notes, user_documentation (i.e. description of
  jumpers, test points, etc), test_point_notes (i.e. to specify information
  about, test points, and tolerances of voltages when doing diagnostic, repair
  or testing during assembly or rapair, etc).

  name is a user provided name. Not only it is used as a documentation and
  comment, but it required to provide stable designator references in the
  generated files. If not provided (i.e. empty or same for many components), the
  names might change between runs, making it hard to do incremental changes
  concurrently with PCB layout work.
  """
  global _current_schematic

  _current_schematic.global_id += 1

  tb = traceback.extract_stack()
  for tf in tb[:-1]:
    if 'contextlib.py' in tf.filename:
      continue
    # print(f"    {tf.filename}:{tf.lineno} function {tf.name} : {tf.line} # Locals: {tf.locals}")

  # designator prefix
  prefix = prefix if prefix else type

  if _current_schematic.stable_component_ids[type][name] and False:
    id = _current_schematic.stable_component_ids[type][name]
  else:
    _current_schematic.component_id[type] += 1
    id = prefix + str(_current_schematic.component_id[type])
    _current_schematic.stable_component_ids[type][name] = id
  full_notes = notes + edag_notes.shared_notes_stack

  assert isinstance(pin_nets, dict) or isinstance(pin_nets, list)

  if common_properties and 'pin_map' in common_properties:
    pin_map = common_properties['pin_map']
    assert isinstance(pin_map, dict)

    _all_pins_numbers = {}
    for pin_key, pin_list in pin_map.items():
      assert isinstance(pin_key, str) or isinstance(pin_key, int), f"pin_map keys must be str or int, but found: {pin_key}: {pin_list}"

      assert isinstance(pin_list, list) or isinstance(pin_list, int), f"pin_map values must be int or list of ints, but found: {pin_key}: {pin_list}"
      if isinstance(pin_list, int):
        pin_list = [pin_list]
      assert len(pin_list) > 0, f"pin_map value should be not an empty list, but found: {pin_key}: {pin_list}"  # TODO(baryluk): Maybe there is a use for empty lists?
      for pin in pin_list:
        if pin in _all_pins_numbers:
          assert False, f"Duplicate pin {pin} found in {pin_key} and {_all_pins_numbers[pin]}"
      for pin in pin_list:
        _all_pins_numbers[pin] = pin_key

    # Assert that every used pin is in the pin_map.
    if isinstance(pin_nets, dict):
      for pin_key in pin_nets.keys():
        assert pin_key in pin_map, f"A pin key {pin_key} from pin_net dict, not found in pin_map"
    elif isinstance(pin_nets, list):
      for pin_key, _ in enumerate(pin_nets):
        assert pin_key in pin_map, f"A pin key {pin_key} from pin_net list, not found in pin_map"
    else:
      assert False, f"Impossible condition. Internal error or incorrect type for pin_nets parameter (can be dict or list), found: {type(pin_nets)}"

    # Check the reverse. That every pin in pin_map is used in the pin_nets.
    # TODO(baryluk): Possibly using metadata in the pin_map to tell which ones
    # are OK to be unconnected.
    for pin_key, pin_list in pin_map.items():
      if isinstance(pin_nets, dict):
        assert pin_key in pin_nets, f"A pin_key {pin_key} from pin_map key, not found in pin_nets dict"
      elif isinstance(pin_nets, list):
        assert isinstance(pin_key, int)
        assert pin_nets[pin_key] is not None, f"A pin_key {pin_key} from pin_map key, not found in pin_nets list"  # What? This looks like  a typo maybe?
      else:
        assert False

  c = Component(name, type, id, _current_schematic.global_id, pin_nets, common_properties, own_properties, full_notes)
  _current_schematic.register_component(c)
  return c


tofloat = edag_utils.tofloat


from contextlib import ContextDecorator


class SubschematicCapture(object):
  def __init__(self, name=None):
    global _current_schematic
    self.name = name
    self.parent_schematic = _current_schematic
    # self.path = path + [name]

  def __enter__(self):
    global _current_schematic
    assert self.parent_schematic is _current_schematic
    self.old_state = _current_schematic.current_scope
    _current_schematic.current_scope = _current_schematic.new_scope(node_i=0)
    return self

  def captured(self):
    global _current_schematic
    assert self.parent_schematic is _current_schematic
    return _current_schematic.current_scope

  def __exit__(self, type, value, traceback):
    global _current_schematic
    assert self.parent_schematic is _current_schematic
    self.captured = _current_schematic.current_scope
    _current_schematic.current_scope = self.old_state
    return


def sub(function, *args, **kwargs):
  """A function to instantiate a subschematic function and capture all components
  and nets created during call to subschematic.

  Example:

    def mycircuit(resistance):
      vs = voltage_source(voltage=10)
      res("load", resistance, a=vs.pin_nets[0], b=vs.pin_nets[1])

    m1 = sub(mycircuit, "1k")
    m2 = sub(mycircuit, "2k")
  """
  with SubschematicCapture() as sc:
    function(*args, **kwargs)
    return sc.captured()


# Aka node
Pin = namedtuple("Pin", ["id", "component_global_id", "pin"])


def export():
  """Export all components and connected nets, as a netlist in KiCad pcbnew compatible format.

  This also saves a database with all captured internal information about
  schematic, components and nets. These information are used in subsequent
  runs to ensure stable designators.
  """
  return export_(_current_schematic)


def export_(self):
  print("(export (version D)")
  used_nets = Counter()
  net_pins = defaultdict(list)
  print("  (components")
  for component in self.registered_components:
    value = component.own_properties if component.own_properties else component.type
    print(f"    (comp (ref {component.id}) (value {value}) (footprint X) "
          f"(sheetpath (names /) (tstamps /)) (tstamp 5F9A2166)) "
          f" # \"{component.name}\"; {'; '.join(repr(note) for note in component.notes)}")
    if type(component.pin_nets) is list:
      for pin, net in enumerate(component.pin_nets):
        # print(net)
        used_nets[net.name] += 1
        net_pins[net.name].append(Pin(component.id, component.global_id, pin))
    else:
      for pin_name, net in component.pin_nets.items():
        # print(net)
        used_nets[net.name] += 1
        net_pins[net.name].append(Pin(component.id, component.global_id, pin_name))
  print("  )")

  print("  (nets")
  i = 0
  for net_name, component_count in used_nets.items():
    i += 1
    print(f"    (net (code {i}) (name \"{net_name}\")")
    for pin in net_pins[net_name]:
      print(f"      (node (ref {pin.id}) (pin {pin.pin}))")
    print("    )")
  print("  )")

  print(")")


def process(schematic_function):
  """Processes a schematic function. This will do all processing, import of old
  ids, build schematic with components and nets, do an export and save new ids.

  Example:

    def mycircuit():
      vs = voltage_source(voltage=10)
      res("load", "1k", a=vs.pin_nets[0], b=vs.pin_nets[1])

    process(mycircuit)


  If you want to pass extra parameters to mycircuit, simply wrap it in an extra lever of indirection:

    def mycircuit(resistance, voltage):
      vs = voltage_source(voltage=voltage)
      res("load", resistance, a=vs.pin_nets[0], b=vs.pin_nets[1])

    def mycircuit_full():
      mycircuit(resistance="1k", voltage=10)

    process(mycircuit_full)


    The capture of the schematic is fully implicit. The schematic function itself
    doesn't need to return any value. All build components will be captured
    automatically (it is possible to supress some components and nets, by using
    special scopes).
  """
  if True:  # with NewGlobalScope() as schematic:
    schematic = _current_schematic

    assert _current_schematic is schematic
    assert _schematic_stack[-1] is schematic
    schematic.load_stable_ids()
    schematic_function()
    export_(schematic)
    schematic.save_stable_ids()


def DifferentialPair():
  pass


# Length matched traces, phase matched traces.
def PhaseMatchedBus():
  pass


# For length matching of T junctions, etc.
def BifurcationPoint():
  pass


# TODO: There might be more to it, ie. there might be termination
# resistors or copouling capacitors, where some sections of various nets
# need to have various length / phase matching requirements.
