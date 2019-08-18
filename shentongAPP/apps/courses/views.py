from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from .models import CourseInfo, SourceInfo, VideoInfo
from django.db.models import Q
from pure_pagination import Paginator, PageNotAnInteger
from operations.models import UserLove, UserComment, UserCourse
# from django.contrib.auth.mixins import LoginRequiredMixin
from Utils.mixin_utils import LoginRequiredMixin


class CouseListView(View):
    """
    课程列表页
    """
    def get(self, request):
        all_courses = CourseInfo.objects.all().order_by("-add_time")  # -add_time前面的 - 代表降序排列
        hot_courses = CourseInfo.objects.all().order_by("-click_num")[:3]

        # 关键词搜索
        search_keywords = request.GET.get('keyword', "")
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) |
                                             Q(detail__icontains=search_keywords))

        sort = request.GET.get('sort', "")  # 课程排序
        if sort:
            if sort == "study_num":
                all_courses = all_courses.order_by("-study_num")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_num")

        # 对公开课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        P = Paginator(all_courses, 6, request=request)
        courses = P.page(page)
        return render(request, 'course-list.html', {
            'all_courses': courses,
            'sort': sort,
            'hot_courses': hot_courses,
        })


class CourseDetailView(View):
    """
    课程详情页
    """
    def get(self, request, course_id):
        course = CourseInfo.objects.get(id=int(course_id))

        # 增加课程点击数
        course.click_num += 1
        course.save()

        have_love_course = False
        have_love_org = False
        if request.user.is_authenticated:
            if UserLove.objects.filter(user=request.user, love_id=course.id, love_type=2):
                have_love_course = True
            if UserLove.objects.filter(user=request.user, love_id=course.orginfo.id, love_type=1):
                have_love_org = True

        tag = course.tag
        if tag:
            relate_courses = CourseInfo.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []
        return render(request, 'course-detail.html', {
            'course': course,
            'relate_courses': relate_courses,
            'have_love_course': have_love_course,
            'have_love_org': have_love_org,
        })


class CourseInfoView(LoginRequiredMixin, View):
    """
    课程章节信息
    """
    def get(self, request, course_id):
        course = CourseInfo.objects.get(id=int(course_id))
        course.study_num += 1
        course.save()

        # 查询用户是否关联了课程
        user_courses = UserCourse.objects.filter(user=request.user)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        # 学习该课程的同学还学过的课程
        user_courses = UserCourse.objects.filter(study_course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.study_course.id for user_course in all_user_courses]
        relate_courses = CourseInfo.objects.filter(id__in=course_ids).order_by("-click_num")[:3]

        course_resources = SourceInfo.objects.filter(courseinfo=course)
        return render(request, 'course-video.html', {
            'course': course,
            'course_resources': course_resources,
            'relate_courses': relate_courses,
        })


class CourseCommentView(LoginRequiredMixin, View):
    """
    课程评论
    """
    def get(self, request, course_id):
        course = CourseInfo.objects.get(id=int(course_id))

        course_resources = SourceInfo.objects.filter(courseinfo=course)
        course_comment = UserComment.objects.all()
        return render(request, 'course-comment.html', {
            'course': course,
            'course_resources': course_resources,
            'course_comment': course_comment,

        })


class AddcommentView(View):
    """
    添加评论
    """
    def post(self, request):

        if not request.user.is_authenticated:
            # 判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', "")
        if int(course_id) > 0 and comments:
            course_comment = UserComment()
            course = CourseInfo.objects.get(id=int(course_id))  # get()如果没有找到数据或找到多条数据会抛出异常，filter（）不会
            course_comment.course = course
            course_comment.comments = comments
            course_comment.user = request.user
            course_comment.save()
            return HttpResponse('{"status":"success", "msg":"评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"评论失败"}', content_type='application/json')


class VideoPlayView(View):
    """
    视频播放页面
    """
    def get(self, request, video_id):
        video = VideoInfo.objects.get(id=int(video_id))
        course = video.lessoninfo.courseinfo
        course.study_num += 1
        course.save()

        # 查询用户是否关联了课程
        user_courses = UserCourse.objects.filter(user=request.user)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        # 学习该课程的同学还学过的课程
        user_courses = UserCourse.objects.filter(study_course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.study_course.id for user_course in all_user_courses]
        relate_courses = CourseInfo.objects.filter(id__in=course_ids).order_by("-click_num")[:3]

        course_resources = SourceInfo.objects.filter(courseinfo=course)
        return render(request, 'course-play.html', {
            'course': course,
            'course_resources': course_resources,
            'relate_courses': relate_courses,
            'video': video,
        })
