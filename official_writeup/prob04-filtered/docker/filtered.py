#!/usr/bin/env python3

import re
from re import Pattern
from dataclasses import dataclass
from typing import TextIO


RE_REPLACE = re.compile(r'^(重复)?把【([^】]+)】替换成【([^】]*)】(喵)?$')
RE_BRANCH = re.compile(r'^如果(没)?看到【([^】]+)】就跳转到【([^】]+)】(喵)?$')
RE_LABEL = re.compile(r'^(.+)：$')


class Inst:
  pass


@dataclass(frozen=True)
class Replace(Inst):
  repeat: bool
  regex: Pattern[str]
  to: str


@dataclass(frozen=True)
class Branch(Inst):
  neg: bool
  regex: Pattern[str]
  label: str


@dataclass(frozen=True)
class Machine:
  insts: list[Inst]
  labels: dict[str, int]

  def run(self, s: str) -> str:
    pc = 0
    while pc < len(self.insts):
      inst = self.insts[pc]
      pc += 1
      if isinstance(inst, Replace):
        if inst.repeat:
          while inst.regex.search(s):
            s = inst.regex.sub(inst.to, s)
        else:
          s = inst.regex.sub(inst.to, s)
      elif isinstance(inst, Branch):
        if inst.neg != bool(inst.regex.search(s)):
          pc = self.labels[inst.label]
    return s


def parse(f: TextIO) -> Machine:
  insts = []
  labels = {}
  for no, line in enumerate(f):
    line = line.strip()
    if replace := RE_REPLACE.findall(line):
      repeat, regex, to, meow = replace[0]
      if not meow:
        raise RuntimeError(f'第 {no + 1} 行，你怎么不喵😡😡😡')
      insts.append(Replace(bool(repeat), re.compile(regex), to))
    elif jump := RE_BRANCH.findall(line):
      neg, regex, label, meow = jump[0]
      if not meow:
        raise RuntimeError(f'第 {no + 1} 行，你怎么不喵😡😡😡')
      insts.append(Branch(bool(neg), re.compile(regex), label))
    elif label := RE_LABEL.findall(line):
      labels[label[0]] = len(insts)
    elif line == '谢谢喵':
      break
  else:
    raise RuntimeError('你怎么不说谢谢😡😡😡')
  return Machine(insts, labels)


if __name__ == '__main__':
  import sys
  if len(sys.argv) < 3:
    print(f'用法喵：{sys.argv[0]} 规则文件喵 输入文件喵', file=sys.stderr)
    exit(1)

  with open(sys.argv[1]) as f:
    machine = parse(f)

  with open(sys.argv[2]) as f:
    s = f.read()

  print(machine.run(s))
