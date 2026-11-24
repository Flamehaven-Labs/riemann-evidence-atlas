# P0–P3 독립 검수 보고서 · 2026-11-23

**판정: BOUNDED ACCEPT / GLOBAL ACCEPTANCE HELD.**

이 문서는 11월 23일에 관측한 상태를 보존한다. 캐시 경로 지정과 영수증 대조는 [현재 P3 재현 절차](P3_LANDAU_TAIL_ko.md)에서 확인할 수 있다.

## 1. 검사 대상
- 로컬 경로: D:\Sanctum\research-sidequests\riemann-lean-2026-11-22
- 로컬 main HEAD: 74beab42c6dfb1b4096cf782c0fb46511c5227f9
- 공개 저장소: https://github.com/Flamehaven-Labs/riemann-evidence-atlas
- 공개 main HEAD: 360ba23f411b39c03b0cddb6d266816d93d5433c (Initial commit)
- GitHub Actions 실행 0건, Release 0건. 원격 동기화·릴리스 승인 전 상태.

## 2. 직접 재실행 근거
- Python 3.10.22/3.14.10 각각 **43/43** 회귀 테스트와 기존 10개 수치 사례 REPORT MATCH. 영수증 r_88779462-1670-42ab-9751-341f880458aa.
- Lean 4.33.1 고정 Rat 끝점 대수 컴파일 PASS; propext/Classical.choice/Quot.sound 공리 출력 확인. 영수증 r_88779462-1670-42ab-9751-341f880458aa.
- Mathlib 실수 적분 5개 정리 PASS는 **저장된 사전 실행 기록** docs/landau-tail-lean-replay.json에 존재. 해당 보고서 SHA-256 a4bbb8951ec28fec7044e982c1df48f88e457edffe3bb865fe46b61b8590c828.
- **이번 독립 실수 정리 재실행은 ENV_BLOCKED.** formal/landau/.lake/packages/mathlib이 없어 verifier가 종료 코드 2를 반환했다. Lean 자체의 proof failure가 아니다. 영수증 r_6276bf3e-7c99-4cef-8fb6-177add530de3.
- 비교 검증을 위한 스크립트: tools/audit_p3_landau_tail_real_local.ps1.

## 3. 단계별 수용 판정
| 단계 | 판정 | 아직 보류된 것 |
|---|---|---|
| P0 | LOCAL GREEN | 클린 원격 checkout과 CI의 독립 재현 |
| P1.1 | BOUNDED GREEN | 원본 RH의 완전한 전이 폐쇄 |
| P1.2 | HELD | VwinOfRow.olean 고정 본체 및 직접 proof VALUE |
| P1.3 | PARTIAL | 원본 RH에서 Classical.choice 전체 도달성 |
| P2 | LOCAL ARITHMETIC GREEN | Masullo 주값 적분과 Euler factor의 analytic equivalence |
| P3.1 | SAVED LEAN PASS / CURRENT REPLAY ENV_BLOCKED | 이번 환경에서 고정 Mathlib 캐시 복원 후 전수 재생 |
| P3.2 | HELD | 정확한 시험 함수, Haar measure, 주값·cutoff, Mellin–Laplace, trace 연결 |
| P3.3 | SCOPED GREEN | 다른 운영자/CI 재현 및 원 논문 전체 정리 검증 |

**Landau 계산의 정확한 범위**: 양의 실수축 바깥 구간 (0,∞)\[1,3]에서 integrand u^3 exp(-3u)/3!의 적분. 고정 Lean Mathlib 구현은 J=(1-13 exp(-3)+172 exp(-9))/81 및 1/300<J<=1/200의 정리를 가진다. RH·GRH 전체 정리, 원래 부등식의 나머지 항, 앞의 2C0 인자는 판정하지 않는다.

## 4. 주요 개선과 수용 게이트
1. **G0 P3 재현:** Mathlib 커밋 0df444a360eaa60ab8c11dca51a86af692955474 및 Lake lock SHA-256 799c3b1ddf8eeffc9ed81510f37d8d6beb5479dc261ce3b3c01a205cd6d27667 고정. Mathlib 캐시를 준비하고 동일 verifier의 5개 실수 정리와 공리 기록을 원장과 재대조. ENV_BLOCKED를 PASS로 처리하지 말 것.
2. **G1 CI:** Python Windows/Linux × 3.10/3.14와 Lean 4.33.1+고정 Mathlib job 분리. 완전한 소스/결과 해시와 negative-case 결과를 실행 증거로 보존.
3. **G2 GitHub:** 로컬 커밋을 검수 후 동기화. 공개 main은 아직 Initial commit, Actions run 없음. README links, workflow, commit hash를 실제 GitHub에서 확인하기 전 태그·릴리스 보류.
4. **G3 P1:** VwinOfRow.olean 및 Classical.choice 전이 경로를 보류로 유지. 공개 그래프 후보를 컴파일 증명 근거로 대체하지 말 것.
5. **G4 P2/P3.2:** Masullo 원문 519–520쪽의 시험 함수·측도·주값·cutoff, 522쪽의 최종 진술 결손을 소수 2 국소산술의 GREEN과 분리.
6. **G5 문서 drift:** README의 구식 'Landau 실수 적분 후속' 문장을 고정 결과의 현재 상태로 갱신. PATCH_SEQUENCE의 과거 23/23와 현재 43/43을 시점이 다른 영수증으로 분리.
7. **G6 재현 등급:** 수치 산술, Lean Rat, Lean Real, Lean proof-ref 추출, original proof kernel replay 및 source theorem equivalence를 하나의 GREEN으로 합치지 말 것.

## 5. 로컬 명령
- Python: pwsh -NoProfile -File tools/validate_python_matrix.ps1
- Lean Rat: pwsh -NoProfile -File tools/verify_p3_1_endpoint_algebra.ps1
- Lean Real (Mathlib 준비 후): python -E -S tools/verify_landau_tail.py --lean <lean4.33.1> --mathlib-project formal/landau
- 감사 도구: pwsh -NoProfile -File tools/audit_p3_landau_tail_real_local.ps1

이 기록은 원저자의 정리 증명 또는 peer review를 대체하지 않는다. 재현 가능한 checkable surface와 그 경계를 기록한다.
