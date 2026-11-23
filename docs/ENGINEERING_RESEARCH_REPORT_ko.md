# Equation to Artifact — RH/NSRW/TOE: Machine-first Proof Atlas 및 재현 연구 설계

**기준:** 2026-11-22, 연구 설계·정적 검사 단계. **수학적 정리 재증명/검증 결과가 아니다.**

**실제 점검 워크스페이스:** `D:\Sanctum\research-sidequests\riemann-lean-2026-11-22` (Flamehaven MCP 읽기 전용).
**검수 분리:** (A) 제공된 소스의 현재 파일 내용 직접 열람; (B) 외부 1차 출처의 공개 검증 기록; (C) 독립적으로 구현·검증해야 하는 연구 제안. 이 셋을 혼동하지 않는다.

## 0. 즉시 결론

현 워크스페이스는 원본 RH Lean 배포 아카이브 14개, 고정 명제/진입점, 175,187모듈 import 그래프, 관련 PDF 4종, NSRW 기반 구간 계산과 비교 기록까지 포함한 의미 있는 **소스 수집 + 기계 색인 + 제한된 계산 실험**이다. 그러나 `rh-proof-trace.json` 자체에 `kernel_dependency_closure: NOT_RUN`이 명시되어 있고, `RH_NSRW_Window.ipynb`의 notebook output은 비어 있다. `window-results.json`에는 `window_kernel.py`에서 정의한 6개 케이스 중 5개만 기록되어 있다. 이 셋은 직접 확인한 개선 지점이다. 전체 수학적 증명 검증이나 독립 운용 재현을 주장할 근거가 아니다.

**핵심 전환:** 자료를 `파일 목록`이 아니라 `명제 × 가정 × 실제 proof term × 수치 인증서 × 계산 결과 × 문서 해석 × 적용 실험`의 **이종 증거 그래프(heterogeneous evidence graph)**로 관리한다. 최종 성과는 새로운 theorem claim이 아니라, 무슨 연결이 있는지와 무엇이 빠졌는지 표시하는 `Evidence Cut Atlas`다.

## 1. RH의 구체적 역공학 진입점

현지 보존된 `sources/rh-Main.lean`은 `Statements`와 `Supplements.Kernels.MainTheoremsAll`을 import하고 다섯 개의 최상위 정리를 연결한다. 정리 `riemannHypothesis`는 Mathlib의 `RiemannHypothesis`이고, `rhOfAll : RiemannHypothesis := Formalism.VW.rh_of_every allChi`로 조립된다. `allChi`는 `UpperTheory.EveryCharacter`로 향한다. 이것은 최종 결론의 **표시와 출구**다. 최종 12줄을 확인했다고 내부 증명 전체의 신뢰 기저가 12줄이 되는 것은 아니다. 정리 선언, Mathlib 정의, 모든 import, 실제 사용된 declaration dependency, Lean 커널 및 실행 환경은 분리된 감사 대상이다.

`rh-proof-trace.json`은 175,187개 모듈과 753,569 내부 import edge를 기록하고, `Main → … → landauWindowIneq`의 **한 import 경로**를 저장한다. 그러나 import 경로는 proof term이 그 선언을 실제 참조한다는 논리적 증거가 아니다. `Main` 정리에서 시작해 Lean elaborated term의 `ConstantInfo.type`, `.value`, 전개된 definition, instance 선택 및 universe parameter를 이용해 **선언 단위의 transitive dependency closure**를 추출해야 한다. `lean4export`와 `leagent`의 단일 선언 추출 방식, LeanDojo의 AST/전술 상태 추출을 후보 구현 경로로 검토한다. 여기서 얻은 그래프만이 정리별 실제 수학적 종속 후보를 표현한다.

### RH Bridge L1: `landau_window_ineq` vs `window_kernel.py`

Python은 제한된 구간의 다음 적분에 대해 정확 유리수로 직렬화된 포함 구간을 계산한다.

\[
J_{k,r}(a,b)=\int_a^b \frac{u^k e^{-ru}}{k!}\,du,
\quad k\in\mathbb N,\ r>0,\ 0\le a<b.
\]

이 값에는 닫힌 형식이 있다.

