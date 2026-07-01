# Food-101 CNN Fine-Tuning Backend

Food-101 음식 이미지 분류 모델을 FastAPI로 서비스화한 백엔드 프로젝트입니다.  
사전 학습 CNN 모델을 Food-101 데이터셋에 맞게 파인튜닝하고, 사용자가 업로드한 음식 이미지를 API에서 전처리한 뒤 Top-3 예측 결과를 반환하는 구조로 구현했습니다.

이 프로젝트는 단순히 모델을 학습하는 데서 끝나지 않고, 학습된 모델을 실제 웹 애플리케이션에서 사용할 수 있도록 API 서버, 모델 로딩, 이미지 전처리, 예측 결과 반환, 모델 상태 확인 기능까지 연결한 엔드투엔드 배포형 개인 프로젝트입니다.

## Project Goal

Food-101 데이터셋은 101개의 음식 클래스로 구성되어 있으며, 음식 이미지는 조명, 배경, 구도, 장식, 재료의 형태가 다양해 분류 난도가 높은 편입니다.  
본 프로젝트의 목표는 이러한 음식 이미지를 입력받아 모델이 예측한 상위 3개 음식 클래스와 confidence 값을 반환하는 이미지 분류 백엔드를 구축하는 것입니다.

핵심 목표는 다음과 같습니다.

- Food-101 분류 모델을 FastAPI 예측 API로 연결
- 이미지 업로드부터 전처리, 모델 추론, JSON 응답까지 하나의 흐름으로 구현
- 모델 파일 누락이나 로딩 실패 상황에서도 서버가 바로 중단되지 않도록 안정성 보완
- React 프론트엔드와 연동 가능한 API 구조 제공
- 포트폴리오에서 모델 학습 결과가 실제 서비스 구조로 이어졌음을 보여주는 백엔드 구현

## Why These Experiments Were Done

프로젝트에서는 여러 기초 실험과 전이학습 실험을 진행했고, 각 실험은 최종 모델과 배포 구조를 결정하기 위한 근거로 사용했습니다.

| 실험 | 실험 이유 | 프로젝트 반영 |
|---|---|---|
| 데이터 분할 비율 실험 | 학습/검증/테스트 데이터 비율이 일반화 성능 평가에 미치는 영향을 확인하기 위해 수행 | Food-101 학습에서도 검증 성능과 테스트 성능을 분리해서 해석해야 한다는 기준 확보 |
| 활성화 함수 비교 | Sigmoid, Tanh, ReLU의 기울기 특성과 학습 안정성을 비교하기 위해 수행 | CNN 은닉층에서 ReLU 계열 활성화 함수를 사용하는 근거 확보 |
| 증강 기법 비교 | 이미지 변형이 일반화 성능을 높이는지, 또는 라벨 의미를 훼손하는지 확인하기 위해 수행 | 음식 이미지는 과도한 rotation/shift보다 라벨 의미를 유지하는 제한적 증강이 적합하다고 판단 |
| 직접 CNN 구성 | 합성곱, 풀링, 완전연결층이 이미지 특징을 어떻게 학습하는지 이해하기 위해 수행 | Food-101 문제를 CNN 기반 이미지 분류 문제로 설계하는 이론적 근거 확보 |
| VGG16 전이학습 | Feature Extraction과 Fine-Tuning의 차이를 비교하기 위해 수행 | 사전 학습 모델도 Food-101에 맞춘 Fine-Tuning이 필요하다는 결론 도출 |
| ResNet50 실험 | 최종 배포 모델 후보의 성능과 튜닝 가능성을 확인하기 위해 수행 | 충분한 파인튜닝 후 ResNet50을 최종 모델로 선택 |
| ResNet50 vs VGG16 비교 | 모델 선택을 정확도뿐 아니라 안정성, 구조, 튜닝 난이도 관점에서 비교하기 위해 수행 | 초기 안정성은 VGG16이 높았지만, 최종 성능 확장성은 ResNet50이 높다고 판단 |

## Model Selection

