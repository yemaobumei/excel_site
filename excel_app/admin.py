from django.contrib import admin
from .models import Student, Assignment, Score

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # 列表页显示配置
    list_display = ('student_id', 'name',)
    # 搜索字段配置
    search_fields = ('student_id', 'name')
    # 每页显示数量
    list_per_page = 20
    # 默认排序方式
    ordering = ('student_id',)
    # 快速编辑字段
    list_editable = ('name',)

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at',)
    search_fields = ('title',)
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'
    # 字段显示顺序（详情页）
    fields = ('title', 'created_at',)
    readonly_fields = ('created_at',)

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    # 列表页显示配置
    list_display = ('student_info', 'assignment_info', 'score', 'grade', 'updated_at')
    # 侧边过滤器配置
    list_filter = ('assignment__title', 'grade')
    # 搜索配置
    search_fields = ('student__name', 'student__student_id')
    # 每页显示数量
    list_per_page = 30
    # 直接编辑字段
    list_editable = ('score', 'grade')
    # 优化外键显示
    raw_id_fields = ('student', 'assignment')
    # 日期导航
    date_hierarchy = 'updated_at'

    def student_info(self, obj):
        return f"{obj.student.name} ({obj.student.student_id})"
    student_info.short_description = '学生信息'

    def assignment_info(self, obj):
        return f"{obj.assignment.title} ({obj.assignment.created_at.year})"
    assignment_info.short_description = '作业信息'

    # 自定义字段显示顺序（详情页）
    fieldsets = (
        ('基本信息', {
            'fields': ('student', 'assignment')
        }),
        ('成绩信息', {
            'fields': ('score', 'grade'),
            'classes': ('wide',)
        }),
        ('时间信息', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        })
    )