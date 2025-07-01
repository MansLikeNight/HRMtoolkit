from django.shortcuts import render, redirect
from .models import LeaveRequest
from .forms import LeaveRequestForm

def leave_list(request):
    leaves = LeaveRequest.objects.all()
    return render(request, 'leave/leave_list.html', {'leaves': leaves})

def leave_create(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('leave-list')
    else:
        form = LeaveRequestForm()
    return render(request, 'leave/leave_form.html', {'form': form})
