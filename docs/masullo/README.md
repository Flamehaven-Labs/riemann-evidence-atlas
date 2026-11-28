# Masullo Manuscript and Prime-2 Baseline

**Alessandro Maria Masullo, *The Music of the Primes***, 2026-11-20 edition, 940 pages. [Original PDF](https://math216.wordpress.com/wp-content/uploads/2026/11/the-music-of-the-primes.pdf) · [Public announcement](https://math216.wordpress.com/2026/11/20/hurried-announcement-alessandro-masullo-grh/)

The local copy is `sources/masullo-2026-11-20/The_Music_of_the_Primes_Masullo_2026-11-20.pdf` with SHA-256 `e039d3f6cf0a4b14f03c7edb85097752dd65c0a2fe543c76fe992be234f97bf5`. Record the cutoff editorial note on p. 514, the trace formula on pp. 519–520, and the missing statement in Theorem 13.3.1.2 on p. 522 separately. [P2](../PATCH_SEQUENCE_P0_P3.md#p2--compare-the-local-term-in-both-sources) studies the correspondence between the principal-value integral and Alpöge's Euler factor. [Biorthogonal norm analysis](BIORTHOGONAL_GAP.md) traces the uniform bound on p. 451 and its downstream uses.

The exact rational baseline compares the Euler factor, finite prime-power sum, and exact tail for the trivial character at $p=2$ and $s=2,3,4$. [Pinned JSON](P2_LOCAL_SURFACE.json) · [Replay code](../../tools/prime_two_local_surface.py)

~~~sh
python -E -S tools/prime_two_local_surface.py --verify-report docs/masullo/P2_LOCAL_SURFACE.json
~~~

P2 extends the calculation to nontrivial and ramified characters and to differing conductors and moduli. See the [prime-2 character comparison](P2_CHARACTER_COMPARISON.md) for the exact results and the status of the principal-value correspondence.
