#텍스트 파일 엑셀로 변환할때 사용
import pandas as pd
import os
import shutil

input_dir = "인풋 데이터"
output_dir = "아웃풋 데이터"


txt_files = [f for f in os.listdir(input_dir) if f.endswith(".txt")]


for txt_file in txt_files:
    input_path = os.path.join(input_dir, txt_file)
    
    excel_file_name = txt_file.replace(".txt", ".xlsx")
    output_path = os.path.join(output_dir, excel_file_name)

    df = pd.read_csv(input_path, delimiter="\t", dtype=str)


    df.to_excel(output_path, index=False)

    print(f"변환 완료: {txt_file} → {excel_file_name}")

print(f"\n모든 파일이 '{output_dir}' 폴더로 이동 완료!")
