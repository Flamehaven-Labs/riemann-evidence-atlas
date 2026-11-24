# 가까운 두 영점에서 Mellin 승수가 작용하는 방식

## 두 벡터의 행렬

간격을 $\delta=|t-u|>0$라 하고, 단위 벡터 $v_t,v_u$의 내적이 실수 $\rho=e^{-\delta}$라고 가정한다. 선형 사상 $A$는 $A v_t=a v_t$, $A v_u=b v_u$를 만족한다. 여기서 $a=m(t)$, $b=m(u)$다. 이 가정에서 $w=e^\delta v_u-v_t$는 $v_t$와 직교하고 $\|w\|^2=e^{2\delta}-1$이다. $D=\sqrt{e^{2\delta}-1}$로 쓰면 $e_2=w/D$는 단위 벡터이며 $v_u=e^{-\delta}(v_t+D e_2)$다. 따라서 $(v_t,e_2)$는 두 벡터가 생성한 공간의 정규직교 기저다.

$$
A e_2=\frac{b-a}{D}\,v_t+b e_2,\qquad
[A]_{(v_t,e_2)}=
\begin{pmatrix}a & (b-a)/D \\ 0 & b\end{pmatrix}.
$$

## 승수 차이가 충분히 작을 때

$|b-a|\le K\delta$와 $K\ge0$이면 $D\ge\sqrt{2\delta}$이므로 비대각 성분의 절댓값은 $K\sqrt{\delta/2}$ 이하다. 따라서 같은 $K$가 적용되는 쌍에서 이 성분은 $\delta\to0^+$일 때 0으로 수렴한다.

승수값을 계속 $a=0$, $b=1$로 두면 비대각 성분의 절댓값은 $1/D$다. 양의 $D$가 0으로 접근하므로 이 값은 $+\infty$로 발산한다. 두 경우의 차이는 정확히 승수값 차이의 크기다. 이 반례는 두 벡터 모형에서 승수를 자유롭게 지정한 경우에 해당한다.

고정 수직선에서 $m(t)=\int_{\mathbb R}k(x)e^{itx}\,dx$라고 쓸 때, $k$가 적분 가능하고 $\int_{\mathbb R}|xk(x)|\,dx<\infty$라면 이 절대 1차 모멘트를 $K$로 쓸 수 있다. $\lvert e^{iux}-e^{itx}\rvert\le \lvert u-t\rvert\lvert x\rvert$를 적분하면 된다. 이 계산은 해당 수직선에서 Lipschitz 조건을 확인하는 해석적 기준이다.

## Lean에서 점검하는 명제

| 선언 | 내용 |
| --- | --- |
| `orthonormal_block` | 복소 내적 공간의 Gram–Schmidt 계산과 두 행렬 열의 정확한 등식 |
| `off_diagonal_norm_le` | Lipschitz 차이 조건 아래의 $K\sqrt{\delta/2}$ 상한 |
| `off_diagonal_tendsto_zero` | 양의 간격을 0으로 보낼 때 복소 비대각 성분의 수렴 |
| `fixed_jump_diverges` | 승수 차이를 1로 고정한 반례에서 비대각 성분의 절댓값이 $+\infty$로 발산 |

Lean의 입력은 정확한 Gram 내적과 두 고유벡터 등식이다. 정리는 이 두 벡터가 생성한 공간에 제한한 행렬을 계산한다. 전체 공간에서 창을 분리하는 사상, 무한 창의 $S_1$ 노름 합, 기하학적 trace의 비교는 별도의 문제다. 공개 논의의 유한 창 제안은 창 전체를 원본 몫 공간의 연산자로 다룬다. [Lean 소스](../../tests/lean/E2ATwoZeroBlock.lean) · [공개 유한 창 제안](https://github.com/mccorvie/riemann-masullo/issues/1169#issuecomment-7055349843)

2026-11-24 Windows와 새 Colab Linux 런타임에서 고정 Lean 4.33.1 및 Mathlib `0df444a360eaa60ab8c11dca51a86af692955474`로 네 선언을 재실행했다. 증명 파일과 공리 출력 해시가 일치했다. 이 파일의 GitHub Actions 실행은 아직 수행하지 않았다. [Windows 영수증](two-zero-block-windows-replay.json) · [Colab 원본 영수증](two-zero-block-colab-replay.json)

고정 의존성을 갖춘 저장소에서 아래 명령으로 재실행할 수 있다.

~~~sh
cd formal/landau
lake env lean --root=../.. -j 2 ../../tests/lean/E2ATwoZeroBlock.lean
~~~

양의 고정 폭을 도입하면 $1-\rho(\delta)$는 간격의 제곱 차수로 감소한다. 이때 비대각 성분이 승수의 도함수에 비례하는 0이 아닌 값으로 수렴할 수 있다. [양의 띠 폭에서의 형식 검증](POSITIVE_STRIP_GRAM_ko.md)