초기 비교 실험에서는 VGG16이 ResNet50보다 안정적인 결과를 보였습니다. ResNet50은 초기 설정에서 학습이 거의 진행되지 않는 결과가 있었고, 이 때문에 단순 정확도만 보면 VGG16이 더 적합해 보였습니다.

하지만 이후 ResNet50의 learning rate, batch size, trainable layer 범위, input resolution 등을 조정하면서 성능이 크게 개선되었습니다. 최종적으로는 Residual Connection을 가진 ResNet50이 더 깊은 feature를 안정적으로 학습할 수 있고, 충분한 파인튜닝 후 더 높은 성능을 낼 수 있다고 판단했습니다.

최종 모델은 ResNet50 기반 Full Fine-Tuning 모델로 선정했습니다.

선정 이유:

- Food-101 101개 클래스 분류에서 가장 높은 검증 성능을 기록
- Residual Connection으로 깊은 네트워크 학습 안정성 확보
- Transfer Learning에서 Full Fine-Tuning으로 확장할수록 성능 향상이 명확함
- Keras `.h5` 모델로 저장해 FastAPI 추론 API에 연결하기 적합함

## Backend Role

이 백엔드는 학습된 CNN 모델을 서비스 API로 노출하는 역할을 담당합니다. 프론트엔드가 이미지를 업로드하면 백엔드는 이미지를 읽고, 모델 입력 형식에 맞게 전처리한 뒤 예측 결과를 반환합니다.

예측 처리 흐름:

1. 클라이언트가 음식 이미지를 업로드
2. FastAPI가 업로드 파일을 수신
3. PIL을 이용해 이미지를 RGB 형식으로 변환
4. 이미지를 224x224 크기로 조정
5. ResNet 전처리 함수를 적용
6. Keras 모델로 101개 클래스 확률 예측
7. confidence가 높은 상위 3개 라벨을 JSON으로 반환

## Main Features

### Food Image Prediction

`POST /predict` 엔드포인트는 음식 이미지 파일을 입력받아 Top-3 예측 결과를 반환합니다. 응답은 프론트엔드에서 바로 사용할 수 있도록 라벨과 confidence 값으로 구성했습니다.

응답 구조:

```json
{
  "top3": [
    {"label": "bibimbap", "confidence": 0.82},
    {"label": "fried_rice", "confidence": 0.07},
    {"label": "sushi", "confidence": 0.03}
  ]
}
```

### Model Health Check

`GET /predict/health` 엔드포인트는 모델 파일 존재 여부, 라벨 개수, 모델 로딩 상태를 확인합니다.  
모델 파일이 없는 경우에도 서버가 시작되도록 모델 로딩을 첫 예측 시점으로 지연했고, 모델 준비 상태는 health API에서 확인할 수 있게 했습니다.

이 구조는 배포 환경에서 모델 파일 누락이나 경로 오류를 빠르게 확인할 수 있도록 하기 위한 안정성 보완입니다.

### User and Post API

프로젝트에는 예측 기능 외에도 회원 및 게시글 CRUD API가 포함되어 있습니다. 이는 음식 예측 기능을 단독 API로만 두지 않고, 기본적인 웹 애플리케이션 구조 안에서 사용할 수 있도록 구성하기 위한 기능입니다.

- `/user`: 회원 생성, 로그인, 조회, 수정, 삭제
- `/post`: 게시글 생성, 조회, 수정, 삭제

## Technical Stack

| 영역 | 기술 |
|---|---|
| Backend Framework | FastAPI |
| Model Inference | TensorFlow / Keras |
| Image Processing | Pillow, NumPy |
| Database | SQLite 기본 구성, SQLAlchemy ORM |
| API Documentation | FastAPI Swagger UI |
| Frontend Integration | React + Axios 연동 |
| Model Format | Keras `.h5` |

## Project Structure

