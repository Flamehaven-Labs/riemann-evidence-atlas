# 양의 띠 폭에서 가까운 두 영점의 극한

공개된 양의 띠 폭 모형에서 Sobolev 차수를 $s=2$로 고정하고, 같은 중심선 위의 두 모드를 비교한다. 고정 $\alpha>0$에서 가중치, 정규화 상수, 2차 모멘트는 다음과 같다. [공개 가중 공간 모형](https://github.com/mccorvie/riemann-masullo/issues/1169#issuecomment-7057208991)

$$
w_\alpha(x)=\frac{e^{-2\alpha|x|}}{1+x^2},\qquad
Z_\alpha=\int_{\mathbb R}w_\alpha(x)\,dx,\qquad
M_2(\alpha)=\frac{\int_{\mathbb R}x^2 w_\alpha(x)\,dx}{Z_\alpha}.
$$

$w_\alpha$와 $x^2w_\alpha$는 모두 $e^{-2\alpha|x|}$ 이하이며, 이 함수의 양쪽 반직선 적분은 유한하다. 두 적분은 연속인 비음수 함수가 각각 $x=0$과 $x=1$에서 양수이므로 양수다.

정규화된 중심선 모드 $e^{itx}/\sqrt{Z_\alpha}$의 내적에서 사인 항은 가중치의 짝대칭으로 소거된다. 따라서 실수 상관함수 $\rho_\alpha(\delta)$는 $\cos(\delta x)w_\alpha(x)$의 적분을 $Z_\alpha$로 나눈 값이다. 아래 두 계산은 코사인 적분과 추상 복소 내적 공간에서 각각 증명한다.

## 적분에서 직교화 분모까지

$$
\frac{1-\cos(\delta x)}{\delta^2}
=\frac{x^2}{2}\operatorname{sinc}^2\left(\frac{\delta x}{2}\right).
$$

연속인 $\operatorname{sinc}$는 0에서 1이고 절댓값이 1 이하이다. 따라서 지배수렴을 적용할 수 있고, $(1-\rho_\alpha(\delta))/\delta^2\to M_2(\alpha)/2$다. Lean은 충분히 작은 양의 $\delta$에서 다음 양쪽 부등식도 증명한다.

$$
\frac{M_2(\alpha)}4\,\delta^2
\ \le\ 1-\rho_\alpha(\delta)\
\le\ \frac{3M_2(\alpha)}4\,\delta^2.
$$

일반적인 실수 내적 $\rho$가 $|\rho|<1$을 만족하는 두 단위 고유벡터 $u,v$에 대해 두 번째 정규직교 벡터는 $(v-\rho u)/\sqrt{1-\rho^2}$다. 이 기저에서 비대각항은 $\rho(b-a)/\sqrt{1-\rho^2}$다. 위 가중치에서는 $\sqrt{1-\rho_\alpha(\delta)^2}/\delta\to\sqrt{M_2(\alpha)}$다.

## 비대각항의 세 가지 경우

| 승수 차이 | 고정 양의 폭에서 증명한 결과 |
| --- | --- |
| $|b-a|\le K\delta$ | 충분히 작은 양의 간격에서 비대각항의 절댓값은 $2K/\sqrt{M_2(\alpha)}$ 이하 |
| $b=m(t+\delta)$, $a=m(t)$이며 $m$이 $t$에서 미분 가능 | 비대각항은 $m'(t)/\sqrt{M_2(\alpha)}$로 수렴 |
| $a=0$, $b=1$ | 비대각항의 절댓값은 $+\infty$로 발산 |

$m(t)=t$에서는 극한이 $1/\sqrt{M_2(\alpha)}\ne0$이다. 폭 0에서 확보한 $O(\sqrt{\delta})$ 감소와 양의 고정 폭에서의 유계성은 각 가중치에 따른 결과다. 폭과 간격을 동시에 0으로 보내는 문제는 이 증명의 범위 밖에 있다. [폭 0의 두 영점 모형](TWO_ZERO_BLOCK_ko.md)

보조 수치 계산에서 $\alpha=1/4$를 놓으면 $M_2\approx1.324157806194$, 선형 승수의 비대각 극한은 약 $0.869020712016$이다. 대칭성을 사용한 구간 $[0,80]$의 Simpson 적분을 16,000개와 32,000개로 나누어 계산했고, $\delta=10^{-6}$에서 비대각항은 약 $0.869020712016$이었다. 이 값은 수치 관찰이다.

## 검증 범위

Lean은 적분의 극한과 일반 실수 Gram 내적에 대한 정확한 행렬 등식을 증명하고, 가중치가 주는 극한을 비대각항에 적용한다. 원고의 이델 몫 공간, 서로 다른 실수부의 영점 또는 중복 영점, 전체 창 사영, 무한 Schatten 노름 합은 열린 연구 과제다. [Lean 소스](../../tests/lean/E2APositiveStripGram.lean)

2026-11-24 Windows와 새 Colab Linux 런타임에서 Lean 4.33.1 및 고정 Mathlib `0df444a360eaa60ab8c11dca51a86af692955474`로 12개 선언을 확인했다. 호스트 표기를 제외한 영수증 필드가 모두 일치했다. 공리 기록은 `propext`, `Classical.choice`, `Quot.sound`를 표시했다. GitHub Actions에서는 이 파일을 아직 실행하지 않았다. [Windows 영수증](positive-strip-gram-windows-replay.json) · [Colab 원본 영수증](positive-strip-gram-colab-replay.json)

고정 Mathlib 의존성을 복원한 저장소에서 재실행한다.

~~~sh
cd formal/landau
lake env lean --root=../.. -j 2 ../../tests/lean/E2APositiveStripGram.lean
~~~
