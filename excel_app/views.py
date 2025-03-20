from django.shortcuts import render
import pandas as pd
from .forms import ExcelUploadForm
from .models import ExcelFile

def upload_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'upload_success.html')
    else:
        form = ExcelUploadForm()
    return render(request, 'upload.html', {'form': form})

def view_data(request):
    latest_file = ExcelFile.objects.last()
    if latest_file:
        df = pd.read_excel(latest_file.file.path)
        # 简单统计示例
        stats = {
            'row_count': len(df),
            'columns': list(df.columns),
            'describe': df.describe().to_html(),
            'head': df.head().to_html()
        }
        return render(request, 'view_data.html', {'stats': stats})
    return render(request, 'view_data.html')
