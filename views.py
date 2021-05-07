from fw.templater import render


class Index:
    def __call__(self, request):
        date = request.get('date', None)
        return '200 OK', render('index.html', date=date)


class Courses:
    def __call__(self, request):
        return '200 OK', render('courses.html', date=request.get('date', None))


class About:
    def __call__(self, request):
        return '200 OK', render('about.html', date=request.get('date', None))


class NotFound404:
    def __call__(self, request):
        return '404 WHAT', 'Ошибка 404: страница не найдена.'
