# modified from https://github.com/markusstraub/mdsplit/blob/main/mdsplit.py

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

FENCES = ['```']
MAX_HEADING_LEVEL = 6

MAX_LEVEL = 3
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
		assert len(match[1]) <= MAX_HEADING_LEVEL
		return HeadingLine(line, len(match[1]), match[2].strip())
	return Line(line)


def split_by_heading(lines: Iterator[str]):
	cur_parent_headings: list[str] = []
	cur_heading_line = HeadingLine('# mpv', 1, 'mpv')
	cur_lines = []
	within_fence = False

	for line in map(parse_line, lines):
		if any(line.text.startswith(fence) for fence in FENCES):
			within_fence = not within_fence

		if not within_fence and isinstance(line, HeadingLine) and line.heading_level <= MAX_LEVEL:
			yield Chapter(cur_parent_headings[:-1], cur_heading_line, cur_lines)

			cur_parent_headings = [
				*cur_parent_headings[: cur_heading_line.heading_level - 1],
				cur_heading_line.heading_title,
			]
			cur_heading_line = line
			cur_lines = []

		cur_lines.append(line.text)

	yield Chapter(cur_parent_headings[:-1], cur_heading_line, cur_lines)


def to_filename(title: str):
	return '-'.join(re.findall(r'[\w\.]+', title)).lower()


parser = argparse.ArgumentParser()
parser.add_argument('input', help='input file')
parser.add_argument('output', help='output folder')
args = parser.parse_args()

input = Path(args.input)
output = Path(args.output)
output.mkdir(parents=True, exist_ok=True)

hash_to_headings: dict[str, list[str]] = {}

with open(input) as file:
	cur_parent_headings: list[str] = []
	cur_heading_line = HeadingLine('# mpv', 1, 'mpv')
	within_fence = False

	for line in map(parse_line, file):
		if any(line.text.startswith(fence) for fence in FENCES):
			within_fence = not within_fence

		if not within_fence and isinstance(line, HeadingLine):
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

		def transform_link(m: re.Match[str]):
			headings = hash_to_headings.get(m[1])
			if headings is None:
				print(f'Fail to link to #{m[1]}')
				return m[0]

			page_heading, *headings = headings[SKIP_LEVEL:]
			hash = f'#{m[1].replace(".", "")}'
			return (
				f'({hash})'
				if page_heading == chapter.heading.heading_title
				else f'({to_filename(page_heading)}.md{hash if headings else ""})'
			)

		assert not chapter.parent_headings[SKIP_LEVEL:]
		filename = to_filename(chapter.heading.heading_title)
		with open((output / filename).with_suffix('.md'), 'w') as file:
			file.write('---\n')
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
					}.get(w, w.title())
					if w.isupper()
					else w,
					chapter.heading.heading_title.split(),
				)
			)
			file.write(f'title: {title[0].upper()}{title[1:]}\n')
			file.write('---\n\n')
			for line in chapter.lines[2:]:  # skip heading
				file.write(re.sub(r'\(#(.+?)\)', transform_link, line))
