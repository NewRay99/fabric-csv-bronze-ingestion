# Fabric notebook CI/CD guidance

Researched 11 September 2026 against Microsoft and tool-maintainer documentation.

**Recommendation for this client:** retain Azure Repos and the existing Fabric Git integration, add Azure Pipelines validation, then promote a reconciled Dev workspace through Fabric deployment pipelines to Test and Production. This is a Microsoft-documented architecture, rather than a single universal industry standard. Microsoft also documents direct deployment from Git with the `fabric-cicd` library; that is a good alternative when releases must be built from an exact commit and require extensive environment substitutions. [Microsoft workflow comparison](https://learn.microsoft.com/en-us/fabric/cicd/manage-deployment)

## Repository format and release source

Fabric Git integration represents a notebook as an item folder containing `.platform` and `notebook-content.py`, with optional resources and settings. The Python file includes cell boundaries, Markdown, magic cells and metadata that Fabric reconstructs; it is more than an ordinary Python script. Cell outputs are excluded. Preserve the complete item structure when deploying through Git. [Notebook source control](https://learn.microsoft.com/en-us/fabric/data-engineering/notebook-source-control-deployment)

```text
fabric/                         # Proposed live deployment root
  notebooks/
    90_run_archive_pipeline.Notebook/
      .platform
      notebook-content.py
```

The converted numbered `.py` files currently in `project X` are the editable source. They are not yet a complete Git deployment tree. Before CD, either move those primary files into canonical item folders and update the tests' discovery paths, or add deterministic packaging into a dedicated `fabric/` directory, retaining stable item metadata and checking that generated contents match the primary files. For native Git sync, the complete generated definitions must be committed to its connected repository folder. Choose one editing location; independently editing both copies would recreate drift. These are recommendations for this repository, inferred from Fabric's documented item layout.

The local [comparison](notebook-comparison/README.md) found six code differences and two original notebooks absent from the supplied WMPP snapshot. That snapshot is evidence for reconciliation, not a release payload. Keep `reports/current/WMPP` out of deployment discovery. Obtain the current client definitions, preserve the agreed item identities and dependencies, resolve the six differences explicitly, and confirm the two runner dependencies before creating the deployment tree. The supplied snapshot alone does not establish the live workspace's current state.

## Two supported deployment routes

| Route | Flow | Tradeoff |
|---|---|---|
| Existing Git integration plus native Fabric deployment pipelines | PR validation → merge → synchronize approved definitions into Dev → validate in Fabric → deploy Dev to Test → validate → approve and deploy Test to Production | Closest fit for the client's existing workflow; deployment source is the workspace, so verify it matches the reviewed release. |
| Azure Pipelines plus `fabric-cicd` | PR validation → merge → build versioned item artifact → deploy artifact to Test with environment parameters → validate → approve and deploy the same artifact to Production | Strong control over release contents and substitutions; needs a deployment script and managed package version. |

Microsoft supports both routes. With direct Items API deployment, Test and Production do not need Git connections. Avoid two independent mechanisms writing releases into the same destination. [Microsoft workflow comparison](https://learn.microsoft.com/en-us/fabric/cicd/manage-deployment)

For native automation, Azure Pipelines can call `POST /v1/deploymentPipelines/{deploymentPipelineId}/deploy` with explicit source and target stage IDs. Poll its long-running operation until completion; HTTP 202 only means accepted. The caller needs deployment-pipeline admin and workspace permissions. Service principals and managed identities are supported only if every item involved supports them. [Fabric deployment REST API](https://learn.microsoft.com/en-us/rest/api/fabric/core/deployment-pipelines/deploy-stage-content)

For direct deployment, Microsoft publishes an Azure DevOps tutorial using `FabricWorkspace` and `publish_all_items()`. Item-type scoping is not a promise to deploy only changed notebooks: publishing processes all in-scope definitions. Do not copy its orphan-deletion step into this project: `unpublish_all_orphan_items()` can delete valid destination notebooks absent from an incomplete release directory. [Microsoft fabric-cicd tutorial](https://learn.microsoft.com/en-us/fabric/cicd/tutorial-fabric-cicd-azure-devops)

## Which YAML files are needed?

| File | Purpose | When needed |
|---|---|---|
| `azure-pipelines.yml` | Python setup, dependency installation, pre-commit, pytest, test-result publishing; later deployment stages or calls to deployment templates | Azure Pipelines automation |
| `.pre-commit-config.yaml` | Shared local and CI hook definitions | To run pre-commit |
| `parameter.yml` inside the deployment root | Per-environment definition substitutions | When using `fabric-cicd` and substitutions are required |
| A separate deployment YAML/template | Organizes Test and Production deployment jobs | Optional; one multi-stage YAML is also possible |

There is no extra notebook-specific YAML required merely because notebooks use `.py`. Native Fabric deployment pipelines are Fabric resources; Azure YAML orchestrates validation and deployment API calls. A YAML file must also be registered as a pipeline in Azure DevOps. [Notebook source control](https://learn.microsoft.com/en-us/fabric/data-engineering/notebook-source-control-deployment), [Microsoft Azure DevOps setup](https://learn.microsoft.com/en-us/fabric/cicd/tutorial-fabric-cicd-azure-devops)

**Yes, pre-commit and pytest belong in the YAML.** Run `pre-commit run --all-files` as a CI command. `pre-commit install` installs a local Git hook for developers and is not required on the CI agent. Configure hooks to respect Fabric metadata and magic cells; use the project's Fabric-aware parser for notebook checks. [pre-commit CI documentation](https://pre-commit.com/#usage-in-continuous-integration)

Run `python -m pytest` with JUnit XML output, then publish it using `PublishTestResults@2`, including on test failure. These tests validate portable behavior and source structure; they do not prove Spark, Delta, permissions, data connections or Fabric execution work. Add a controlled Fabric Test-workspace smoke run before promotion. [Microsoft Python pipeline guidance](https://learn.microsoft.com/en-us/azure/devops/pipelines/ecosystems/customize-python?view=azure-devops), [PublishTestResults task](https://learn.microsoft.com/en-us/azure/devops/pipelines/tasks/reference/publish-test-results-v2?view=azure-pipelines)

**Azure Repos detail:** enable required PR build validation in the target branch's policies. A YAML `pr:` block does not implement Azure Repos PR validation. YAML `trigger:` handles push/merge CI. [Azure Repos triggers](https://learn.microsoft.com/en-us/azure/devops/pipelines/repos/azure-repos-git?view=azure-devops#pr-triggers)

## Identity, configuration and promotion

Prefer an Azure Resource Manager service connection using workload identity federation where supported in the client's tenant, instead of storing a client secret. Microsoft recommends federation for new connections. Fabric workspace authorization is separate from having an Azure service connection. [Azure service connections](https://learn.microsoft.com/en-us/azure/devops/pipelines/library/connect-to-azure?view=azure-devops)

For `fabric-cicd`, a practical combination is `AzureCLI@2` using that connection and a deployment script passing `AzureCliCredential()` explicitly to `FabricWorkspace`. Current library documentation requires `token_credential`; older samples relying on an implicit `DefaultAzureCredential` fallback are outdated. Pin the library and identity dependencies to versions validated in Test. [fabric-cicd authentication](https://microsoft.github.io/fabric-cicd/latest/example/authentication/)

Enable the Fabric tenant setting permitting service principals to use Fabric APIs and grant the deployment identity the applicable workspace roles. Microsoft’s direct-deployment tutorial uses Member or Admin. Keep credentials out of repository files and command-line arguments; if federation is unavailable, use the client's managed secret store and runtime environment injection. [Microsoft deployment prerequisites](https://learn.microsoft.com/en-us/fabric/cicd/tutorial-fabric-cicd-azure-devops)

For native pipelines, version attached environment dependencies alongside notebooks and verify destination bindings. Notebook deployment supports default-lakehouse and environment auto-binding; target-stage lakehouse deployment rules override auto-binding. Git lakehouse auto-binding is configured in Fabric notebook settings; do not hand-edit the generated `notebook-settings.json`. [Notebook binding and deployment rules](https://learn.microsoft.com/en-us/fabric/data-engineering/notebook-source-control-deployment)

For direct deployment, `parameter.yml` belongs at `FabricWorkspace.repository_directory` and maps values by the supplied environment name. Scope replacements to the relevant item/file. Validate that every required environment is present: missing environment mappings can be skipped. Map workspace/lakehouse/connection references and operational defaults deliberately, especially archive replay/reset controls. [fabric-cicd parameterization](https://microsoft.github.io/fabric-cicd/latest/how_to/parameterization/)

Use Azure DevOps deployment jobs linked to Test/Production Environments, with approvals and an exclusive lock configured on those resources. Approvals/checks are managed in Azure DevOps, outside YAML. Record the commit and deployment result; promote the tested content and retain its predecessor for a code rollback. Data/schema rollback requires separate planning for this ingestion project. [Azure deployment approvals and locks](https://learn.microsoft.com/en-us/azure/devops/pipelines/process/approvals?view=azure-devops)

The immediate deliverable is CI. Client CD still needs the reconciled item tree, selected deployment route, workspace/stage IDs, identity authorization, destination bindings and a successful Fabric smoke run. No client workspace was accessed or deployed during this research.
