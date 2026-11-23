# Riemann Lean Evidence — 2026-11-23 코드 정비 및 로컬 실행 검수

**상태:** LOCAL_DEVELOPMENT_VALIDATION / claim_authority: NONE
**기준선:** v0.1.0 annotated tag → 8192cf0923995e200185f271fba76b2387db9d67 (기존 태그는 변경하지 않음)
**개발 목표:** v0.2.0 proof-reference pilot의 검증 강화. **아직 v0.2.0 릴리스 판정 아님.**

## 1. 이번에 실제 구현한 경계

- riemann_evidence/proof_dependency.py: Lean 직접 참조 레코드를 strict schema로 받아 **동일 모듈 내 VALUE edge**만 추적한다. type/value/import를 혼동하지 않으며, 외부 참조는 unresolved로 표시한다.
- tools/replay_proof_dependency.py: 실제 공식 Lean 4.33.1 실행 파일과 입력 .olean SHA-256을 확인한 뒤, 선언별 직접 참조를 여러 번 추출하고 한 모듈 내 VALUE 경로를 분석한다. readModuleData로 저장된 표현식을 읽는 검사이며 커널 proof replay는 아니다.
- tests/lean/ChoiceDependenceFixture.lean: 직접 증명에서의 Classical.choice와 선택된 값을 참조하는 계산 정의/정리의 경로를 Lean 소스와 .olean 양쪽으로 시험한다.
- tests/test_proof_dependency.py: 모듈 import 오인 금지, proof/data 선택 경로 분리, 누락/외부 참조/사이클/잘못된 schema/중복 간선/예산 초과 거절, 기존 Main pilot 결과에 대한 회귀 등 **신규 10개**.
- tools/local_notebook_smoke.py: RH_Window.ipynb의 실제 코드 셀을 표준 라이브러리만 사용하여 **임시 디렉터리에서 실행**한다. 저장소의 window-results-v2.json을 덮어쓰지 않고 생성 파일의 내용과 SHA를 비교한다. Google Colab 서버가 아니라 **로컬 실행**이다.
- tools/validate_local_pilot.ps1: 공식 4.33.1 Windows Lean, 저장된 Main.olean, 오프라인 Python을 사용하여 통합 검수하고 결과 JSON은 무시된 outputs/에만 보존한다.
- tools/validate_python_matrix.ps1: uv로 오프라인 Python 3.10·3.14 인터프리터를 찾고 unittest + saved report + notebook cell replay를 각 버전에서 수행한다.
- .github/workflows/checks.yml: 원래의 Windows/Linux Python 3.10/3.13 테스트 구성에 오프라인 notebook smoke를 추가. **이번에는 원격 GitHub CI를 실행하지 않았다.**

## 2. 실제 실행 영수증

| 검증 | 관측값 | 실행 receipt |
| --- | --- | --- |
| 원본 Main.olean 직접 참조 | type: RiemannHypothesis; value: rhOfAll; imported module을 참조로 오인하지 않음 | r_03fa109c-24e9-4fc8-9495-ecd0caaa78fb |
| Lean version | Lean 4.33.1 Windows, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6 | 동일 |
| Python version | CPython 3.14.10 Windows | 동일 |
| Python unittest | **17개 실행, 17개 PASS** | 동일 |
| 수치 JSON 재계산 | REPORT MATCH; 10개 사례 | 동일 |
| 노트북 오프라인 실제 코드 셀 | 10개 사례, saved JSON과 동일한 SHA-256 | 동일 |
| 합성 Lean fixture | .olean 컴파일 성공 | 동일 |
| 합성 Choice 경로 분리 | data-definition path = 1+, direct proof-value path = 1+ | 동일 |
| 오프라인 Python matrix | Python 3.10.22 및 3.14.10 모두 17개 PASS, report match, notebook smoke 성공 | r_2cb8d4e3-8827-4176-81d7-2c828f1b0323 |
| leanchecker 별도 시도 | --help 시 메모리 오류; 합성 .olean 절대경로를 모듈로 해석하지 못함 | r_17211129-eca5-4c10-b744-d6275a642141 |

### 파일 및 증거 identity

- 원본 Main.olean SHA-256: **9146dfb4148e24d2252e04c50742f3e49dd126dfcc5006d10bf5f873ddf796ad**.
- 이전 pilot JSON은 보존됨: docs/rh-proof-refs-pilot.json.
- 이번 원본 분석: outputs/rh-proof-value/validation/original-main-value-paths.json
  SHA-256 **ac23095dd157c9d194cc98951d3ae753ab73c88504b0255343e4d23e980190a9**.
- 이번 합성 분석: outputs/rh-proof-value/validation/choice-fixture-value-paths.json
  SHA-256 **f417e7a64cf455945fabf5042ea0726dde85895c9e7b120194599689ba9a420e**.
- 저장된 수치 결과/노트북 생성 결과 SHA-256: **ad3d31ceaf5a9a78e5f17f5c25ac087394eb57ebfb3cfdd977aa57c61ac66bf1**.
- 원래 RH_Window.ipynb SHA-256: **e55a9f45b0a4d190d154050eb3184d83fa975aac75a53a9d19c3b2af34289eb1**.

