import pandas as pd
import sys
import os

def load_master_course_names(master_csv_path: str) -> set[str]:
    """마스터 CSV에서 과목명 목록을 로드하고 공백 제거 후 set으로 반환."""
    master_df = pd.read_csv(master_csv_path)
    return set(master_df['name'].str.replace(' ', '', regex=False).str.strip())


def load_department_course_names(dept_csv_path: str) -> list[str]:
    """학과 CSV에서 과목명 목록을 로드."""
    dept_df = pd.read_csv(dept_csv_path, sep='|')
    return dept_df['과목이름'].dropna().unique().tolist()


def normalize(name: str) -> str:
    """과목명 정규화: 공백 제거."""
    return name.replace(' ', '').strip()


def validate(dept_course_names: list[str], master_course_names: set[str]) -> list[str]:
    """학과 과목명 중 마스터에 없는 과목명 리스트를 반환."""
    mismatched = []
    for name in dept_course_names:
        if normalize(name) not in master_course_names:
            mismatched.append(name)
    return mismatched


def main():
    # ── 인자 검증 ──
    if len(sys.argv) < 2:
        print("Error: department_name argument is required.")
        print("Usage: python scripts/validate-course.py {학과이름} [--strict]")
        sys.exit(1)

    department_name = sys.argv[1]

    # ── 경로 설정 ──
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)

    master_csv_path = os.path.join(script_dir, 'csv', 'all_course_v1.csv')
    dept_csv_dir = os.path.join(
        base_dir, '.agents/skills/csv-parse-automation/target', department_name, 'csv'
    )
    dept_csv_path = os.path.join(dept_csv_dir, f'{department_name}.csv')

    # ── 파일 존재 확인 ──
    if not os.path.isfile(master_csv_path):
        print(f"Error: Master CSV not found: {master_csv_path}")
        sys.exit(1)

    if not os.path.isfile(dept_csv_path):
        print(f"Error: Department CSV not found: {dept_csv_path}")
        print(f"  → merge-csv.py를 먼저 실행하여 병합 CSV를 생성하세요.")
        sys.exit(1)

    # ── 검증 실행 ──
    master_names = load_master_course_names(master_csv_path)
    created_course_names = load_department_course_names(dept_csv_path)
    mismatched = validate(created_course_names, master_names)

    # ── 결과 출력 ──
    print(f"=== 과목명 검증 결과: {department_name} ===")
    print(f"  생성한 과목 수: {len(created_course_names)}")
    print(f"  마스터 과목 수: {len(master_names)}")
    print()

    if not mismatched:
        print("✅ 모든 과목이 마스터 데이터와 일치합니다.")
        sys.exit(0)
    else:
        print(f"❌ 불일치 과목 {len(mismatched)}건:")
        print("-" * 50)
        for i, name in enumerate(mismatched, 1):
            print(f"  {i:3d}. {name}")
        print("-" * 50)
        print()
        print("위 과목들이 all_course_v1.csv에 존재하지 않습니다.")
        print("과목명 오타 또는 마스터 데이터 누락 여부를 확인하세요.")


if __name__ == '__main__':
    main()
