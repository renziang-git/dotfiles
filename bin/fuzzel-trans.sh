#!/bin/sh

text="$*"
[ -z "$text" ] && exit 0

trans -b "$text"

