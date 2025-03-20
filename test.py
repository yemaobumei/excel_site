from django.test import TestCase

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'excel_site.settings')
import django
django.setup()
import pandas as pd
from excel_app.models import ExcelFile, Student, Assignment, Score
def handle_uploaded_excel(file_path):
    """处理Excel文件并返回统计结果"""

    f = pd.ExcelFile(file_path)
    for sheet in f.sheet_names:
        print(sheet)
        df = pd.read_excel(file_path,sheet_name=sheet,skiprows=1, header=0)
        df.columns.values[0]="分组"
        df.columns.values[1]="学号"
        df.columns.values[2]="姓名"
        # 验证必要列存在
        required_columns = ['姓名', '学号']
        print(df.columns)
        if not all(col in df.columns for col in required_columns):
            raise ValueError("Excel缺少必要列：姓名、学号")

        # 获取作业列（排除前3列）
        assignment_cols = df.columns[3:]

        # 初始化计数器
        result = {
            'students': 0,
            'assignments': len(assignment_cols),
            'scores': 0
        }

        # 处理作业列表
        assignments = {}
        for col in assignment_cols:
            obj, created = Assignment.objects.get_or_create(title=col.strip())
            assignments[col] = obj

        # 处理学生数据
        start_row = 3
        for index, row in df.iterrows():
            if index < start_row:
                continue
            student, created = Student.objects.update_or_create(
                student_id=row['学号'],
                defaults={'name': row['姓名']}
            )
            if created:
                result['students'] += 1

            # 处理成绩
            for col in assignment_cols:
                score_value = row[col]
                print(row['学号'],row['姓名'],col,score_value)
                if pd.notnull(score_value):  # 跳过空值
                    if isinstance(score_value, str):
                        Score.objects.update_or_create(
                            student=student,
                            assignment=assignments[col],
                            defaults={'grade': score_value}
                        )
                        print(score_value)
                    else:
                        Score.objects.update_or_create(
                            student=student,
                            assignment=assignments[col],
                            defaults={'score': score_value}
                        )

handle_uploaded_excel("media/excel_files/1741582914011.xlsx")