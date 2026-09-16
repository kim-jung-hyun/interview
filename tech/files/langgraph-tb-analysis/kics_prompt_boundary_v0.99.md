Prompt Boundary 기반 경량 탐지기를 이용한
LLM 보안 위협 탐지에 관한 연구

김정현
LG전자
jh.kim@lge.com

A Study on
LLM Security Threat Detection Using a Lightweight Detector at the Prompt Boundary

JungHyun Kim
LG Electronics

요 약

대형 언어 모델(LLM)을 활용한 생성형 AI 서비스가 확산됨에 따라, 사용자 입력을 통해 시스템 동작을 조작하는 Prompt Injection 공격이 주요 보안 위협으로 부각되고 있다. 기존 LLM 보안 연구는 모델 내부 안전성 강화, 프롬프트 설계 기법, 또는 출력 결과에 대한 사후 검증 방식에 초점을 두어 왔다. 그러나 실제 서비스 환경에서는 사용자 입력이 LLM으로 전달되기 전 여러 처리 단계가 존재하며, 이 과정에서 명확한 신뢰 경계(boundary)가 형성된다.

본 논문에서는 Prompt Injection을 모델 내부 문제가 아닌 **Prompt Boundary에서 발생하는 경계 위협(boundary threat)**으로 정의하고, 해당 경계에서 **DistilBERT 기반 경량 탐지기(lightweight detector)**를 이용하여 입력을 사전 선별하는 구조를 제안한다. 제안 기법은 Prompt Boundary에서 입력 텍스트에 대한 위협 시그널(score)을 산출하고, 이를 기반으로 allow, sanitize, block과 같은 다단계 정책 결정을 수행한다.

OWASP LLM Top 10을 참고하여 구성한 공개 데이터셋과 합성 데이터 기반의 실험 결과, 제안한 탐지기는 Prompt Injection 공격에 대해 실용적인 탐지 성능을 보였으며, 경계 기반 LLM 보안 구조가 기존 접근 방식과 구별되는 효과적인 보안 제어 지점이 될 수 있음을 확인하였다.

Ⅰ. 서 론

생성형 AI와 대형 언어 모델(LLM)은 대화형 서비스, 검색 보조, 코드 생성, 자동 문서 작성 등 다양한 분야에서 활용되고 있다. 그러나 LLM은 자연어 입력을 직접 추론 과정에 반영한다는 특성으로 인해 기존 소프트웨어 시스템과는 다른 유형의 보안 위협에 노출된다. 특히 Prompt Injection 공격은 사용자 입력을 통해 시스템 프롬프트를 무력화하거나, 내부 정책 및 제어 문맥을 왜곡하는 대표적인 공격 기법으로 알려져 있다[1].

기존 LLM 보안 접근 방식은 크게 세 가지로 구분할 수 있다. 첫째, 모델 내부에서 안전 필터링이나 정렬(alignment)을 강화하는 방식이다. 둘째, 시스템 프롬프트를 강화하거나 입력을 제한하는 프롬프트 설계 중심의 방식이다. 셋째, 출력 결과를 검사하거나 수정하는 사후 처리 방식이다. 이러한 접근은 각각 장점을 가지지만, 모델 종속성, 적용 비용, 서비스 유연성 측면에서 한계를 가진다.

실제 AI 기반 서비스 환경에서는 사용자 입력이 곧바로 모델로 전달되지 않는다. 입력은 애플리케이션 또는 백엔드 로직을 거쳐 프롬프트 빌더(prompt builder)에 의해 시스템 프롬프트와 결합된 후 LLM으로 전달된다. 이 과정에서 사용자 입력과 시스템 제어 정보가 결합되는 지점, 즉 Prompt Boundary라는 명확한 신뢰 경계가 형성된다.

본 논문에서는 Prompt Injection을 이 Prompt Boundary에서 발생하는 경계 위협으로 재정의하고, 모델을 수정하지 않고도 적용 가능한 경량 탐지 기반 보안 구조를 제안한다.

Ⅱ. 관련 개념 및 위협 모델
2.1 AI Boundary 개념

AI 기반 서비스는 단일한 모델 호출로 구성되지 않으며, 입력 처리, 프롬프트 구성, 추론, 출력 전달 등 여러 단계로 구성된다. 각 단계는 서로 다른 신뢰 수준을 가지며, 본 연구에서는 이를 AI Boundary로 정의한다.

대표적인 AI Boundary는 다음과 같다.

Input Boundary: 사용자 또는 디바이스에서 서비스로 입력이 전달되는 경계

Prompt Boundary: 사용자 입력과 시스템 프롬프트가 결합되는 경계

Retrieval Boundary: RAG 환경에서 외부 지식이 결합되는 경계

Tool Boundary: 외부 도구(API, 결제, 코드 실행 등)가 호출되는 경계

Output Boundary: LLM 출력이 사용자에게 전달되는 경계

본 논문은 이 중 Prompt Boundary에 초점을 맞춘다.

