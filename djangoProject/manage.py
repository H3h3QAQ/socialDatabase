# encoding: GBK

from django.shortcuts import render
from django.http import HttpRequest
from . import invite
from . import social
from InviteModel.models import Invitee


def is_valid(request):
    if "name" in request.POST and request.POST["name"] != "":
        return {}
    else:
        ctx = invite.get_ctx({}, 4)
        ctx["warning"] = "�������û�����"
        return ctx

def is_Admin(request):
    try:
        if request.session["isAdmin"]:
            return True
    except:
        pass
    return False

def add_user(request):
    if not is_Admin(request):
        return social.get_school(request, {"warning":"����ԽȨ����"})
    ctx = is_valid(request)
    if ctx == {}:
        ctx["success_message"] = "��ӳɹ�"
        user = Invitee(name=request.POST["name"])
        user.save()
    return manage_list(request, ctx)


def del_user(request):
    if not is_Admin(request):
        return social.get_school(request, {"warning":"����ԽȨ����"})
    ctx = invite.get_ctx({}, 4)
    if "name" in request.POST:
        user_list = Invitee.objects.filter(name=request.POST["name"])
        for user in user_list:
            if user.isAdmin:
                ctx["warning"] = "�޷�ɾ������Ա�û�"
                break
            user.delete()
        ctx["success_message"] = "ɾ���û��ɹ�"
    return manage_list(request, ctx)


def edit_user(request: HttpRequest):
    if not is_Admin(request):
        return social.get_school(request, {"warning":"����ԽȨ����"})
    ctx = invite.get_ctx({}, 4)
    warning = ""
    if request.method == "POST":
        try:
            id = request.POST["id"]
            if request.POST["name"] == "" or request.POST["code"] == "":
                warning = "�û����������벻��Ϊ��"
            else:
                user = Invitee.objects.get(id=id)
                user.name = request.POST["name"]
                user.code = request.POST["code"]
                user.isActive = True if request.POST["active"] == "true" else False
                user.isAdmin = True if request.POST["admin"] == "����Ա" else False
                user.save()
                ctx["success_message"] = "�޸����ݳɹ�"
        except:
            warning = "���ύ��������"
    ctx["warning"] = warning
    return manage_list(request, ctx)


def manage_list(request: HttpRequest, ctx=None):
    if ctx == None:
        ctx = {}
    each_num = 10  # ÿҳ��ʾ������
    if "page" in request.GET:
        page = int(request.GET["page"])
    else:
        page = 1
    if "q" in request.GET:
        query = request.GET["q"]
        user_list = Invitee.objects.all().filter(name__contains=query)
    else:
        query = ""
        user_list = Invitee.objects.all()
    last_page = invite.get_lastpage(user_list.count(), each_num)
    if invite.isIllegal(request) or not "name" in request.session:
        return invite.isIllegal(request)
    else:
        if not request.session["isAdmin"]:
            ctx = invite.get_ctx(ctx, 3)
            ctx["warning"] = "�����ǹ���Ա�û���"
            return invite.get_form(request, ctx)
        else:
            ctx = social.get_ctx(ctx, "user_list", user_list[(page - 1) * each_num:page * each_num], page, last_page, 4,
                                 "�û���")
        if query == "":
            ctx["page_url"] = "/social/user/list/?page="
        else:
            ctx["page_url"] = "/social/user/list/?q=%s&page="%query
    return render(request, "manage.html", ctx)
