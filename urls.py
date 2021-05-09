from datetime import date, datetime
from views import *  # из модуля нужны все вьюхи
from fw.auth import login


# front controllers
def front_add_date(request):
    request['date'] = date.today()


def front_add_key(request):
    request['key'] = 'KEY'


def front_request_allowed(request):
    if login(request):
        request['allowed'] = 'yes'
        request.pop('key')
    else:
        request['allowed'] = 'no'


front_controllers = [front_add_date, front_add_key, front_request_allowed]

# routes = {
#     '/': Index(),
#     '/courses/': Courses(),
#     '/about/': About(),
#     '/study_programs/': StudyPrograms(),
#     '/courses-list/': CoursesList(),
#     '/create-category/': CreateCategory(),
#     '/create-course/': CreateCourse(),
#     '/category-list/': CategoryList(),
#     '/copy-course/': CopyCourse()
# }
