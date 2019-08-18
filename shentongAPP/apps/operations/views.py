from django.shortcuts import render
from django.views.generic import View
from .models import CourseInfo


class OrgView(View):
    def get(self, request):
        """
        课程机构列表功能
        :param request:
        :return:
        """
        return render(request, 'org-list.html', {})
