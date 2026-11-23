# RH × NSRW × Flamehaven-TOE — 기계용 증명 역추적 및 교차 검증 실행 명세

**문서 ID:** FH-E2A-CROSS-REPO-RFC-2026-11-23  
**버전:** 1.0 / DESIGN_AND_AUDIT_SPEC  
**기준일:** 2026-11-23 (Asia/Bangkok)  
**범위:** D:\Sanctum\research-sidequests\riemann-lean-2026-11-22, NSRW, Flamehaven-TOE  
**원본 자료:** docs/idea1.txt, docs/idea2.txt, docs/ENGINEERING_RESEARCH_REPORT_ko.md, docs/unit_test_receipt.json  
**권위:** claim_authority = NONE. 이 문서는 새 Lean 컴파일, 독립 커널 검증, 원 논문 정리의 재증명, TOE 물리적 검증 완료를 뜻하지 않는다.

> 증명은 원저자의 정리를 확립한다. E2A는 정리의 출처, 실제 명제, 수치 계산, 기대 출력, 실행 환경과 실패 경계를 좁게 보존한다. 기술 이전의 유효성은 새로운 경험적 주장으로 따로 시험한다.

---

## 1. 결정: 단순한 PDF 요약에서 Evidence Cut Atlas로

IDEA1의 원본 바이트 고정·수치 교차검사·실패 대조와 IDEA2의 실측 최신 NSRW MB08·TOE 확인, Value-DAG, 비구성적 선택 감사를 합쳐 **5개의 서로 다른 증거 축**으로 관리한다.

1. **Source axis:** 저자, paper/theorem/equation/page, 소스 해시, Lean/Mathlib pin.
2. **Formal axis:** 실제 elaborated theorem type, definition closure, proof value 의존 선언, 공리 및 typeclass.
3. **Numerical axis:** 정확 유리수/구간, 엄밀 remainder, 정밀도 예산, 독립 검사기.
4. **Execution axis:** 코드·런타임·입력·출력 해시, 독립 운영자 clean replay, 적대적 변이.
5. **Transfer axis:** NS/TOE에서 명시적 대상 식, 단위, 기준 진단, 반증 가능성, 관측 비교.

위 축을 하나의 PASS로 합치지 않는다. 다음의 연결 관계는 모두 방향과 증거를 가져야 한다.

~~~text
PDF equation --[reviewed correspondence]--> Lean declaration type
Lean declaration --[value dependencies]--> actually used lemmas/defs
Numeric certificate --[independent checker]--> bounded inequality
Bounded inequality --[formal bridge]--> theorem precondition/consequence
Executable primitive --[domain adapter + baseline]--> NS or TOE application
~~~

**핵심 질문**은 '수학적으로 무슨 결론을 얻었는가'뿐 아니라 '그 결론에 도달하면서 어디에서 새로운 가정, 정량 상계, 비구성 선택, 외부 계산, 의미적 변환이 들어왔는가'다.

## 2. 직접 열람 근거와 상태 등급

2026-11-23 Flamehaven MCP로 확인한 주요 실물:

| 위치 | 직접 관측한 범위 | 판정 한계 |
| --- | --- | --- |
| RH sidequest | 14-part 아카이브 매니페스트, 175,187 모듈/753,569 import edge 기록, RH Main/Statements, Landau 소스, 수치 검사기 | 대형 아카이브 신규 해시 재계산 및 proof-term closure 실행은 하지 않음 |
| NSRW formal/p2/P2_MB06_NormalizedJ.lean | mbRepairRatio와 조건부 normalized angular moment 정리 존재 | 현재 내용만 열람; 신규 컴파일 증거 아님 |
| NSRW formal/p2/P2_MB08_TemplateJet.lean 및 P2_MB08_ResetAmplitude.lean | hD 도함수 상한을 조건으로 하는 fixed reset + amplitude 정리 존재 | 원본 선택 cutoff의 해당 hD 무조건적 증명 아님 |
| NSRW src/nsrw/m5/lean_export.py | type-expression 인덱싱 구현 및 value_expression_id 필드 존재 | 파일의 명시적 설명상 proof value는 역참조하지 않음 |
| NSRW docs/momentbound/FIXED_PROFILE_THRESHOLD_FINDING_2026-11-14.md | 고정 튜플에 관한 기존 충분조건의 obstruction 유도 | 그 특정 경로의 obstruction이며 전체 PDE 해 불가능성 아님 |
| NSRW docs/momentbound/MB08_SOURCE_CUTOFF_BOUND_DECISION_2026-11-14.md | chosen cutoff의 명시적 numerical jet 상한 공백 분석 | 선택된 함수의 도함수에 유한 상한이 없다는 뜻 아님 |
| TOE docs/PHYSICS_CONTRACTS.md | open gap C_prec, G3 기재 | 해당 문서의 날짜·상태를 새로운 실행 성공으로 승격하지 않음 |
| TOE toe-scrutiny-suite | Ricci tolerance=0.5, Pontryagin 반올림 관련 검사, Gödel discriminant threshold 코드 존재 | HTTP 회귀/진단은 엄밀한 위상·인과 정리와 다름 |

