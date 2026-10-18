# Model review and interpretation limits

## Treatment-head model

The final deck describes a tungsten-alloy target (density 18.0 g/cm³), copper backing, lead-antimony collimators, an alloy flattening filter, aluminium support and air. The electron source is placed at the target origin. The source comment describes downward emission; the SDEF card supplies VEC but no explicit DIR. Directional behavior must be checked against the exact MCNP version before claiming a directed pencil beam. No maintained transport deck is silently substituted for the historical input.

The M1 card uses 95% W, 3.75% Ni and 1.25% Fe by mass; its comment incorrectly says 1.75% Fe. M5 rounded air fractions sum to 0.999999. Input comments and card values must be distinguished.

Final input requests 1e9 source histories. The selected saved mesh was normalized using 100,320,422 electron histories. Original summary electron source energy is about 6.0002 MeV per source electron. These are electrons; secondary photon tracks are not independent source histories.

## Source discretization

The notebook samples Cauchy density heights and calls its doubled radial Cauchy density truncated. Doubling gives the nonnegative half-Cauchy density on the infinite half-line; cutting at 1 cm retains only `2*atan(10)/pi`, approximately 0.93655 of its mass. Explicit finite-support normalization is needed.

The maintained illustration uses exact CDF differences over 34 bins on energy [0,12] MeV and radius [0,1] cm. It is an analytically normalized reconstruction of the intended distribution, not a byte-equivalent reproduction of the deck's SI/SP histograms. Histogram SP entries are weights; pointwise density values only approximate interval probabilities, especially for unequal-width bins. Radius probabilities are per dr; they are not uniform areal probabilities and are not multiplied by r without changing the physical source model. FWHM is twice the Cauchy scale.

## Mesh interpretation

The reader supports only this archive's photon OUT=IJ format, a single energy group and a single z slice per tally. It preserves Y-down/X-across table ordering, while plotting x/y in physical increasing coordinates. Mesh z intervals are [-1.25,-0.75], [-13.9,-13.4], and [-101.25,-100.25] cm. Tally 54 lies near the flattening-filter support: a nearby input comment labels it as after secondary collimators, but its coordinates disagree. Coordinates take precedence in interpretation.

These track-length mesh tallies are photon fluence per starting electron, with cm⁻² units for cm geometry. They are not absorbed dose in Gy. MCNP's relative errors are retained; zero-fluence bins are excluded from the descriptive median and relative-error threshold counts. Relative error alone does not demonstrate adequate sampling or unbiased results. Bin-to-bin correlations are not available, so no uncertainty of a summed fluence or normalized profile is invented.

## Recorded issues and remaining validation

The original `outw` reports termination by tty interrupt, repeated random-number-stride exceedances, all seven tally fluctuation bins failing one or more of ten checks, and bins with larger errors than recommended. The summary contains a negative electron-bank counter, consistent with a possible counter overflow but not independently diagnosed. Meshes alone cannot resolve these issues.

Before making transport accuracy claims: review geometry overlaps/voids with the intended runtime; specify and verify source angular behavior; reconcile SI/SP probabilities and comments; verify material data and cutoffs; resolve random-number stride warnings; rerun independent seeds with adequate histories; examine tally fluctuation diagnostics; and compare appropriate fluence/depth-dose/profile observables with independently measured or trusted benchmark data and uncertainties. No new MCNP transport was run for this repository.

## References

- [LANL MCNP manuals](https://mcnp.lanl.gov/manual.html): runtime-specific source, histogram, mesh and statistical-check definitions.
- [MCNP 6.3.1 Theory & User Manual (2024)](https://mcnp.lanl.gov/pdf_files/TechReport_2024_LANL_LA-UR-24-24602Rev.1_KuleszaAdamsEtAl.pdf): modern reference for tally normalization and uncertainty concepts, not a claim of historical version compatibility.
