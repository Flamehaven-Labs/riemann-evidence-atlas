# E2A 꼬리 질량 상한 검증 원장

2026-11-23에 고정 입력 한 건의 수치 보고서를 재현하고 두 임계값을 Lean에서 확인했다. 대상은 양의 실수축에서 `[1, 3]` 바깥에 있는 `u³ exp(-3u) / 3!`의 질량이다. Python 모델의 입력은 `outside_window`, `k=3`, `rate=3`, `a=1`, `b=3`, 정밀도 128비트다.

| 검증 단계 | 관측 결과 | 범위 |
| --- | --- | --- |
| Python 수치 재현 | `REPRODUCED`, 전체 22/22, 저장 보고서 `REPORT MATCH` | 해당 모델의 정방향 재계산과 입력·구간·판정 확인 |
| 수치 결과와 Lean 결속 | `REPLAY_BINDING_MATCH` | 두 입력 SHA-256, 정밀도, 판정, 유리수 양 끝점과 두 임계값을 재현 결과와 대조 |
| Lean 소스 검사 | `LEAN_SOURCE_CHECK`, 종료 코드 0 | Lean 4.33.1에서 유리수 부등식 및 구간을 가정한 함의 검사 |
| 독립 검사기 | `NOT_RUN` | 버전 고정 모듈 해석, 의존성 폐쇄, 자원 상한이 있는 독립 재검사 환경 필요 |
| 원천 명제 대응 | `REVIEW_PENDING` | 실수 적분이 저장된 구간 안에 들어간다는 해석적 근거 및 원천 명제와의 대응 검토 필요 |

## 동일 구간에 대한 양성·음성 사례

| 사례 | 임계값 | Python 결과 | Lean에서 확인한 비교 | 입력 SHA-256 |
| --- | --- | --- | --- | --- |
| `landau_tail_valid_cap` | `1/200` | `PASS` | 구간의 상한 ≤ 임계값 | `ea5ed7211fb86cf13903c773fce203bd6fed318701bf4a98ffa2cc3067b65ede` |
| `landau_tail_violated_cap` | `1/300` | `FAIL` | 임계값 < 구간의 하한 | `c6dc828a961aa6ccb3741da57c17245d336f78ccf2577f960806bd8ec4425337` |

하한은 `127263766859979925728141246211069006267/27562871720596015540533343201973225127936`이다. 상한은 `10605313904998327144011770517589083871/2296905976716334628377778600164435427328`이다.

[Lean 소스](../tests/lean/E2ATailCapCertificate.lean)는 하한과 상한의 순서를 증명한다. 유리수 `mass`에 대해 `mass ≤ upper`를 가정하면 `mass ≤ 1/200`을, `lower ≤ mass`를 가정하면 `1/300 < mass`를 증명한다. 별도 음성 대조에서는 `¬ (upper ≤ 1/300)` 증명이 수용됐고, 같은 증명 항으로 `upper ≤ 1/300`을 주장하면 타입 불일치로 거부됐다. 기록된 공리는 `propext`, `Classical.choice`, `Quot.sound`다. `sorryAx`는 관측되지 않았다.

이 파일럿의 형식 검증 범위는 유리수 구간의 임계값 판정이다. 실수 적분과 유리수 구간을 연결하는 정리, 외향 오차 상계의 형식 증명, 원천 명제에 대한 독립 검토는 아직 필요하다. 이 실험은 리만 가설 또는 보존된 `Main.olean`을 판정하는 데 사용하지 않는다.

후속 P3에서 고정 입력의 실수 지수 포함과 꼬리 적분 등식을 Lean으로 연결했다. [P3 실행 기록](P3_LANDAU_TAIL_ko.md)

## 로컬 MCP 실행 증거

기본 Flamehaven-MCP 체크아웃에서 임시 설정으로 FH-MCPd 0.3.6의 로컬 stdio를 실행했다. `fh_verify_profile`은 호스트에 고정한 Python 3.12.16과 Lean 4.33.1을 사용했다. Python 재현 검사 8/8과 `LEAN_SOURCE_CHECK`가 같은 영수증에 기록됐으며 `evidenceComplete=true`, `checkedSource.unchanged=true`였다. 실험 도구는 운영 daemon과 다른 프로세스에서 실행됐다.

| 항목 | 관측값 |
| --- | --- |
| Gateway 세대 | `78e11d321232d62f21ab3007deffa44facd356dcfc37b68988aeaa5bccd7965f` |
| 검증 영수증 | `r_63a9863f-d031-4ac5-84f6-e7eb9cae9440` |
| 입력 해시 관측 전 / 후 | `r_7f87befe-2c44-42bd-83a7-8ad5550d1df2` / `r_8e014966-09eb-4845-a291-5ceab00ce839` |
| Python 바이너리 SHA-256 | `246221b571e7a692a8b26818b628cac4c163e836de9897812eaebc2a8e1efa90` |
| Lean 바이너리 SHA-256 | `af49bacfabaa1fea71332ca0feae0fa1a60912219d5902291adc79f905bffb8d` |
| `window_kernel.py` SHA-256 | `9c7c14b2fb5539ff450fed8ee8c8d65117396c1389d5cc2a074891854881502f` |
| `window-results-v2.json` SHA-256 | `ad3d31ceaf5a9a78e5f17f5c25ac087394eb57ebfb3cfdd977aa57c61ac66bf1` |
| `tests/test_replay.py` SHA-256 | `450b44f506235c11aeaa820cf9806b4e93177bc0c487ff331aad96605cc60818` |
| `E2ATailCapCertificate.lean` SHA-256 | `419f3d44c7be96a700dd7d5a790bddd220e3144044ea0f5df889f28aeac18a47` |
