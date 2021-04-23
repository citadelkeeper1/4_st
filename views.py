from fw.templater import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', data=request.get('data', None))


class Contact:
    def __call__(self, request):
        return '200 OK', render('contact.html', data=request.get('data', None))
        # return '200 OK', 'contact'


class About:
    def __call__(self, request):
        return '200 OK', render('about.html', data=request.get('data', None))
        # return '200 OK', 'about'


class NotFound404:
    def __call__(self, request):
        return '404 WHAT', 'Ошибка 404: страница не найдена.'

