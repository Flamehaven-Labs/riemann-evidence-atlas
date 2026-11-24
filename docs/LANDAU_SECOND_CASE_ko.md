# RH 내부 두 번째 Landau 꼬리 적용 사례

두 번째 Landau 사례의 실수 적분을 Lean으로 증명하고, Windows와 Colab Linux에서 저장된 수치 구간을 대조했다.

## 출처와 범위

원본: Deduction.landau_window_ineq의 우변 세 번째 항에서 계수 2*C0를 제외한 양의 꼬리 적분.
원본 소스: sources/rh-landauWindowIneq.lean (SHA-256 e3d5d760bcefe1242d4f5b0ced44fc055f1fa8dfe048a2222cf2c39ae812e59c).
[추출 매니페스트](../lean-extract-manifest.json). 신규 값은 원문이 보고한 새 정리가 아니라 같은 일반 커널의 독립적인 파라미터 특수화다.

| 항목 | v0.2.0 고정 형식 인증 | 이번 추가 수치 검증 |
|---|---|---|
| k | 3 | 1 |
| rate = sigma - 2 | 3 | 2 |
| 제외 창 [a,b] | [1,3] | [1/2,2] |
| 실수 적분 | (1-13 exp(-3)+172 exp(-9))/81 | (1-2 exp(-1)+5 exp(-4))/4 |
| 실수 Lean 인증 | PASS (Windows/Colab/CI) | PASS (Windows/Colab) |

## 분리한 경계

- riemann_evidence/rational_intervals.py: 정확한 Fraction 입력과 지원 정밀도(128/256/512 fractional bits)를 받아 두 Fraction 끝점을 반환한다. Landau 식, cap 판정, 출처 또는 영수증을 알지 못한다.
- window_kernel.py: Landau의 다항식·전체 질량·창/꼬리 식 및 decide_upper_cap을 관리한다.
- landau_second_case.py: 기존 CHECK를 그대로 호출하며 새 입력의 출처, 코드·매니페스트 해시 및 결과 영수증을 관리한다.
- riemann_evidence/verification.py: 입력 바이트 해시, 상태, 증거 및 claim_authority=NONE을 기록한다.

기존 구간 계산기와 판정기 파일은 변경하지 않았다. 이미 같은 경로를 사용하는 회귀 입력들이 있었으므로 이것은 문자 그대로 두 번째 수치 입력이 아니라, 별도 출처·대조·고정 영수증을 갖춘 두 번째 Landau 특수화다. 새 공용 패키지와 NSRW 어댑터는 만들지 않았다.

## 고정 판정과 반증

새 적분 J는 약 0.08895482802519657이다. [정확한 유리수 끝점과 입력/결과](landau-second-case.json).

| 대조 | 정밀도 | 기대 상태 |
|---|---:|---|
| cap = 1/10 | 128 | PASS |
| cap = 1/20 | 128 | FAIL |
| 근접 cap (고정 유리수, 영수증 참조) | 128 | UNRESOLVED |
| 동일 근접 cap | 256 | PASS |

판정 계약: 유효한 구간 [L,U]에서 U <= cap이면 PASS, L > cap이면 FAIL, L <= cap < U인 상태로 정밀도 예산이 소진되면 UNRESOLVED. 입력 거부도 기존 CLI에서는 FAIL로 기록하므로 부등식 반증과는 reason으로 구분한다. 순서가 뒤집힌 구간 또는 Fraction이 아닌 끝점은 계산 오류로 거부한다.

정상 구간을 직접 교대 Taylor 급수 180/181차의 유리수 상·하계로 대조한다. 두 양의 x=1,4에서 해당 차수 이후 항의 크기가 단조 감소하며 0으로 간다는 교대급수 조건을 이용한다. 변조된 정상 순서의 끝점, precision 타입, cap 및 UNRESOLVED를 PASS로 위장한 영수증도 거부한다.

