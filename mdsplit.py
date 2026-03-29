# modified from https://github.com/markusstraub/mdsplit/blob/main/mdsplit.py

import argparse
import copy
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

SKIP_LEVEL = 2
DEFAULT_MAX_LEVEL = 3
SPECIAL_MAX_LEVEL = 4
SPECIAL_HEADING = 'Command interface'
INDEX_HEADING = 'Description'


@dataclass
class Line:
	text: str


@dataclass
class HeadingLine(Line):
	heading_level: int
	heading_title: str


@dataclass
class Chapter:
	parent_headings: list[str]
	heading: HeadingLine
	lines: list[str]


def parse_line(line: str):
	if match := re.match(r'(#+)(.+)', line):
		level = len(match[1])
		title = match[2].strip()
		if level == 3 and title.isupper():
			first, *rest = title.split()
			dict = {
				'MACOS': 'macOS',
				'WINDOWS': 'Windows',
				'JAVASCRIPT': 'JavaScript',
				'JSON': 'JSON',
				'GUI': 'GUI',
				'IPC': 'IPC',
			}
			title = ' '.join([dict.get(first, first.title()), *(dict.get(w, w.lower()) for w in rest)])
		return HeadingLine(line, level, title)
	return Line(line)


def split_by_heading(lines: Iterator[str]):
	cur_parent_headings: list[str] = []
	cur_heading_line = HeadingLine('# mpv', 1, 'mpv')
	cur_lines = []

	def parents():
		return cur_parent_headings[: cur_heading_line.heading_level - 1]

	for line in map(parse_line, lines):
		max_level = (
			SPECIAL_MAX_LEVEL
			if SPECIAL_HEADING in [*parents(), cur_heading_line.heading_title]
			else DEFAULT_MAX_LEVEL
		)
		if isinstance(line, HeadingLine) and line.heading_level <= max_level:
			yield Chapter(parents(), cur_heading_line, cur_lines)

			cur_parent_headings = [*parents(), cur_heading_line.heading_title]
			cur_heading_line = line
			cur_lines = []

		cur_lines.append(line.text)

	yield Chapter(parents(), cur_heading_line, cur_lines)


def to_filename(title: str):
	return '-'.join(re.findall(r'[\w\.]+', title)).lower()


parser = argparse.ArgumentParser()
parser.add_argument('input', help='input file')
parser.add_argument('output', help='output folder')
args = parser.parse_args()
output = Path(args.output)

hash_to_headings: dict[str, list[str]] = {}
with open(args.input) as file:
	cur_parent_headings: list[str] = []
	cur_heading_line = HeadingLine('# mpv', 1, 'mpv')

	for line in map(parse_line, file):
		if isinstance(line, HeadingLine):
			cur_parent_headings = [
				*cur_parent_headings[: cur_heading_line.heading_level - 1],
				cur_heading_line.heading_title,
			]
			hash = to_filename(cur_heading_line.heading_title)
			hash_to_headings[hash] = cur_parent_headings
			cur_heading_line = line

with open('zensical.toml') as file:
	zensical = file.readlines()

NavItems = list[dict[str, 'str | NavItems']]
nav: NavItems = []
with open(args.input) as file:
	for chapter in split_by_heading(file):
		if chapter.heading.heading_level <= SKIP_LEVEL:
			continue

		filename = output
		for h in [*chapter.parent_headings[SKIP_LEVEL:], chapter.heading.heading_title]:
			filename /= to_filename(h)
		if chapter.heading.heading_title == SPECIAL_HEADING:
			chapter = copy.deepcopy(chapter)
			chapter.parent_headings.append(chapter.heading.heading_title)
			chapter.heading.heading_level += 1
			filename /= 'index'
		elif chapter.heading.heading_title == INDEX_HEADING:
			filename = filename.with_name('index')
		filename = filename.with_name(f'{filename.name}.md')
		filename.parent.mkdir(parents=True, exist_ok=True)

		def transform_link(m: re.Match[str]):
			headings = hash_to_headings.get(m[1])
			if headings is None:
				print(f'Fail to link to #{m[1]}')
				return m[0]

			max_level = SPECIAL_MAX_LEVEL if SPECIAL_HEADING in headings else DEFAULT_MAX_LEVEL
			ref = output
			for h in headings[SKIP_LEVEL:max_level]:
				ref /= to_filename(h)
			ref = ref.relative_to(filename.parent, walk_up=True)
			hash = f'#{m[1].replace(".", "")}'
			return (
				f'({hash})'
				if str(ref) == to_filename(chapter.heading.heading_title)
				else f'({ref}.md{hash if headings[max_level:] else ""})'
			)

		with open(filename, 'w') as file:
			file.write('---\n')
			file.write(f'title: {chapter.heading.heading_title}\n')
			file.write('---\n\n')
			for line in chapter.lines[2:]:  # skip heading
				file.write(re.sub(r'\(#(.+?)\)', transform_link, line))

		cursor = nav
		for h in chapter.parent_headings[SKIP_LEVEL:]:
			if cursor and h in cursor[-1]:
				cursor = cursor[-1][h]
				assert not isinstance(cursor, str)
			else:
				children: NavItems = []
				cursor.append({h: children})
				cursor = children
		cursor.append({chapter.heading.heading_title: str(filename.relative_to(output))})


with open('zensical.toml', 'w') as file:

	def write(items: NavItems, indent=1):
		for item in items:
			k = next(iter(item))
			v = item[k]
			file.write(' ' * indent * 4)
			file.write(f'{{ "{k}" = ')
			if isinstance(v, str):
				file.write(f'"{v}" }},\n')
			else:
				file.write('[\n')
				write(v, indent + 1)
				file.write(' ' * indent * 4)
				file.write('] },\n')

	in_nav = False
	for line in zensical:
		if in_nav and line == ']\n':
			in_nav = False
		if not in_nav:
			file.write(line)
		if line == 'nav = [\n':
			in_nav = True
			write(nav)
