# DISO: Defence, Intelligence and Security Ontologies

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20059507.svg)](https://doi.org/10.5281/zenodo.20059507)

**DISO** is a collection of publicly available OWL ontologies covering the domains of **defence, intelligence, and security**. The resource is publicly available at this [DOI](https://doi.org/10.5281/zenodo.20059507).

* ontology $\cdot$ [docs](docs/index.html) $\cdot$ [ttl](metadata/diso-ontology.ttl) $\cdot$ [owl](metadata/diso-ontology.owl)
* dataset $\cdot$ [ttl](metadata/diso-network.ttl) $\cdot$ [owl](metadata/diso-network.owl)

Base IRI: `https://city-artificial-intelligence.github.io/diso/`

## Overview

The DISO dataset aims to inform the UK Government intelligence community about the public ontologies relevant to defence and national security and related areas. 
The ontologies in DISO were identified and obtained during an **ontology search** exercise undertaken in November and December of 2025. Each ontology is accompanied by documentation that provides information such as a full name, a short description, relevant context, a web presence, and the source from which the ontology was obtained.

## Subdomains (categories, clusters)

Most of the ontologies in DISO cluster into categories (or subdomains) of the umbrella domains of defence, intelligence and security. The structure of this repository reflects this clustering. Sometimes, an ontology fits into more than one cluster (subdomain). However, each ontology appears only once in the repository: in the cluster where the fit is deemed strongest.

## Relaxed domain definitions

The domains of **defence, intelligence and security** have been **interpreted broadly**. The connection between some of the subdomain clusters and the umbrella domains may appear tenuous. In the README files for these subdomains, we provide information and cite sources to explain and justify our decision to include the subdomain within DISO.

## Merged ontologies and the compact distribution

Some of the ontologies in DISO are distributed as networks of component ontologies, woven together with `owl:imports` statements. For some of these, we have **merged** the component ontology files into a single ontology file, using the Protege ontology editor.

The [diso-compact/](diso-compact/) directory bundles a canonical file per ontology. If an ontology belongs to multiple clusters, a copy is placed in each cluster to which it belongs. As such, the compact distribution contains some duplicate ontologies; see [diso-compact/README.md](diso-compact/README.md) for details. The compact distribution is packaged for the convenience of downstream consumers, such as [the DISO ontology matching pipeline](https://github.com/city-artificial-intelligence/DISO-mappings).

## DISO cluster conceptual overlaps

This diagram provides a view of the conceptual overlaps that exist between various clusters (or subdomains) of the DISO collection of defence, intelligence and security ontologies.

![DISO](figs/diso-cluster-overlaps.png)


## The DISO OAEI track

### Curation roadmap

The following steps describe the curation process in preparation for a **defence, intelligence & security** OAEI track.

| Milestone                                                                       | Status      |
|---------------------------------------------------------------------------------|-------------|
| Analyse and evaluate the ontologies in DISO                                     | COMPLETE    |
| Conduct exploratory alignments within each subdomain                            | COMPLETE    |
| Identify intra-cluster candidate pairs (i.e., alignment tasks)                  | COMPLETE    |
| Identify one or more cluster ontologies suitable for inter-cluster analysis     | COMPLETE    |
| Conduct exploratory inter-cluster alignments                                    | COMPLETE    |
| Identify inter-cluster candidate pairs (i.e., alignment tasks)                  | COMPLETE    |
| Select a final (small) set of ontology pairs (i.e., alignment tasks)            | COMPLETE    |
| Establish preliminary (silver) reference alignments for the final set of alignment tasks | COMPLETE    |
| Establish the defence, intelligence & security OAEI track                       | IN PROGRESS |

### Repositories

This repository serves as the resource layer for a small ecosystem of repositories that support an OAEI track for defence, intelligence, and security ontologies.

[**DISO-mappings**](https://github.com/city-artificial-intelligence/DISO-mappings) is a Python pipeline that consumes the DISO compact distribution and produces pairwise alignments between selected ontology pairs. It uses a configurable set of ontology matching systems (AML, LogMap, LogMapLt, BERTMap, and BERTMapLt by default; with an extendable `Matcher` base class that enables custom external matchers). The pipeline aggregates the per-system alignments into an unverified silver-standard consensus alignment via a family-based voting mechanism. This alignment is then manually verified, adapted and used as the basis for a partial reference alignment. To reproduce our alignments, follow the steps within the repository’s `make` workflow.

[**DISO-oaei**](https://github.com/city-artificial-intelligence/DISO-oaei) is the home page for the OAEI track and will describe and house the evaluation harness that scores participant-submitted matchers against the above-mentioned reference alignment.

## Ontology Licensing

For licensing information regarding the ontologies included in DISO, see the [ontology licensing table](ONTOLOGY-LICENSING.md).

## Versioning

Major version bumps are most likely to follow an annual release cadence (mirroring the OAEI competition year). Minor version bumps may be used to capture upstream ontology updates and curation fixes.

## Citation

If you use DISO, please cite the dataset using the metadata in [CITATION.cff](CITATION.cff). If the accompanying resource paper is published, the paper will be added as the preferred citation.

## Contributing

Contributions of additional defence, intelligence and security ontologies are welcome. Please open an issue describing the proposed addition before submitting a pull request.

## Acknowledgements

This research was supported by Turing Innovations Limited and The Alan Turing Institute’s Defence and Security Programme via the [GUARD project](https://ernestojimenezruiz.github.io/projects/guard/).

## Contributors

[Ernesto Jiménez-Ruiz](https://ernestojimenezruiz.github.io/), [Pedro Cotovio](https://pedrocotovio.github.io/), [Jon Dilworth](https://dilworth.io/), and [Dave Herron](https://djherron.github.io/).

## License

The curation layer of this repository is released under the [MIT License](LICENSE). Each ontology in this collection retains its original upstream license.
