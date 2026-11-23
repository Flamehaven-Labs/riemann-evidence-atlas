# Riemann Evidence Atlas

리만 가설 Lean 선언의 의존성, 논문의 원문과 계산 가능한 보조항을 추적하는 독립 연구 저장소입니다. 저장소 이름은 `riemann-evidence-atlas`이며, Python 모듈은 `riemann_evidence`입니다. 현재 로컬 릴리스 후보는 `v0.2.0-rc.1`입니다.

## 빠른 실행

Python 3.10 이상. 수치 실행과 회귀 검사에는 Python 표준 라이브러리만 필요합니다.

~~~sh
python -E -S tools/verify_baseline.py
python window_kernel.py
~~~

직접 입력은 JSON으로 전달합니다. 다음 입력은 양의 반직선에서 창 $[1,3]$을 제외한 부분의 적분이 $1/200$ 이하인지 판단합니다.

~~~json
{"component":"outside_window","k":3,"rate":"3","a":"1","b":"3","cap":"1/200","precision_bits":128}
~~~

~~~sh
python window_kernel.py --window case.json
~~~

| 종료 | 의미 |
| --- | --- |
| 0 | 계산된 상한이 임계값 이하 |
| 1 | 계산된 하한이 임계값을 초과했거나 입력 거부 |
| 2 | 구간이 임계값을 가르고 지정한 정밀도 예산이 소진됨 |
| 3 | 기타 실행 상태 |

`--ratio`는 과거 기준과 비교하는 회귀 사례입니다. 고정 $\lambda=10^{-12}$의 MB-06 비율을 같은 산술 방식으로 비교하는 선택 입력입니다. `lambda`, `cap`, `precision_bits`를 전달합니다. 기존 Navier–Stokes 저장소에서 가져온 산술과 실행기 부분은 이 저장소에 포함되어 있습니다. 다른 저장소, 패키지 설치, 네트워크 연결 없이 실행합니다. [출처와 라이선스](NOTICE.md)

## 계산과 검증 범위

저자 소스의 `landau_window_ineq`에서 $s=\sigma-2>0$인 양의 커널 $u^k e^{-su}/k!$을 선택했습니다. $P_k(x)=\sum_{j=0}^k x^j/j!$에 대해 $-e^{-su}P_k(su)/s^{k+1}$을 원시함수로 사용합니다. 양의 반직선 적분 $s^{-(k+1)}$에서 유한 창 적분을 빼면 전체 꼬리를 계산할 수 있습니다.

- 입력은 무차원이며 $0\le k\le64$, $0\le a<b$, $s>0$, $sb\le16$을 지원합니다.
- 관측량은 입력 바이트 SHA-256, 적분의 정확한 유리수 구간, 판정에 사용된 정밀도입니다. 128, 256, 512 fractional bits 중 지정된 예산을 사용합니다.
- 예시 꼬리 적분은 약 $0.00461721725334$입니다. $1/200$은 상한으로 채택되고, $1/300$은 기각됩니다.
- 최상위 Lean 선언 등의 소스 참조 13개와 Landau 부등식 모듈까지의 import 경로를 기록했습니다. 원본 Lean 4.33.1의 5개 모듈에서 7개 선언과 6개 연결 VALUE 간선을 재현했고, 별도로 378개 미해결 직접 참조를 분류했습니다. 전체 전이 폐쇄, 원본 RH 전체 커널 재검사 및 Landau 실수 적분의 형식 연결은 후속 단계입니다.

[Lean 추적 기록](rh-proof-trace.json) · [독립 실행 결과](window-results-v2.json) · [이전 Colab 기준 결과](window-results.json) · [현재 실행 기록](docs/standalone-replay.json)

## Colab

[독립 노트북](RH_Window.ipynb)은 이 저장소의 Python 파일을 그대로 사용합니다. Colab에서 열고 `window_kernel.py`, `riemann_evidence/__init__.py`, `riemann_evidence/rational_intervals.py`, `riemann_evidence/verification.py` 네 파일을 요청에 따라 올립니다. 노트북은 가져온 파일의 SHA-256을 확인하고 CLI와 동일한 10개 사례를 실행합니다. 저장소 폴더에서 열면 업로드 단계 없이 실행합니다. 이전 Colab 기준 결과의 범위와 이번 실행 검사는 [현재 상태](docs/REPOSITORY_BASELINE_ko.md)에 기록했습니다.

## 원본과 설계 문서

| 자료 | 역할 |
| --- | --- |
| [교차 연구 실행 명세](docs/CROSS_REPO_WORKFLOW_AND_VERIFICATION_SPEC_ko.md) | 소스, 형식 증명, 수치 인증, 실행, 전이의 근거와 다음 단계 |
| [엔지니어링 연구 보고서](docs/ENGINEERING_RESEARCH_REPORT_ko.md) | 원본 Landau 분석, NSRW와 TOE에 적용할 후보 실험 |
| [현재 상태](docs/REPOSITORY_BASELINE_ko.md) | 과거 기록 보존, 이번 검수와 미실행 항목 |
| [증명 항 참조 실험](docs/PROOF_DEPENDENCY_PILOT_ko.md) | 원본 Lean 컴파일 산출물에서 타입·증명 항의 직접 참조 추출 |
| [P0–P3 재패치 순서](docs/PATCH_SEQUENCE_P0_P3_ko.md) | 기존 검수 기준선, 원본 Lean 경로 확장, 두 연구의 국소 항 비교와 형식 연결 |
| [2026-11-23 로컬 검수 기록](docs/LOCAL_VALIDATION_2026-11-23_ko.md) | 17개 회귀 테스트, Lean 4.33.1 직접 참조, 합성 Choice 전이, Python 다중 버전과 노트북 실행의 정확한 범위 |
| [Inspector 검수와 수용 판정](docs/INSPECTOR_REVIEW_2026-11-23_ko.md) | 검수별 근거와 ACCEPT·AMBER·REJECT |
| [P0 기준선 재현](docs/P0_BASELINE_REPLAY_ko.md) | 새 체크아웃에서의 실행과 원본 증거 재생 |
| [Masullo 원고와 소수 2 기준선](docs/masullo/README_ko.md) | PDF 출처·중요 페이지와 실행 가능한 유리수 항등식 |
| [자료 목록](sources.json) · [PDF 페이지 색인](pdf-pages.jsonl) | 4개 PDF 및 공개 입력의 출처, 해시, 원본 페이지 |
| [Lean 아카이브](lean-archive-manifest.json) · [추출물 기록](lean-extract-manifest.json) | 아카이브 14조각과 추출 파일 15개의 경로 및 SHA-256 |
| [변경 기록](CHANGELOG.md) | 로컬 기준선 및 릴리스 후보 |

소스 추적을 다시 실행할 때는 원본 조각을 아카이브 목록의 URL에서 지정된 `sources/lean-parts/` 경로에 저장합니다. 필요한 추출 파일은 추출물 기록의 아카이브 항목을 사용합니다. `python verify_lean_archive.py`로 조각과 지정된 원본 파일을 확인하고, `python trace_lean.py`로 import 그래프를 다시 만듭니다. PDF 색인 재생성에는 선택적으로 `pypdfium2`와 자료 목록의 원본 파일이 필요합니다. 다운로드한 원본, 대형 import 그래프, 내부 메모는 로컬에 보존합니다.