자료 identity:
- docs/idea1.txt SHA-256: 5542a34dedebfa15345ef57065b3bf57f6bc6782dea96801f5381a52a1f3b472
- docs/idea2.txt SHA-256: cd920555126d00af8d3cc9f50845e293858e080b0d06a98b1d2ae751827d727e
- docs/ENGINEERING_RESEARCH_REPORT_ko.md SHA-256: d8ba0f259861a0625b9481fea226ae20b10fa6127ebf5fb9e2d01347e867fe7c
- docs/unit_test_receipt.json SHA-256: b2727a2e59eae5ea33d4ae441c01cf41fefdf061cc2b0ff446705d0d63b3c768
- RH 보존 병합 SHA-256: 9631b4f020199e580ba86178cb56c6e9b09f690c2369a80dc4334aa93f49c7fc (매니페스트의 과거 검사 기록)
- RH toolchain: leanprover/lean4:v4.33.1. NSRW의 다른 Lean v4.34.0-rc2 환경과 합치지 않는다.
- NSRW upstream: openai/NavierStokesAndEuler commit 8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538.

**Evidence class** = OBSERVED_SOURCE / HISTORICAL_RECEIPT / SOURCE_DERIVATION / PROPOSED_DESIGN / HYPOTHESIS. 문서만 작성한 사실은 OE-2 실행 증거가 아니다. 외부 Linux CPython 3.13.5 환경의 13/13 테스트 영수증은 sidequest Windows 독립 실행 영수증과 동일하지 않다.

## 3. 통합 F1–F10 감사·개선 원장

| ID | 문제 | 즉시 개선 작업 | 현재 |
| --- | --- | --- | --- |
| F1 | window_kernel.py run_cases() 6개 vs window-results.json 5개; notebook outputs 없음 | 기존 기록 보존, 새 versioned 6-case 결과·실행 manifest 생성 | OBSERVED / OPEN |
| F2 | 보존된 rh-*.lean 추출 파일 중 일부의 통합 출처 매핑 누락 | archive member 경로/해시/source pin 전수 인덱스 | OBSERVED / OPEN |
| F3 | rh-proof-trace.json kernel_dependency_closure = NOT_RUN, import 최단 경로의 논리적 과대해석 | TYPE_CONST / VALUE_CONST 그래프 분리 | OBSERVED / OPEN |
| F4 | finite Landau kernel 포락이 RH 영점 배제 전체를 검증하지 않음 | RH 탐색 실험과 NSRW 실제 형식 병목 구분 | OBSERVED / OPEN |
| F5 | MB06 numeric ratio 하한은 기록됐지만 formal_bridge는 NOT_COMPILED_OR_ADMITTED | source mbRepairRatio 하한을 Lean 커널에 연결 | OBSERVED / OPEN |
| F6 | 외부 e2a_atlas 13-test receipt와 해당 Windows 디렉터리의 실제 패키지 소스가 분리 | 동일 hash 원본 반입 또는 별도 아티팩트 위치 고정 | OBSERVED / OPEN |
| F7 | RH/NSRW Lean toolchain 불일치 위험 | 프로젝트별 pinned environment·comparator | PREVENTION / OPEN |
| F8 | 2026-10-05 E2A claim ledger와 11월 MB08 최신 코드/영수증 시점 혼용 | latest dated receipt 확인 후 원장 append-only 갱신 | OBSERVED / OPEN |
| F9 | TOE 수치 회귀·휴리스틱·엄밀 불변량 판정 혼합 | exact invariant / numerical approximation / model heuristic 분리 | OBSERVED / OPEN |
| F10 | MB08 Nonempty.some 선택 함수의 명시적 수치 derivative bound 미확보 | 원본 유지 트랙 vs constructive companion 트랙 분기 | OBSERVED / OPEN |

