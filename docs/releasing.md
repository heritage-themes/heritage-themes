# Releasing

The JetBrains plugin, the VS Code extension, the Sublime Text package and the Zed extension share
one version, `VERSION` in `build.py`, and one `v<version>` tag. Each has its own changelog:

| Product | Changelog | Publishes to |
|---|---|---|
| JetBrains plugin | `CHANGELOG.md` | JetBrains Marketplace |
| VS Code extension | `vscode/CHANGELOG.md` | VS Marketplace, Open VSX |
| Sublime Text package | `sublime/CHANGELOG.md` | Package repository, listed on Package Control |
| Zed extension | `zed/CHANGELOG.md` | Extension repository, listed in Zed's extension registry by a pull request |

A release includes each product whose changelog has entries under `[Unreleased]`. A product
without entries is not published and skips that version number: after 1.3.0 for all and 1.3.1 for
the VS Code extension only, the plugin goes from 1.3.0 to the next release that includes it.

Every version has one GitHub release, which becomes the latest. It carries every product: the new
build of each included product, and the build of its last release for a product left out, so the
latest release always has the current build of every product. Pushing the tag publishes; there is
no approval step, except that a Zed release reaches users once Zed's maintainers merge the registry pull
request that Publish opens.

## Branches and CI

Work on `dev`. `master` receives commits only when a release is cut.

| Workflow | Runs on | Does |
|---|---|---|
| `build.yml` (Build) | Push to `master`, every pull request, manual run | `python3 build.py --vsix`, which also validates every product and its theme files |
| `publish.yml` (Publish) | Push of a `v<digit>…` tag | Checks the tag; for each included product builds and publishes it (the plugin signed, the Sublime Text package and the Zed extension pushed to their repositories, the Zed registry pull request opened); creates the GitHub release |
| `vscode-identity.yml` (VS Marketplace identity) | Manual run | Prints the Marketplace ID of the identity Publish signs in as |

A push to `dev` runs nothing. Run the same check locally with `python3 build.py --vsix`.

## Cut a release

1. Add the changes under `[Unreleased]` in the changelog of each product they affect: a change to a
   palette or a new theme goes in all four. Commit and push `dev`.
2. Run the release script on `dev`:

   ```bash
   scripts/release.sh            # patch: 1.0.0 → 1.0.1
   scripts/release.sh minor      # 1.0.x → 1.1.0
   scripts/release.sh major      # 1.x.y → 2.0.0
   scripts/release.sh 1.0.0      # an explicit version
   scripts/release.sh --dry-run  # print the version and the included products, then stop
   ```

   It prints the version and the included products and asks for confirmation. It then sets
   `VERSION` in `build.py`, stamps the changelogs of the included products, runs
   `python3 build.py --vsix`, commits and pushes `dev`, fast-forwards `master` to it and pushes it,
   waits for Build to pass on that commit, and pushes an annotated tag, which starts Publish. It
   stops before changing anything if no changelog has entries under `[Unreleased]`, the version
   is not greater than the last release in each changelog, it is not on `dev`, the working tree is
   dirty, `dev` differs from `origin/dev` or the tag exists, and stops before tagging if Build
   fails.

Publish includes a product when its changelog has a section for the version. It fails before
uploading if the tag differs from `VERSION` in `build.py`, the tagged commit is not on `master`,
no changelog has a section for the version, or a secret or variable of an included product is
empty. It creates the GitHub release once every included product has published. If one fails,
re-run the failed jobs in GitHub Actions; the products that published are not uploaded again.

To withdraw a tag pushed by mistake, run `git push origin :refs/tags/<tag>` and
`git tag -d <tag>`. The workflow may already be running; cancel it in GitHub Actions.

## One-time setup: JetBrains Marketplace

The Marketplace accepts API uploads only for a plugin that already exists, so upload the first
version by hand.

1. Run `python3 build.py`, then upload `build/heritage-themes-<version>.zip` at
   <https://plugins.jetbrains.com/plugin/add>.
2. Generate the signing key and certificate in a private directory outside the repository and
   outside any synced folder. The first command prompts for a passphrase, which is
   `PRIVATE_KEY_PASSWORD`. The second prompts for the passphrase and the certificate fields; only
   the common name matters, for example `Heritage Themes`.

   ```bash
   mkdir -m 700 ~/.heritage-signing && cd ~/.heritage-signing
   openssl genpkey -aes-256-cbc -algorithm RSA -pkeyopt rsa_keygen_bits:4096 -out private.pem
   openssl req -key private.pem -new -x509 -days 3650 -out chain.crt
   ```

