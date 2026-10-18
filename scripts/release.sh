#!/usr/bin/env bash
# Cuts a release from dev: sets the version, stamps the changelog, builds, commits and pushes dev,
# fast-forwards master to it, waits for Build to pass, then pushes the release tag, which starts the
# publish workflow. See docs/releasing.md.
#
# Usage: scripts/release.sh [patch|minor|major|X.Y.Z] [--vscode] [--dry-run]
#   --vscode release the VS Code extension: VSCODE_VERSION, vscode/CHANGELOG.md and a vscode-v<version>
#            tag, which starts Publish VS Code. Without it, the JetBrains plugin: VERSION, CHANGELOG.md
#            and a v<version> tag, which starts Publish.
#   patch    third component +1 (default)
#   minor    second component +1, third reset
#   major    first component +1, the others reset
#   X.Y.Z    an explicit version, for example 1.0.0
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

kind="patch"
dry_run=false
vscode=false
for arg in "$@"; do
  case "$arg" in
    --dry-run) dry_run=true ;;
    --vscode) vscode=true ;;
    patch | minor | major) kind=$arg ;;
    [0-9]*.[0-9]*.[0-9]*) kind=explicit; explicit=$arg ;;
    *) echo "release: unknown argument '$arg'" >&2; exit 1 ;;
  esac
done

fail() { echo "release: $*" >&2; exit 1; }

if $vscode; then
  variable=VSCODE_VERSION changelog=vscode/CHANGELOG.md prefix=vscode-v product="VS Code extension "
  build_args=(--vsix)
else
  variable=VERSION changelog=CHANGELOG.md prefix=v product=""
  build_args=()
fi

current=$(sed -n "s/^$variable = \"\(.*\)\"/\1/p" build.py)
[ -n "$current" ] || fail "no $variable in build.py"
IFS=. read -r major minor patch <<<"$current"

case "$kind" in
  patch) version="$major.$minor.$((patch + 1))" ;;
  minor) version="$major.$((minor + 1)).0" ;;
  major) version="$((major + 1)).0.0" ;;
  explicit) version=$explicit ;;
esac
tag="$prefix$version"

echo "Current ${product}version: $current"
echo "Release:         $version ($kind)"
$dry_run && exit 0

[ "$(git branch --show-current)" = dev ] || fail "not on dev"
[ -z "$(git status --porcelain)" ] || fail "working tree is not clean"
git fetch --tags origin
git rev-parse -q --verify "refs/tags/$tag" >/dev/null && fail "$tag already exists"
[ "$(git rev-parse dev)" = "$(git rev-parse origin/dev)" ] || fail "dev is not in sync with origin/dev"
git merge-base --is-ancestor origin/master dev || fail "dev does not contain origin/master"

# Stamping an empty section would publish release notes with no content.
awk '/^## \[Unreleased\]/ {on = 1; next} /^## \[/ {on = 0} on && /^- / {found = 1} END {exit !found}' "$changelog" \
  || fail "$changelog has no entries under [Unreleased]"

read -r -p "Release $tag from $(git rev-parse --short dev)? [y/N] " answer
[ "$answer" = y ] || fail "cancelled"

sed -i "s/^$variable = .*/$variable = \"$version\"/" build.py
sed -i "0,/^## \[Unreleased\]/s//## [Unreleased]\n\n## [$version] - $(date +%F)/" "$changelog"

python3 build.py "${build_args[@]}"

git add build.py "$changelog"
git commit -q -m "chore(release): release ${product}version $version" -m "Releases ${product}version $version."
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

git tag -a "$tag" -m "Release ${product}$version"
git push origin "$tag"
git switch dev
if $vscode; then workflow="Publish VS Code"; else workflow=Publish; fi
echo "Pushed $tag. $workflow: gh run list --workflow \"$workflow\" --limit 1"