**OPEN은 논문의 오류 발견을 뜻하지 않는다.** 미실행·미연결·정량 미확정·미검토 항목을 가리킨다. 과거 HELD/FAIL은 나중 PASS가 나와도 삭제하지 않는다.

---

## 4. Lean 기계용 산출물을 역으로 읽는 프로토콜

### 4.1 실제 Value-DAG를 import DAG와 구별

기존 NSRW의 lean_export.py는 스트리밍 2-pass offset 기반으로 정리 type expression을 정규화한다. value_expression_id를 보유하지만 theorem proof value를 역참조하지 않는다고 명시한다. 확장 구현은 다음과 같다.

**Pass A — declaration index:** 이름/모듈/kind/type_expression_id/value_expression_id/universe parameters/source SHA를 인덱싱한다. 독립 Lean export source pin이 없으면 차단.

**Pass B — expression traversal:** 목표 정리의 type subtree 및 value subtree를 각각 순회한다. CONST 참조는 qualification 및 target declaration kind와 함께 기록. opaque/axiom/external 경계는 지우지 않고 terminal로 보존한다.

**Pass C — transitive closure:** type-closure와 value-closure를 각각 구성해 실제 의존 정리 및 definition body를 복원. 누락 선언, 순환·중복, schema revision, 탐색 예산 초과 시 HELD로 기록.

**Pass D — semantic crosswalk:** PDF theorem/equation ID, 양화사, 정의역, 조건, 정량 상수와 Lean binder/constructor/conclusion을 비교한다. EXACT / ONE_WAY_IMPLICATION / CONDITIONAL / APPROXIMATION / NARRATIVE_ONLY / UNMAPPED 중 하나로 수동 검수한다.

**Pass E — hypothesis/choice miner:** theorem 가정으로만 주어진 non-vacuity witness, data-definition에서 Classical.choice/Nonempty.some 선택으로 발생한 quantitative witness 공백, 동일 기호에 대한 다른 source definition, ∃와 explicit witness의 차이를 표시한다.

출력 계약(제안이며 실제 파일 생성 여부는 별도):

~~~json
{
  "schema": "flamehaven.e2a.proof_edge.v1",
  "source_identity": "sha256:<pinned archive or export>",
  "declaration": "A.B.theorem",
  "edge_kind": "VALUE_REFERENCES",
  "target_declaration": "C.D.lemma",
  "extraction_mode": "ELABORATED_VALUE",
  "status": "NOT_RUN"
}
~~~

**검수 fixture:** 사용된 lemma 1개와 import만 된 lemma 1개로 proof-value traversal의 false positive를 구분한다. 중앙성이 높은 import node가 곧 수학적 핵심 아이디어라는 주장은 금지한다. Minimum cut-set은 *그래프의 구조적 심사 후보*이지 수학적 최소 필요조건의 정리가 아니다.

### 4.2 Classical.choice: 공리 오염이 아니라 정량 비구성 경계

MB08 실제 정리:

~~~lean
theorem mb_fixed_reset_and_amplitude_of_template_derivative_bound
  (d : TailData) ...
  (hD : ∀ y : ℝ,
    |deriv AngularMomentReset.template y|
      ≤ (125 / 81 : ℝ) * 10 ^ (318 : ℕ)) :
  ∃ w : ResetWitness d 81162000,
    9 / 10 < CorrectedPulseAmplitude.amplitude
      d w.coefficients (1 / 1048576) := by
  ...
~~~

이는 **hD가 주어지면** 정리가 성립한다는 조건부 proof이다. source cutoff 분석은 일반 인터페이스로부터 지정 numerical jet bound를 추출할 수 없다고 설명한다. 특정 함수에는 어떤 유한한 상한이 존재할 수 있다. 따라서 다음을 각각 분리한다.

