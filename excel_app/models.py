from django.db import models

# Create your models here.

class ExcelFile(models.Model):
    file = models.FileField(upload_to='excel_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


from django.db import models


class Student(models.Model):
    """学生基本信息"""
    student_id = models.CharField(max_length=20, unique=True, verbose_name="学号")
    name = models.CharField(max_length=50, verbose_name="姓名")

    def __str__(self):
        return f"{self.name} ({self.student_id})"


class Assignment(models.Model):
    """作业元数据"""
    title = models.CharField(max_length=200, unique=True, verbose_name="作业标题")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.title


class Score(models.Model):
    """成绩记录"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="scores")
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="scores")
    score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="分数",null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")


    # 原有其他字段保持不变...
    grade = models.CharField(
        max_length=20,
        blank=True,
        default='',
        verbose_name="等级"
    )
    class Meta:
        unique_together = [['student', 'assignment']]  # 确保每个学生的每个作业只有一个记录

    def __str__(self):
        return f"{self.student} - {self.assignment}: {self.score}"