#!/usr/bin/env bash
# Cuts a release from dev: sets the version, stamps the changelog, builds, commits and pushes dev,
# fast-forwards master to it, waits for Build to pass, then pushes the v<version> tag, which starts
# Publish. See docs/releasing.md.
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

echo "Current version: $current"
echo "Release:         $version ($kind)"
$dry_run && exit 0

[ "$(git branch --show-current)" = dev ] || fail "not on dev"
[ -z "$(git status --porcelain)" ] || fail "working tree is not clean"
git fetch --tags origin
git rev-parse -q --verify "refs/tags/$tag" >/dev/null && fail "$tag already exists"
[ "$(git rev-parse dev)" = "$(git rev-parse origin/dev)" ] || fail "dev is not in sync with origin/dev"
git merge-base --is-ancestor origin/master dev || fail "dev does not contain origin/master"

# Stamping an empty section would publish release notes with no content.
awk '/^## \[Unreleased\]/ {on = 1; next} /^## \[/ {on = 0} on && /^- / {found = 1} END {exit !found}' CHANGELOG.md \
  || fail "CHANGELOG.md has no entries under [Unreleased]"

read -r -p "Release $tag from $(git rev-parse --short dev)? [y/N] " answer
[ "$answer" = y ] || fail "cancelled"

sed -i "s/^VERSION = .*/VERSION = \"$version\"/" build.py
sed -i "0,/^## \[Unreleased\]/s//## [Unreleased]\n\n## [$version] - $(date +%F)/" CHANGELOG.md

python3 build.py

git add build.py CHANGELOG.md
git commit -q -m "chore(release): release version $version" -m "Releases version $version."
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
