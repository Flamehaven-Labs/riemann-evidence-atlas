# Source and license

The repository code is licensed under [MIT](LICENSE). Two local modules adapt MIT-licensed code
from Flamehaven contributors at the NSRW release commit
`6119a2208e1992c1ecea5c9862eac712d604e77f`.

| Local module | Upstream path | Upstream file SHA-256 |
| --- | --- | --- |
| `riemann_evidence/rational_intervals.py` | `src/nsrw/math_kernel/p2_core_scalars.py` | `9ac2f7717708e9ceb6526bed288033c09ccd5b66b6bbf5935b8582f2fbf41eb6` |
| `riemann_evidence/verification.py` | `src/nsrw/research_verification.py` | `d23c3bc32ee813e7b2c22326d3e27487e31b7b67439235103c11488145ae411f` |

The arithmetic module retains the exponential enclosure functions. The
verification module uses the local report format identifier. See the
[NSRW evidence archive](docs/evidence/nsrw/README.md) for the MB-06 input,
receipts, negative control, and their relationship to the standalone replay.
Papers and Lean sources belong to their original authors. Their URLs and
identities are recorded in [the source catalog](docs/evidence/source-index/sources.json) and
[the archive manifest](docs/evidence/source-index/lean-archive-manifest.json). The cited papers and compiled archives are separately sourced. This repository records their identities and selected declaration-reference metadata.
