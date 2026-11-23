# Masullo 원고 및 소수 2 기준선

**Alessandro Maria Masullo, *The Music of the Primes*** · 2026-11-20 판 · 940쪽. [원본 PDF](https://math216.wordpress.com/wp-content/uploads/2026/11/the-music-of-the-primes.pdf) · [공개 공지](https://math216.wordpress.com/2026/11/20/hurried-announcement-alessandro-masullo-grh/)

로컬 파일은 `sources/masullo-2026-11-20/The_Music_of_the_Primes_Masullo_2026-11-20.pdf`에 저장한다. SHA-256은 `e039d3f6cf0a4b14f03c7edb85097752dd65c0a2fe543c76fe992be234f97bf5`다. 514쪽 cutoff 편집 메모, 519–520쪽 trace formula, 522쪽 정리 13.3.1.2의 편집 결손을 각각 기록한다. 원고의 주값 적분과 Alpöge 쪽 오일러 인자의 대응은 [P2](../PATCH_SEQUENCE_P0_P3_ko.md#p2--두-연구의-공통-국소-항-검증)에서 다룬다.

순수 유리수 기준선은 자명 문자에서 $p=2$, $s=2,3,4$의 Euler factor와 유한 소수 거듭제곱 합, 정확한 꼬리를 대조한다. [고정 JSON](P2_LOCAL_SURFACE.json) · [실행 코드](../../tools/prime_two_local_surface.py)

~~~sh
python -E -S tools/prime_two_local_surface.py --verify-report docs/masullo/P2_LOCAL_SURFACE.json
~~~

비자명·분기 문자와 conductor/modulus가 다른 사례는 후속 P2 작업이다. 이 기준선의 주장 범위는 유리수 항등식이다.