3. Create a permanent token at <https://plugins.jetbrains.com/author/me/tokens>.
4. Store the four repository secrets from the same directory:

   ```bash
   gh secret set CERTIFICATE_CHAIN -R heritage-themes/heritage-themes < chain.crt
   gh secret set PRIVATE_KEY -R heritage-themes/heritage-themes < private.pem
   gh secret set PRIVATE_KEY_PASSWORD -R heritage-themes/heritage-themes
   gh secret set PUBLISH_TOKEN -R heritage-themes/heritage-themes
   ```

   `gh secret list -R heritage-themes/heritage-themes` shows the names that are set.
   `signPlugin` skips itself, and Gradle still reports success, when `CERTIFICATE_CHAIN` or
   `PRIVATE_KEY` is empty. The workflow's "Check release secrets" step fails the run before
   signing if any of the four secrets is empty.

5. Save `private.pem`, `chain.crt` and the passphrase in the password manager, then delete the
   directory: `cd ~ && rm -r ~/.heritage-signing`. Sign every release with this key; never
   generate a new one.

Publish uploads to the plugin whose descriptor `<id>` is `heritage.themes`.

## One-time setup: VS Marketplace and Open VSX

Publish signs in to the VS Marketplace with Microsoft Entra ID through GitHub's OpenID
Connect token, so no Marketplace token is stored. The extension ID is
`<VSCODE_PUBLISHER>.<VSCODE_NAME>` from `build.py`; the first publish creates the extension.

1. Create the publisher at <https://marketplace.visualstudio.com/manage> with the ID in
   `VSCODE_PUBLISHER`. The ID must match `VSCODE_PUBLISHER` exactly, including case, and cannot be
   changed.
2. Create the GitHub environment the workflows run in:

   ```bash
   gh api -X PUT repos/heritage-themes/heritage-themes/environments/vscode-marketplace
   ```

3. Create the managed identity in the Azure portal at <https://portal.azure.com>, not in Azure
   DevOps. The account needs an Azure subscription and a directory it owns; a personal Microsoft
   account with neither gets an "Interaction required" error and an empty directory list. Create a
   free account at <https://azure.microsoft.com/free> first if needed.
   1. Search for **Managed Identities**, select **Create**, and choose a subscription and a resource
      group. Name the identity `heritage-themes-publish`.
   2. Print the numeric GitHub IDs that the credential form asks for:

      ```bash
      gh api repos/heritage-themes/heritage-themes --jq '{owner_id: .owner.id, repo_id: .id}'
      ```

   3. On the identity, open **Settings | Federated credentials** and select **Add credential**.
      Choose the scenario **GitHub Actions deploying Azure resources** and enter:

      | Field | Value |
      |---|---|
      | Organization | `heritage-themes` |
      | Organization ID | `owner_id` from the command above |
      | Repository | `heritage-themes` |
      | Repository ID | `repo_id` from the command above |
      | Entity | **Environment** |
      | Environment | `vscode-marketplace` |

4. Store the identity's client ID and tenant ID as repository variables. The client ID is on the
   identity's **Overview** page. The tenant ID is the `tenantId` in its **JSON View** and the
   **Tenant ID** on the **Microsoft Entra ID** overview page; it differs from the client ID.

   ```bash
   gh variable set AZURE_CLIENT_ID -R heritage-themes/heritage-themes --body '<client id>'
   gh variable set AZURE_TENANT_ID -R heritage-themes/heritage-themes --body '<tenant id>'
   ```

5. Print the identity's Marketplace ID and add it to the publisher:

   ```bash
   gh workflow run vscode-identity.yml -R heritage-themes/heritage-themes
   gh run list --workflow vscode-identity.yml -R heritage-themes/heritage-themes --limit 1
   gh run view <run id> -R heritage-themes/heritage-themes --log
   ```

   The ID is the GUID on the last line of the `az rest` step. On the publisher's page at
   <https://marketplace.visualstudio.com/manage>, open **Members**, select **Add**, enter the ID and
   choose the **Contributor** role. The identity needs no Azure role assignment.
6. Sign in at <https://open-vsx.org> with a GitHub account, sign the publisher agreement, and create
   an access token under **Settings | Access Tokens**. Create the namespace with the same ID as the
   publisher:

   ```bash
   OVSX_PAT=<token> scripts/vscode/node_modules/.bin/ovsx create-namespace <VSCODE_PUBLISHER>
   ```

   `scripts/vscode/node_modules` exists after the first `python3 build.py --vsix`. The token is used
   only for this command; delete it afterwards.
