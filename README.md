# TAFS(Trauma-stimulating Accident video Filtering Service) 

### 1. 개발 배경
 숏폼 미디어의 스크롤과 자동 재생은 사용자를 예기치 않은 자극적인 콘텐츠에 노출시킬 수 있으며, 특히 사고 영상은 기존 필터링에서 제외되는 경우가 많다. 이를 해결하기 위해, 사용자가 사고 카테고리를 선택하고 분류 모델로 영상을 필터링하는 응용 프로그램을 개발했다.

### 2. 전체 구성
 이 프로젝트는 영상 분류 모델, 데이터베이스, 응용 프로그램 세 부분으로 구성된다. 영상 분류 모델은 새롭게 개발한 화재, 침수, 폭행 분류 모델과 선행 연구에서 가져온 교통사고 분류 모델로 구성된다. 데이터베이스는 서버와 연동되어 사고 장면이 포함된 Youtube shorts 영상 데이터를 관리한다. 응용 프로그램은 데모 프로그램과 확장 프로그램으로 나뉘며, 사용자가 선택한 카테고리에 따라 영상을 필터링하고 경고 창으로 사고 카테고리 포함 여부를 알린다.

### 3. 구현 환경
 개발은 Windows 10, 11 및 Kali Linux 가상 머신 환경에서 진행되었다. 분류 모델은 Colab 환경에서 Python을 사용하여 개발했으며, 확장 프로그램은 JSON, JavaScript, HTML, PHP를 활용하여 만들어졌다. 데모 프로그램 역시 Python을 사용하여 개발되었다.

 ### 4. 구현 결과
 현재 본 프로젝트에서는 5개의 카테고리 중 군중 밀집, 교통사고를 제외하고 화재, 침수, 폭행 분류 모델의 개발을 완료했다. 화재와 침수 분류 모델의 성능은 기존 모델과 비교하여 정확도, 오차 행렬, 정밀도/재현율, AUC 스코어를 종합적으로 평가한 결과, 본 프로젝트에서 개발된 모델이 기존 모델보다 우수한 성능을 나타내고 있다.
 이러한 개발된 분류 모델들을 활용하여, 모델 예측 및 데이터베이스 입출력 기능을 시연하는 데모 프로그램과 사용자 인터페이스 데모 버전인 확장 프로그램을 개발했다.

# Service Arcitecture
![image](https://github.com/rkdming/TAFS/assets/70503864/2640b154-0e98-43e9-a0f6-6f3e4d8c7e05)

 #### 응용 프로그램 시연 영상
https://youtube.com/playlist?list=PLhz68fYXiMWOvUYPJP4YXXShzpJW_sA5_&si=i7kBLD961hu4EtkO

---
 ### 오픈 소스
|구분|URL|
|---|---|
|화재 분류 모델 구조|https://www.kaggle.com/code/agnishwarbagchi/fire-detection|
|폭행 Open Pose|https://github.com/CMU-Perceptual-Computing-Lab/openpose|
|교통 사고 모델|https://www.kaggle.com/code/fahaddalwai/cnn-accident-detection-91-accuracy|
|확장 프로그램|https://github.com/drodil/youtube_auto_pause|
---
### 데이터셋
<table>
    <thead>
        <tr>
            <th>구분</th>
            <th>URL</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan=6>화재</td>
            <td>https://www.kaggle.com/datasets/phylake1337/fire-dataset</td>
        </tr>
        <tr><td>https://www.kaggle.com/datasets/atulyakumar98/test-dataset</td></tr>
        <tr><td>https://www.kaggle.com/datasets/mikhailma/house-rooms-streets-image-dataset</td></tr>
        <tr><td>https://universe.roboflow.com/lee-escpi/candle-8bocu/dataset/1</td></tr>
        <tr><td>https://universe.roboflow.com/gabrielainteli/fire_detection-ihaqe</td></tr>
        <tr><td>https://universe.roboflow.com/1009727588-qq-com/sun-nxvfz</td></tr>
        <tr>
          <td rowspan=7>침수</td>
          <td>https://universe.roboflow.com/ko-dongyeon/car-flooding/dataset/11/download/yolov8</td>
        </tr>
        <tr><td>https://universe.roboflow.com/weatherdetection/snowy-weather/dataset/1</td></tr>
        <tr><td>https://universe.roboflow.com/ai-msji4/flood-b5y9q</td></tr>
        <tr><td>https://www.kaggle.com/datasets/arnaud58/landscape-pictures</td></tr>
        <tr><td>https://universe.roboflow.com/ko-dongyeon/car-flooding/dataset/11/download/yolov8</td></tr>
        <tr><td>https://universe.roboflow.com/flooding24/flooding24/dataset/7</td></tr>
        <tr><td>https://www.kaggle.com/datasets/clorichel/boat-types-recognition</td></tr>
        <tr>
          <td rowspan=3>군중 밀집</td>
          <td>http://www.crowd-counting.com/</td>
        </tr>
        <tr><td>https://www.kaggle.com/datasets/tthien/shanghaitech-with-people-density-map</td></tr>
        <tr><td>https://www.crcv.ucf.edu/data/ucf-cc-50/</td></tr>
        <tr>
          <td rowspan=2>폭행</td>
          <td>https://www.kaggle.com/datasets/mohamedmustafa/real-life-violence-situations-dataset</td>
        </tr>
        <tr><td>https://www.kaggle.com/datasets/karandeep98/real-life-violence-and-nonviolence-data/</td></tr>
        <tr>
          <td>교통 사고</td>
          <td>https://www.kaggle.com/datasets/ckay16/accident-detection-from-cctv-footage/code?datasetId=804753&sortBy=voteCount</td>
        </tr>
    </tbody>
</table>

---
### 참고문헌
Human skeletons and change detection for efficient violence detection in surveillance videos
https://www.sciencedirect.com/science/article/pii/S1077314223001194
