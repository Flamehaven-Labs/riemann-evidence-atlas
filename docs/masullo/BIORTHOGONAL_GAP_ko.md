# 가까운 제타 영점과 쌍직교 노름 상계

## 원고에서 상수를 쓰는 위치

2026-11-20 판의 고정 PDF를 대조했다. 451쪽 식 (10.3.1.18) 직후에는 Markushevich 기저의 정규화를 근거로 영점과 미분 차수에 무관한 상수 $C$를 택한다. 미분 차수 0, $\mathbb Q$의 자명 문자, 중심선 $a=1/2$, Sobolev 차수 $s=2$로 제한해도 이 상계는 성립하지 않는다. [고정 원고의 출처와 해시](README_ko.md) · [반례 보고 #1169](https://github.com/mccorvie/riemann-masullo/issues/1169)

| 위치 | 확인한 의존 관계 |
| --- | --- |
| 444쪽, 용어 10.2.1.2와 따름정리 10.2.1.4 | 원고는 기저 벡터의 노름이 0에서 떨어져 있으면 쌍직교 함수열이 유계라고 추론한다. 447쪽 따름정리 10.2.2.3은 같은 용어로 띠의 기저를 다룬다. |
| 451–452쪽, (10.3.1.18)–(10.3.1.23) | 같은 $C$가 (10.3.1.19), (10.3.1.20), (10.3.1.22)에 전달된다. (10.3.1.23)의 Schatten 노름에서의 Cauchy 결론을 뒷받침하는 상계다. |
| 454–455쪽, 정리 10.3.2.1 | 양의 폭을 가진 띠에 앞선 증명 방법을 사용하며, 변환의 도함수에 대한 합을 별도로 추정한다. |
| 463–464쪽, (10.4.2.24), (10.4.2.34) | 쌍직교 벡터의 lift에 대해 다시 공통 상한을 택한다. 이어 지표와 무관한 상수로 rank-one 연산자의 합을 제어하고 $S_1$ 극한을 주장한다. |

## 간격이 강제하는 하한

$\delta=|t-u|>0$라 하자. 가중 이중 노름에서 $\|\eta_t\|^2=\pi c$다. Fourier 항등식 $\int_{\mathbb R}\cos(\delta x)/(1+x^2)\,dx=\pi e^{-\delta}$를 쓰면 $\|\eta_t-\eta_u\|^2=2\pi c(1-e^{-\delta})$다. 쌍직교성은 $(\eta_t-\eta_u)(\psi_t)=1$을 준다. 평가의 연산자 노름 부등식을 적용하면 아래 하한을 얻는다. 몫 노름에서는 평가가 대표원에 무관하므로 대표원 노름의 하한을 취한다.

$$
\|\eta_t\|\|\psi_t\|
\ge \frac{1}{\sqrt{2(1-e^{-\delta})}}
\ge \frac{1}{\sqrt{2\delta}}.
$$

따라서 공통 상한 $C>0$가 있다면 모든 서로 다른 단순 영점 쌍은 $\delta\ge 1/(2C^2)$를 만족해야 한다. Conrey의 정리 1과 영점 계수식을 적용하면 높이 $T$까지의 단순 임계선 영점 수는 $\gg T\log T$다. 고정 간격으로 분리된 집합의 개수는 $O(T)$이므로 임의로 작은 양의 간격이 존재한다. [Conrey 논문, 식 (8)과 정리 1](https://www.maths.dur.ac.uk/users/herbert.gangl/morethan2_5.PDF)

## Lean에서 확인한 범위

| 선언 | 증명한 내용 |
| --- | --- |
| `inverse_sqrt_gap_le` | $1-e^{-\delta}\le\delta$에서 역제곱근 부등식을 얻는다. |
| `biorthogonal_product_lower` | 두 연속 선형 함수가 같은 벡터에서 1과 0을 주고 정규화된 거리식이 성립할 때, 노름 곱의 하한을 얻는다. |
| `gap_lower_of_uniform_cap` | 공통 상한 $C>0$에서 간격의 필요조건 $\delta\ge1/(2C^2)$를 얻는다. |
| `no_uniform_cap_of_close_pairs` | 임의로 작은 양의 간격과 각 쌍의 하한을 가정하면 공통 상한은 존재할 수 없다. |

Lean 선언에서 정규화된 거리식과 가까운 영점 쌍의 존재는 가정이다. 원본 공간에 적용하는 Fourier 항등식과 영점 계수는 위에 인용한 해석적 근거에 해당한다. [Lean 소스](../../tests/lean/E2ABiorthogonalGap.lean)

2026-11-24 Windows와 새 Colab Linux 런타임에서 Lean 4.33.1 및 고정 Mathlib `0df444a360eaa60ab8c11dca51a86af692955474`로 네 정리를 컴파일했다. 네 선언의 공리는 `propext`, `Classical.choice`, `Quot.sound`였다. GitHub Actions에서 이 파일의 실행은 아직 확인되지 않았다. [Windows 영수증](biorthogonal-gap-windows-replay.json) · [Colab 원본 영수증](biorthogonal-gap-colab-replay.json)

고정 의존성을 복원한 뒤 저장소 루트에서 아래 명령을 실행한다.

~~~sh
cd formal/landau
lake env lean --root=../.. -j 2 ../../tests/lean/E2ABiorthogonalGap.lean
~~~

## 교체 가능한 추정

간격에 따라 달라지는 상계를 쓰려면 그 상계와 Mellin 변환을 곱한 항의 총합을 새로 제어해야 한다. 현재 확보한 것은 노름 곱의 하한이다. 다른 경로는 가까운 영점 묶음에 대응하는 제한 연산자의 노름을 직접 추정하는 것이다. 공개 논의의 후보가 원고의 공간에서 성립하는지와 그 추정이 trace 합까지 이어지는지는 다음 검토 대상이다. [공개 수정 제안](https://github.com/mccorvie/riemann-masullo/issues/1169#issuecomment-7053478224)

두 영점만 놓은 경우에는 Mellin 승수의 값 차이가 비대각항의 증가를 상쇄하는 조건을 증명했다. [두 영점 모형](TWO_ZERO_BLOCK_ko.md)