7. Register the workflow as a trusted publisher, so that it publishes with a short-lived token and no
   secret is stored. Under <https://open-vsx.org/user-settings/namespaces>, open the namespace's
   **Trusted publishers** section and add:

   | Field | Value |
   |---|---|
   | Repository | `heritage-themes/heritage-themes` |
   | Workflow | `publish.yml` |
   | Environment | `vscode-marketplace` |

8. Claim the namespace. Until it has an owner, Open VSX marks every version with a warning that the
   publisher is not verified. Open an issue at
   <https://github.com/EclipseFdn/open-vsx.org/issues/new/choose> with the namespace claim template:
   - Namespace: `heritage-themes`.
   - Tick the **Option 1** checkbox. The "Chose one of the following" items are plain Markdown and
     cannot be ticked.
   - In **Claim evidence**, state the second sub-option, give the Open VSX username that owns the
     token, and link a commit in this repository authored by the GitHub account filing the issue.
     The commit must show that account as its author.

   Once the maintainers grant ownership, versions published by a namespace member show as verified.
   Add any other publishing account, such as a bot, as a **Contributor** under
   <https://open-vsx.org/user-settings/namespaces>.

## One-time setup: Sublime Text package

Package Control installs a package from a public repository that holds the package at its root and
tags each version with a semantic version. This repository holds more than the package, so Publish
pushes the generated package to a separate repository and tags it there. That repository contains
generated files only; every publish replaces its contents.

1. Create the public repository `heritage-themes/heritage-themes-sublime` with a first commit on its
   default branch, for example a README, which the first publish replaces.
2. Create a fine-grained personal access token with **Contents: Read and write** on that repository
   only, and store it as the repository secret `SUBLIME_REPO_TOKEN`:

   ```bash
   gh secret set SUBLIME_REPO_TOKEN -R heritage-themes/heritage-themes
   ```

3. Cut a release that includes the package. Publish pushes the files and the tag `<version>`, without
   a `v`.
4. Submit the package to the Package Control channel: fork
   <https://github.com/wbond/package_control_channel>, add this entry to `repository/h.json` in
   alphabetical order, run **ChannelRepositoryTools: Test Default Channel** in Sublime Text, and open a
   pull request.

   ```json
   {
       "name": "Heritage Themes",
       "author": "Andrzej Piontek",
       "details": "https://github.com/heritage-themes/heritage-themes-sublime",
       "labels": ["theme", "color scheme", "dark", "light"],
       "releases": [
           {
               "sublime_text": ">=4000",
               "tags": true
           }
       ]
   }
   ```

   Package Control picks up later releases from the tags without another pull request.

## One-time setup: Zed extension

Zed's extension registry, the repository `zed-industries/extensions`, pins each extension as a
submodule at a commit of a public repository that holds the extension at its root, with the version in
`extensions.toml`. Publish pushes the generated extension to a separate repository, tags it
`v<version>`, and opens a pull request against the registry that moves the submodule and the version.
That repository contains generated files only; every publish replaces its contents.

1. Create the public repository `heritage-themes/heritage-themes-zed` with a first commit on its
   default branch, for example a README, which the first publish replaces.
2. Create a fine-grained personal access token with **Contents: Read and write** on that repository
   only, and store it as the repository secret `ZED_REPO_TOKEN`:

   ```bash
   gh secret set ZED_REPO_TOKEN -R heritage-themes/heritage-themes
   ```

3. Fork <https://github.com/zed-industries/extensions> into the organisation as
   `heritage-themes/extensions`.
4. Create a classic personal access token with the `public_repo` scope, which can push to the fork and
   open pull requests against the registry, and store it as the repository secret
   `ZED_REGISTRY_TOKEN`. A fine-grained token cannot open a pull request in a repository of another
   owner.

   ```bash
   gh secret set ZED_REGISTRY_TOKEN -R heritage-themes/heritage-themes
   ```

5. Cut a release that includes the extension. Publish pushes the files and the tag, and skips the
   registry pull request with a notice, because the registry has no entry for the extension yet.
6. Submit the extension to the registry by hand, following Zed's
   [publishing guide](https://zed.dev/docs/extensions/publishing/publishing-guide): in a branch of the fork,
   add the submodule at the tagged commit and the entry, run `pnpm sort-extensions`, and open a pull
   request.

   ```bash
   git submodule add https://github.com/heritage-themes/heritage-themes-zed.git extensions/heritage-themes
   git -C extensions/heritage-themes checkout v<version>
   ```

   ```toml
   [heritage-themes]
   submodule = "extensions/heritage-themes"
   version = "<version>"
   ```

   Install the extension in Zed from the tagged commit first: **zed: install dev extension** on a
   checkout of `heritage-themes-zed`. The registry requires a manual test at the submitted commit.

Once the entry is merged, Publish opens the pull request for each later release.
