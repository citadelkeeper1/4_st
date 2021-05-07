def login(request):
    if request.get('key') == 'KEY':
        return True
    else:
        return False
