import pandas as pd
import glob
import sys
import os

# 인자 검증
if len(sys.argv) < 2:
    print("Error: department_name argument is required.")
    print("Usage: python scripts/merge-csv.py {학과이름}")
    sys.exit(1)

department_name = sys.argv[1]

# 경로 설정: 스크립트 파일 위치를 기준으로 target 디렉토리 찾기
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(script_dir)
csv_dir = os.path.join(base_dir, '.agents/skills/csv-parse-automation/target', department_name, 'csv')

if not os.path.isdir(csv_dir):
    print(f"Error: Directory not found: {csv_dir}")
    sys.exit(1)

# csv 파일 리스트 불러오기 (병합 결과 파일은 제외)
merged_filename = f'{department_name}.csv'
csv_file_list = [
    f for f in glob.glob(f'{csv_dir}/*.csv')
    if os.path.basename(f) != merged_filename
]

if len(csv_file_list) == 0:
    print(f"Error: No CSV files found in {csv_dir}")
    sys.exit(1)

print(f"Found {len(csv_file_list)} CSV files to merge.")

# 병합
csv_list = [pd.read_csv(file, sep='|') for file in csv_file_list]
combined_df = pd.concat(csv_list, ignore_index=True)
unique_combined_df = combined_df.drop_duplicates(subset=['과목이름'])

# 정렬
custom_order = {
    'ABEEK 영역': ['전문교양', 'MSC', 'BSM', '전공', '설계'],
    '과목 영역': ['필수', '선택']
}
unique_combined_df['ABEEK 영역'] = pd.Categorical(unique_combined_df['ABEEK 영역'], categories=custom_order['ABEEK 영역'], ordered=True)
unique_combined_df['과목 영역'] = pd.Categorical(unique_combined_df['과목 영역'], categories=custom_order['과목 영역'], ordered=True)
sorted_df = unique_combined_df.sort_values(by=['ABEEK 영역', '과목 영역', '과목이름'])

# 저장
output_path = os.path.join(csv_dir, merged_filename)
sorted_df.to_csv(output_path, sep='|', index=False)

print(f"Merged CSV saved to: {output_path}")
print(f"Total rows: {len(sorted_df)}")
