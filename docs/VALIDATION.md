# Validation scope

Automated checks validate source probabilities against independently calculated Cauchy CDF values, symmetry, normalization and invalid-input rejection. Mesh checks compare known original matrix entries and coordinates, verify the 100,320,422 history count and three expected dimensions, and reject truncated or unsupported layouts. Archive checks verify published file hashes.

The command-line analysis is exercised against the complete historical mesh. GitHub Actions repeats the tests and plotting on Python 3.11 and 3.12 and uploads the generated summary and images. The root badge links to the current check results.

Local verification passed all 12 tests, nine archived-file hashes and the complete plotting workflow. The saved run gives the following descriptive statistics (threshold counts include only nonzero-fluence bins):

| Tally | Mesh dimensions | Nonzero bins | Bins with relative error < 0.1 | Median relative error of nonzero bins |
| --- | --- | --- | --- | --- |
| 44 | 100 × 100 | 10,000 | 5,355 | 0.089565 |
| 54 | 100 × 100 | 10,000 | 7,170 | 0.068685 |
| 64 | 250 × 250 | 40,180 | 0 | 0.69725 |

The far-plane mesh is particularly noisy: none of its nonzero bins meets the descriptive 0.1 threshold. This is not hidden by normalizing the map. Grey cells in uncertainty plots mark zero-fluence bins, whose reported zero relative error should not be interpreted as precision.

These checks establish the behavior of the maintained postprocessing code. They do not validate MCNP particle transport, clinical dosimetry, machine commissioning or a new billion-history run. No MCNP executable was available in this environment. Original diagnostic failures are documented in MODEL_REVIEW.md and preserved as extracted evidence.