- CLASSICAL_CHOICE_IN_PROOF: 일반적인 고전 논리 사용; 그 자체로 거절 금지.
- NONCONSTRUCTIVE_DATA_SELECTION: 선택된 함수/데이터 자체가 외부 수치 계약 대상.
- QUANTITATIVE_WITNESS_MISSING: 필요한 명시적 상수가 현재 소스 증거에서 부재.
- FORMAL_PREMISE_OPEN: 전체 목표에 필요한 hD 가정의 실제 적용이 미결.

**방어:** sorry 0개, 표준 3공리만 사용, 얇은 Main 파일만 확인했다는 이유로 수치 증거나 논문 의미까지 검증했다고 주장하지 않는다.

### 4.3 PDF는 의미 지도, Lean은 formal proposition

Alpöge–Buckmaster의 README에 따르면 해당 프로젝트는 Lean 형식화 이후 논문이 재작성됐다. 따라서 그 사례에서는 PDF를 Lean의 문자 그대로의 컴파일 로그로 취급하면 안 된다.

PDF page/equation/theorem ID와 Lean qualified declaration을 연결할 때 다음을 보존:

- hypotheses, domain, units, boundary conditions, quantifier order, implicit instances;
- strict < vs nonstrict ≤, weak vs smooth, closeness to candidate, blow-up rate, rate uniformity;
- source PDF 페이지와 공식·원문 유형(저자, 재작성, 해설, 2차 로드맵);
- 비어 있는 쌍은 UNMAPPED, 방향이 다른 쌍은 ONE_WAY_IMPLICATION.

PDF 텍스트 추출·수식 검색은 후보 발견만 수행한다. 정확한 수식 의미 일치는 원문 페이지 시각 검수 및 Lean 선언 검토 후 기록한다. 빈 표를 EXACT로 채워 넣지 않는다.

---

## 5. 해를 얻는 전략의 수학적 검수: RH/NSRW 공통

### Track Formal: theorem identity → genuine proof

1. 출처 아카이브 및 dependency hashes 고정.
2. Mathlib-only Challenge 명제와 Solution 연결, 방대한 proof와 명제를 분리.
3. theorem별 #print axioms; 환경 전체 공리 목록과 해당 정리의 실제 의존 공리 구별.
4. clean pinned Lake build, external independent kernel checker / comparator는 tool version·mode별 상태 기록.
5. value-DAG에서 정의·lemma·opaque/axiom 경계 복원.
6. 인간 수학 검토는 Lean theorem이 논문과 같은 명제인지 따로 판정.

### Track Analytic: 수학 전략 → 검증할 구체적 절단면

- RH: finite-field Stepanov → forced divisibility → slope / theta lift → Riesz mean one-sided bound → Landau window → zero-free region이라는 독해 *가설*을, 실제 proof closure에서 사용된 선언·상수·균일성으로 확인. Pei의 해설을 커널 출력과 동일시하지 않는다.
- NSRW: strict L2/L3, DeltaM<0, repair-zero, local J, global Profile J의 가정·결론을 claim ID별 분리. 후속 파일 존재는 상류 미해결 가정의 해결을 뜻하지 않는다.
- TOE: 물리 수식, 극한에서의 기존 이론, numerical solver, independent observations를 각기 다른 증거로 보존.

### Track Numerical: counterexample와 3치 판정

- PASS: 정밀도 예산 내에서 엄밀 interval이 목표 구간/부호를 분리함.
- FAIL: 명시적 조건 위반 또는 목표에 대한 반례가 증명됨. 위조 인증서를 거부하는 FAIL은 기대된 동작.
- UNRESOLVED: 포함 구간이 threshold를 가르지 못하거나 remainder/precision budget이 부족.
- INVALID: 스키마/단위/정의역 오류. FAIL과 같은 수학적 의미로 기록하지 않는다.

동일 함수 두 번 호출은 독립 검증이 아니다. 서로 다른 유리수 양항 급수와 엄밀 구간 라이브러리, 또는 다른 수학적 표현을 비교하면 공통모드 위험이 감소하지만 완전한 독립성을 뜻하지는 않는다.

---

## 6. NSRW 실전 구현 설계

### 6.1 MB06: 직접 구현 가능한 exact ratio bridge

