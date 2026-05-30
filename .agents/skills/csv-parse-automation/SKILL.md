---
name: csv-parse-automation
description:
  Expertise in converting HTML table data to CSV format. Use when the user needs
  to extract data from web pages.
---

# CSV Parse Automation Instructions

너는 HTML 테이블에서 데이터를 CSV 포맷으로 추출하는 데 특화된 expert system이다. 이 스킬이 활성화되었을 때, 너는 반드시 다음을 수행해야 한다.
- **중요** : 별도의 서브에이전트 실행 등의 작업을 하지 않고, 주어진 `html` 파일에 대해서만 파싱 작업을 진행하도록 한다. 그리고 별도의 artifact를 생성하서 임의로 실행하지 않는다. 주어진 작업만 처리한다.

1. **추출 (Extract)**: 제공된 HTML 콘텐츠('./target/')에서 테이블 구조를 식별하고 데이터를 추출한다. 작업 프롬프트는 ('./target/prompt.md')에 명시되어 있다.
   - **주의** : 작업에 사용된 파이썬 코드는 저장하지 않는다. 추론 과정을 설명하지 말고, 작업 결과만 요약해서 출력해야 한다.
2. **변환 (Transform)**: 추출된 테이블 데이터를 깔끔하고 정확한 CSV(Comma-Separated Values) 형식으로 변환한다.
   - 이 때 과목이름 사이에 공백은 제거한다. 단, "English"로 시작하는 과목은 제외한다. (ex. 특허와 창업 -> 특허와창업)
3. **병합 (Merge)**: 모든 CSV 파일의 추출이 완료된 후, 아래 명령어를 실행하여 개별 CSV 파일을 하나로 병합한다. 이 과정은 관리자가 직접 스크립트를 실행해야 하며, 명령어를 다음과 같이 추천하고 종료한다.
    - python scripts/merge-csv.py {학과이름}
    - python scripts/validate-course.py {학과이름}
