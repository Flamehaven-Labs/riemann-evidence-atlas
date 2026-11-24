# RH 반사 단계에서 코사인 인자가 하는 일

## 원본 증명

`Formalism.VW.rh_of_right`는 $\operatorname{Re}z>1/2$이고 $z\ne1$이면 $\zeta(z)\ne0$이라는 가정에서 출발한다. 자명 영점과 극점 조건을 제외한 영점 $s$가 왼쪽에 있다고 가정하면 $t=1-s$는 오른쪽에 놓인다. 원본은 Mathlib의 함수방정식을 $t$에 적용한다.

$$
\zeta(s)=2(2\pi)^{-t}\,\Gamma(t)\,\cos(\pi t/2)\,\zeta(t).
$$

우변 마지막 인자는 처음 가정으로 0이 아니다. $t$의 실수부가 양수이므로 감마 인자도 0이 아니다. 밑이 0이 아닌 복소 거듭제곱까지 확인한 뒤, 남는 일은 코사인 인자가 0이 아님을 보이는 것이다. 원본을 읽으면 이 확인에 왜 $s=0$과 자명 영점을 각각 처리해야 하는지가 드러난다.

원본 `RhOfRight.lean` 5행에 정리, 28행에 함수방정식 적용, 34–59행에 코사인 논증, 60행에 인자들을 곱해 모순을 얻는 단계가 있다. 파일은 배포 아카이브의 `lean/src/Formalism/GammaFactorNonvanishing/RhOfRight.lean`에서 추출했다. SHA-256은 `7e2c0b519ee420192cad8fb281c2d2bfebae2ba553342fd579c81c2aa0bd3dc5`다. [아카이브 고정 기록](../lean-archive-manifest.json) · [원본 선언의 참조 기록](rh-next-layer-module-set.json)

## 보조정리의 정확한 범위

Mathlib의 `Complex.cos_eq_zero_iff`에 따르면 복소 코사인의 영점은 $(2k+1)\pi/2$이며 $k$는 정수다. 이에 $\pi(1-s)/2$를 대입하고 $\pi\ne0$으로 소거하면

$$
\cos\bigl(\pi(1-s)/2\bigr)=0
\quad\Longleftrightarrow\quad s=-2k\quad(k\in\mathbb Z).
$$

따라서 $\operatorname{Re}s<2$에서는 $k\ge0$이다. $k=0$이면 $s=0$이고, $k>0$이면 $s$는 음의 짝수다. 원본은 $\zeta(0)=-1/2$로 첫 경우를 제거하고, 비자명 영점이라는 가정으로 나머지를 배제한다.

**코사인 인자만 보면 실수부 조건을 $\operatorname{Re}s<2$로 넓힐 수 있다.** $s=2$에서 코사인 인자는 다시 0이고 $2$는 $-2n$ 꼴이 아니므로, 위 분류에서 경계를 포함할 수 없다. 원본 전체의 반사 논증에는 $\operatorname{Re}s<1/2$가 여전히 필요하다. 그래야 $\operatorname{Re}(1-s)>1/2$인 점에서 처음의 무영점 가정을 적용할 수 있다.

## 실행과 증명 항 확인

- 원본 `RhOfRight.olean`을 Lean 4.33.1로 읽어 `Complex.cos_eq_zero_iff`가 `rh_of_right`의 증명 항에 직접 등장함을 확인했다. 원본 소스에서는 이 정리가 코사인 인자를 정수 조건으로 바꾸는 데 쓰인다.
- Mathlib의 `Complex.olean`만 읽으면 이 보조정리는 본체 없는 `axiomInfo`로 나타났다. Lean의 `readModuleDataParts`에 `Complex.olean`과 `Complex.olean.private`를 순서대로 전달하자, 같은 타입을 가진 `thmInfo`의 증명 본체를 확인했다. 증명 항이 보이지 않을 때에는 어떤 파일을 읽었는지 먼저 확인해야 공리 의존성을 정확히 판단할 수 있다.
- 별도 Lean 파일에서 정확한 영점 분류, $\operatorname{Re}s<2$인 경우, 원본 분기의 코사인 비소멸, $s=2$ 경계 사례를 컴파일했다. 네 선언의 공리는 `propext`, `Classical.choice`, `Quot.sound`였다. [검증한 Lean 소스](../tests/lean/E2ARhReflectionCos.lean)

2026-11-24 Colab Linux에서 고정 Lean 4.33.1과 Mathlib으로 네 선언을 다시 컴파일했다. 공리 출력 네 줄이 Windows 기준과 모두 일치했다. Colab 출력의 SHA-256은 `a062993d32ef6d25882cb836896d7fb7a90b9a7a90105f23d669fe69407779ad`다. 이 실행은 위 보조정리 파일을 검사했다. 원본 RH 전체의 커널 재검사는 남아 있다. [실행 입력과 범위](ROADMAP_ko.md#단계-전환-때-재현)

고정 Mathlib을 준비한 Lake 작업 폴더에서 Lean 파일을 아래와 같이 실행한다.

~~~sh
cd formal/landau
lake env lean -j 2 ../../tests/lean/E2ARhReflectionCos.lean
~~~
