import csv
import uuid
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import login as abc, authenticate, logout as deff
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Sum
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.status import (HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView

from .models import *
from .ser import *


class ListUsersOnClick(APIView):
    def get(self, request):
        try:
            temp = ""
            if request.GET.get('id'):
                idd = request.GET.get('id')
                lst = Profile.objects.filter(location_id=idd)
                sm = Profile.objects.filter(location_id=idd).aggregate(Sum('id'))
                aa = sm['id__sum']
                serializers_class = UserListOnClickSerializer(lst, many=True)
                temp = render_to_string("Location/user_list_onlick.html", {"dat": serializers_class.data, "aa": aa})
            return Response({"data": temp})
        except Exception as e:
            print(e)
            return Response({"data": temp}, status=status.HTTP_400_BAD_REQUEST)


class ProfileRegistrationViewSet(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer

    def create(self, request, *args, **kwargs):
        a = data_filt(request)
        print(a)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class ProfileSignUpViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = UserProfileListSerializer

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

        def perform_update(self, serializer):
            serializer.save()


class MeetingQuestionViewSet(viewsets.ModelViewSet):
    queryset = Meeting_Questions.objects.all()
    serializer_class = MeetingQuestionSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def list(self, request):
        queryset = Location.objects.all()
        serializer = LocationSerializer(queryset, many=True)
        # return Response(serializer.data)
        temp = render_to_string("Location/location_list_table.html", {"dat": serializer.data})
        return Response({"data": temp})


class UserCheckViewSet(APIView):
    def get(self, request):
        try:
            temp = ""
            if request.GET.get('phone'):
                if request.GET.get('email'):
                    idd = request.GET.get('phone')
                    em = request.GET.get('email')
                    if Exist.objects.filter(phone=idd, email=em).exists():
                        lst = Exist.objects.filter(phone=idd, email=em)
                        serializers_class = UserCheckSerializer(lst, many=True)
                        # temp = render_to_string("Location/user_list_onlick.html", {"dat": serializers_class.data})
                        return Response(serializers_class.data)
                    else:
                        val = {"msg": "some issue"}
                        return Response(val, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(serializers_class.data, status=status.HTTP_400_BAD_REQUEST)


def add_new_csv(request):
    lstexist = models.Exist.objects.all()
    lstlocation = models.Location.objects.all()
    if request.method == 'POST':
        loc = request.POST['location']
        fl = request.FILES['fl']
        decoded_file = fl.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        for row in reader:
            if models.Exist.objects.filter(email=row['email'], phone=row['phone']).exists():
                messages.success(request, "Some data already exist!")
                return redirect('/csv/')
            else:
                rec = models.Exist(email=row['email'], phone=row['phone'], address=row['address'],
                                   surname=row['surname'], thousand=row['thousand'], location_id=loc)
                rec.save()
                return redirect('/location_list/')
    return render(request, 'up.html', {'all': lstexist, 'lstlocation': lstlocation})


def add_new_location(request):
    return render(request, 'loc.html')


def signup(request):
    phone = ""
    email = ""
    fetch = ""
    if request.GET.get('phone') and request.GET.get('email'):
        phone = request.GET.get('phone')
        email = request.GET.get('email')
        fetch = models.Exist.objects.get(phone=phone, email=email)
    if request.method == 'POST':
        name = request.POST['name']
        surname = request.POST['surname']
        email_id = request.POST['email']
        phone_no = request.POST['phone']
        address = request.POST['address']
        lid = request.POST['location']
        username = request.POST['uname']
        password = request.POST['password']
        pwd = make_password(password)
        usave = models.User(username=username, email=email_id, password=pwd)
        usave.save()
        key = User.objects.all().last()
        uid = key.id
        psave = models.Profile(name=name, surname=surname, phone=phone_no, address=address, location_id=lid, uid_id=uid)
        psave.save()
        eupdate = models.Exist.objects.filter(email=email_id)
        eupdate.update(sts=True)
        return redirect('/')
    return render(request, 'signup.html', {'phone': phone, 'email': email, 'fetch': fetch})


def user_exististan_check(request):
    return render(request, 'Registration/user_exististan_check.html')


def location_list_with_user(request):
    return render(request, 'locationlist.html')


def logout(request):
    deff(request)
    return redirect('/')


def login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/index/')
        elif request.user.is_staff == False:
            return redirect('/home/')
    if (request.method == 'POST'):
        uname = request.POST['uname']
        pwd = request.POST['pwd']
        auth = authenticate(username=uname, password=pwd)
        if auth is not None:
            if auth.is_superuser == True:
                abc(request, auth)
                return redirect('/index/')
            elif auth.is_staff == False:
                abc(request, auth)
                return redirect('/home/')
        else:
            error = 'username & password.'
            return render(request, 'login.html', {'error': error})
    form = AuthenticationForm()
    return render(request, 'login.html')


def new_meeting(request):
    location_list = models.Location.objects.all()
    meeting_id = uuid.uuid4()
    if request.method == 'POST':
        code_id = request.POST['meeting_id']
        title = request.POST['title']
        date = request.POST['date']
        time = request.POST['time']
        loc = request.POST['loc']
        create = models.Meeting(meeting_id=code_id, meeting_title=title, meeting_location_id=loc, meeting_date=date,
                                meeting_no=0, meeting_time=time)
        create.save()
        return redirect('/meeting_list/')
    return render(request, 'newmeeting.html', {'code': meeting_id, 'location_list': location_list})


def meeting_list(request):
    lists = models.Meeting.objects.all().order_by('-ts')
    return render(request, 'mlist.html', {'lists': lists})


def meeting_terminate(request, id):
    m = models.Meeting.objects.filter(meeting_id=id)
    dt = datetime.now()
    m.update(meeting_sts=True, meeting_end_detail=dt)
    return redirect("/meeting_list/")


def getfile(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="file.csv"'
    list = Meeting.objects.all()
    writer = csv.writer(response)
    for employee in list:
        writer.writerow([employee.meeting_title, employee.meeting_end_detail,
                         employee.meeting_date])
    return response


def logs(request, id):
    meeting_detail = models.Meeting.objects.get(meeting_id=id)
    location_id = meeting_detail.meeting_location_id
    chk = models.Meeting_Question_Logs.objects.filter(meeting_id_id=meeting_detail.meeting_id)
    # chk=models.Meeting_Question_Logs.objects.all().distinct()
    total_user = models.Profile.objects.filter(location_id=location_id).count()
    response_total = models.Meeting_Question_Logs.objects.filter(meeting_id_id=id).count()
    aa = total_user * 0.5;
    if response_total < aa:
        response_counts = False
    else:
        response_counts = True

    meeting_question = models.Meeting_Questions.objects.filter(meeting_id=id)
    return render(request, 'logs.html',
                  {'lists': chk, 'meeting_detail': meeting_detail, 'response_count': total_user,
                   'response_counts': response_counts,
                   'meeting_question': meeting_question})


def user_home(request):
    first = timezone.localtime(timezone.now())
    chk = models.Profile.objects.get(uid_id=request.user.id)
    lo = chk.location_id

    meet = models.Meeting.objects.filter(meeting_location_id=lo, meeting_date=datetime.today(), meeting_sts=False)
    check_response_for_this_meeting = models.Meeting_Question_Logs.objects.filter(user_id=request.user.id)
    meet2 = models.Meeting.objects.filter(meeting_location_id=lo, meeting_sts=False).exclude(
        meeting_date=datetime.today())
    history = models.Meeting_Question_Logs.objects.filter(user_id=request.user.id)

    Meeting_list = []
    for a in meet:
        dic = {}
        dic['meeting_title'] = a.meeting_title
        dic['meeting_date'] = a.meeting_date
        dic['meeting_time'] = a.meeting_time
        dic['meeting_sts'] = a.meeting_sts
        dic['meeting_id'] = a.meeting_id
        act = False
        if models.Attend.objects.filter(user=request.user, meeting_id=a.meeting_id).exists():
            act = True
        dic['act'] = act
        first = timezone.localtime(timezone.now())
        dat = False
        if models.Meeting.objects.filter(meeting_date=first.date(), meeting_time__lte=first.time(),
                                         meeting_id=a.meeting_id).exists():
            dat = True
        dic['dat'] = dat
        Meeting_list.append(dic)

    return render(request, 'join.html', {'meet': Meeting_list, 'meet2': meet2, 'history': history, 'act': act})


def data_filt(request):
    data2 = {}
    try:

        lst = [{"name": request.data.get("name", ''),
                "surname": request.data.get("sname", ''),
                "phone": request.data.get("phone", ''),
                "address": request.data.get("address", ''),
                "location_id": request.data.get("loc_id", ''),
                }]

        data2['vote_user'] = lst
        data2['username'] = request.data.get("username", '')
        data2['password'] = request.data.get("password", '')
        data2['email'] = request.data.get("email", '')
        return data2
    except Exception as e:
        print(e)


def deligate(request, id):
    meet_id = id
    uid = request.user.id
    lst = models.Profile.objects.get(uid_id=uid)
    location = lst.location_id
    all = models.Profile.objects.filter(location_id=location).exclude(uid_id=uid)
    if request.method == 'POST':
        uname = request.POST['uname']
        data = {}
        data['delegated_to'] = request.POST['uname']
        data['user'] = request.user.id
        data['meeting_id'] = meet_id
        data['delegated_sts'] = True
        data['sts'] = False
        serializer = DelegateSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse({'message': 'Save'}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'message': 'Not save', }, status=HTTP_400_BAD_REQUEST)
    return render(request, 'daligate_to.html', {'all': all, 'meet_id': meet_id})


def notification(request):
    all = models.Daligate.objects.filter(delegated_to_id=request.user.id, sts=False, delegated_sts=True)
    if request.GET.get('method') == 'accept':
        notify_id = request.GET.get('notify_id')
        notify_detail = models.Daligate.objects.filter(id=notify_id)
        notify_detail.update(sts=True, delegated_sts=False)
    if request.GET.get('method') == 'reject':
        notify_id = request.GET.get('notify_id')
        notify_detail = models.Daligate.objects.filter(id=notify_id)
        notify_detail.update(sts=False, delegated_sts=False)

    return render(request, 'notification.html', {'all': all})


def index(request):
    total_meeting = Meeting.objects.all().count()
    total_meeting_open = Meeting.objects.filter(meeting_sts=False).count()
    total_meeting_close = Meeting.objects.filter(meeting_sts=True).count()
    return render(request, 'index.html', {'total_meeting': total_meeting, 'total_meeting_open': total_meeting_open,
                                          'total_meeting_close': total_meeting_close})


def uindex(request):
    return render(request, 'uindex.html')


def upcomming(request):
    chk = Profile.objects.get(uid_id=request.user.id)
    lo = chk.location_id
    meet = Meeting.objects.filter(meeting_location_id=lo, meeting_sts=False)
    return render(request, 'upcomming_list.html', {'meet': meet})


def delegate_meeting_list(request):
    all = Daligate.objects.filter(delegated_to_id=request.user.id)
    return render(request, 'delegate_list.html', {'all': all})


def answer(request, id):
    chk = models.Meeting.objects.get(meeting_id=id)

    first = timezone.now()
    dat = False
    if models.Meeting.objects.filter(meeting_date=first, meeting_time__gte=first, meeting_id=id).exists():
        dat = True
    mquest = models.Meeting_Questions.objects.filter(meeting_id=id).exclude(
        id__in=models.Meeting_Question_Logs.objects.values_list('question_id', flat=True))
    return render(request, 'answer.html', {'chk': chk, 'mquest': mquest, 'dat': dat})


def meetingattend(request, id):
    models.Attend.objects.create(user=request.user, meeting_id_id=id)
    return redirect('/home/')


def answersubmit(request):
    if request.method == 'POST':
        mid = request.POST['mid']
        uid = request.POST['uid']
        qid = request.POST['qid']
        vote = request.POST['ask']
        create = models.Meeting_Question_Logs(meeting_id_id=mid, user_id=uid, answer=vote, question_id=qid)
        create.save()
    return redirect('/uindex/')


def delegate_answer(request, id):
    chk = models.Meeting.objects.get(meeting_id=id)
    mquest = models.Meeting_Questions.objects.filter(meeting_id=id).exclude(
        id__in=models.Meeting_Question_Logs.objects.values_list('question_id', flat=True))
    return render(request, 'delegate_answer.html', {'chk': chk, 'mquest': mquest})


def delegate_answersubmit(request):
    if request.method == 'POST':
        mid = request.POST['mid']
        myid = request.user.id
        delegater_id = request.POST['uid']
        qid = request.POST['qid']
        vote = request.POST['ask']
        create = models.Meeting_Question_Logs(meeting_id_id=mid, user_id=delegater_id, answer=vote, question_id=qid,
                                              delegated_id=myid)
        create.save()
        dalegate_update = Daligate.objects.filter(meeting_id_id=mid)
        dalegate_update.update(sts=True, delegated_sts=True)
    return redirect('/uindex/')


def update_user(request, id):
    if request.method == 'POST':
        name = request.POST['name']
        surname = request.POST['surname']
        phone = request.POST['phone']
        address = request.POST['address']
        get_data = Profile.objects.get(id=id)
        get_data.name = name
        get_data.surname = surname
        get_data.phone = phone
        get_data.address = address
        get_data.save()
    return redirect('/location_list/')