\[
J_{k,r}(a,b)=\frac{e^{-ra}P_k(ra)-e^{-rb}P_k(rb)}{r^{k+1}},
\qquad P_k(z)=\sum_{j=0}^{k}\frac{z^j}{j!}.
\]

이 식은 적분 자체에 관한 확인 가능한 부분이다. RH의 `landau_window_ineq_int`에는 `σ>2`에서 `u^k exp((2-σ)u)/k!`를 `[0,∞)` 위 적분 가능하게 하는 정리가 있다. **후보 매핑** `r=σ−2`가 있으나, Python의 `[a,b]` 구간, Lean의 `Ioi 0`, 또 `WindowHypU`에서 사용하는 `[U,(1+δ)U]`와 `g≤R`·가중 적분 상계 사이에는 최소 3개의 별도 의무가 있다.

1. `r=σ−2`, 변수·측도·`k!` 정규화 및 구간의 정확한 대응 증명.
2. Python 수치 상계가 analytic function `R(u)` 또는 `g(u)`의 상계를 제공한다는 별도 형식 연결; 현재는 보이지 않음.
3. 무한 꼬리 및 가중치, `θ`, `δ`, `η`, `U`, `γ`의 양화순서와 적분 가능성·부호 조건 보존.

**중요:** 구간 내 양의 커널 질량을 검증하는 일과 복소 함수의 영점을 배제하는 일은 다르다. 이 둘은 `RH-L1`~`RH-L5`의 독립 bridge obligations로 보존해야 한다.

### RH Bridge L2: 수학적 '아이디어'의 압축

제3자 읽기 가이드 Yan Ru Pei(2026-11)의 분석에 따르면 원래의 시도는 유한체 위 Stepanov 보조다항식 방법의 구조를 정수론·자동형식·산술기하학의 환경으로 옮긴 것으로 해석할 수 있다. 첫째, inert prime에서 강제 divisibility를 얻고, 둘째, Bost slope inequality로 전역 비용을 제약하며, 셋째, theta lift를 연쇄해 신호를 누적하고 비용을 나누는 구조다. 최종적으로 Riesz mean의 한쪽 오차항을 제어해 windowed Landau 정리로 전달한다. **이것은 가이드 작성자의 해석**이며 우리 자신의 수학적 새 정리나 직접 검증 결과가 아니다.

실제 약점 위치로는 강제 divisibility (`adm2`, `SelectionServed`), frame defect 포함 평균 slope, archimedean/main-term 정밀 상쇄, 균일 Selmer 상계 (`WWin`), covolume (`VolumeTheoremX`), `RecTExists`/`RowOb`의 약한 선언과 downstream 사용 조건이 지목된다. 이름으로 뜻을 확정해서는 안 되므로 각각 선언된 type, 인스턴스와 증명 term을 추출해 **분모·상수·균일성·비공허성**을 체크해야 한다.

기술적 패턴만 분리하면 추상 비용모형 `E(m)=Ax/m+Bm`에서 `m≈√(Ax/B)`로 균형을 맞춘다는 것이 남는다. 이는 NSRW의 증명 탐색 예산, 증거 체인 분할, 고정비/반복비 설계에 **휴리스틱**으로 쓸 수 있다. 물리적 오류나 theta-lift 성립을 보장하는 수학적 함의가 전혀 없으며, TOE에 이 지수법칙이 유효하다는 뜻도 아니다. 패키지 `math_patterns.py`에 이 모형의 **정확 유리수 정수 최적화**를 구현했다.

## 2. Blind spot / Missing-link 공격 목록

