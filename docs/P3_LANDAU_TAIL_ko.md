# P3 · Landau 꼬리 적분 검증

고정 입력은 $k=3$, $\sigma=5$ (감쇠율 $s=3$), $U=1$, $V=3$이다. 검증 대상은 `Deduction.landau_window_ineq` 세 번째 우변 항에 들어가는 적분이다. 앞에 곱해지는 $2C_0$, 다른 우변 항, 원래 정리의 전체 결론은 별도 대상이다. [원본 Lean 추출 핀](../lean-extract-manifest.json) · [Python 결과](../window-results-v2.json)

$$J=\int_{(0,\infty)\setminus[1,3]}
 \frac{u^3e^{-3u}}{3!}\,du
 =\frac{1-13e^{-3}+172e^{-9}}{81}.$$

**로컬 실행 PASS.** 유리수 끝점 모듈의 감사 선언 2개, 유리수 급수 모듈 8개, 실수 모듈 5개를 컴파일했다. 공리 출력은 `propext`, `Classical.choice`, `Quot.sound` 범위이며 `sorryAx`는 검출되지 않았다. Python 3.10·3.14에서 각각 43개의 회귀 테스트를 통과했다. [실행 기록과 해시](landau-tail-lean-replay.json)

## 증명 구성

- [끝점 전파](../tests/lean/E2ATailEndpointAlgebra.lean)는 항 $-13e^{-3}$에서 끝점의 순서를 바꾸고, 두 유리수 경계가 Python 128비트 기록과 동일함을 확인한다.
- [유리수 지수 계산](../tests/lean/E2ALandauTailRational.lean)은 $3/8$에서 37차, $9/32$에서 34차 Taylor 합을 계산한다. Python에서 쓰는 기하급수 나머지와 [Mathlib 지수 상계](https://github.com/leanprover-community/mathlib4/blob/0df444a360eaa60ab8c11dca51a86af692955474/Mathlib/Analysis/Complex/Exponential.lean#L523)에 쓰이는 나머지를 각각 192비트 dyadic 상한 안에 넣는다. 분할 지수의 양의 끝점을 각각 8제곱과 32제곱한 후 역수의 순서를 뒤집어 기존 128비트 경계에 연결한다. 이 증명은 중간 반올림을 생략한 유리수 거듭제곱으로 같은 최종 끝점의 유효성을 보인다.
- [실수 연결](../tests/lean/E2ALandauTailReal.lean)은 Mathlib의 실수 지수 급수 상·하계로 두 지수값을 감싼다. 감마 적분에서 전체 질량 $1/81$을 구하고, 명시적 원시함수로 $[1,3]$ 적분을 계산한 후 전체에서 빼는 방식이다. 끝점 전파를 적용하면 동일 구간에서 $1/300<J\le1/200$을 얻는다.

## 재실행

먼저 `python -E -S tools/verify_baseline.py`로 수치 결과를 재생한다. Lean 4.33.1 실행 파일을 `LEAN_BIN`으로 지정한다.

~~~sh
python -E -S tools/verify_landau_tail.py --lean "$LEAN_BIN"
~~~

실수 단계는 [고정 Lake 프로젝트](../formal/landau/lakefile.toml)와 [의존성 잠금](../formal/landau/lake-manifest.json)을 사용한다. 전체 Lean 배포본에서 `formal/landau`를 작업 폴더로 두고 아래 명령으로 필요한 캐시를 준비한다.

~~~sh
lake exe cache get Mathlib.Analysis.Complex.Exponential \
  Mathlib.Analysis.SpecialFunctions.Gamma.Basic \
  Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus \
  Mathlib.Tactic.Positivity Mathlib.Tactic.NormNum Mathlib.Tactic.Ring Mathlib.Tactic.Linarith
~~~

저장소 루트로 돌아와 실행한다.

~~~sh
python -E -S tools/verify_landau_tail.py --lean "$LEAN_BIN" --mathlib-project formal/landau
~~~

실행기는 Lean 커밋과 각 Lake 의존성의 커밋·추적 파일 상태를 확인한다. 임시 폴더에서 세 모듈을 차례대로 컴파일하고 소스 해시와 명명된 정리의 공리 출력을 기록한다. Mathlib 실수 검사의 학술적 범위는 이 고정 적분이다. 보존된 RH 전체 증명 커널 검사와 Colab 재현은 별도 실행이다.

## P3.2 원문 간 연결

F=Q에서 노름만 따르는 후보 $\varphi(c)=h(|c|)$를 두고 $h(1)=0$이라면 단위 껍질은 사라진다. 다른 껍질에서는 정규화 Haar 측도에 의해 국소 가중치가 $\log 2\,h(2^{-m})2^{-|m|/2}$로 좁혀진다. 노름 방향의 지지가 양의 반직선에서 콤팩트하면 이 합에는 유한 개의 $m$만 남는다. P2의 오일러 로그미분 전체 급수와 연결하려면 시험 함수족, 양·음 껍질의 대응, 꼬리와 극한 교환을 따로 정당화해야 한다. 원고에 근거한 이 연결은 HELD다. [두 원문 위치와 가정](masullo/P2_CHARACTER_COMPARISON_ko.md)

## P3.3 검증 범위

| 자료 | 적합한 검증 | 열린 항목 |
| --- | --- | --- |
| Alpöge Lean | 고정 `.olean`에서 타입·증명 항을 추출하고 두 경로를 확인 | `VwinOfRow.olean` 확보와 원본 RH 전체 커널 재실행 |
| Masullo 원고 | 고정 PDF에서 수식 위치·측도·시험 함수 가정을 대조 | 주값 적분과 Euler 인자의 해석적 연결 |
| 수치 코드 | 정확 유리수 값, 잘못된 부호·도체, 정밀도 소진, 보고서 변조를 구별 | 다른 입력으로의 해석적 증명 일반화 |
| Lean 꼬리 인증 | 지수 포락과 임계값을 고정 입력의 실수 적분에 연결 | 실제 Colab 및 별도 운영자 재현 |
