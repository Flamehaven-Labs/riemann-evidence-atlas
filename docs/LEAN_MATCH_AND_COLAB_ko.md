# Lean 대조 및 Colab 실행 순서

2026-11-24 · Lean 4.33.1, 커밋 `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`

| 시점 | 환경 | 완료 기준 |
| --- | --- | --- |
| P0 | 로컬 깨끗한 체크아웃 | Python 기준선과 기존 Windows 고정 영수증 재현. `v0.2.0-rc.1`에 고정 |
| P1 지금 | 로컬 고정 Lean | 합성 선언의 두 Choice 경로, 선언 종류·TYPE·VALUE, 원본 보조 증명의 직접 참조를 각각 대조 |
| P1 Colab | Colab Linux CPU | Python 기준선과 합성 Lean 영수증 재생 완료. 원본 `RhOfRight.olean` 대조는 후속 작업 |
| P2 | 로컬 우선, P1이 통과한 Colab에서 재생 | 소수 2 유리수 비교와 실패 대조. 원문 대응은 별도 증거로 기록 |
| P3 | Lean 환경과 Mathlib 핀 확정 뒤 로컬 또는 Colab | Rat 임계값과 실수 적분 증명을 구분해 컴파일. 소스·정리문·공리·실행 로그와 결과 해시 보존 |

Colab Linux CPU에서 Python, 합성 Lean, Landau 유리수·실수 증명을 순서대로 재현했다. 다른 세션에서 재생할 때는 브랜치 이름 대신 커밋을 지정한다. 원본 `.olean` 대조에는 SHA-256이 확인된 파일을 별도로 사용한다. Colab의 플랫폼과 Lean 버전 문자열을 기록하고, 선언 대조에는 고정 Lean 커밋, 입력·검사 코드 해시, 타입·값 참조와 판정을 사용한다.

## Colab 재현 방법

확정된 Git 커밋의 저장소 루트에서 실행한다. CPU 런타임과 `elan`이 준비된 환경을 사용한다.

~~~sh
elan toolchain install leanprover/lean4:v4.33.1
LEAN_BIN="$(elan which lean)"
python -E -S tools/verify_baseline.py
python -E -S tools/verify_lean_match.py --lean "$LEAN_BIN" \
  --expect docs/rh-lean-fixture-match-v2.json > /content/rh-lean-fixture-match.json
~~~

원본을 추가할 때는 `--rh-of-right /content/RhOfRight.olean`을 전달하고 기대 파일을 `docs/rh-lean-helper-match-v2.json`으로 바꾼다. `--expect`는 로컬과 Colab의 플랫폼 문자열을 별도로 보존하면서 선언 대조와 입력 핀의 SHA-256을 검사한다. 파일 결측, 해시 불일치, Linux에서의 원본 `.olean` 로드 실패는 해당 실행 기록에 남긴다. P3.1의 유리수·실수 단계는 [Landau 재현 명령](P3_LANDAU_TAIL_ko.md#재실행)을 따른다.

## 2026-11-24 Colab 실행 결과

커밋 `aff300de0b5a0be2affb3c89f1c7f5e5fddb704e`의 추적 파일로 입력 ZIP을 만들었다. 입력 ZIP의 SHA-256은 `d958058f9de18c4d1a79b7462c6213f47b8327fa9a68717fdb552a5ada620bbf`다. Colab Linux x86-64 CPU와 Python 3.13.18에서 Python 45개 테스트·10개 수치 사례, 합성 Lean 선언 대조, Landau 유리수 단계와 고정 Mathlib 실수 정리 5개를 통과했다.

실수 영수증의 SHA-256은 `45fb8d94c5969278472f0c9b828d21dd7f97db81edf7ab898e989fed8cbd975e`다. Lean 플랫폼 배너 외의 필드는 Windows 영수증과 모두 일치했다. [Colab 영수증](landau-tail-colab-replay.json) · [Windows 기준 영수증](landau-tail-lean-replay.json)

첫 실행 묶음에서 Git 추적 매니페스트 3개가 빠져 같은 커밋에서 보완했다. 그다음 Mathlib 캐시 도구가 Lake 작업 폴더의 `lean-toolchain`을 요구한다는 점을 확인했다. Colab에서 루트 핀의 바이트를 복사해 재실행했고, 저장소에는 [Lake 프로젝트 핀](../formal/landau/lean-toolchain)과 CI의 일치 검사를 추가했다. Colab에서는 원본 RH의 `.olean` 대조와 전체 커널 재실행을 수행하지 않았다. GitHub Actions에서 각 커밋의 실행 결과를 확인할 수 있다. [워크플로 실행 기록](https://github.com/Flamehaven-Labs/riemann-evidence-atlas/actions/workflows/checks.yml)

## P1 로컬 대조 결과

- 합성 Lean에서 정의 경유 Choice와 증명 경로 Choice를 모두 확인했다. 값이 없는 공리의 `value_refs`는 `null`로 기록하며, 참조가 없는 저장 본체는 빈 목록으로 표현한다. [합성 기준 기록](rh-lean-fixture-match-v2.json)
- 원본 `rh_of_right._proof_1_1`과 `_proof_1_2`의 직접 VALUE 참조는 각각 57개이고 두 집합이 일치한다. 중복 제거한 57개 중 53개를 Lean `Init`에서 대조했다. 네 미해결 선언은 `Int.instLinearOrder`, `LinearOrder.toPartialOrder`, `PartialOrder.toPreorder`, `Preorder.toLT`다. [원본 기준 기록](rh-lean-helper-match-v2.json)
- P3 환경을 준비하면서 고정 Mathlib의 세 컴파일 파일에서 위 네 선언을 추가로 확인했다. 직접 참조 57개가 `Init` 또는 고정 Mathlib에서 확인됐다. [후속 대조 기록](rh-mathlib-frontier-match.json)
- USTAR·PAX·GNU 긴 경로 테스트를 통과했다. 보존된 압축 조각 36개를 제한적으로 재검색한 결과 `VwinOfRow.olean`는 `HELD`다. 고정된 14조각 소스 아카이브에서는 `VwinOfRow.lean` 4행의 `theorem UpperTheory.One.vwin_of_row`를 확인했다. 해당 소스의 SHA-256은 `d2df45a5cf337190ae6f885e8e43056ae4e804ae8da250a2ab0abd64b1ca7080`이다. 컴파일된 VALUE 간선의 추가 추출에는 여전히 고정 `.olean`이 필요하다. [소스 아카이브](../lean-archive-manifest.json)

P1의 선언 매치는 저장된 표현식의 검증 범위다. RH 전체 증명의 Lean 커널 재검사와 독립 운영자 재현은 별도 실행으로 기록한다.