## 3. 'Classical.choice 의존'을 둘로 나눈 실제 결과

이번 합성 Lean 파일에서 관측한 실제 VALUE reference path:

~~~text
auditProofCallsChoice (theorem) → Classical.choice
  position: PROOF_VALUE_PATH_CANDIDATE

auditProofMentionsComputed (theorem)
  → auditComputedFromChosen (definition)
  → auditChosenNat (definition)
  → Classical.choice
  position: DATA_DEFINITION_PATH_CANDIDATE
~~~

**중요:** 이 분류는 소스/증명 항의 **구문적·정의 의존 경로 후보**다. 이것만으로 실제 계산이 그 값을 평가해야 한다거나 원본 함수의 도함수 상한이 부재함을 증명하지 않는다. 출력에 **numeric_relevance: NOT_ESTABLISHED**를 명시한다.

원본 riemannHypothesis는 아직:

~~~text
type → RiemannHypothesis
value → rhOfAll (EXTERNAL_OR_UNRESOLVED)
transitive original closure → NOT_RUN
independent original kernel replay → NOT_RUN
~~~

직접 reference가 없는 import를 실제 proof edge로 만들지 않는다.

## 4. 오류·차단 결과는 보존한다

### Python 실행 파일 경로 문제 — 해결

처음 MCP의 python-unittest 검증 프로필은 Windows Store의 python 별칭으로 인해 실제 실행을 시작하지 못했다. 이어진 PowerShell 방식에서도 기본 alias가 종료 코드 9009로 실패했다. 이후 **오프라인 uv 관리 인터프리터**를 명시적으로 사용해 Python 3.10.22와 3.14.10 실행 검증에 성공했다. 외부 패키지나 네트워크를 설치하지 않았다.

### leanchecker 자원 및 모듈 경로 문제 — 미해결

내장 Lean 4.33.1의 leanchecker.exe에 대한 추가 검사는 --help 호출에서 **INTERNAL PANIC: out of memory**로 종료되었고, 합성 .olean의 **절대 파일 경로**는 모듈 이름으로 해석되지 않았다. 두 실패는 checker 성공이나 원본 정리의 참·거짓을 말해주지 않는다.

파일 tools/check_leanchecker_fixture.ps1은 **재시도 중단을 위한 안전 차단 스크립트**로 바꿨다. 공식 CLI 옵션/모듈 해석 계약, 의존 olean closure, 메모리 상한, 프로세스 제한이 별도로 정립되기 전에는 해당 executable에 재진입하지 않는다. 이것은 **BLOCKED[LEANCHECKER_RESOURCE_AND_MODULE_RESOLUTION]**, 정리 거짓 판정이 아니다.

## 5. 실행 명령 및 미확인 영역

워크스페이스 루트의 Windows PowerShell 7에서:

~~~powershell
pwsh -NoProfile -File .\tools\validate_python_matrix.ps1
pwsh -NoProfile -File .\tools\validate_local_pilot.ps1
~~~

수치 모듈 및 notebook smoke는 Python 표준 라이브러리만 필요하다. 원본 .olean 추출은 별도로 확보한 공식 Lean 4.33.1 및 정확한 Main.olean이 필요하다. 두 파일은 outputs/에 보존하며 Git에 포함하지 않는다.

**아직 미완료:**
1. 실제 Google Colab 런타임에서 RH_Window.ipynb의 업로드·재생·receipt 확보. 이 세션에는 인증된 Colab 실행 세션이 없으므로 **NOT_RUN**.
2. 원본 RH 전체의 transitive proof value dependency closure. rhOfAll 및 그 아래 imported declaration 원본 .olean 미수집은 **OPEN**.
3. 원본 RH 전체 kernel/독립 checker replay. **BLOCKED / NOT_RUN**.
4. GitHub remote 및 원격 CI의 실제 실행. **NOT_RUN**.
5. NSRW MB06 ratio lower에 대한 source-pinned formal Lean bridge 및 TOE domain transfer. **NOT_RUN**.

## 6. 다음 단계의 엄밀한 승격 규칙

- **v0.1.0:** 최초 10-case standalone numerical baseline, 로컬 검증 완료. 기존 annotated tag 불변.
- **v0.2.0 pilot:** 실제 원본 한 선언 direct type/value refs + 합성 같은 모듈의 transitive choice 경로까지 재실행 성공. *Imported theorem graph의 확장 또는 source Mathlib closure는 포함하지 않는다*.
- **v0.2.0 release candidate:** 최소 1개 이상의 imported target declaration을 별도 pinned .olean에서 읽어 연결하고, 정의 의존/opaque/axiom 경계를 지닌 실제 cross-module value closure를 검수한다. 그 뒤 독립 재현 증거를 확보한다.
- **v0.3.0:** 작은 exp/ratio bound를 정확한 source definition/assumption에 연결한 Lean proof의 pinned compile/kernel evidence가 필요.

**최종 주장:** 우리는 2026-11-23 현재 독립 수치 replay, local notebook execution, theorem direct-reference extraction 및 synthetic choice path classification의 **좁고 검증 가능한 계산 표면**을 고정했다. 이는 RH 정리의 새 증명 또는 전체 검증이 아니다.