| 코드 | 구체적 문제 | 왜 중요한가 | 독립 관측 수단 | 판정 |
| --- | --- | --- | --- | --- |
| B01 | import 경로를 proof term dependency로 착각 | 미사용 모듈을 핵심 정리로 오판 가능 | elaborated `.type/.value` 또는 export closure | `NOT_RUN` 확인 |
| B02 | PDF 설명을 Lean 명제와 동일시 | PDF가 코드 이후에 생성·수정될 수 있음 | 문장·양화사·단위·가정/결론 대응표 + reviewer | OPEN |
| B03 | `WindowHypU` 가정과 finite kernel 계산 사이의 연결 | 양의 적분만으로 영점 배제 불가 | bridge Lean lemma, source-to-code fixture | OPEN |
| B04 | `sorry` 0건을 형식적 완결성과 동일시 | 전 환경 공리와 실제 증명 의존 공리가 다름 | `#print axioms`, 독립 커널, statement comparator | 외부 일부 실행, 로컬 미실행 |
| B05 | 조건부 형식정리의 전제가 비어 있을 수 있음 | `P→Q`는 `P`가 구성되지 않아도 정리 | 실제 `P` 만족 witness, 타입과 필수 상수 검사 | OPEN |
| B06 | 수치 인증서를 같은 알고리즘으로 재계산 | 동일 오류가 반복될 수 있음 | 독립 식 전개·대체 backend·mutation | OPEN |
| B07 | 초고정밀 계산에서 실제 error provenance 누락 | 128/200/320 bit라는 숫자가 엄밀성 보증은 아님 | 엄밀 remainder, dyadic outward proof, sign test | OPEN |
| B08 | 소스 업데이트 및 patched package 미재빌드 | 이전 release PASS를 현재 bytes에 부당 상속 | patch-by-patch rebuild 및 깨끗한 CI | OPEN |
| B09 | test 코드 6건 vs 저장 결과 5건 | 증거 패키지의 case coverage 드리프트 | Python AST inventory × JSON result keys | 차이 확인 |
| B10 | Notebook execution count/output 없음 | 재현 의도와 재현 증거의 차이 | 신규 clean run의 명령·stdout·해시 receipt | 확인 |
| B11 | Git identity 부재 | 소스 바이트 고정과 repository commit provenance는 별개 | Git commit/clean checkout 또는 content manifest | MCP git unavailable |
| B12 | 새로운 물리 도메인으로 무검증 전이 | 비슷한 PDE/적분이 도메인 유효성을 보장하지 않음 | 단위·baseline·실험·heldout test | 검증 전이 금지 |

### B05 상세: 비공허성(non-vacuity)·숨은 가정 감시

Lean 커널이 확인하는 것은 **정확히 선언된 명제의 증명**이다. 형식 증명으로 `∀x, H(x)→Q(x)`를 얻었더라도 응용하려면 원하는 `x`에 대해 `H(x)`를 증명해야 한다. 자동 감사에는 `(1) theorem type의 모든 explicit/implicit binder`, `(2) typeclass instance`, `(3) 가정의 존재 증거`, `(4) '조건이 있으면'이라는 문구를 숨긴 문서 문장`을 함께 저장한다. 불가능한 가정을 내세워 참이 되는 형식적으로 올바른 정리는 **논리적 결함이 아니라 연구 목표/적용 경계의 결함**이다. 악성 코드와 구별해야 한다.

### B06 상세: 독립성 등급

- 동일 함수 재호출: 동일 계산 경로; 회귀에는 유용하나 독립 아님.
- 동일 공식, 다른 구현/언어: 구현 독립성 일부 확보; 공식 해석 오류는 공유.
- 수학적으로 동등한 다른 표현식 + 다른 수치법: 공통모드 위험 추가 감소.
- Lean 타입/커널 재생: 논리 일관성 확인; paper semantics·물리적 유용성까지 확인하지 않음.
- 독립 연구자/도메인 전문가의 가정·정리 일치 검토: 의미·현실 대응을 보완.

## 3. PDF의 machine-first 역추적 — '논문 인용'이 아니라 '명제 지도' 생성

**Source-first 트라이앵글**

```text
Original archive / Lean declaration --(term dependency, kernel replay)--> exact formal claim
            |                                                      |
            | source / line / hash                                | explicit assumptions
            v                                                      v
       PDF page & equation --(human checked semantic map)--> bridge-obligation graph
            |                                                      |
            | narrative / intuition                                | executable witness
            v                                                      v
        hypothesis registry --(falsifiers & counterexamples)--> runtime receipt
```

