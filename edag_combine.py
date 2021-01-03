#!/usr/bin/env python3

# TODO(baryluk): It would be nice to say something like this:
# parallel(series(res, cap), series(res, res, cap), cap, cap).
# Super useful for building compensation networks, filters, etc.

# This should only be really usable for two-pin devices, but
# technically a parallel could work with more I guess, as long
# as all of them have same pin names.


# We need to create a meta-component, that is technically not registered, but
# is only used in case it is used in other parallel / series operations.

def parallel(*components):
  assert len(components) >= 1
  c0 = components[0]
  if isinstance(c0.pin_nets, list):
    pass
  pass

from edag import net
from edag_components import res

R12 = parallel(res("r1", "1k", a=net(), b=net()),
               res("r2", "2k", a=net(), b=net()))

R34 = parallel(res("r3", "3k", a=net(), b=net()),
               res("r4", "4k", a=net(), b=net()))

R5 = parallel(R12,
              res("r5", "5k", a=net(), b=net()))

RAll = parallel(R12, R34, R5)

parallel(R12, R12)  # This is the tricky one. That is very tricky.
# This one can be probably detected, but what about other cases like:

# parallel(R1, R2)
# parallel(R2, R1)

# This might create some strange things and shorts.


# In fact R12 is already problematic. calling res() registers the component and its nets,
# but parallel makes the connections between the possibly anonymous nets.


def series(*components):
  assert len(components) >= 1
  pass
