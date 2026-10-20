# Releasing

The JetBrains plugin and the VS Code extension are released separately, each with its own version,
changelog and tags:

| Product | Version | Changelog | Tag | Workflow | Publishes to |
|---|---|---|---|---|---|
| JetBrains plugin | `VERSION` in `build.py` | `CHANGELOG.md` | `v<version>` | `publish.yml` (Publish) | JetBrains Marketplace |
| VS Code extension | `VSCODE_VERSION` in `build.py` | `vscode/CHANGELOG.md` | `vscode-v<version>` | `publish-vscode.yml` (Publish VS Code) | VS Marketplace, Open VSX |

Pushing a tag publishes that product and attaches its build to a GitHub release. There is no
approval step: the tag push is the gate.

## Branches and CI

Work on `dev`. `master` receives commits only when a release is cut.

| Workflow | Runs on | Does |
|---|---|---|
| `build.yml` (Build) | Push to `master`, every pull request, manual run | `python3 build.py --vsix`, which also validates the plugin, the extension and their theme files |
| `publish.yml` (Publish) | Push of a `v<digit>…` tag | Checks the tag, builds, signs, uploads to the JetBrains Marketplace, creates the GitHub release |
| `publish-vscode.yml` (Publish VS Code) | Push of a `vscode-v…` tag | Checks the tag, builds the `.vsix`, publishes to the VS Marketplace and Open VSX, creates the GitHub release |
| `vscode-identity.yml` (VS Marketplace identity) | Manual run | Prints the Marketplace ID of the identity Publish VS Code signs in as |

A push to `dev` runs nothing. Run the same check locally with `python3 build.py --vsix`.

## Cut a release

1. Add the changes under `[Unreleased]` in `CHANGELOG.md` for the JetBrains plugin, or in
   `vscode/CHANGELOG.md` for the VS Code extension. Commit and push `dev`.
2. Run the release script on `dev`. Add `--vscode` to release the VS Code extension:

   ```bash
   scripts/release.sh            # patch: 1.0.0 → 1.0.1
   scripts/release.sh minor      # 1.0.x → 1.1.0
   scripts/release.sh major      # 1.x.y → 2.0.0
   scripts/release.sh 1.0.0      # an explicit version
   scripts/release.sh --dry-run  # print the version and stop
   scripts/release.sh --vscode 1.0.0
   ```

   It prints the version and asks for confirmation. It then sets the version in `build.py`, stamps
   the changelog, runs `build.py`, commits and pushes `dev`, fast-forwards `master` to it and pushes
   it, waits for Build to pass on that commit, and pushes an annotated tag, which starts the publish
   workflow. It stops before changing anything if it is not on `dev`, the working tree is dirty,
   `dev` differs from `origin/dev`, the tag exists or `[Unreleased]` has no entries, and stops
   before tagging if Build fails.

A publish workflow fails before uploading if the tag differs from the version in `build.py`, the
tagged commit is not on `master`, the changelog has no section for the version, or a secret or
variable is empty. The GitHub release of the VS Code extension is not marked as the latest, so the
latest release stays the JetBrains plugin that the README links to.

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

Publish VS Code signs in to the VS Marketplace with Microsoft Entra ID through GitHub's OpenID
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
   | Workflow | `publish-vscode.yml` |
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
