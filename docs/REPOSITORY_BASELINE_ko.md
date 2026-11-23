# 독립 저장소 v0.1.0 기준

2026-11-23 · 현재 수치 실행 범위

| 증거 | 상태 |
| --- | --- |
| `window-results.json` | 이전 Colab 결과의 SHA-256과 바이트 보존. 기존 10개 사례 |
| `window-results-v2.json` | 자체 산술 모듈과 실행기로 재생성. 10개 사례 전체의 입력 해시·유리수 끝점·판정이 이전 Colab 기준과 일치 |
| `lean-extract-manifest.json` | 아카이브 조각 14개의 SHA-256 및 로컬 추출물 15개의 일치 항목을 기록 |
| `unit_test_receipt.json` | 별도 Proof Atlas 개발 환경의 역사적 13개 테스트. 그 패키지의 실행 가능한 소스는 이 작업 폴더에서 확인되지 않음 |
| 이번 Lean 검수 | 원본 바이트 대조 및 정적 소스 추적. proof-value closure, 커널 실행, 독립 운영자 재현은 미수행 |

[실행 명세](CROSS_REPO_WORKFLOW_AND_VERIFICATION_SPEC_ko.md)의 사례 누락 검수는
수치 실행이 다섯 건이었던 이전 스냅샷을 설명한다. 지금의 케이스 목록은
이전 Colab과 독립 구현 양쪽에 열 건 있으며, 삭제·변조 사례는
[회귀 검사](../tests/test_replay.py)에서 기각된다. 이전 파일의 이력은 보존했다.

MB-06은 과거와 비교 가능한 산술 사례다. NSRW와 TOE 계획은 연구 전이 문서에
남긴다. 새 저장소의 계산·회귀 검사는 두 저장소나 두 프로젝트의 Lean 환경에
접근하지 않고 실행한다.
