#!/usr/bin/env python3

# Executable to run built-in tests and quickly check syntax errors.

from edag import make_component


# TODO: list['NET'], supported in python 3.9
def gate_and(name:str, *inputs:list, output:'NET'):
  todo


def gate_or(name:str, *inputs:list, output:'NET'):
  todo


def gate_nor(name:str, *inputs:list, output:'NET'):
  todo


def gate_nand(name:str, *inputs:list, output:'NET'):
  todo


def gate_xor(name:str, *inputs:list, output:'NET'):
  todo


def gate_not(name:str, input:'NET', output:'NET'):
  """Inverter"""
  todo


# In terms of primitivness we can have multiple levels:
#
# 1) none - use abstract part.
#
# 2) equiv - do some minor exchanges, i.e. T flip-flop can be trivially
#    implemented from a single JK flip-flop with no extra components.
#
# 3) standard - for complex parts that are composed of smaller abstract
#    parts, i.e. dual-edge-triggered D flip-flop can be implemented as 2
#    D-flip-flops, inverter and multipliex
#
# 4) primitive - use only and, or, nor, nand, xor, not gates. synthetize
#    i.e. for FPGA or distribution across ICs. This often will be followed by
#    logic simplification, common expression elimination, inverter folding,
#    multi-input folding, etc, and other logical optimisations, followed by
#    translation to only supported gate types (i.e. NAND + NOT, or something
#    like this), followed by logic synthesis.
#
# 5) transistor - i.e. CMOC dynamic logic implementation using n and p
#    channel MOSFETs. For IC fabrication itself, spice simulations and
#    breadboard education.
#
# This library of logical components allows expressing things in first 4 levels,
# and converting some components to more primitive types.
#
# Selection of the primitivness level is done at creation stage. Default
# primitivness levels for various abstract parts, is set so it is easy to create
# it from available off-the-shelve ICs, like 7400 series logic. For example
# T flip-flop is converted to J-K flip-flop with proper nets. Small decoders
# are using multiplexers, or common decoders (BCD, 7-segment, etc). Complex ones
# use PLA or ROM based approach, etc. If the truth table is relatively simple,
# it synthesies it using dedicated gates.
#
# But in the future versions of the library it is possibel that there will
# be a post-processing function that does it for you based on policy.

def flipflop_nor(name:str, *,
                 s:'NET', r:'NET',
                 q:'NET', not_q:'NET'=None,
                 primitive:bool=True):
  """SR NOR latch.

  `not_q` is optional.

  If primitive is False, synthetize the flipflop / latch from NOR or NAND gates
  instead of using a single functional unit. This is useful for some simulations,
  or FPGA synthesis.
  """
  todo


def flipflop_nand(name:str, *,
                  not_s:'NET', not_r:'NET',
                  q:'NET', not_q:'NET'=None,
                  primitive:bool=True):
  """~S~R NAND latch."""
  pass


def flipflop_and_or(name:str, *,
                    s:'NET', r:'NET',
                    q:'NET',
                    primitive:bool=True):
  """SR AND-OR latch."""
  pass


# def flipflop_jk():
#   pass


def jk_latch():
  pass


def flipflop_gated_sr(name:str, *,
                      s:'NET', r:'NET',
                      q:'NET', not_q:'NET'=None,
                      e:'NET'=None,
                      primitive:bool=True):
  pass


def gated_d_latch(name:str, *,
                  d:'NET', e:'NET',
                  q:'NET', not_q:'NET'=None,
                  primitive:bool=True):
  # By default it will use ~S~R NAND latch internally if using primitive.
  pass


def earle_latch(name:str, *,
                d:'NET', e_l:'NET',
                e_h:'NET', q:'NET',
                primitive:bool=True):
  """
  Another gated latch design with lower latency, but requires separate clocks.
  Often used in computers and pipelined computers, or when optimizing logic design.

  Atributed to John G. Earle when designing IBM System/360 Model 91.

  Clocks should be skewed with respect to each other to prevent logic hazards.
  """
  # By default it will use NAND gates internally if using primitive.
  pass


def flipflop_d(name:str, *,
               d:'NET', e:'NET',
               s:'NET'=None, r:'NET'=None,
               q:'NET', not_q:'NET'=None,
               primitive:bool=True):
  """Delay or data flip-flop.

  Captures state of `d` at rising edge of `e` and transfers atomically to 'q'.

  At other times (including being at high or level) q doesn't change.

  These are often used to create shift registers, specifically SIPO
  (serial-in, parallel-out) and SISO (serial-in / serial-out).
  But there is even more possibilities, including random
  number / bitstream generation, driving LED strings,
  parallel to serial decode maybe?
  """
  # Only d (data), e (enable, often called clock) and q (non-inverted output) are required.
  pass


# TODO: We can improve some common combinations of D flip-flops, like master-slave D flip-flop,
# can be realised as two D flip-flops and 1 inverter, but often are available as an integrated
# part with less internal gates, and obviously smaller footprint / better integration.


def flipflop_master_slave_d():
  pass


def flipflop_d_dualedge(name:str, *,
                        d:'NET', e:'NET',
                        q:'NET', not_q:'NET'=None,
                        primitive:bool=True):
  """Stores and transfers on both rising and falling edge of the clock.


  Can be implemented as two parallel D type flip-flops, one with inverted clock,
  and output multiplexer drive by clock.
  """
  pass


def flipflop_d_dynamic():
  """Often used in dynamic logic designs. Often state is stored in a capacitance of capacitor or gate."""
  pass


def flipflop_t(name:str, *,
               t:'NET', e:'NET',
               q:'NET', not_q:'NET'=None,
               primitive:bool=True):
  """Toggle flip-flop.

  If input is high, the state (and output) changes on each clock input strobe.

  If input is low, the state (and output) doesn't change.

  Can be synthetized using JK flip-flop (J&K connected together and act as T)
  or D flip-flop (T input xor Q_prev drives the D input).
  """
  return flipflop_jk(name, j=t, k=t, e=e, q=q, not_q=not_q, primitive=primitive)


def flipflop_jk(name:str, *,
                j:'NET', k:'NET',
                e:'NET',
                q:'NET', not_q:'NET'=None,
                primitive:bool=True):
  pass


def decoder():
  pass


def lut(name:str, *, inputs, output, table):
  """Lookup table decoder"""
  pass


# A some form of HDL based on something similar to ABEL maybe?
# For programming PLDs (PLA, PAL, GAL, FPGA).