PDF 파이프라인은 페이지별 텍스트 색인만으로 충분하지 않다. 기호·수식·양화사·인용 위치까지 보존하는 `Equation ID`를 만들고, PDF 페이지/수식 스냅샷을 Lean declaration type과 연결한다. 등가성 자동 판정은 금지하고, `EXACT`, `ONE_WAY_IMPLICATION`, `CONDITIONAL`, `APPROXIMATION`, `NARRATIVE_ONLY`, `UNMAPPED` 중 하나로 reviewer가 상태를 남긴다. `EXACT`도 검토자 기록이 없으면 `UNVERIFIED`다.

**역변환 순서:** Lean의 ① 최종 목표 ② 현재 proof-closure의 최소 cut-set ③ 대상 이론에서 가장 큰 축약 정리 ④ 단위/정규화/정의 ⑤ 원문 대응 ⑥ 사용된 외부 부정확한 직관 확인 ⑦ 가설을 깨는 작은 반례/테스트 순서로 읽는다. PDF 순서대로 읽는 것은 발표·설명의 순서를 따르기 때문에 실제 증명 경로를 놓칠 수 있다.

**새로운 `proof idea miner` 연구 가설:** 두 graph에서 Lean 중간 정리가 강한 의미적 병목(제거 시 최종 증명이 연결되지 않음)을 형성하고, PDF에서 해당 정리의 정당화가 짧거나 없으면 우선 검토 대상으로 승격한다. 이를 `MISSING_EXPLANATION_CANDIDATE`로 표시한다. 이는 미발견 수학적 오류 판정이 아니라 **사람이 읽지 못한 의미 구간의 후보**다.

### 3.1 점수화는 검토 우선순위에만 사용

`Priority = 4×semantic gap + 3×certificate absence + 2×dependency centrality + 2×fragile precision + 1×unreviewed assumptions` 같은 정수 점수는 **작업 배치 휴리스틱**일 뿐 수학적 진위 확률이 아니다. 함수·가중치는 공개하고 순위에만 사용하며 `VERIFIED` 단계에는 절대 연결하지 않는다.

## 4. 원본 RH 증명 검수 설계

### Track A: 논리/형식 검증

1. 공개 아카이브 14개 바이트/병합 SHA pin; toolchain Lean v4.33.1 + 정확 Mathlib rev.
2. Mathlib-only `Challenge` 명제 구성, `Main` 결과와 Comparator/독립 비교 (수동 type annotation만으로 비교했다고 주장 금지).
3. 개별 정리 `#print axioms`를 자동 수집하여 실제 사용된 공리를 whitelist 대조; 환경 전체 `sorryAx` 존재를 결과 의존성과 혼동 금지.
4. clean Lake build, exported declaration/term closure, 독립 `leanchecker`/`nanoda`; 각각 tool commit, host/exit code, memory, output hash 기록.
5. 필요 시 kernel 회피/컴파일러 신뢰 공리 `native_decide` 관련 의존 확인. `noncomputable` 자체는 오류가 아니다.
6. 타입 정의의 의미·Mathlib theorem fidelity 검토, signed semantic mapping.

**독립 체커 상태를 한 칸의 PASS로 뭉치지 말 것:** MIT 기록에서는 일부 checker의 'declined/unsupported'가 정리 거짓의 증거가 아니라 checker 지원 미비인 사례도 표시된다. statement comparator mode와 전체 proof checker mode를 반드시 별도 row로 기록한다.

### Track B: 전략·수학적 독립 검수

1. `rhOfAll`에서 거꾸로 내려오는 **실제** 선언 closure를 구성한다.
2. analytic/number-theoretic bridge를 검토한다: Riesz mean → one-sided window inequality → zero-free half plane → GRH.
3. 강제 divisibility, slope inequality, theta lifts의 정량 상계, Selmer/covolume을 별도 작은 명제로 나눠 원문 조건과 대조한다.
4. 모든 불등식에서 상수의 `uniform in` 변수 범위, 부호, strict/non-strict 비교, 작은/큰 매개변수의 극한 순서를 추출한다.
5. 사용한 수학적 결과·가정의 최소 강도만 따로 적고, 실제 proof에서 전제가 유도되는지 확인한다.
6. 연구 결과는 `PROOF_STRUCTURE_RECONSTRUCTED`, `SOURCE_AGREEMENT_REVIEWED`, `INDEPENDENT_MATHEMATICAL_ARGUMENT`처럼 구분한다. 앞의 두 결과가 세 번째를 보장하지 않는다.

