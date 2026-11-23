# Inspector 검수 및 P0–P3 수용 판정

| 검수 ID | 근거 식별자 | 초점 |
| --- | --- | --- |
| INSP-01 | 첨부 `1aa46712-df13-415a-8aeb-7de0b3756b79` | 저장소 이름·독립성·단계별 수용 기준 |
| INSP-02 | 첨부 `ece9e921-c950-42f7-9b23-3bb3e9de6b89` | 코드·Lean 추출·수치·원고 구조 |
| FOLLOWUP-01 | 작업 ID `7dc0a3eb-a72c-474a-8202-011bc50041b0` | 아카이브 긴 경로, 보조 증명, 소수 2, 꼬리 적분 |

`INSP-01`과 `INSP-02`는 보고서 추적용 ID다. 첨부에서 검수자의 계정이나 실명을 확인할 수 없었다. INSP-02의 읽기 영수증은 `r_23a32497-1feb-4bf0-80bb-cf68959ee040`, `r_13b09e8f-d007-4ef5-a904-90e57a07edb4`, `r_2eb6969f-3fa3-4ab7-b286-b79a0c0255e3`, `r_22fae20b-0970-495c-a12e-cecec718a27b`, `r_b4c18468-ff03-4594-be2c-86aaf913ae5c`, `r_955a5d19-81ad-4689-b8c3-bcc6ad8caab0`이다. 후속 검수의 제공 영수증은 `r_c9e8f413-874b-4600-bf2f-7f290929081a`, `r_2d7a5389-fc75-4c33-a9f7-dc4d3c9d75dc`, `r_2ccbd5c8-a400-47e6-81dd-534f22645857`, `r_32efaf80-ca64-449e-b513-2521e5ba6c11`이다.

| 단계 | 판정 | 대조 근거와 채택 범위 |
| --- | --- | --- |
| P0 명칭 및 기준선 | **ACCEPT** | Riemann Evidence Atlas (`riemann-evidence-atlas`)를 공식 표기로 채택. `riemann_evidence` import와 역사적 포맷 유지. `v0.1.0` 유지, 다음 판은 로컬 `v0.2.0-rc.1`. |
| P0 문서와 고정 입력 | **ACCEPT** | 계획 파일에서 U+000B 두 곳과 빠진 TeX 명령을 확인. 새 체크아웃에서 산술·문서를 실행하고 별도 캐시로 원본 입력을 대조. 원본 결측은 `ENV_BLOCKED`, 해시 불일치는 실패. |
| P0 이력 재기록·대형 자료 자동 도입 | **REJECT / AMBER** | 역사적 결과나 태그 재기록은 기각. 전체 원본 자동 다운로드와 원격 Lean CI는 입력·실행 자원과 원격이 확보되면 검토. |
| P1 경로 탐색·Lean 추출 | **ACCEPT** | 합류 정점을 공유하는 proof-only 경로와 definition 경유 경로에서 기존 BFS가 후자를 누락. `(node, via_definition)` 방문 상태와 두 경로가 보이는 회귀 테스트 계획 채택. `ProofRefs` 선언 종류 및 `ProofFrontier`의 `type_refs` 확장. |
| P1 `omega` 보조 증명 | **ACCEPT / AMBER** | 두 보조 증명의 직접 VALUE 참조는 각각 57개이며 집합이 같다. `Lean.Omega.*`가 있고 직접 `Classical.choice`는 없다. 전이 의존성과 정확한 소속 모듈은 다음 추출에서 확인한다. |
| P1 긴 tar 경로 | **ACCEPT / AMBER** | 합성 표준 USTAR 헤더에서 143바이트 경로가 prefix와 name으로 나뉘는데 `seek_member.py`가 처음 100바이트만 읽는다. PAX 경로 헤더도 처리하지 않는다. 실제 아카이브에서 유일한 실패 원인인지, 캐시로 파일을 확보할 수 있는지는 해당 파일 해시와 선언을 검증할 때까지 보류. |
| P2 소수 2 | **ACCEPT / AMBER** | 정확 유리수로 자명·비자명·분기 문자 값을 대조했고 원본 `ClaimStrip`의 `prim_zero`와 `LFunction_changeLevel` 위치를 확인. Mod 4 비원시 문자에는 modulus 4와 conductor 1 인자를 함께 기록. Masullo의 주값 적분·측도·테스트 함수 연결은 보류. |
| P2 자동 상쇄 또는 두 증명 기여의 동일시 | **REJECT** | 분기 문자의 단위 평균이 0이어도 남은 가중치가 단위에 의존할 수 있다. 비완성 오일러 인자의 국소 대조만으로 completed L-function 또는 global trace, RH·GRH 판정을 인정할 수 없다. |
| P3 Landau 꼬리 | **ACCEPT** | 고정 예의 감마 꼬리 다항식에 3과 9를 넣으면 각각 13과 172. 급수·외향 반올림의 Rat 검증과 실수 지수·적분 포락의 Lean 증명을 각각 진행. |
| P3 `Init.Data.Rat`만으로 실수 적분 인증 | **REJECT** | 유리수 결정 절차는 주어진 유리수 부등식의 검증에 적용된다. 원본 실수 적분 및 `Real.exp`와 연결하는 분석 정리가 필요하다. |

실행 순서와 각 단계의 완료 조건은 [P0–P3 계획](PATCH_SEQUENCE_P0_P3_ko.md)에 있다.
