# Releasing

Pushing a `v*` tag publishes a signed plugin to JetBrains Marketplace through
`.github/workflows/publish.yml` and attaches it, with the `.icls` schemes, to a GitHub release.
There is no approval step: the tag push is the gate.

## Branches and CI

Work on `dev`. `master` receives commits only when a release is cut.

| Workflow | Runs on | Does |
|---|---|---|
| `build.yml` (Build) | Push to `master`, every pull request, manual run | `python3 build.py`, which also validates the descriptor, theme files and icons |
| `publish.yml` (Publish) | Push of a `v*` tag | Checks the tag, builds, signs, uploads to the Marketplace, creates the GitHub release |

A push to `dev` runs nothing. Run the same check locally with `python3 build.py`.

## Cut a release

1. Add the changes under `[Unreleased]` in `CHANGELOG.md`. Commit and push `dev`.
2. Run the release script on `dev`:

   ```bash
   scripts/release.sh            # patch: 1.0.0 → 1.0.1
   scripts/release.sh minor      # 1.0.x → 1.1.0
   scripts/release.sh major      # 1.x.y → 2.0.0
   scripts/release.sh 1.0.0      # an explicit version
   scripts/release.sh --dry-run  # print the version and stop
   ```

   It prints the version and asks for confirmation. It then sets `VERSION` in `build.py`, stamps
   the changelog, runs `build.py`, commits and pushes `dev`, fast-forwards `master` to it and pushes
   it, waits for Build to pass on that commit, and pushes an annotated `v<version>` tag, which
   starts Publish. It stops before changing anything if it is not on `dev`, the working tree is
   dirty, `dev` differs from `origin/dev`, the tag exists or `[Unreleased]` has no entries, and
   stops before tagging if Build fails.

Publish fails before uploading if the tag differs from `VERSION`, the tagged commit is not on
`master`, `CHANGELOG.md` has no section for the version, or a secret is empty.

To withdraw a tag pushed by mistake, run `git push origin :refs/tags/v1.0.0` and
`git tag -d v1.0.0`. The workflow may already be running; cancel it in GitHub Actions.

## One-time setup

The Marketplace accepts API uploads only for a plugin that already exists, so upload the first
version by hand.

1. Run `python3 build.py`, then upload `build/heritage-themes-<version>.zip` at
   <https://plugins.jetbrains.com/plugin/add>.
2. Generate the signing key and certificate. Keep both files in a password manager; sign every
   release with the same key.

   ```bash
   openssl genpkey -aes-256-cbc -algorithm RSA -pkeyopt rsa_keygen_bits:4096 -out private.pem
   openssl req -key private.pem -new -x509 -days 3650 -out chain.crt
   ```

3. Create a permanent token at <https://plugins.jetbrains.com/author/me/tokens>.
4. Store the four repository secrets:

   ```bash
   gh secret set CERTIFICATE_CHAIN < chain.crt
   gh secret set PRIVATE_KEY < private.pem
   gh secret set PRIVATE_KEY_PASSWORD
   gh secret set PUBLISH_TOKEN
   ```

Publish uploads to the plugin whose descriptor `<id>` is `heritage.themes`.
