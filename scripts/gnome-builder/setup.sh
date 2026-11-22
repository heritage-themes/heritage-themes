#!/bin/sh
# Creates the Builder test project in DIR (default ~/heritage-builder-test) as a git repository whose working tree
# differs from its last commit, so that the gutter shows added, changed and removed lines, then opens it in Builder
# with --open. project/ holds the files and baseline/ the committed versions of those that differ.
set -eu
here=$(cd "$(dirname "$0")" && pwd)
dir=${1:-$HOME/heritage-builder-test}
[ -e "$dir" ] && { echo "$dir exists; remove it first" >&2; exit 1; }
mkdir -p "$dir"
cp "$here"/project/* "$dir"/
cp "$here"/baseline/* "$dir"/
git -C "$dir" init -q
git -C "$dir" add .
git -C "$dir" -c user.name=Test -c user.email=test@example.org commit -q -m "Baseline"
cp "$here"/project/* "$dir"/
echo "$dir"
if [ "${2:-}" = "--open" ]; then exec gnome-builder -p "$dir" "$dir/main.c"; fi