### Track C: 반례/실패 모드

- 명제 변형: `≤`→`<`, 분모 양수 가정 제거, `k=0`/극대 `k`/경계 파라미터.
- 인증서 변형: 정밀도 하향, 분모가 0을 포함하는 구간, 의도적 endpoint shift, 출력 한 비트 변경.
- 소스 변형: SHA pin mismatch, Mathlib version switch, import graph 재생성 후 witness 불일치.
- 의미 변형: finite interval에서 `Ioi 0`로 부당 확장, `weak`→`smooth` 결론 과잉 서술.
- 증거 변형: 과거 성공 로그를 새로운 코드에 연결, notebook output 없는 상태에서 executed 표시.

이는 각 항목에 *사전 실패 예측*을 고정하고 실행한 경우에만 OE-4 증거가 된다.

## 5. NSRW로 직접 가져올 수 있는 것

**현재 활성 경로:** 기존 E2A 원장(2026-10-05)의 `strict L2`는 clean compile 미확인, `L3`는 OPEN, 이어지는 `DeltaM<0`과 repair zero는 상위 의존성 때문에 HELD였다. 2026-11-22 현재 상태는 이 과거 snapshot으로부터 승격하면 안 되며 실제 최신 receipt를 따로 확인한다.

- `C1`: 논문/Latex 수식 ↔ Lean 정리 선언 ↔ NSRW numeric record **양방향 linkage**.
- `C2`: `statement.lock` 외에 `hypothesis.lock`, `definition fingerprint` 및 local evaluator provenance; 명제가 표면상 그대로여도 정의 변경/형 변환은 새 identity를 부여.
- `C3`: 고정밀 witness가 `local J`만 검증할 때 `global profile J` 자동 승격 금지. `SAME_SOURCE_PROFILE_F`, `F_AMP_ETA_GT_9_OVER_10`, `EXACT_FIRST_WINDOW_LOCAL_MASS_ZERO`와 누락된 Lean wrapper는 원장에 각자 OPEN으로 기록.
- `C4`: `Remainder → exact dyadic interval → Lean proof of bound`의 분리를 통해 numerics와 formal logic 연결. 초월 함수 불등식의 remainder proof가 없으면 수치값 기록만으로 승격 금지.
- `C5`: 지역 실험을 확대하기 전에 Taylor–Green vortex 같은 규칙적 benchmark와 precision/resolution drift를 먼저 검증. TR-3에서 동일 연산비용으로 기존 잔차·CFL·발산검사 등의 baseline과 비교.

**새 2026 Navier–Stokes 논문(Alpöge–Buckmaster)과 기존 NSRW 소스(OpenAI 2026)의 연구 관계는 서로 다른 소스·문제·방법임을 유지해야 한다.** 새 저자 README는 Appendix B 인증 데이터와 Arb/FLINT 128bit 검사 구현이 공개 Lean 패키지에 없으며, cell-layer 패치 적용본을 다시 전체 빌드했는지도 당시 확인하지 않았다고 기록한다. 또한 formal statement가 paper의 강한 결론 일부(`close to candidate`, `smooth profile`)를 직접 담지 않는 구간이 있다. NSRW의 최우선 이식 포인트는 전체 새 수학을 가져오는 것이 아니라 `CertificateChallenge → ExtendedCertificateChallenge → CellLayerChallenge → Solution`의 **조건부 증명 인터페이스**를 절단면으로 보는 것이다.

## 6. TOE: 수학적 모형 → 물리적 예측의 경계

이 워크스페이스에는 TOE scrutiny suite 전체 코드가 포함되어 있지 않았다. 따라서 아래는 TOE의 현재 구현 상태 판정이 아니라 **이식 제안**이다.

TOE의 각 가설은 다섯 개 독립 표면을 가져야 한다.