현재 지원 범위에서 _small_exp의 내부 1024회 한계는 유효 입력으로 도달할 수 없는 것으로 해석된다: y<=1/2, 최대 work bits=576이면 1024차 이후 기하 나머지는 2^(-1024)보다 작아 허용 오차 2^(-580)보다 작다. 이번에는 역사적 계산기를 수정하지 않았다. 내부 한계가 바뀌거나 입력 범위가 확대될 경우, 예산 소진 예외를 입력 오류와 분리하는 검사를 추가해야 한다. 이번 UNRESOLVED는 유효 구간이 cap을 가로지르는 판정 예산 소진이다.

## 재현

~~~sh
python -E -S landau_second_case.py --verify-report docs/landau-second-case.json
python -E -S -m unittest discover -s tests -p test_landau_second_case.py -v
python -E -S tools/verify_baseline.py
~~~

기존 10개 사례 영수증과 Lean/Colab 증거는 수정하지 않는다. 추가 영수증의 SHA-256은 1e2ba00fd1ff34bf13145ad1838f12b01029ada14a0baac670a6bd7758d15121이다.

2026-11-24 초기 수치 실행에서 Python 3.10.22 및 3.14.10은 각각 51개 테스트를 통과했다. 기존 10개 수치 사례와 로컬 노트북 스모크도 통과했다. 수치 영수증은 그 시점에 실수 Lean 증명이 미실행임을 기록한다. 실행 영수증 r_a9265237-bbae-48be-b902-5bf99fdf4458.

## 실수 적분의 Lean 증명

감마 적분으로 양의 반직선 전체 기여가 $1/4$임을 확인하고, 원시함수로 $[1/2,2]$의 기여를 계산해 뺀다. Mathlib의 Taylor 나머지 정리로 $e$의 유리수 구간을 증명한다. 양의 구간에서 역수와 네제곱을 이용해 $e^{-1}$, $e^{-4}$를 감싼다. 닫힌식의 계수 $-2$에는 반대쪽 끝점을 써서, 두 항의 경계를 Python에 저장된 정확한 256비트 구간 안으로 연결한다. [Lean 소스](../tests/lean/E2ALandauSecondCase.lean)

고정 Lean 4.33.1과 Mathlib에서 적분 등식, $e$의 구간, 꼬리 적분의 256비트 포함, 임계값 비교를 각각 컴파일했다. 실제 적분은 $1/20$보다 크고 고정한 근접 임계값 및 $1/10$ 이하다. 네 선언의 공리는 `propext`, `Classical.choice`, `Quot.sound`다. [형식 증명 영수증](landau-second-case-lean-replay.json)

기존 수치 영수증의 끝점·근접 임계값은 그대로다. 실행기는 Lean 파일의 세 유리수 값과 수치 영수증을 대조하며, 별도 임시 디렉터리에서 의존 정리와 새 실수 정리를 컴파일한다. Mathlib 환경 복원이 필요한 경우 기존 [Landau 재현 절차](P3_LANDAU_TAIL_ko.md#재실행)를 따른다.

~~~sh
python -E -S tools/verify_landau_second_case_lean.py --lean "$LEAN_BIN" \
  --mathlib-project formal/landau --expect docs/landau-second-case-lean-replay.json
~~~

Windows에서 두 번 컴파일해 동일한 영수증을 얻었다. SHA-256은 `8524abfecbbde27117d3ebbe4dcd8caba2bd0667bd7a5f17e2f648ca71f0fa12`다. 2026-11-24 Colab Linux에서 고정 Lean 4.33.1과 Mathlib으로 네 선언을 다시 컴파일했다. Lean 배너의 호스트 표기를 제외한 영수증 필드가 모두 일치했다. Linux 영수증 SHA-256은 `d4eab82887fa2d7f70414da71de6b74457a1a1dca84a552a532ba4fe1f5c1d93`이다. 이 추가 사례의 GitHub Actions 실행은 남아 있다. [Colab 원본 영수증](landau-second-case-colab-replay.json)
