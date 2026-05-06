# HTML 테이블 → CSV 변환 규칙
## 입력
- `./target/{학과이름}/html` 하위의 `.html` 파일
## 출력
- 구분자: `|` (파이프)
- 헤더: `학과이름|과목이름|ABEEK 영역|과목 영역|설계학점`
  - 헤더의 '학과이름'은 "학과이름" 텍스트를 그대로 작성한다. 폴더의 이름을 사용하지 않는다.
- 출력 위치: `./target/{학과이름}/csv/{파일이름}.csv`
  - 각 html 파일에 대해 ./target/{학과이름}/csv/{파일이름}.csv 형태로 저장한다.
  - 모든 .csv 파일을 하나의 파일에 합치지 말고, 각각의 .html 파일에 대해 .csv 파일을 생성해야 한다.

## 추출 대상 열
각 `<tr>`에서 아래 4개 열만 추출한다 (학년/학기 열은 무시):
1. **교과구분** (3번째 `<td>`)
2. **인증구분** (4번째 `<td>`)
3. **교과목명** (5번째 `<td>`)
4. **학점(설계)** (6번째 `<td>`)
> `rowspan`이 적용된 학년/학기 `<td>`는 후속 행에서 생략되므로,
> 각 행의 첫 번째 `<td>`가 교과구분인지 학년/학기인지 판별해야 한다.

## 무시할 행
- 헤더 행 (학년, 학기, 교과구분, ...)
- 소계 행 (`colspan` 속성이 있거나 텍스트가 "소계"인 행)
- 빈 행 (모든 `<td>`가 `&nbsp;` 또는 빈 값인 행)

## 텍스트 정제
- HTML 태그(`<p>`, `<br>` 등)를 제거하고 순수 텍스트만 추출
- `&nbsp;` 제거
- 앞뒤 공백 trim

### ABEEK 영역 (교과구분 → 변환)
| 원본     | 변환 값  |
| -------- | -------- |
| 전필     | 전공     |
| 전선     | 전공     |
| MSC      | MSC      |
| BSM      | BSM      |
| 전문교양 | 전문교양 |
> 단 교과목명에 "설계"가 포함된 경우, ABEEK 영역을 "설계"로 변환한다.

### 과목 영역 (인증구분 → 변환)
| 원본 | 변환 값 |
| ---- | ------- |
| 인필 | 필수    |
| 인선 | 선택    |

### 설계학점
- `(숫자)`: 괄호 안의 숫자를 그대로 사용
- `없음`: 0

### 변환 전
```html
<tr style="user-select: auto !important;">
    <td rowspan="14" style="user-select: auto !important;">1</td>
    <td rowspan="7" style="user-select: auto !important;">1</td>
    <td style="user-select: auto !important;">전문교양</td>
    <td style="user-select: auto !important;">인필</td>
    <td style="user-select: auto !important;">문제해결을 위한 글쓰기와 발표</td>
    <td style="user-select: auto !important;">3</td>
</tr>
<tr style="user-select: auto !important;">
        <td style="user-select: auto !important;">전선</td>
        <td style="user-select: auto !important;">인선</td>
        <td style="user-select: auto !important;">메카트로닉스응용설계</td>
        <td style="user-select: auto !important;">3(1)</td>
    </tr>
```
### 변환 후
```csv
학과이름|과목이름|ABEEK 영역|과목 영역|설계학점
항공우주공학과|문제해결을 위한 글쓰기와 발표|전문교양|필수|0
항공우주공학과|메카트로닉스응용설계|전공|선택|1
```