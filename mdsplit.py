# modified from https://github.com/markusstraub/mdsplit/blob/main/mdsplit.py

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

DEFAULT_MAX_LEVEL = 3
SPECIAL_MAX_LEVEL = 4
SPECIAL_HEADING = 'COMMAND INTERFACE'
SKIP_LEVEL = 2


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
		return HeadingLine(line, len(match[1]), match[2].strip())
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

			cur_parent_headings = [
				*cur_parent_headings[: cur_heading_line.heading_level - 1],
				cur_heading_line.heading_title,
			]
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

input = Path(args.input)
output = Path(args.output)

hash_to_headings: dict[str, list[str]] = {}

with open(input) as file:
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

with open(input) as file:
	for chapter in split_by_heading(file):
		if chapter.heading.heading_level <= SKIP_LEVEL:
			continue

		filename = output
		for h in [*chapter.parent_headings[SKIP_LEVEL:], chapter.heading.heading_title]:
			filename /= to_filename(h)
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

		with open(f'{filename}.md', 'w') as file:
			file.write('---\n')
			if chapter.heading.heading_level == 3 and chapter.heading.heading_title.isupper():
				title = ' '.join(
					map(
						lambda w: {
							'MACOS': 'macOS',
							'JAVASCRIPT': 'JavaScript',
							'JSON': 'JSON',
							'GUI': 'GUI',
							'IPC': 'IPC',
							'(LIBMPV)': '(libmpv)',
							'ON': 'on',
							'INTO': 'into',
						}.get(w, w.title()),
						chapter.heading.heading_title.split(),
					)
				)
				file.write(f'title: {title[0].upper()}{title[1:]}\n')
			else:
				file.write(f'title: {chapter.heading.heading_title}\n')
			file.write('---\n\n')
			for line in chapter.lines[2:]:  # skip heading
				file.write(re.sub(r'\(#(.+?)\)', transform_link, line))