관측한 원본 정리는

\[
R(\lambda)=\frac{e^{17\lambda/10}-1}{e^{2\lambda}-1}
\]

을 **mbRepairRatio**로 정의한다. \(\lambda>0\)에서 분모는 양수이다.

**새 컴파일을 수행하지 않은 엄밀 수학 유도**:

\[
0<\lambda<\frac12 \implies
R(\lambda)\ge\frac{17}{20}(1-2\lambda).
\]

이는 \(e^{a\lambda}-1\ge a\lambda\), \(e^{-2\lambda}\ge1-2\lambda>0\)를 사용하면 \(e^{2\lambda}-1\le 2\lambda/(1-2\lambda)\)에서 나온다.

고정 \(\lambda=10^{-12}\)이면

\[
R(\lambda)\ge\frac{8499999999983}{10000000000000}.
\]

**구현 목표(파일 제안):** formal/p2/P2_RationalExpm1Bridge.lean

- Source mbRepairRatio 정의 자체를 사용, 임의 새 ratio 함수를 증명해 원본에 대한 증명이라고 주장하지 않음.
- Real.add_one_le_exp 등 원본 pinned Mathlib에서 실제 사용 가능한 보조정리/정의 확인 후 numerator/denominator bound를 각각 Lean에서 proof.
- fixed tuple 하한을 norm_num으로 검사.
- #print axioms 및 clean source build 영수증.
- Python mpmath interval crosscheck는 독립 오류 탐지 보조; Lean 수학적 증명을 대신하지 않음.

**해결되지 않는 가정:** SAME_SOURCE_PROFILE_F, F_AMP_ETA_GT_9_OVER_10, EXACT_FIRST_WINDOW_LOCAL_MASS_ZERO, LOCAL_J_NORMALIZATION_BRIDGE_NOT_COMPILED, SOURCE_PROFILE_FIXED_TUPLE_NOT_CONSTRUCTED, COMBINED_SCALE_AND_RESET_K_UNRESOLVED. 이 의무들을 해당 Lean/실행 영수증 없이는 유지한다.

### 6.2 MB08: Original과 constructive companion을 다른 결과로

기존 FIXED_PROFILE_THRESHOLD_FINDING_2026-11-14.md는 upstream의 combinedScale d K ≤ 1/1000 충분조건이 \(\lambda=10^{-12}\) 고정값에 맞지 않으며, 필요조건 \(\lambda<1/(30000\cdot2^{120})\approx2.508\times10^{-41}\)을 제시한다. 이는 그 충분조건 경로의 obstruction이며 Navier–Stokes의 비존재 정리가 아니다.

**Original track (O):** upstream AngularMomentReset.template을 고정하고 기존 hD를 가정으로 보존. Source의 chosen cutoff에 대한 명시적 상한 증거 없으면 HELD[QUANTITATIVE_JET_WITNESS_MISSING].

**Constructive track (C):** explicit smooth cutoff (support/plateau/smoothness/derivative bounds), 실제 matrix+quadratic operator, reset·energy polynomial을 모두 그 새로운 함수에 대해 재계산/재증명. 원본 함수와 같음을 증명하지 않으면 다른 artifact/claim ID. 성공하더라도 원본 hD의 자동 해결이 아님.

**대안 수학 연구:** 원본 template derivative 전체의 상한을 우회하면서도 실제 reset small-jets를 직접 증명하는 경로. 이 경우에도 조건 약화의 정확한 논리적 근거가 필요하다.

### 6.3 Challenge & comparator 설계

- P2_Challenge.lean에는 source-defined object와 논문/목표 theorem type만.
- Solution 모듈에는 증명 terms. statement lock + hypothesis lock + definition fingerprint.
- 외부 comparator로 정확 target type/axiom 비교, local proof build 별도.
- 결과 ledger에 MB06 ratio lower, MB06 local J, MB08 original hD, MB08 constructive companion을 서로 다른 claim ID로 유지한다.

---

## 7. TOE 실전 이식: C_prec/G3/RH1

### 7.1 C_prec — Eguchi–Hanson Pontryagin 적분

