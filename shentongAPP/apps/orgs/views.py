from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q
from .models import CityInfo, OrgInfo, TeacherInfo
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserAskForm
from django.http import HttpResponse
from operations.models import UserLove
from courses.models import CourseInfo


class AddLoveView(View):
    """
    用户收藏 对应js在org_base里面
    """
    def post(self, request):
        love_id = request.POST.get('love_id', 0)
        love_type = request.POST.get('love_type', 0)
        if not request.user.is_authenticated:
            # 判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        exist_records = UserLove.objects.filter(user=request.user, love_id=int(love_id), love_type=int(love_type))
        if exist_records:
            # 如果记录已存在，则表示取消收藏
            exist_records.delete()

            # 取消收藏，则收藏数 -1
            if int(love_type) == 1:
                course_org = OrgInfo.objects.get(id=int(love_id))
                course_org.love_num -= 1
                if course_org.love_num < 0:
                    course_org.love_num = 0
                course_org.save()
            elif int(love_type) == 2:
                course = CourseInfo.objects.get(id=int(love_id))
                course.love_num -= 1
                if course.love_num < 0:
                    course.love_num = 0
                course.save()
            elif int(love_type) == 3:
                teacher = TeacherInfo.objects.get(id=int(love_id))
                teacher.love_num -= 1
                if teacher.love_num < 0:
                    teacher.love_num = 0
                teacher.save()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            user_love = UserLove()
            if int(love_id) > 0 and int(love_type) > 0:
                user_love.user = request.user
                user_love.love_id = int(love_id)
                user_love.love_type = int(love_type)
                user_love.save()

                # 点击收藏，相应收藏数 +1
                if int(love_type) == 1:
                    course_org = OrgInfo.objects.get(id=int(love_id))
                    course_org.love_num += 1
                    course_org.save()
                elif int(love_type) == 2:
                    course = CourseInfo.objects.get(id=int(love_id))
                    course.love_num += 1
                    course.save()
                elif int(love_type) == 3:
                    teacher = TeacherInfo.objects.get(id=int(love_id))
                    teacher.love_num += 1
                    teacher.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


class OrgHomeView(View):
    """
    机构首页
    """
    def get(self, request, org_id):
        current_page = "home"
        course_org = OrgInfo.objects.get(id=int(org_id))
        course_org.click_num += 1
        course_org.save()
        have_love = False
        if request.user.is_authenticated:  # 判断用户登录状态，接着判断用户的收藏状态
            if UserLove.objects.filter(user=request.user, love_id=course_org.id, love_type=1):
                have_love = True
        all_courses = course_org.courseinfo_set.all()[:3]
        all_teachers = course_org.teacherinfo_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'have_love': have_love,
        })


class OrgCourseView(View):
    """
    机构课程列表页
    """
    def get(self, request, org_id):
        current_page = "course"
        course_org = OrgInfo.objects.get(id=int(org_id))
        have_love = False
        if request.user.is_authenticated:  # 判断用户登录状态，接着判断用户的收藏状态
            if UserLove.objects.filter(user=request.user, love_id=course_org.id, love_type=1):
                have_love = True
        all_courses = course_org.courseinfo_set.all()
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
            'have_love': have_love,
        })


class OrgDescView(View):
    """
    机构介绍页
    """
    def get(self, request, org_id):
        current_page = "desc"
        course_org = OrgInfo.objects.get(id=int(org_id))
        have_love = False
        if request.user.is_authenticated:  # 判断用户登录状态，接着判断用户的收藏状态
            if UserLove.objects.filter(user=request.user, love_id=course_org.id, love_type=1):
                have_love = True
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'have_love': have_love,
        })


class OrgTeacherView(View):
    """
    机构讲师
    """
    def get(self, request, org_id):
        current_page = "teacher"
        course_org = OrgInfo.objects.get(id=int(org_id))
        have_love = False
        if request.user.is_authenticated:  # 判断用户登录状态，接着判断用户的收藏状态
            if UserLove.objects.filter(user=request.user, love_id=course_org.id, love_type=1):
                have_love = True
        all_teachers = course_org.teacherinfo_set.all()
        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'have_love': have_love,
        })


class AddUserAskView(View):
    """
    用户添加咨询
    """
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse("{'status':'success'}", content_type='application/json')
        else:
            return HttpResponse("{'status':'fail', 'msg':'添加出错'}",
                                content_type='application/json')


class OrgView(View):
    def get(self, request):
        """
        课程机构列表功能
        :param request:
        :return:
        """
        all_orgs = OrgInfo.objects.all()  # 所有课程机构
        hot_orgs = all_orgs.order_by("click_num")[:3]
        all_cities = CityInfo.objects.all()  # 所有城市

        # 关键词搜索 机构
        search_keywords = request.GET.get('keyword', "")
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))

        cityinfo_id = request.GET.get('city', "")  # 筛选城市
        if cityinfo_id:
            all_orgs = all_orgs.filter(cityinfo_id=int(cityinfo_id))

        category = request.GET.get('ct', "")  # 机构类别筛选
        if category:
            all_orgs = all_orgs.filter(category=category)

        sort = request.GET.get('sort', "")  # 机构类别筛选
        if sort:
            if sort == "study_num":
                all_orgs = all_orgs.order_by("-study_num")
            elif sort == "course_num":
                all_orgs = all_orgs.order_by("-course_num")

        org_nums = all_orgs.count()  # 过早统计会无法统计筛选出来的数目，而是总数

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        P = Paginator(all_orgs, 6, request=request)
        orgs = P.page(page)
        return render(request, 'org-list.html', {"all_orgs": orgs,
                                                 "org_nums": org_nums,
                                                 "all_cities": all_cities,
                                                 "cityinfo_id": cityinfo_id,
                                                 "category": category,
                                                 "hot_orgs": hot_orgs,
                                                 "sort": sort,
                                                 })


class TeacherListView(View):
    """
    课程讲师列表页
    """
    def get(self, request):
        all_teacher = TeacherInfo.objects.all()

        # 根据人气讲师排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "hot":
                all_teacher = all_teacher.order_by("-click_num")

        # 排行榜
        sorted_teacher = TeacherInfo.objects.all().order_by("-click_num")[:3]

        # 关键词搜索 讲师
        search_keywords = request.GET.get('keyword', "")
        if search_keywords:
            all_teacher = all_teacher.filter(Q(name__icontains=search_keywords) | Q(work_position__icontains=search_keywords) |
                                             Q(work_company__icontains=search_keywords))

        # 对讲师进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        P = Paginator(all_teacher, 4, request=request)
        teachers = P.page(page)

        return render(request, 'teachers-list.html', {
            'all_teacher': teachers,
            'sorted_teacher': sorted_teacher,
            'sort': sort,
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = TeacherInfo.objects.get(id=int(teacher_id))
        teacher.click_num += 1
        teacher.save()
        all_courses = CourseInfo.objects.filter(teacherinfo=teacher)

        # 判断收藏状态
        have_teacher_love = False
        if UserLove.objects.filter(user=request.user, love_id=teacher.id, love_type=3):
            have_teacher_love = True
        have_org_love = False
        if UserLove.objects.filter(user=request.user, love_id=teacher.work_company.id, love_type=1):
            have_org_love = True

        # 排行榜
        sorted_teacher = TeacherInfo.objects.all().order_by("-click_num")[:3]
        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'all_courses': all_courses,
            'sorted_teacher': sorted_teacher,
            'have_teacher_love': have_teacher_love,
            'have_org_love': have_org_love,
        })
