from django.shortcuts import render, redirect
from .models import Document
from .forms import DocumentForm

def document_list(request):
    print("✅ views.py is loaded")  # Add at the top of views.py
    documents = Document.objects.all()
    return render(request, 'documents/document_list.html', {'documents': documents})

def document_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('document-list')
    else:
        form = DocumentForm()
    return render(request, 'documents/document_upload.html', {'form': form})