현재 문서의 C_prec 문제는 \(h=10^{-4}\) 부근의 오차 \(|I+2|<0.1\) 같은 정량 격차다. HTTP 응답의 **is_2z_integer** 표시나 \(\mathrm{round}(I/2)\cdot2\)만으로 적분의 위상 정수성을 증명하지 못한다.

제안:
1. metric·orientation·normalization·radial integrand·integration domain과 수치 tail/경계조건 고정;
2. 엄밀 interval quadrature + truncation/tail remainder bound;
3. 정확 구간 \([L,U]\) 및 정밀도 budget 기록;
4. **별도 수학적 정리**로 해당 invariant가 \(2\mathbb Z\)인 것이 입증되고 \([L,U]\subset(-3,-1)\)이 되면 -2로 고립;
5. 정수성 정리가 없다면 결과는 NUMERIC_ENCLOSURE_ONLY. domain/수치 경계 미충족 시 UNRESOLVED.

### 7.2 G3 — Gödel CTC

toe_p3.py의 ctc_discriminant < 0.9는 회귀 휴리스틱이다. **closed timelike curve**의 실제 정리에는 metric signature, \(\phi\) 주기성, 고정시간 곡선의 tangent norm 부호, 좌표/정의역, 전역 closure 조건이 필요하다.

- 독립 Lean Challenge에서 정확한 명제 및 hypotheses 추출.
- 코드의 ctc_status, ctc_discriminant, ctc_order_parameter의 의미를 formal theorem binder와 대조.
- coordinate/gauge 변환, 경계 조건, sign flipping, float tolerance mutation을 고정.
- 정리 컴파일/의미 심사 없이는 CTC_DIAGNOSTIC_CANDIDATE로 표시.

### 7.3 RH1은 ANT1의 research-only 모델

TOE docs/ALGEBRAIC_NUMBER_THEORY_INTEGRATION.md의 ANT1 및 research_only_heuristics 패턴을 재사용한다. RH SmallClassNumbers와 Landau finite window를 물리 vacuum 게이트로 연결하지 않는다.

TOE 신규 mixed proposal의 routing example:

~~~json
{
  "proposal_type": "mixed",
  "primary_router": "ai-slop-detector",
  "secondary_router": "spar",
  "toe_scope": "optional_layer",
  "claim_authority": "NONE",
  "research_tag": "RH1_NON_GATING"
}
~~~

**ai-slop-detector**는 integrity/배선/문서 표류, **SPAR**는 수학·물리 admissibility를 검토한다. 둘 다 독립 Lean checker, 정확 수치 인증서, 관측 재현을 대체하지 않는다.

### 7.4 엄밀 수학과 모델 휴리스틱 분리

| 분류 | 예 | 허용되는 주장 |
| --- | --- | --- |
| MATHEMATICAL_CONTRACT | 정확하게 정의된 Ricci=0, integer charge, theorem binder | 해당 계약의 명확한 증거가 있을 때만 |
| NUMERICAL_ENCLOSURE | 구간 구적, remainder 및 고정 입력 | 그 입력·정밀도·범위의 포함 관계 |
| MODEL_HEURISTIC_BENCHMARK | omega=(gs*b*si)^(1/3), tolerance scoring, SPAR 점수 | 모델 회귀/진단 결과 |
| EMPIRICAL_CLAIM | held-out 관측과 기존 모델 비교 | preregistered 데이터 및 측정 범위의 경험적 결과 |

차원 일치는 물리적 참의 필요조건일 수 있으나 충분조건은 아니다. TOE의 연구 성과는 formal derivation·numerical result·observation을 각각 평가한다.

---

## 8. 실제 파일·코드 변경 후보 (현재 제안 단계)

