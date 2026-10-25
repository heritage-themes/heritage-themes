#!/usr/bin/env bash
# Cuts a release from dev: sets the version, stamps the changelogs, builds, commits and pushes dev,
# fast-forwards master to it, waits for Build to pass, then pushes the release tag, which starts the
# publish workflow. See docs/releasing.md.
#
# The JetBrains plugin, the VS Code extension, the Visual Studio extension, the Sublime Text package,
# the Zed extension, the Neovim plugin and the Notepad++ themes share VERSION in build.py and the
# v<version> tag. The release includes each product whose changelog has entries under [Unreleased]:
# CHANGELOG.md for the JetBrains plugin, vscode/CHANGELOG.md for the VS Code extension,
# visualstudio/CHANGELOG.md for the Visual Studio extension, sublime/CHANGELOG.md for the Sublime Text
# package, zed/CHANGELOG.md for the Zed extension, nvim/CHANGELOG.md for the Neovim plugin,
# notepadpp/CHANGELOG.md for the Notepad++ themes. A product without entries keeps its last published
# build, which the GitHub release attaches.
#
# Usage: scripts/release.sh [patch|minor|major|X.Y.Z] [--dry-run]
#   patch    third component +1 (default)
#   minor    second component +1, third reset
#   major    first component +1, the others reset
#   X.Y.Z    an explicit version, for example 1.0.0
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

kind="patch"
dry_run=false
for arg in "$@"; do
  case "$arg" in
    --dry-run) dry_run=true ;;
    patch | minor | major) kind=$arg ;;
    [0-9]*.[0-9]*.[0-9]*) kind=explicit; explicit=$arg ;;
    *) echo "release: unknown argument '$arg'" >&2; exit 1 ;;
  esac
done

fail() { echo "release: $*" >&2; exit 1; }

# The first Python 3 that runs. On Windows, python3 can be the Microsoft Store placeholder, which fails.
python=""
for candidate in python3 python py; do
  if "$candidate" -c 'import sys; sys.exit(sys.version_info < (3,))' >/dev/null 2>&1; then
    python=$candidate
    break
  fi
done
[ -n "$python" ] || fail "Python 3 not found"

# Succeeds when the changelog has at least one entry under [Unreleased].
has_unreleased() {
  awk '/^## \[Unreleased\]/ {on = 1; next} /^## \[/ {on = 0} on && /^- / {found = 1} END {exit !found}' "$1"
}

# Prints the newest released version in the changelog.
latest_release() {
  sed -n '/^## \[[0-9]/{s/^## \[\([^]]*\)\].*/\1/p;q}' "$1"
}

# Succeeds when version $1 is greater than version $2.
newer() {
  [ "$1" != "$2" ] && [ "$(printf '%s\n%s\n' "$1" "$2" | sort -V | tail -n 1)" = "$1" ]
}

current=$(sed -n 's/^VERSION = "\(.*\)"/\1/p' build.py)
[ -n "$current" ] || fail "no VERSION in build.py"
IFS=. read -r major minor patch <<<"$current"

case "$kind" in
  patch) version="$major.$minor.$((patch + 1))" ;;
  minor) version="$major.$((minor + 1)).0" ;;
  major) version="$((major + 1)).0.0" ;;
  explicit) version=$explicit ;;
esac
tag="v$version"

changelogs=() products=() summary=""
for product in "JetBrains plugin:CHANGELOG.md" "VS Code extension:vscode/CHANGELOG.md" \
  "Visual Studio extension:visualstudio/CHANGELOG.md" \
  "Sublime Text package:sublime/CHANGELOG.md" "Zed extension:zed/CHANGELOG.md" \
  "Neovim plugin:nvim/CHANGELOG.md" "Notepad++ themes:notepadpp/CHANGELOG.md"; do
  name=${product%%:*} changelog=${product#*:}
  previous=$(latest_release "$changelog")
  # The marketplaces reject a version that is not greater than the last one they received.
  [ -z "$previous" ] || newer "$version" "$previous" \
    || fail "$version is not greater than $previous, the last release in $changelog"
  if has_unreleased "$changelog"; then
    changelogs+=("$changelog") products+=("$name")
    summary+="  $name: $version"$'\n'
  else
    summary+="  $name: unchanged, attaches ${previous:-nothing}"$'\n'
  fi
done
[ ${#products[@]} -gt 0 ] || fail "no product changelog has entries under [Unreleased]"

echo "Current version: $current"
echo "Release:         $version ($kind)"
printf '%s' "$summary"
$dry_run && exit 0

[ "$(git branch --show-current)" = dev ] || fail "not on dev"
[ -z "$(git status --porcelain)" ] || fail "working tree is not clean"
git fetch --tags origin
git rev-parse -q --verify "refs/tags/$tag" >/dev/null && fail "$tag already exists"
[ "$(git rev-parse dev)" = "$(git rev-parse origin/dev)" ] || fail "dev is not in sync with origin/dev"
git merge-base --is-ancestor origin/master dev || fail "dev does not contain origin/master"

read -r -p "Release $tag from $(git rev-parse --short dev)? [y/N] " answer
[ "$answer" = y ] || fail "cancelled"

sed -i "s/^VERSION = .*/VERSION = \"$version\"/" build.py
for changelog in "${changelogs[@]}"; do
  sed -i "0,/^## \[Unreleased\]/s//## [Unreleased]\n\n## [$version] - $(date +%F)/" "$changelog"
done

"$python" build.py --vsix

included=""
for i in "${!products[@]}"; do
  case $i in
    0) included=${products[i]} ;;
    $((${#products[@]} - 1))) included+=" and ${products[i]}" ;;
    *) included+=", ${products[i]}" ;;
  esac
done
git add build.py "${changelogs[@]}"
git commit -q -m "chore(release): release version $version" -m "Releases version $version of the $included."
git push origin dev

git switch master
git merge --ff-only origin/master
git merge --ff-only dev
git push origin master

sha=$(git rev-parse HEAD)
echo "Waiting for Build on $sha..."
run=""
for _ in $(seq 1 60); do
  run=$(gh run list --workflow Build --commit "$sha" --json databaseId -q '.[0].databaseId')
  [ -n "$run" ] && break
  sleep 10
done
[ -n "$run" ] || fail "no Build run appeared for $sha; tag not pushed"
gh run watch "$run" --exit-status || fail "Build failed; tag not pushed"

git tag -a "$tag" -m "Release $version"
git push origin "$tag"
git switch dev
echo "Pushed $tag. Publish: gh run list --workflow Publish --limit 1"
