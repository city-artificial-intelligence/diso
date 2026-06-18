# DISO metadata: a VoID + Dublin Core description of the network

This directory contains a small, machine-readable description of **DISO**
(Defence, Intelligence and Security Ontologies) - the network of ontologies
itself - expressed with the [VoID](https://www.w3.org/TR/void/) and
[Dublin Core Terms](http://purl.org/dc/terms/) vocabularies.

It has two parts: a tiny **vocabulary** (TBox) and the **ABox data** that
describes the actual network - the DISO collection, its subdomain clusters, and
its 47 member ontologies.

## Files

**Vocabulary (TBox)**

| File | What it is |
|---|---|
| `diso-ontology.ttl` | The **`diso` vocabulary**, authored in Turtle - the source of truth. |
| `diso-ontology.owl` | The vocabulary as **RDF/XML** (ROBOT-converted). |

**ABox (the dataset description)**

| File | What it is |
|---|---|
| `diso-network.nt` / `.ttl` / `.owl` | The ABox in N-Triples, Turtle and RDF/XML - three serialisations of **one graph** (verified identical with `robot diff`). |
| `catalog-v001.xml` | OASIS catalog mapping the vocabulary import IRI to the local file (offline build/validate). |

## The model (kept simple)

The vocabulary defines three classes, each `rdfs:subClassOf void:Dataset`:

- `diso:OntologyNetwork` - the whole DISO collection (1 instance: `.../dataset/network/DISO`).
- `diso:Cluster` - a subdomain cluster (16 instances: 13 top-level + the 3 `smart-environments` sub-clusters).
- `diso:MemberOntology` - a member ontology (47 instances).

...and one datatype property, `diso:spdxLicenseExpression`, which records each
dataset's licence as a verbatim [SPDX expression](https://spdx.org/licenses/)
(faithfully capturing compound expressions like `MIT AND CC-BY-4.0` and the value `NOASSERTION`).

Structure is expressed with `void:subset`:
`DISO ⊃ clusters ⊃ member ontologies`, with `smart-environments ⊃
{smart-buildings, smart-cities, smart-homes}`. Member/cluster membership follows
the `Cluster (home)` column of [`../ONTOLOGY-LICENSING.md`](../ONTOLOGY-LICENSING.md),
plus the four cross-cluster listings that exist as stub directories in the repo
(`BOnSAI`, `SOUPA`, `JC3IEDM`, `OntoSecRPA`). Descriptive metadata reuses
Dublin Core Terms (`dcterms:title`, `description`, `creator`, `publisher`,
`license`, `issued`, `identifier`, ...).

Each member ontology also carries its **access points**: the local DISO copy
(`void:dataDump`, for the redistributable ones), the authoritative
`diso:upstreamSource`, alternative `diso:mirror`s (DISO-raw / pinned / web-archive),
and a human `diso:projectPage`. The first three are `rdfs:subPropertyOf
void:dataDump`, so a generic VoID tool still sees every dump location; the DISO
node also gets `void:sparqlEndpoint` when built with `DISO_SPARQL`. Canonical-vs-mirror
precedence for `diso:mirror`: pinned-commit upstream, then branch upstream, then
web-archive, then the DISO-hosted copy.

Licence-aware redirects use a _persistent_ URL pointing at either the **local copy** 
where the licence permits, otherwise the **upstream RDF**, e.g., the SEPSES renderings 
of the MITRE cyber ontologies, reclassified as redistributable. 

## IRI scheme

The base IRI is a **placeholder** on GitHub Pages and is expected to move to a `w3id.org` PURL once an identifier is agreed:

```
base:     https://city-artificial-intelligence.github.io/diso/
vocab:    https://city-artificial-intelligence.github.io/diso/ontology   (terms at .../ontology#)
data:     https://city-artificial-intelligence.github.io/diso/dataset/   (network/..., cluster/..., ontology/...)
```