1. **Formal theory:** action, field equations, parameter and symmetries, admissible domain. 모든 자유계수의 dimension/units와 gauge/coordinate convention 고정.
2. **Limiting theory:** Newtonian, SR, GR, QM 등 주장한 한계에서 기존 예측을 정말 재현하는가? 정확한 교차항·한계 순서·특이 극한을 검증. 해당 이론을 재현한다는 주장 자체도 증명이 필요.
3. **Computational prediction:** theory로부터 나온 observable + uncertainty budget + numerical solver validity; solver 수렴을 물리적 실재와 혼동하지 않는다.
4. **Empirical comparison:** measured dataset ID, instrument/selection assumptions, likelihood, residual, named baseline, held-out data, prior registration.
5. **Adversarial falsifier:** gauge 변환, units 변환, perturbation, instrument systematic, out-of-domain input, degeneracy와 identifiability.

`math_patterns.py`의 `navier_stokes_unit_guard`는 위에서 가장 작은 물리 모델 선행 검사를 구현한다. `u_t`, convection, kinematic pressure gradient, `ν Δu`가 모두 `L/T²`인지 확인하며 viscosity 차원 변이를 감지한다. 이것은 **필요조건**이지 NS 방정식을 검증하거나 TOE가 옳다는 뜻이 아니다. TOE에는 같은 인터페이스를 인자별 SI dimension vector + gauge-invariance test로 확장할 수 있다.

추천 실험 우선순위: TOE에 RH의 초거대 정리를 전송하는 대신, 하나의 구체적 모형·식·파라미터 조합을 선택해 `dimensional guard → limiting case → reproducible numeric → baseline comparison → falsification`의 1개 end-to-end vertical slice를 만든다.

## 7. 산출물: 이번 구현/테스트 범위

패키지: `e2a_proof_atlas.zip` — Python 표준 라이브러리, Windows 호환, 루트 읽기 전용 (출력은 다른 위치).

- `e2a_atlas/audit.py`: source SHA pin, PDF catalog identity, 선택적 14-part archive replay, Lean lexical scan, 선택적 85MB import DAG reachable count, bridge obligations, case inventory gap.
- `e2a_atlas/semantic_graph.py`: 외부 Lean elaborator/export가 만든 *선언별* type/value 의존성 그래프의 구조를 분석. 제공 예시는 synthetic이며 실제 RH dependency closure가 아니다.
- `e2a_atlas/math_patterns.py`: 비용 균형 `Ax/m+Bm`의 정확 유리수 정수 최적화, Navier–Stokes 최소 차원 검증.
- `spec/riemann_nsrw_toe_2026-11-22.json`: RH/NSRW/새 NS2026/TOE의 4개 branch, 열린 obligations와 실제 로컬 source SHA pins.
- `tests/test_audit.py`: SHA drift, 주석 안의 잘못된 위험 토큰, static/kernal 구분, archive mutation, open bridge, path traversal, case discrepancy, exact budget, dimension mutation.
- `README.md`: 복사 후 테스트·실행 명령.

현재 패키지는 별도 실행 환경에서 **13/13 unit tests PASS**를 기록했다. 직접 연결된 Windows 워크스페이스에서의 전체 runner 실행이나 Lean build, PDF 수식의 인간 심사는 하지 않았다. 그러므로 OE 상태는 **패키지 자체 개발 테스트 완료**와 **대상 연구 주장 검증 대기**를 구별한다.

### 권장 PowerShell

```powershell
# 압축 해제한 e2a_proof_atlas 디렉터리에서 실행
python -m unittest discover -s tests -v
$Root = 'D:\Sanctum\research-sidequests\riemann-lean-2026-11-22'
python -m e2a_atlas --root $Root --spec spec/riemann_nsrw_toe_2026-11-22.json --out .\audit-preflight.json
# 모든 아카이브를 해싱하면 파일 약 239 MB를 재읽는다. 원본 디렉터리는 변경하지 않는다.
python -m e2a_atlas --root $Root --spec spec/riemann_nsrw_toe_2026-11-22.json --archive-manifest lean-archive-manifest.json --import-graph rh-import-graph.json --out .\audit-fullstatic.json
```

**단일 파일만 출력하는 audit preflight는 형식 증명 검사 실행이 아니다.** 보고서의 `source_pin_ok`는 byte identity, `bridges`의 `HELD`는 증거 연결의 누락/미확인, `case_inventory`는 테스트 기록 커버리지 상태를 뜻한다.

## 8. 다음 3개 실제 연구 실험 (검수 가능한 목표)

