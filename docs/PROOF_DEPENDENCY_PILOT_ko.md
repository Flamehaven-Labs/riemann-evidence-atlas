# Lean 선언의 직접 참조 추출

대상은 원본 RH 프로젝트 `Main.lean`의 `riemannHypothesis` 한 건이다.
이 점검의 결과는 선언의 **직접 참조**다. 전이 의존성, 증명의 커널 재검사,
수치 평가 대상의 비구성성은 별도 작업이다.

## 입력과 추출 방법

[Proofs & Reasons의 빌드 아카이브](https://proofsandreasons.io/rh-oleans.html)에서
`alp-oleans-Main-and-small.tar.gz`를 받아 아카이브와 내부
`alp-oleans/lib/Main.olean`을 각각 SHA-256으로 확인했다.
내부 파일의 SHA-256 `9146dfb4148e24d2252e04c50742f3e49dd126dfcc5006d10bf5f873ddf796ad`는
[MIT 검증 기록](https://math.mit.edu/~drew/grh/)과 일치한다.
외부 원본은 `outputs/` 아래에 보존했다. 일반 수치 회귀는 이 파일이나
Lean 설치에 의존하지 않는다.

Windows용 [Lean 4.33.1 배포본](https://github.com/leanprover/lean4/releases/tag/v4.33.1)의
`lean-4.33.1-windows.tar.zst`를 공식 SHA-256
`f63029c0e1e6daed0f4807481b6fcd8f8b77fbce6d63f205c7f9191072387a7a`와
대조했다. 기존 4.34.0-rc2는 원본 모듈을 헤더 호환 오류로 거부했다.

[Lean 추출기](../tools/ProofRefs.lean)는 `Lean.readModuleData`로 컴파일
산출물 하나를 읽는다. `ConstantInfo.type`과
`ConstantInfo.value? (allowOpaque := true)`에 대해 각각
`Expr.getUsedConstants`를 적용한다. 모듈 헤더의 import 배열은 별도 필드에
기록한다. 원본 Lean을 재실행하거나 소스 문자열에서 참조를 추정하는 단계는
이 추출 과정에 들어가지 않는다.

## 원본 결과

Lean 4.33.1에서 원본 `Main.olean`을 읽어 아래 결과를 얻었다.
[실행 기록 JSON](rh-proof-refs-pilot.json)

| 읽은 위치 | 직접 확인한 참조 |
| --- | --- |
| 모듈 헤더 | `Init` 두 항목, `Statements`, `Supplements.Kernels.MainTheoremsAll` |
| 정리의 타입 | `RiemannHypothesis` |
| 정리의 증명 항 | `rhOfAll` |

`Statements`와 `Supplements.Kernels.MainTheoremsAll`은 이 선언의
직접 타입·증명 참조 목록에 나타나지 않는다. 여기서의 검증 결과는 전체
import 그래프와 다른 직접 참조를 실제로 추출할 수 있다는 것이다.
직접 참조에 `Classical.choice`가 없더라도 전이 의존성을 판정할 수
없다. 위 MIT 기록은 이 선언의 전이 공리를 별도로 보고한다.

비교 자료로 공개된 [프로젝트 의존성 그래프](https://proofsandreasons.io/rh-graph.html)
전체 압축 파일의 SHA-256을 확인하고 두 노드를 읽었다. 그래프에서
`riemannHypothesis`의 body는 `rhOfAll`을, `rhOfAll`의 body는
`Formalism.VW.rh_of_every`와 `allChi`를 참조한다. 이 그래프는
Mathlib과 Lean 코어 선언을 생략한다. 첫 노드의 signature 배열이 비어 있는
것은 Mathlib에 있는 `RiemannHypothesis`의 참조 부재를 뜻하지 않는다.

## 대조 사례

[합성 대조 모듈](../tests/lean/ProofRefsFixture.lean)을 Lean 4.33.1로
컴파일했다. `probeTarget`의 타입은 `ProbeProperty`를, 증명 항은
`probeWitness`를 참조한다. 헤더에 있는 `Lean.Util.FoldConsts`는 두
참조 목록에 들어가지 않았다.

합성 `probeUsesChoice`와 `probeChosenNat`의 값에서는 모두
`Classical.choice`가 검출됐다. 첫 선언은 명제의 증명이고, 둘째는
선택된 자연수를 값으로 갖는 정의다. 원본 cutoff가 수치 평가 경로에
실제로 도달하는지는 이 직접 참조 검사만으로 판정할 수 없다.

## 원본 두 모듈 연결

같은 고정 배포 아카이브에서 `Main.olean`과
`Supplements/Kernels/MainTheorems.olean`을 읽었다. 두 번째 파일의 SHA-256은
`ccf715ec0e2be6075cefe8cae3f43de6e18501959fa768970b1e11d81683d02f`다.
[실행 기록](rh-module-set-pilot.json)

| 선언 | 타입의 직접 참조 | 증명 항의 직접 참조 |
| --- | --- | --- |
| `riemannHypothesis` | `RiemannHypothesis` | `rhOfAll` |
| `rhOfAll` | `RiemannHypothesis` | `Formalism.VW.rh_of_every`, `allChi` |
| `allChi` | `UpperTheory.EveryCharacter` | `UpperTheory.FinalTheorems.everyCharacter` |

`riemannHypothesis → rhOfAll`은 서로 다른 두 컴파일 파일에서 추출한
선언을 연결한 값 참조다. `rhOfAll → allChi`는 두 번째 모듈 안의 값
참조다. `rh_of_every`와 `everyCharacter`의 본체는 이 실행의 미해결 값
참조로 남겼다. `RiemannHypothesis`와 `EveryCharacter`는 별도의 타입
참조다. 이 범위에서 확인한 두 값 간선 외의 원본 전이 의존성은 미확정이다.
열린 가지 아래의 `Classical.choice` 도달 여부와 수치적 관련성도 이 실행으로
판정할 수 없다.

## 두 가지 추가 연결

배포자 [프로젝트 파일별 체크섬 목록](https://photos.proofsandreasons.io/alp-oleans-357309b5dd12/SHA256SUMS-project-oleans.txt.gz)의
압축 파일 해시를 [공개 체크섬](https://photos.proofsandreasons.io/alp-oleans-357309b5dd12/SHA256SUMS)과
대조했다. 공개 `Formalism`과 `Development-AutomorphicArithmetic` 묶음에서
아래 두 파일을 각각 추출해 파일별 SHA-256을 검증했다. 이 기록의 검증 단위는
두 추출 파일이며, 대형 아카이브 전체 해시는 이 실행에서 재계산하지 않았다.

| 파일 | SHA-256 | 직접 읽은 선언 |
| --- | --- | --- |
| `CritLine.olean` | `10eb57ebfe01dffd2cff3890214eed84dc5e1373da81ddadb6c98eccc40341e7` | `Formalism.VW.rh_of_every` |
| `MainConclusion.olean` | `96f053d27b81461fcf5ca2fe9a234384bc6ead9697de76cee37e13686aa156df` | `UpperTheory.FinalTheorems.everyCharacter` |

Lean 4.33.1에서 **네 모듈의 선언 다섯 개와 내부 VALUE 간선 네 개**를
연결했다. 새 간선은 `rhOfAll → Formalism.VW.rh_of_every`와
`allChi → UpperTheory.FinalTheorems.everyCharacter`다.
첫 가지는 `rh_of_right`와 `DirichletCharacter.LFunction_modOne_eq` 등을
참조한다. 두 번째 가지는 `everyCharacter_of_row`와
`galoisLocalGlobalStrong_recParameter`를 참조한다.
[확장 실행 기록](rh-branch-module-set.json)

두 번 생성한 LF JSON의 바이트가 일치했다. 원본 전체 전이 의존성과
`Classical.choice`까지의 경로는 이 다섯 선언 범위 밖이다.

## 두 분기의 다음 단계

`RhOfRight.olean`은 앞선 실행에서 보존한 `Formalism` 아카이브
앞부분에서 추출했다. 배포자의 파일별 SHA-256
`cf24f82f3f24144070062b19beedf83f0919c4e894c56759597fa76e2e93bc70`과
일치했다. `everyCharacter_of_row`는 기존 `MainConclusion.olean`에서
읽었다. [다음 단계 실행 기록](rh-next-layer-module-set.json)

| 새 VALUE 간선 | 도착 선언의 주요 직접 참조 |
| --- | --- |
| `Formalism.VW.rh_of_every → Formalism.VW.rh_of_right` | `riemannZeta_one_sub`, `Complex.Gamma_ne_zero_of_re_pos`, `propext` |
| `UpperTheory.FinalTheorems.everyCharacter → UpperTheory.FinalTheorems.everyCharacter_of_row` | `every_character_of_literature_of_vWin`, `UpperTheory.One.vwin_of_row`, `UpperTheory.Zero.LLC.recTExists` |

Lean 4.33.1에서 다섯 모듈의 일곱 선언을 읽어 연결된 VALUE 간선 여섯 개를
기록했다. 두 번 추출한 LF JSON은 바이트 단위로 일치했다.
`propext`는 `rh_of_right`의 직접 VALUE 참조에서 관측됐다.
다른 공리와 `Classical.choice`의 전이 도달 여부는 현재 기록의 미해결
참조를 확장해야 판단할 수 있다. 전체 증명의 커널 재검사는 수행하지 않았다.

## 미해결 VALUE 참조의 출처와 종류

다음 단계에서는 저장된 일곱 선언의 미해결 VALUE 참조를 이름별로
모았다. 같은 이름을 참조하는 증명은 각 항목에 함께 기록했다.
[분류 결과](rh-frontier-classification.json)

- 원본 `.olean`에 실제 선언이 있으면 모듈과 Lean의 선언 종류를 읽는다.
  그 선언에 저장된 값이 있으면 직접 VALUE 참조도 추출한다.
- Lean 4.33.1 배포 환경에서 발견한 상수는 환경이 제공하는 모듈과 선언
  종류를 기록한다. 이 실행에서 배포 환경 상수의 값을 재귀적으로 따라가지 않는다.
- 공개 의존성 그래프에만 있는 이름은 원본 파일·선언 종류의 후보로 남긴다.
  이때 공리 여부는 미확인이다. 두 입력에서 모두 확인하지 못한 이름도
  미확인으로 기록한다.

| 확인 근거 | 고유 참조 수 |
| --- | ---: |
| Lean 4.33.1 `Init` 환경에서 직접 확인 | 76 |
| 원본 RH `.olean`에서 직접 확인 | 2 |
| 공개 의존성 그래프의 출처·종류 후보 | 10 |
| 미확인 | 290 |

`rh_of_right`가 직접 참조하는 `propext`는 `Init.Core`의 공리 선언이다.
같은 `RhOfRight.olean`에 저장된 두 보조 증명
`rh_of_right._proof_1_1`, `rh_of_right._proof_1_2`도 읽었다. 각 증명 항의
직접 참조 57개를 기록했다. `vwin_of_row`는 공개 그래프에서만 확인한
후보다. 컴파일 산출물 확보 후 종류와 본체를 직접 확인할 수 있다.

Lean·Std 전체를 가져오는 시도는 120초를 초과했다. 성공한 두 번의 실행은
`Init`과 고정 RH 컴파일 파일에 한정했으며 JSON은 바이트 단위로 일치했다.
공리 분류는 각 상수 자체의 선언 종류를 가리킨다. RH의 전체 공리 의존성과
`Classical.choice`까지의 전이 경로는 미확인이다.

## 재현 명령

아래 명령은 저장소 루트에서 실행한다. `lean`은 원본에 고정된 4.33.1을
사용한다. Python 래퍼는 `Main.olean`의 해시와 Lean 버전을 검사한 후
원본 선언 한 건만 추출한다.

```powershell
python -E -S tools/replay_rh_proof_refs.py --lean (Get-Command lean).Source --module outputs/rh-proof-value/alp-oleans/lib/Main.olean
python -E -S tools/replay_rh_module_set.py --lean (Get-Command lean).Source --archive outputs/rh-proof-value/alp-oleans-Main-and-small.tar.gz
python -E -S tools/replay_rh_module_set.py --lean (Get-Command lean).Source --archive outputs/rh-proof-value/alp-oleans-Main-and-small.tar.gz --branch-dir outputs/rh-proof-value/branch-inputs
python -E -S tools/replay_rh_module_set.py --lean (Get-Command lean).Source --archive outputs/rh-proof-value/alp-oleans-Main-and-small.tar.gz --branch-dir outputs/rh-proof-value/branch-inputs --next-layer
python -E -S tools/replay_rh_frontier.py --lean (Get-Command lean).Source --frontier docs/rh-next-layer-module-set.json --archive outputs/rh-proof-value/alp-oleans-Main-and-small.tar.gz --branch-dir outputs/rh-proof-value/branch-inputs --graph outputs/rh-proof-value/verified-rh-graph.json.gz
lean -o outputs/rh-proof-value/ProofRefsFixture.olean tests/lean/ProofRefsFixture.lean
lean --run tools/ProofRefs.lean outputs/rh-proof-value/ProofRefsFixture.olean probeTarget
```
