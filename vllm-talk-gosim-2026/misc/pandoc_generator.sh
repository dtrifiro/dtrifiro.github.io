#!/bin/bash

source_file="markdown/vllm-pandoc.md"
output_file="pandoc-index.html"
theme="black"

pandoc --standalone \
	-t revealjs \
	-o "${output_file}" \
	-V revealjs-url='' \
	-V theme="$theme" \
	$source_file
