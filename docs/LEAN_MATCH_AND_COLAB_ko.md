# Lean 대조 및 Colab 실행 순서

2026-11-23 · Lean 4.33.1, 커밋 `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`

| 시점 | 환경 | 완료 기준 |
| --- | --- | --- |
| P0 | 로컬 깨끗한 체크아웃 | Python 기준선과 기존 Windows 고정 영수증 재현. `v0.2.0-rc.1`에 고정 |
| P1 지금 | 로컬 고정 Lean | 합성 선언의 두 Choice 경로, 선언 종류·TYPE·VALUE, 원본 보조 증명의 직접 참조를 각각 대조 |
| P1 다음 | Colab Linux CPU, 공개 Git 커밋 확정 후 | Python 기준선과 합성 Lean 영수증을 같은 커밋으로 재생. 고정 `RhOfRight.olean`을 확보한 세션은 원본 대조까지 확장 |
| P2 | 로컬 우선, P1이 통과한 Colab에서 재생 | 소수 2 유리수 비교와 실패 대조. 원문 대응은 별도 증거로 기록 |
| P3 | Lean 환경과 Mathlib 핀 확정 뒤 로컬 또는 Colab | Rat 임계값과 실수 적분 증명을 구분해 컴파일. 소스·정리문·공리·실행 로그와 결과 해시 보존 |

첫 Colab은 P1의 합성 Lean과 Python 재현에 사용한다. 공개 저장소 생성 후 브랜치 이름 대신 커밋을 지정해 체크아웃하면 된다. 원본 `.olean` 세션은 SHA-256이 확인된 파일을 별도로 제공할 수 있을 때 수행한다. Colab의 플랫폼과 Lean 버전 문자열을 기록하고, 선언 대조에는 고정 Lean 커밋, 입력·검사 코드 해시, 타입·값 참조와 판정을 사용한다.

## Colab 첫 실행

확정된 Git 커밋의 저장소 루트에서 실행한다. CPU 런타임과 `elan`이 준비된 환경을 사용한다.

~~~sh
elan toolchain install leanprover/lean4:v4.33.1
LEAN_BIN="$(elan which lean)"
python -E -S tools/verify_baseline.py
python -E -S tools/verify_lean_match.py --lean "$LEAN_BIN" \
  --expect docs/rh-lean-fixture-match-v2.json > /content/rh-lean-fixture-match.json
~~~

원본을 추가할 때는 `--rh-of-right /content/RhOfRight.olean`을 전달하고 기대 파일을 `docs/rh-lean-helper-match-v2.json`으로 바꾼다. `--expect`는 로컬과 Colab의 플랫폼 문자열을 별도로 보존하면서 선언 대조와 입력 핀의 SHA-256을 검사한다. 파일 결측, 해시 불일치, Linux에서의 원본 `.olean` 로드 실패는 해당 실행 기록에 남긴다. 첫 실행은 실제 Colab VM에서 아직 수행되지 않았다.

## P1 로컬 대조 결과

- 합성 Lean에서 정의 경유 Choice와 증명 경로 Choice를 모두 확인했다. 값이 없는 공리의 `value_refs`는 `null`로 기록하며, 참조가 없는 저장 본체는 빈 목록으로 표현한다. [합성 기준 기록](rh-lean-fixture-match-v2.json)
- 원본 `rh_of_right._proof_1_1`과 `_proof_1_2`의 직접 VALUE 참조는 각각 57개이고 두 집합이 일치한다. 중복 제거한 57개 중 53개를 Lean `Init`에서 대조했다. 네 미해결 선언은 `Int.instLinearOrder`, `LinearOrder.toPartialOrder`, `PartialOrder.toPreorder`, `Preorder.toLT`다. [원본 기준 기록](rh-lean-helper-match-v2.json)
- USTAR·PAX·GNU 긴 경로 테스트를 통과했다. 보존된 압축 조각 36개를 제한적으로 재검색한 결과 `VwinOfRow.olean`는 `HELD`다. 공개 그래프는 후보 선언 위치를 제공한다. 실제 원본 간선은 해당 파일의 고정 해시와 선언을 검사한 뒤 수용한다.

P1의 선언 매치는 저장된 표현식의 검증 범위다. RH 전체 증명의 Lean 커널 재검사와 독립 운영자 재현은 별도 실행으로 기록한다.
