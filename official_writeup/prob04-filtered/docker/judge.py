#!/usr/bin/env python3

from tempfile import NamedTemporaryFile
import subprocess
import re
from brainfuck import to_function


LEVEL1 = ['empty.txt', 'newlines.txt',
          'haruhikage.txt', 'yoomu.txt', 'xqc.txt']
LEVEL2 = ['empty.txt', 'newlines.txt',
          'haruhikage.txt', 'yoomu.txt', 'xqc.txt']
LEVEL3 = ['hello.txt', 'ayaka.txt']


NEWLINES = re.compile(r'\n+')


def show_flag(id: int) -> None:
  '''
  Prints the flag of the given ID to `stdout`.
  '''
  with open(f'/flag{id}') as f:
    print(f.read())


def run_program(program: str, input: str) -> str:
  '''
  Runs the given program with the given input.

  Returns the output.
  '''
  try:
    result = subprocess.run(f'python3 filtered.py {program} {input}',
                            shell=True, timeout=60, stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')
  except subprocess.TimeoutExpired:
    print('超时了喵（60s 喵）')
    exit(-1)


def judge_level1(program: str) -> bool:
  '''
  Judges the result of level 1.

  Returns `True` if passes.
  '''
  for input in LEVEL1:
    out = run_program(program, f'input/{input}')
    with open(f'input/{input}') as f:
      if out.strip() != str(len(f.read())):
        return False
  return True


def get_statistics(s: str) -> tuple[dict[str, int], list[str]]:
  '''
  Returns statistics and lines of the given string.
  '''
  stats = {}
  lines = NEWLINES.split(s.strip('\n'))
  for line in lines:
    stats[line] = stats.get(line, 0) + 1
  return stats, lines


def judge_level2(program: str) -> bool:
  '''
  Judges the result of level 2.

  Returns `True` if passes.
  '''
  for input in LEVEL2:
    out = run_program(program, f'input/{input}')
    out_stats, out_lines = get_statistics(out)
    with open(f'input/{input}') as f:
      ref_stats, _ = get_statistics(f.read())
    if out_stats != ref_stats:
      return False
    last_len = 0
    for line in out_lines:
      if len(line) < last_len:
        return False
      last_len = len(line)
  return True


def judge_level3(program: str) -> bool:
  '''
  Judges the result of level 3.

  Returns `True` if passes.
  '''
  for input in LEVEL3:
    out = run_program(program, f'input/{input}')
    with open(f'input/{input}') as f:
      ref = to_function(f.read())()
    if out.strip() != ref.strip():
      return False
  return True


def read_program() -> str:
  '''
  Reads program from `stdin`.

  Returns the path to program file.
  '''
  program = b''
  eof = '谢谢喵'.encode('utf-8')
  while True:
    line = input().encode('utf-8')
    program += line + b'\n'
    if line.strip() == eof:
      break
    assert len(program) <= 64 * 1024
  with NamedTemporaryFile(delete=False) as f:
    f.write(program)
    return f.name


if __name__ == '__main__':
  print('欢迎喵，来跟我比划比划喵！')
  print('1. 字数统计喵')
  print('2. 排序喵')
  print('3. Brainfuck 喵')
  try:
    id = int(input('选一个喵（1-3）：').strip())
    if id < 1 or id > 3:
      raise RuntimeError
    id -= 1
  except:
    print('不对喵，哭哭喵，再见喵！')
    exit(-1)

  print()
  print('输入替换规则喵，规则长度不能超过 64KB 喵：')
  program = read_program()

  if [judge_level1, judge_level2, judge_level3][id](program):
    print('对了喵，太好了喵！')
    show_flag(id)
  else:
    print('输出好像不太对喵，你再想想喵，别急急急急急急喵！')
    exit(-1)
