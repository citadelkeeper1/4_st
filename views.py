from fw.templater import render
from datetime import date
from patterns.сreational_patterns import Engine, Logger
from patterns.structural_patterns import AppRoute, Debug

site = Engine()
logger = Logger('main')

routes = {}


@AppRoute(routes=routes, url='/')
class Index:
    @Debug(name='Index')
    def __call__(self, request):
        req_date = request.get('date', None)
        return '200 OK', render('index.html', date=req_date)
        # return '200 OK', render('index.html', objects_list=site.categories)


@AppRoute(routes=routes, url='/courses/')
class Courses:
    @Debug(name='Courses')
    def __call__(self, request):
        return '200 OK', render('courses.html', date=request.get('date', None), objects_list=site.categories)


@AppRoute(routes=routes, url='/about/')
class About:
    @Debug(name='About')
    def __call__(self, request):
        return '200 OK', render('about.html', date=request.get('date', None))


class NotFound404:
    @Debug(name='NotFound404')
    def __call__(self, request):
        return '404 WHAT', 'Ошибка 404: страница не найдена.'


@AppRoute(routes=routes, url='/study_programs/')
class StudyPrograms:
    @Debug(name='StudyPrograms')
    def __call__(self, request):
        return '200 OK', render('study-programs.html', data=date.today())


@AppRoute(routes=routes, url='/courses-list/')
class CoursesList:
    @Debug(name='CoursesList')
    def __call__(self, request):
        print('!!! CL')
        # print(request['request_params']['id'])
        logger.log('Список курсов')
        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
            return '200 OK', render('course_list.html', objects_list=category.courses, name=category.name,
                                    id=category.id)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


@AppRoute(routes=routes, url='/create-category/')
class CreateCategory:
    @Debug(name='CreateCategory')
    def __call__(self, request):
        print('creating category')

        if request['method'] == 'POST':
            print(request)
            data = request['data']
            print('data:', data)

            name = data['name']
            name = site.decode_value(name)

            print('name:', name)

            category_id = data.get('category_id')
            print('id:', category_id)

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))
            print('CAT:', category)

            new_category = site.create_category(name, category)

            site.categories.append(new_category)
            print('added:', site.categories)

            return '200 OK', render('courses.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html', categories=categories)


@AppRoute(routes=routes, url='/create-course/')
class CreateCourse:
    category_id = -1

    @Debug(name='CreateCourse')
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course('record', name, category)
                site.courses.append(course)

            return '200 OK', render('course_list.html', objects_list=category.courses,
                                    name=category.name, id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_course.html', name=category.name, id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


@AppRoute(routes=routes, url='/category-list/')
class CategoryList:
    @Debug(name='CategoryList')
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('courses.html', objects_list=site.categories)


@AppRoute(routes=routes, url='/copy-course/')
class CopyCourse:
    @Debug(name='CopyCourse')
    def __call__(self, request):
        print('>>> copycourse')
        # print('site courses:')
        # for c in site.courses:
        #     print(c.name)
        request_params = request['request_params']

        try:
            name = request_params['name']
            old_course = site.get_course(name)
            if old_course:
                new_name = f'copy_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                site.categories[new_course.category.id].courses.append(new_course)
                # print('new name:', new_course.name)
                # print('new category:', new_course.category.name)

                # print('categories:')
                # for c in site.categories:
                #     print(c.name)

                site.courses.append(new_course)
                # print('course added:')
                # for c in site.courses:
                #     print(c.name)

                # print('courses in category:')
                # for c in site.categories[new_course.category.id].courses:
                #     print(c.name)

                return '200 OK', render('course_list.html',
                                        objects_list=site.categories[new_course.category.id].courses,
                                        name=new_course.category.name,
                                        id=new_course.category.id)

            return '200 OK', render('courses.html', objects_list=site.categories)
        except KeyError:
            return '200 OK', 'No courses have been added yet'
