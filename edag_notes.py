#!/usr/bin/env python3

from contextlib import ContextDecorator
from collections import namedtuple

shared_notes_stack = []


class SharedNote(ContextDecorator):
  def __init__(self, note):
    self.note = note

  def __enter__(self):
    global shared_notes_stack
    shared_notes_stack.append(self.note)
    return self

  def __exit__(self, type, value, traceback):
    global shared_notes_stack
    popped = shared_notes_stack.pop()
    assert popped == self.note


def note(note):
  return SharedNote(note)


Comment = namedtuple("Comment", "comment")


def comment(comment):
  return SharedNote(Comment(comment))


PlacementHint = namedtuple("PlacementHint", "hint")


def placement_hint(hint):
  return SharedNote(PlacementHint(hint))


Warning = namedtuple("Warning", "warning")


def warning(warning):
  return SharedNote(Warning(warning))