| Repository | 파일 제안 | 입력 → 출력 | 최소 DoD |
| --- | --- | --- | --- |
| RH sidequest | tools/lean_value_dag.py | pinned export + theorem ID → type/value closure | import-only fixture false positive 차단 |
| RH sidequest | tools/verify_case_inventory.py | window_kernel.py + results → missing cases | six-case inventory + 변조 테스트 |
| RH sidequest | registry/lean_extracted_manifest.json | archive member → SHA pinned records | 15 extracted files cross-check |
| RH sidequest | registry/semantic_bridges.yaml | PDF equation ↔ Lean type ↔ numeric claim | reviewer, 방향, 가정, nonclaims |
| NSRW | formal/p2/P2_RationalExpm1Bridge.lean | λ assumptions → exact ratio lower | clean Lean compile + #print axioms |
| NSRW | formal/p2/P2_Challenge.lean | proof-free source statement | comparator + lock |
| NSRW | src/nsrw/m5/lean_value_dependencies.py | NDJSON export → proof closure/choice sites | 실제 source fixture, deterministic |
| TOE | scrutiny/rigorous_pontryagin.py | integrand + interval cert → enclosure | tail & integer gate 분리 |
| TOE | scrutiny/godel_scope_audit.py | code heuristic ↔ theorem binder | evidence-based gap report |
| TOE | scrutiny/rh1_probe.py | finite arithmetic test → research-only output | SPAR non-gating 격리 |

이는 작성된 소스가 아니라 **구현할 파일명과 계약**이다. 파일을 만들 때 새로운 receipt와 hash를 부여한다.

## 9. 검증 5-Gate와 실패 주입

**Gate A — Identity:** 아카이브 part SHA, 원본 source, toolchain, Mathlib, 실행 전/후 implementation identity. 실패 시 STALE_ARTIFACT.

**Gate B — Formal/semantic:** Challenge↔Solution statement comparator, theorem별 axiom, proof-value closure, definition/binder audit. 지원하지 않는 checker는 UNSUPPORTED이지 정리 거짓이 아님.

**Gate C — Numeric independence:** exact rational producer와 다른 알고리즘의 interval checker; denominator positivity, remainder, precision, units. 동일 알고리즘 반복은 독립성 낮음.

**Gate D — Falsifier:** ratio ±1e-9 shift, 임의 수치 상한 오류, precision exhaustion, fixed template identity 변경, source SHA swap, hidden hypothesis deletion, TOE Ricci tolerance misleading PASS, CTC heuristic→theorem 문서 변이.

**Gate E — Separate clean replay:** 다른 운영자·깨끗한 checkout, stdout/stderr/exit code 및 manifest 저장, historical receipt와 distinct operator임을 명시.

각 Gate별 outcome은 PASS / FAIL / HELD / UNRESOLVED / NOT_RUN / UNSUPPORTED. 단 한 개가 실패하면 상위 claim을 verified로 승격하지 않는다. 예상된 변조 실패는 **검사기 성공**이지만 원 명제가 거짓이라는 판단은 아니다.

## 10. 실행 순서와 완료 기준(Definition of Done)

**M0 / Sidequest evidence repair**
- 기존 JSON 덮어쓰기 금지. 새로운 window-results-v2.json + manifest; 6-case coverage.
- Lean 추출물 full origin hash; notebook을 단일 Python 함수에 연결하고 중복 코드 제거.
- 이전 e2a_atlas 영수증의 구현 파일 원본 확보 또는 외부 보존 위치 명시.
- DoD: pristine PASS, removed case/hash mutation FAIL, old files unchanged.

**M1 / Proof Atlas**
- lean_export.py type 전용 코드를 보존하면서 실제 value closure 확장.
- Main 정리 5건의 lemma/def/axiom dependencies, source pins와 output hashes.
- Semantic PDF crosswalk은 review 완료 건만 EXACT.
- DoD: 실제 proof value extraction receipt + import-only false positive를 테스트.

**M2 / MB06**
- pinned Lean ratio lower proof, fixed λ exact numeric bound, comparator, independent interval crosscheck.
- local J → Profile J 조건이 충족되기 전까지 OPEN 유지.
- DoD: 좁은 Lean bridge compiled receipt, correct scope.

**M3 / MB08**
- Original hD conditional theorem type lock.
- Constructive companion에서 explicit cutoff에 대한 support/derivative/operator/reset/energy 재검증.
- DoD: 결과 두 트랙 분리, source chosen cutoff와 동등성 미증명 시 원본 CLAIM 미승격.

**M4 / TOE**
- C_prec rigorous interval + 별도 integer theorem.
- G3 exact CTC scope audit.
- RH1 research-only non-gating fixture.
- DoD: 각 실험의 입력/조건/기준 구현/negative result와 하나의 reproducible vertical slice.

