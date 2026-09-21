# Admissibility Wiki Public Domain Mirror Handoff

Status: SOURCE_CONFIGURATION_ACTIVE_ACCOUNT_BINDING_PENDING  
Task ID: `ADMISSIBILITY-WIKI-PUBLIC-DOMAIN-001`  
Canonical source: `StegVerse-Labs/admissibility-wiki`  
Target public hostname: `https://admissibility.stegverse.org`

## Goal

Establish `admissibility.stegverse.org` as the branded public hostname for the existing Admissibility Wiki without creating a second wiki, duplicate publication source, runtime, custody plane, or authority surface.

## Canonical topology

```text
StegVerse-Labs/admissibility-wiki = canonical source
GitHub Actions Pages = existing deployment mechanism
admissibility.stegverse.org = branded public hostname
StegVerse-Labs/Site/Papers = downstream directory/link projection
```

## Repository-side configuration

Required source posture:

- Docusaurus `url`: `https://admissibility.stegverse.org`
- Docusaurus `baseUrl`: `/`
- active public-route validators use the branded hostname;
- public activation/status artifacts identify the branded hostname as the target;
- GitHub Pages remains the existing deployment mechanism.

Because this repository deploys with `actions/deploy-pages`, GitHub documents that a source-tree `CNAME` file is not the authoritative custom-domain mechanism for this deployment mode. The repository Pages custom-domain setting must be configured separately.

## Account-level dependencies

### GitHub Pages

Repository: `StegVerse-Labs/admissibility-wiki`

Set:

```text
Settings -> Pages -> Custom domain
admissibility.stegverse.org
```

Save the setting. After DNS validates and GitHub provisions the certificate, enable **Enforce HTTPS**.

### DNS

For the `stegverse.org` DNS zone create:

```text
Type: CNAME
Name: admissibility
Target: stegverse-labs.github.io
Proxy: DNS only
```

Do not point the CNAME at `stegverse-labs.github.io/admissibility-wiki`; DNS CNAME targets are hostnames only and GitHub requires the organization Pages hostname without the repository path.

## Cutover gates

1. Canonical task registration is merged.
2. Repository source validation is green with branded-host configuration.
3. GitHub Pages custom domain equals `admissibility.stegverse.org`.
4. DNS resolves `admissibility.stegverse.org` to the GitHub Pages organization hostname.
5. HTTPS certificate is valid.
6. `https://admissibility.stegverse.org/` is publicly reachable.
7. `https://admissibility.stegverse.org/formalisms/reconstructable-singularity` is publicly reachable.
8. Site/Papers formalism links are migrated to the branded hostname only after gates 3-7 are observed.
9. Old GitHub Pages project URLs may remain technical compatibility routes but are no longer the preferred public/share URLs.

## Authority boundary

Hostname configuration changes publication addressing only. It does not grant execution authority, admissibility authority, custody, certification, runtime activation, or empirical proof.