### Experiment E1 — `Landau finite-window` 의미 연결

입력: RH `landau_window_ineq` pinned declaration + local rational integral `window_kernel.py` + source PDF page. 산출: 변수 매핑표와 1개 Lean bridge lemma 목표, proof-free `Challenge.lean` 명제, 독립 analytical remainder, 3-way test. **성공 기준**: 유한구간 적분의 정확 부등식이 proof terms에 의해 kernel check되며 필요한 `σ>2`, `a<b`, `rate*b≤16` 등이 빠짐없이 보인다. **비주장:** RH 증명 보강 혹은 RH 증명 재검증.

### Experiment E2 — NSRW MB06 Falsifier Gate

입력: fixed `λ`, reference ratio record, exact rational bracket. 산출: independent expm1 interval algorithm 또는 다른 수학적 표현, mutation test (±1e−9 shift), receipt, one-command verifier, local J boundary declaration. **성공 기준:** baseline PASS, shifted FAIL, precision budget UNRESOLVED를 clean secondary operation에서 다시 생성. **비주장:** source profile 존재, strict L2/L3 closure, PDE 정리.

### Experiment E3 — TOE one-observable vertical slice

입력: 고정된 하나의 TOE 식/작용·field·unit schema·source/commit·baseline. 산출: limiting-case derivation, dimension/gauge guards, numerical verification, heldout observable comparison, negative result. **성공 기준:** named baseline을 넘는 지표가 preregistered gate에 따라 재현되거나, 실패가 정직하게 기록됨. **비주장:** TOE 전체 이론 검증.

## 9. 의사결정 규칙 (E2A 채택)

기존 `E2A_RESOURCE_STAGE_CROSSWALK.md`와 같은 상태 체계를 그대로 사용한다.

- `R0/R1`: pinned original source와 exact hypothesis/statement.
- `R2`: bridge design과 expected failure·counterexample 정의 (**OE-4가 아님**).
- `R3/OE-2`: 실행된 bounded artifact + exact environment + receipt.
- `R4/OE-3`: 별도 운영자의 clean replay.
- `R5/OE-4`: 선언된 mutation/assumption drift가 실제로 fail.
- `R6/TR-0`: reuse primitive를 뽑되 엄밀한 upstream lineage 기록.
- `TR-1`~`TR-6`: 도메인 대응 → controlled transfer → preregistered baseline → prototype → domain validation → operational feasibility.

하나의 자료가 `공식 형식 증명 확인`, `사람이 이해한 전략`, `검증한 수치 계산`, `실제 응용 유효성`을 동시에 대표하도록 상태를 합치지 않는다.

## 10. 우선 참고 1차·직접 자료

- Levent Alpöge, announcement: https://alpo.ge/remark.pdf (2026-11-20)
- Lean/Mathlib joint statement: https://leanprover-community.github.io/blog/posts/riemann-hypothesis/ (2026-11-21)
- Andrew Sutherland MIT verification log: https://math.mit.edu/~drew/grh/ (checker mode별 status 구분)
- RH community comparator: https://github.com/leanprover-community/riemann-hypothesis
- Yan Ru Pei roadmap (비구축 서술 분석): https://peabrane.github.io/files/pei-2026-claimed-lean-proof-rh-roadmap.pdf
- Alpöge–Buckmaster NS source & Lean README: https://github.com/tristanbuckmaster/navier-stokes
- Source pin in project: `sources.json` + `lean-archive-manifest.json` + `rh-proof-trace.json`
- NSRW existing source ledger: `E2A_RESOURCE_CLAIM_LEDGER.yaml`, `E2A_RESOURCE_STAGE_CROSSWALK.md`

### 마지막 경계

이 연구의 핵심은 RH, NS, TOE를 한 번에 증명한다는 것이 아니다. **Lean이 실제 증명한 타입, PDF가 설명한 수학, Python이 계산한 구간, 외부 인증서가 보장한 부등식, 실험에서 측정한 현상을 서로 연결하면서 어디까지가 증거이고 어디서부터 새 가정인지 보이게 만드는 것**이다. 새로운 기술이 나온다면 그 기술은 그 경계를 넘어 실제 비교 실험에서 살아남은 작은 계산 원리일 것이다.
