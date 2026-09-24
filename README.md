# 나의 수어 공부방 (sueo-study)

한국수어 기초 학습 웹앱. 휴대폰번호만으로 가입하고 바로 사용합니다.

- 기초: 주제별 단어장(진도 체크·메모), 지문자·지숫자, 카드 복습, 기초 문장, 학습 일지
- 중급: 기초 진도 70% 달성 시 열림 (내용 추가 예정)
- 수형 그림·수형 설명: 국립국어원 한국수어사전 (CC BY-NC-ND 2.0 KR, 비영리·원본 그대로 사용) — `signs.js`
- 수어 동작 영상: 단어별 국립국어원 한국수어사전 상세 페이지 링크
- 저장: Firebase `jeahwan-apps` Firestore, 컬렉션 `sueo-study` (문서 ID = 휴대폰번호)

## 단어 추가
`index.html`의 단어 목록을 바꾼 뒤 `tools/collect_signs.py`로 사전 번호·그림·설명을 다시 모아 `signs.js`를 갱신합니다.

## 설정
1. `index.html`의 `window.FIREBASE_CONFIG`에 웹 설정값 입력
2. `firestore.rules.txt`의 블록을 Firestore 규칙에 추가
3. Settings > Pages > Deploy from a branch > `main` / `(root)`
