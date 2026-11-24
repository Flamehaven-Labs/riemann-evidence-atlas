# P0 기준선 재현

이 절차는 `v0.2.0`의 재현에 사용한다. 후보 기준선은 `v0.2.0-rc.1`, 이전 수치 기준선은 `v0.1.0`에 보존했다. 실행에 필요한 고정 원본 캐시는 Git 체크아웃과 분리한다.

## Python 기준선

~~~sh
python -E -S tools/verify_baseline.py
~~~

완료 표시는 `P0_PORTABLE_BASELINE_PASS`다. Python 회귀 테스트, 10개 창 및 비율 사례, 소수 2 산술 기록, 오프라인 노트북 코드 셀, 보존 JSON 해시를 확인한다. 10개 중 두 MB-06 비율 사례는 과거 산술 회귀에 사용한다. 새 체크아웃에서 NSRW와 네트워크 없이 실행한다.

## 원본 입력과 Lean

기존 로컬 캐시의 파일을 사용해 같은 실행을 확장한다. 아래 세 경로는 각 환경에서 실제 위치를 전달한다.

~~~powershell
python -E -S tools/verify_baseline.py `
  --lean "<Lean 4.33.1 Windows 설치>/bin/lean.exe" `
  --proof-assets "<보존 캐시>/rh-proof-value" `
  --masullo-pdf "<원본 캐시>/The_Music_of_the_Primes_Masullo_2026-11-20.pdf"
~~~

| 입력 | 위치 및 핀 |
| --- | --- |
| Lean | `lean-toolchain`의 4.33.1. 보존 JSON에 실제 플랫폼이 포함되어 Windows 기준 실행을 사용 |
| 5개 원본 모듈 | 캐시의 `alp-oleans-Main-and-small.tar.gz`, `branch-inputs/{CritLine,MainConclusion,RhOfRight}.olean`. [모듈별 아카이브 항목·해시](rh-next-layer-module-set.json) · [아카이브 SHA-256](../tools/replay_rh_module_set.py) |
| 배포자 그래프 | 캐시의 `verified-rh-graph.json.gz`. [고정 SHA-256과 사용 범위](../tools/replay_rh_frontier.py) |
| Masullo 초고 | [원본 URL 및 해시](masullo/README_ko.md) |

완료 표시는 `P0_PINNED_SOURCE_REPLAY_PASS`다. Lean으로 유리수 꼬리 임계값 정리를 검사하고, 원본 5개 모듈의 직접 참조와 378개 분류 결과를 각각 두 차례 생성해 고정 JSON과 바이트 대조한다. 재생성한 표준 출력에 한해 CRLF를 LF로 정규화한다. Masullo PDF는 고정 해시를 대조한다. 원본 파일 결측은 `ENV_BLOCKED`와 종료 2, 깨진 입력이나 실행 오류는 종료 1로 보고한다.

검증 범위는 [P0–P3 계획](PATCH_SEQUENCE_P0_P3_ko.md)과 [수용 판정](INSPECTOR_REVIEW_2026-11-23_ko.md)에 기록한다. 원본 RH 전체 커널 검사, 실제 Colab 실행, 별도 운영자 재현은 미실행이다.