```text
KTB_FastAPI/
  controller/
    predict_controller.py   # 이미지 예측 서비스 로직
    user_controller.py      # 회원 API 로직
    post_controller.py      # 게시글 API 로직
  model/
    food_model.py           # Keras 모델 로딩 및 Top-3 예측
    user_model.py           # 회원 DB 모델
    post_model.py           # 게시글 DB 모델
  router/
    predict_router.py       # 예측 API 라우터
    user_router.py          # 회원 API 라우터
    post_router.py          # 게시글 API 라우터
  utils/
    preprocess.py           # 이미지 리사이즈 및 ResNet 전처리
  label.labels.txt          # Food-101 클래스 라벨 101개
  config.py                 # 환경변수 기반 설정
  db.py                     # SQLAlchemy DB 연결
  main.py                   # FastAPI 앱 엔트리포인트
```

## Implementation Decisions

### Lazy Model Loading

초기 코드에서는 서버 import 시점에 모델을 바로 로딩하는 구조였기 때문에, 모델 파일이 없으면 API 서버 자체가 실행되지 않는 문제가 있었습니다. 이를 개선해 모델을 첫 예측 요청 시점에 로딩하도록 변경했습니다.

이 방식의 장점:

- 모델 파일이 없어도 서버와 API 문서 확인 가능
- 모델 경로 오류를 `/predict/health`로 확인 가능
- 배포 환경에서 서버 시작 실패 원인을 줄일 수 있음

### Environment-Based Configuration

로컬 개발에서는 SQLite를 기본 DB로 사용하고, 배포 환경에서는 환경변수로 DB URL과 모델 경로를 바꿀 수 있도록 구성했습니다.

설정 항목:

- `DATABASE_URL`: 데이터베이스 연결 주소
- `MODEL_PATH`: 학습된 `.h5` 모델 파일 경로

### Image Validation and Error Handling

이미지가 아닌 파일이 업로드되면 `400` 응답을 반환하고, TensorFlow 또는 모델 파일이 준비되지 않은 경우에는 `503` 응답을 반환하도록 처리했습니다.  
이를 통해 프론트엔드가 실패 원인을 구분해서 사용자에게 안내할 수 있는 기반을 마련했습니다.

## What This Project Shows

이 프로젝트는 다음 역량을 보여주기 위해 구성했습니다.

- CNN 기반 이미지 분류 문제를 이해하고 모델을 선택하는 과정
- 사전 학습 모델을 Fine-Tuning하여 도메인 데이터셋에 맞게 개선하는 과정
- 실험 결과를 바탕으로 모델 선택 근거를 정리하는 능력
- 학습된 모델을 FastAPI API로 연결하는 백엔드 구현 능력
- 이미지 업로드, 전처리, 추론, JSON 응답으로 이어지는 서비스 흐름 구현
- 모델 파일 누락, 잘못된 이미지 입력 등 실패 상황을 고려한 API 안정성 개선

## Current Limitations

현재 프로젝트는 부트캠프 개인 프로젝트 및 포트폴리오 제출을 위한 MVP 수준입니다. 운영 서비스 수준으로 확장하려면 다음 보완이 필요합니다.

- 모델 파일을 외부 저장소에서 자동으로 가져오는 배포 스크립트
- Dockerfile 및 docker-compose 구성
- 회원 비밀번호 해싱
- CORS 허용 도메인 제한
- 업로드 파일 크기 제한
- 실제 테스트 이미지셋 기반 Top-1/Top-3 Accuracy 재검증
- 모델 warm-up 및 추론 latency 측정
- API 테스트 코드 추가

## Summary

본 백엔드는 Food-101 CNN Fine-Tuning 프로젝트의 모델 배포 파트를 담당합니다.  
모델 학습 실험에서 도출한 ResNet50 기반 Fine-Tuning 모델을 FastAPI 예측 API로 연결했고, React 프론트엔드에서 업로드한 이미지를 백엔드가 전처리하여 Top-3 음식 분류 결과로 반환하는 구조를 구현했습니다.

이 프로젝트의 핵심은 “모델 학습 결과를 실제 서비스 API로 연결했다”는 점입니다.
