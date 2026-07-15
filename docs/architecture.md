# Architecture

This repository starts as a modular monolith. The API, future worker and future web app share domain packages under `packages/`.

The domain must stay generic. Client-specific concepts belong in database rows such as organizations, workspaces, ICPs, campaigns and imports.

## Data isolation

Business tables include `organization_id` so the platform can serve multiple client organizations without mixing their data.

Current scoped entities:

- `Company`
- `CompanyAlias`
- `Contact`
- `ICP`
- `ScoringRule`

Upcoming scoped entities:

- `Campaign`
- `Opportunity`
- `Activity`
- `EnrichmentRun`
- `ImportJob`
- `ExportJob`
- `AuditLog`

## Providers

External sources must be implemented behind provider interfaces. The domain should not directly depend on a specific enrichment vendor, social network, email finder or LLM provider.

Provider outputs should include:

- source name
- source URL when available
- observed date
- confidence
- whether the value is a fact or inference