2.2 Prompt Injection 위협의 경계적 해석

Prompt Injection은 단순히 “악성 문장”의 문제가 아니라, 사용자 입력이 시스템 제어 문맥과 결합되는 과정에서 발생하는 구조적 문제로 해석할 수 있다. 즉, 공격의 본질은 **경계에서의 신뢰 혼합(trust mixing)**에 있다.

이러한 관점에서 Prompt Injection은 모델 내부 추론 문제가 아니라, Prompt Boundary에서의 입력 검증 및 정책 부재로 인해 발생하는 **경계 위협(boundary threat)**으로 분류할 수 있다.

Ⅲ. Prompt Boundary 기반 탐지 구조
3.1 전체 구조 개요

그림 1은 본 논문에서 제안하는 Prompt Boundary 기반 경량 탐지 구조를 나타낸다. 사용자 입력은 Prompt Builder에 의해 시스템 프롬프트와 결합되기 전에 Prompt Boundary에서 탐지기를 거친다.

[ User Input ]
      |
      v
+--------------------+
|  Prompt Boundary   |
|--------------------|
| DistilBERT-based   |
| Threat Detector    |
| (score output)     |
+--------------------+
      |
      v
+--------------------+
| Policy Decision    |
|--------------------|
| allow / sanitize   |
| block              |
+--------------------+
      |
      v
+--------------------+
| Prompt Builder     |
| system + user      |
+--------------------+
      |
      v
[ LLM Inference ]
      |
      v
[ Output ]


그림 1. Prompt Boundary 기반 경량 탐지 구조

3.2 Threat Signal Engine

탐지기는 DistilBERT 기반 경량 분류 모델로 구성되며, 입력 문장을 공격(prompt injection) 또는 정상(normal)으로 분류한다. 탐지기의 역할은 최종 차단 여부를 판단하는 것이 아니라, **위협 가능성에 대한 정량적 시그널(score)**을 제공하는 것이다.

이러한 설계는 탐지기와 정책 결정을 분리함으로써, 서비스 환경에 따라 정책을 유연하게 조정할 수 있도록 한다.

3.3 정책 결정 단계

정책 계층은 탐지기에서 산출된 score를 기반으로 다음과 같은 후속 조치를 결정한다.

allow: 정상 입력으로 판단되어 그대로 전달

sanitize: 공격 지시어 또는 민감 표현만 제거한 후 전달

block: 입력을 차단하고 오류 또는 대체 응답 반환

sanitize 정책은 명백한 공격이 아닌 경계적·모호한 입력을 처리하기 위한 핵심 요소이다.

Ⅳ. 실 험
4.1 데이터셋 구성

실험은 탐지기 학습과 평가를 분리하여 수행하였다.

학습 데이터: Hugging Face 공개 Prompt Injection 데이터셋

공격 유형: 지시 무력화, 시스템 프롬프트 노출 요구, 역할 전환 등

평가 데이터: OWASP LLM Top 10 기반 합성 hard test set (총 50개 샘플)

4.2 실험 설정

DistilBERT 기반 이진 분류 모델을 사용하였으며, Precision, Recall, F1-score를 성능 지표로 사용하였다. 정책 임계값은 Prompt Boundary 적용을 고려하여 여러 threshold에 대해 비교하였다.

4.3 실험 결과

표 1. Prompt Injection 탐지 성능 (threshold = 0.55)

Metric	Value
Precision	0.6957
Recall	0.8000
F1-score	0.7442

표 2. Confusion Matrix

	Predicted Attack	Predicted Normal
Actual Attack	TP = 16	FN = 4
Actual Normal	FP = 7	TN = 23

실험 결과, 공격 문장에 대한 재현율이 상대적으로 높게 나타났으며, Prompt Boundary에서의 사전 선별 용도로 충분한 성능을 확인하였다.

Ⅴ. 논 의

본 연구의 핵심 기여는 Prompt Injection을 입력 자체의 문제가 아니라 Prompt Boundary에서 발생하는 구조적 위협으로 재정의한 점에 있다. 이는 모델 내부 수정 없이도 적용 가능하며, 서비스 아키텍처 관점에서 명확한 보안 제어 지점을 제공한다.

Ⅵ. 결 론 및 향후 연구

본 논문에서는 Prompt Injection 공격을 Prompt Boundary에서 발생하는 경계 위협으로 정의하고, DistilBERT 기반 경량 탐지기를 이용한 보안 구조를 제안하였다. 실험 결과를 통해 제안 기법이 실용적인 탐지 성능을 가짐을 확인하였다.

향후 연구에서는 Prompt Boundary 외에도 Input, Retrieval, Output Boundary로 확장하고, 다중 위협을 종합적으로 관리하는 위험 평가 구조로 발전시킬 계획이다.

참 고 문 헌

[1] OWASP Foundation, “OWASP Top 10 for Large Language Model Applications,” 2023.
[2] V. Sanh et al., “DistilBERT, a distilled version of BERT,” NeurIPS Workshop, 2019.
