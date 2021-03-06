from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import simplejson
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt

from textile import textile

from models import Page


def fiber_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)

    result = {}
    if user is not None:
        if user.is_active:
            login(request, user)
            result = {
                'status': 'success',
            }
        else:
            result = {
                'status': 'inactive',
                'message': _('This account is inactive.'),
            }
    else:
            result = {
                'status': 'failed',
                'message': _('Please enter a correct username and password. Note that both fields are case-sensitive.'),
            }
    json = simplejson.dumps(result)
    return HttpResponse(json, mimetype='application/json')


@staff_member_required
def page_move_up(request, id):
    page = Page.objects.get(pk=id)

    if (page):
        previous_sibling_page = page.get_previous_sibling()
        if (previous_sibling_page):
            page.move_to(previous_sibling_page, position='left')

    return HttpResponseRedirect('../../')


@staff_member_required
def page_move_down(request, id):
    page = Page.objects.get(pk=id)

    if (page):
        next_sibling_page = page.get_next_sibling()
        if (next_sibling_page):
            page.move_to(next_sibling_page, position='right')

    return HttpResponseRedirect('../../')


@csrf_exempt
def render_textile(request):
    return HttpResponse(
        textile(request.POST['data'])
    )
