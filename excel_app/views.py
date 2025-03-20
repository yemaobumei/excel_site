from django.db.models import Prefetch
from django.shortcuts import render, redirect
from django.contrib import messages
import pandas as pd
from django.views.decorators.csrf import csrf_protect

from .forms import ExcelUploadForm
from .models import ExcelFile, Student, Assignment, Score




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
        start_row = 1
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
                    else:
                        Score.objects.update_or_create(
                            student=student,
                            assignment=assignments[col],
                            defaults={'score': score_value}
                        )

@csrf_protect
def upload_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # 保存上传文件记录
                excel_file = form.save()

                # 调用数据处理函数
                result = handle_uploaded_excel(excel_file.file.path)

                # 添加处理结果到消息
                messages.success(request,
                                 f"成功导入{result['students']}名学生数据，"
                                 f"包含{result['assignments']}个作业，"
                                 f"共{result['scores']}条成绩记录")

                return redirect('view_data')

            except Exception as e:
                # 删除无效文件记录
                excel_file.delete()
                messages.error(request, f"文件处理失败: {str(e)}")
                return render(request, 'upload.html', {'form': form})

    else:
        form = ExcelUploadForm()

    return render(request, 'upload.html', {'form': form})


def view_data(request):
    assignments = Assignment.objects.all().order_by('created_at')
    students = Student.objects.prefetch_related(
        Prefetch('scores', queryset=Score.objects.select_related('assignment'))
    ).all().order_by('student_id')

    students_data = []
    for student in students:
        grades = [s.grade for s in student.scores.all() if s.grade]
        total = len(grades) or 1  # 避免除零

        # 统计各等级数量
        grade_count = {
            'A': grades.count('A'),
            'B': grades.count('B'),
            'C': grades.count('C'),
            'D': grades.count('D'),
            'F': grades.count('F')
        }

        students_data.append({
            'student': student,
            'grades': grade_count,
            'total': total
        })

    return render(request, 'view_data.html', {
        'assignments': assignments,
        'students_data': students_data
    })

def view_data(request):
    assignments = Assignment.objects.all().order_by('created_at')
    students = Student.objects.prefetch_related(
        Prefetch('scores', queryset=Score.objects.select_related('assignment'))
    ).all().order_by('student_id')

    students_data = []
    for student in students:
        # 直接读取grade字段值
        grades_dict = {
            score.assignment_id: score.grade
            for score in student.scores.all()
        }
        students_data.append({
            'student': student,
            'grades': grades_dict
        })
    # print("作业ID列表:", [a.id for a in assignments])
    # print("第一个学生的成绩映射:", students_data[0]['grades'])

    return render(request, 'view_data.html', {
        'assignments': assignments,
        'students_data': students_data
    })
def view_data_st(request):
    assignments = Assignment.objects.all().order_by('created_at')
    students = Student.objects.prefetch_related(
        Prefetch('scores', queryset=Score.objects.select_related('assignment'))
    ).all().order_by('student_id')

    students_data = []
    for student in students:
        grades = [s.grade for s in student.scores.all() if s.grade]
        total = len(grades) or 1  # 避免除零

        # 统计各等级数量
        grade_count = {
            'A': grades.count('A'),
            'B': grades.count('B'),
            'C': grades.count('C'),
            'D': grades.count('D'),
            'F': grades.count('未交')+grades.count('未标记')
        }

        students_data.append({
            'student': student,
            'grades': grade_count,
            'total': total
        })

    return render(request, 'view_data_st.html', {
        'assignments': assignments,
        'students_data': students_data
    })