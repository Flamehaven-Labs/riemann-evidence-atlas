# Riemann Evidence Atlas v0.3.0

This research checkpoint publishes the second Landau case, source-linked Lean and
Colab replays, and the weighted trace comparison over the rationals.

- Exact interval replay and Lean certify the second Landau tail and its close
  threshold. [Calculation and declarations](LANDAU_SECOND_CASE.md)
- The unfolded Fourier integral depends on the cutoff schedule. The product-norm
  frequency mask can leave the stated Schwartz–Bruhat domain.
  [Negative results](masullo/NEGATIVE_RESULT_REGISTER.md)
- The fixed-cutoff weighted quotient has an integrable trace density in the
  trivial-angular sector. The geometric comparison and moving-cutoff limits remain
  open. [Trace model and limits](masullo/S_LOCAL_TRACE_SPLIT.md)
- Colab Lean 4.36.0 recompiled the pinned Masullo rational exterior-zero theorem
  and verified an application with the archived Dirichlet nonvanishing hypothesis.
  Direct use of Alpöge's proof in the shared environment remains AMBER at its
  import closure. [Lean source](evidence/rational-exterior/ConditionalApplication.lean) ·
  [Receipt and replay scope](masullo/RH_PROOF_COMPOSITION_REPLAY.md)

[Research case study](RESEARCH_CASE_STUDY.md) · [Roadmap](ROADMAP.md) ·
[Checksums for public Colab evidence](evidence/rational-exterior/SHA256SUMS) ·
[Changelog](../CHANGELOG.md)

GitHub Actions runs the repository's Python and pinned Lean 4.33.1 checks.
The separate Lean 4.36.0 Colab run is represented by the included source, logs,
and receipt. The release asset contains a local evidence bundle with hash-matched
Colab logs and the documented import blockers.
