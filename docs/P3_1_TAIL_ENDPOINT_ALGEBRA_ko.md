# P3.1a — 고정 Landau 꼬리의 유리수 끝점 전파

이 문서는 P3.1a 당시 실행을 보존한다. 뒤이어 완료한 실수 연결은 [P3 종합 기록](P3_LANDAU_TAIL_ko.md)에 있다.

상태: 유리수 끝점 대수만 검증 대상으로 추가. 실수 지수 및 실수 적분 연결은 HELD. RH 또는 원저자의 전체 정리를 증명했다는 주장이 아니다.

## 입력 고정

- 기준 입력: k=3, s=3, a=1, b=3, precision_bits=128.
- 원본 수치 기준선: ../window-results-v2.json; SHA-256 ad3d31ceaf5a9a78e5f17f5c25ac087394eb57ebfb3cfdd977aa57c61ac66bf1.
- 계산기: ../riemann_evidence/rational_intervals.py의 exp_bounds.
- 실제 꼬리 적분의 목표 공식: (1 - 13 exp(-3) + 172 exp(-9))/81. 이 등식 자체는 이번 패치에서 Lean으로 증명하지 않았다.

## 입력 구간: Python 128비트 외향 유리수 끝점

- exp(-3) 하한: 132356730205244743173018186111025421 / 2658455991569831745807614120560689152
- exp(-3) 상한: 16941661466271327126146327822211253889 / 340282366920938463463374607431768211456
- exp(-9) 하한: 20997090117932310769386338569904347 / 170141183460469231731687303715884105728
- exp(-9) 상한: 41994180235864621538772677139808695 / 340282366920938463463374607431768211456

부호가 음수인 계수 -13에는 exp(-3)의 상한을 하한식에 사용해야 한다. +172에는 exp(-9)의 하한을 사용한다. 반대쪽 경계는 끝점이 반대다.

## 실행 파일

- ../tests/lean/E2ATailEndpointAlgebra.lean: 위 끝점·기준 lower/upper를 Lean의 Rat 상수로 고정하고, 합성식의 등식·순서·임계값 1/200 채택 및 1/300 기각을 검증한다.
- ../tests/test_tail_endpoint_algebra.py: Python exp_bounds 계산 결과, Lean 상수, 원래 10개 사례 중 두 꼬리 사례를 대조한다. 잘못된 부호·끝점 선택에 대한 음성 대조 포함.
- ../tools/verify_p3_1_endpoint_algebra.ps1: Lean 4.33.1 컴파일, Python 3.10 및 3.14 추가 회귀 검사를 실행한다.

## 실행 증거

Lean 4.33.1 (commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6)에서 유리수 대수 정리가 컴파일됐다. 출력된 두 등식 정리의 공리 의존성은 propext, Classical.choice, Quot.sound이다. sorryAx는 관측되지 않았다. Python 3.10.22, 3.14.10에서 각각 전체 43개 회귀 검사가 통과했고 원래 10개 수치 사례의 보고서 해시는 유지됐다. 단독 P3.1a 영수증 r_367f5c29-5d84-4dfb-8e45-5cea514eed40, 전체 매트릭스 영수증 r_a2da68c7-3e5e-43e9-9891-d23dbf58d812. 실제 Colab, 전체 RH 커널 재실행 및 Mathlib 분석 증명은 NOT_RUN이다.

## 남은 실수 증명 의무

1. REAL_EXP_ENCLOSURE_HELD: 네 분수가 실제 Real.exp(-3), Real.exp(-9)의 포함 구간임을 Lean/Mathlib 정리로 증명할 것.
2. REAL_INTEGRAL_IDENTITY_HELD: 양의 실수축의 창 [1,3] 바깥에서 u^3 exp(-3u)/3!를 적분한 값이 목표 공식과 같음을 실수 적분가능성과 끝점 극한까지 포함해 증명할 것.
3. REAL_TO_RAT_BOUND_HELD: 위 실수 적분·실수 지수 부등식을 수치 구간의 Rat 끝점에 결속하고 원래 정리의 전제를 확인할 것.
4. ORIGINAL_SOURCE_LINK_HELD: 원저자의 landau_window_ineq 가정과 이 작은 모델의 관계는 별도 소스 검수 대상.

1–3에 대한 Lean 컴파일·검증이 완료되기 전에는 P3.1 전체 GREEN 또는 REAL_INTEGRAL_CERTIFIED로 표시하지 않는다. 현재 최대 승인 등급은 P3.1a/RAT_ENDPOINT_ALGEBRA_PASS다.