**M5 / Independent replay & translation**
- 독립 운영자 clean replay; mutation 실행; OE-4 검토.
- TR-0 primitive 식별 뒤 TR-1 domain mapping → TR-2 regular regime → TR-3 preregistered baseline.
- DoD: 자격을 갖추지 못한 claim을 HELD로 보존, application은 측정된 범위에서만 주장.

## 11. 권위·상태와 공개 언어 규약

E2A_RESOURCE_STAGE_CROSSWALK의 R0–R13, OPERATIONALLY_EXPOSED의 OE-0–4, ARTIFACT_TO_APPLICATION_TRANSFER_GATES의 TR-0–6은 **서로 다른 축**이다.

- R0 / OE-0: cited. R1 / OE-1: represented. R2: falsifier 설계(아직 OE-4 아님).
- R3 / OE-2: 실행된 bounded artifact + 정확한 환경/영수증.
- R4 / OE-3: 별도 운영자의 clean reproduction.
- R5 / OE-4: 실제 변이/가정 변경이 예상대로 fail.
- R6 / TR-0: lineage가 명시된 small primitive 추출; 기본적으로 OE-4 이후.
- TR-1~6: domain relevance, controlled transfer, 비교, prototype, domain validation, deployment review.

문서/발표에는 다음을 구별해 쓴다.

- **REPRODUCED:** 특정 조건의 숫자/계산을 다시 얻었다.
- **KERNEL_CHECKED:** 특정 Lean proposition과 proof term이 checker에서 허용되었다.
- **SOURCE_ALIGNED:** PDF/Lean 명제의 가정·결론에 대한 별도 의미 검수가 완료되었다.
- **INDEPENDENTLY_REPLAYED:** 격리된 별도 환경/운영자에 의해 동일 경계를 확인했다.
- **TRANSFER_SUPPORTED:** 독립 대상 영역의 사전등록 시험에서 측정된 추가 가치가 있었다.

공리 검사 PASS는 semantic equivalence를 자동으로 주지 않는다. 수치 포락 PASS는 공리나 논문 결론을 증명하지 않는다. TOE 점수 PASS는 관측적 물리 법칙이 아니다.

## 12. 참고 경로

**Sidequest:** README.md, verify_lean_archive.py, trace_lean.py, rh-proof-trace.json, sources/rh-Main.lean, sources/rh-Statements.lean, sources/rh-landauWindowIneq.lean, window_kernel.py, window-results.json, RH_NSRW_Window.ipynb, docs/idea1.txt, docs/idea2.txt.

**NSRW:** formal/p2/P2_MB06_NormalizedJ.lean, P2_MB08_TemplateJet.lean, P2_MB08_ResetAmplitude.lean, docs/momentbound/FIXED_PROFILE_THRESHOLD_FINDING_2026-11-14.md, MB08_SOURCE_CUTOFF_BOUND_DECISION_2026-11-14.md, src/nsrw/m5/lean_export.py, src/nsrw/research_verification_cli.py, src/nsrw/verification_manifest.py.

**TOE:** Flamehaven-TOE(Theory of Everything)/docs/PHYSICS_CONTRACTS.md, ALGEBRAIC_NUMBER_THEORY_INTEGRATION.md, NEW_MODEL_TRIAGE_CHECKLIST.md, SPAR_vs_SLOP_DETECTOR.md, toe-scrutiny-suite/_scrutiny_common.py, toe_p1a.py, toe_p1e_p6.py, toe_p3.py, toe_p4_audit.py.

**원문 링크:** https://alpo.ge/remark.pdf ; https://math.mit.edu/~drew/grh/ ; https://leanprover-community.github.io/blog/posts/riemann-hypothesis/ ; https://github.com/leanprover-community/riemann-hypothesis/tree/40e56bab026552e089d7afcfeff08d2defb9c005 ; https://github.com/openai/NavierStokesAndEuler/tree/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538 ; https://github.com/tristanbuckmaster/navier-stokes.

### 최종 경계

이 명세서의 공헌은 RH·Navier–Stokes·TOE에 대한 새로운 증명을 선언하는 것이 아니다. **paper statement → Lean formal object → actual proof dependencies → certificate → reproducible output → failure boundary → measured domain utility**의 연결을 검사 가능하게 만들고, 어느 단계가 아직 검증되지 않았는지 명확히 기록하는 데 있다.
