import datetime

from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
# Create your views here.
from MyApp.cpuutil import get_memory_info
from MyApp.models import *
def login(request):
    return render(request,'login.html')

def login_post(request):
    uname=request.POST["textfield"]
    password=request.POST["textfield2"]
    a=login_table.objects.filter(username=uname,password=password)
    if a.exists():
        request.session['lid']=a[0].id
        var=login_table.objects.get(username=uname,password=password)
        if var.type=='admin':
            return  HttpResponse('''<script>alert('admin logged in..');window.location='/admin_home_page'</script>''')
        elif var.type=='staff':
            return  HttpResponse('''<script>alert('staff logged in..');window.location='/staff_home_page'</script>''')
        elif var.type=='lab assistant':

            return  HttpResponse('''<script>alert('lab assistant logged in..');window.location='/lab_assistant_home_page'</script>''')
        else:
            return  HttpResponse('''<script>alert('invalid..');window.location='/'</script>''')

    else:
        return HttpResponse('''<script>alert('invalid..');window.location='/'</script>''')


def admin_add_department(request):
    return render(request,'admin/add department.html')

def admin_add_department_post(request):
    department=request.POST['textfield']
    details=request.POST['textfield2']

    dep=department_table()
    dep.department_name=department
    dep.details=details
    dep.save()
    return HttpResponse('''<script>alert('added..');window.location='/admin_view_dept#stats'</script>''')

def admin_view_dept(request):
    a = department_table.objects.all()
    return render(request, 'admin/view dept.html', {'data': a})

def admin_view_dept_post(request):
    a=request.POST['textfield']
    ob=department_table.objects.filter(department_name__icontains=a)
    return render(request,'admin/view dept.html',{'data':ob,"s":a})

def edit_department(request,id):
    dep=department_table.objects.get(id=id)
    request.session['did']=id
    return render(request,'admin/edit department.html',{'dep':dep})

def edit_department_post(request):
    dep=request.POST['textfield']
    detail=request.POST['textfield2']

    ob=department_table.objects.get(id=request.session['did'])
    ob.department_name=dep
    ob.details=detail
    ob.save()
    return HttpResponse('''<script>alert('Edited successfully');window.location='/admin_view_dept#stats'</script>''')

def delete_department(request,id):
    dep=department_table.objects.get(id=id).delete()
    return HttpResponse('''<script>alert('success');window.location='/admin_view_dept#stats'</script>''')



def admin_add_course(request):
    ob=department_table.objects.all()
    return render(request,'admin/add course.html',{"dept":ob})

def admin_add_course_post(request):
    Department = request.POST['select']
    Course_name = request.POST['textfield']
    Details=request.POST['textfield2']

    course=course_table()
    course.DEPT=department_table.objects.get(id=Department)
    course.details=Details
    course.course_name=Course_name
    course.save()
    return HttpResponse('''<script>alert('Course added');window.location='/admin_view_course#stats'</script>''')

def admin_view_course(request):
    a=course_table.objects.all()
    return render(request,'admin/view course.html',{'data':a})

def admin_view_course_post(request):
    a = request.POST['textfield']
    ob =course_table.objects.filter(course_name__icontains=a)
    return render(request, 'admin/view course.html', {'data': ob,"s":a})

def edit_course(request,id):
    crs=course_table.objects.get(id=id)
    ob=department_table.objects.all()
    request.session['cid']=id
    return render(request, 'admin/edit_course.html', {'cour': crs,"dept":ob})

def edit_course_post(request):
    crsn=request.POST['textfield']
    details=request.POST['textfield2']

    cb=course_table.objects.get(id=request.session['cid'])
    cb.course_name=crsn
    cb.details=details
    cb.save()
    return HttpResponse('''<script>alert('Edited successfully');window.location='/admin_view_course#stats'</script>''')

def delete_course(request,id):
    crs=course_table.objects.get(id=id).delete()
    return HttpResponse('''<script>alert('success');window.location='/admin_view_course#stats'</script>''')


def admin_add_subject(request):
    ob=course_table.objects.all()
    return render(request,'admin/add subject.html',{"course":ob})

def admin_add_subject_post(request):
    course=request.POST['course']
    Subject=request.POST['textfield2']
    semester=request.POST['textfield3']
    syllabus=request.FILES['textfield4']

    fs=FileSystemStorage()
    fsave=fs.save(syllabus.name,syllabus)


    sub=subject_table()
    sub.COURSE=course_table.objects.get(id=course)
    sub.subject=Subject
    sub.semester=semester
    sub.semester=semester
    sub.syllabus=fsave
    sub.save()
    return HttpResponse('''<script>alert('Subject added');window.location='/admin_view_subject#stats'</script>''')


def admin_view_subject(request):
    a=subject_table.objects.all()
    return render(request,'admin/view subject.html',{'data':a})

def admin_view_subject_post(request):
    a = request.POST['textfield']
    ob = subject_table.objects.filter(subject__icontains=a)
    return render(request, 'admin/view subject.html', {'data': ob,"s":a})

def edit_subject(request,id):
    sub=subject_table.objects.get(id=id)
    ob=course_table.objects.all()
    request.session['sid']=id
    return render(request, 'admin/edit_subject.html', {'sub':sub,"course":ob})

def edit_subject_post(request):
    sub=request.POST['textfield']
    sem=request.POST['textfield2']

    if 'textfield3' in request.FILES:
        syll=request.FILES['textfield3']
        fs=FileSystemStorage()
        fsave=fs.save(syll.name,syll)

        ob=subject_table.objects.get(id=request.session['sid'])
        ob.subject=sub
        ob.semester=sem
        ob.syllabus=fsave
        ob.save()
        return HttpResponse('''<script>alert('Edited successfully');window.location='/admin_view_subject#stats'</script>''')
    else:
        ob = subject_table.objects.get(id=request.session['sid'])
        ob.subject = sub
        ob.semester = sem

        ob.save()
        return HttpResponse('''<script>alert('Edited successfully');window.location='/admin_view_subject#stats'</script>''')

def delete_subject(request,id):
    sub=subject_table.objects.get(id=id).delete()
    return HttpResponse('''<script>alert('deleted successfully');window.location='/admin_view_subject#stats'</script>''')


def admin_add_lab(request):
    ob=lab_table.objects.all()
    return render(request,'admin/add lab.html')

def admin_add_lab_post(request):
    Labno=request.POST['textfield']
    Floorno=request.POST['textfield2']

    lab=lab_table()
    lab.Lab_no=Labno
    lab.Floor_no=Floorno
    lab.save()
    return HttpResponse('''<script>alert(' Lab added..');window.location='/admin_view_lab#stats'</script>''')

def admin_view_lab(request):
    ob=lab_table.objects.all()
    return render(request,'admin/view lab.html',{'lab':ob})

def admin_view_lab_post(request):
    a=request.POST['textfield']
    ob = lab_table.objects.filter(Lab_no__istartswith=a)
    return render(request, 'admin/view lab.html', {'lab': ob,"s":a})

def edit_lab(request,id):
   lab=lab_table.objects.get(id=id)

   return render(request,'admin/edit lab.html',{'lab':lab})

def edit_lab_post(request):
    id=request.POST['id']
    labno=request.POST['textfield']
    floorno=request.POST['textfield2']

    ob=lab_table.objects.get(id=id)
    ob.Lab_no=labno
    ob.Floor_no=floorno
    ob.save()
    return HttpResponse('''<script>alert('Edited successfully');window.location='/admin_view_lab#stats'</script>''')

def delete_lab(request,id):
    lab=lab_table.objects.get(id=id).delete()
    return HttpResponse('''<script>alert('Deleted successfully');window.location='/admin_view_lab#stats'</script>''')


def admin_assign_lab(request):
    ob=lab_assistant_table.objects.all()
    ob1=lab_table.objects.all()
    return render(request,'admin/assign lab.html',{"ass":ob,"lab":ob1})

def admin_assign_lab_post(request):
    Labasst=request.POST['ass']
    Lab=request.POST['lab']
    lab = assign_lab_table()
    lab.LAB_ASST = lab_assistant_table.objects.get(id=Labasst)
    lab.LAB = lab_table.objects.get(id=Lab)
    lab.date = datetime.datetime.now().today()
    lab.save()
    return HttpResponse('''<script>alert('Lab added');window.location='/admin_view_assigned_lab#stats'</script>''')

def admin_view_assigned_lab(request):
    a=assign_lab_table.objects.all()
    return render(request,'admin/view assigned lab.html',{'data':a})

def admin_view_assigned_lab_post(request):
    a=request.POST['textfield']
    ob = assign_lab_table.objects.filter(LAB__Lab_no__icontains=a)
    return render(request,'admin/view assigned lab.html', {'data': ob,"s":a})

def edit_assign_lab(request,id):
    request.session['id'] = id
    ob = lab_assistant_table.objects.all()
    ob2 = lab_table.objects.all()
    ob1= assign_lab_table.objects.get(id=id)
    return render(request,'edit assign lab.html', {"ass":ob,"lab":ob1,"labno":ob2})

def edit_assign_lab_post(request):
    labasst=request.POST['ass']
    lab=request.POST['lab']
    date=request.POST['textfield2']

    ob=assign_lab_table.objects.get(id=request.session['id'])
    ob.LAB_ASST_id=labasst
    ob.LAB_id=lab
    ob.date=date
    ob.save()
    return HttpResponse('''<script>alert('Edited successfully');window.location='/admin_view_assigned_lab#stats'</script>''')

def delete_assign_lab(request,id):
    lab=assign_lab_table.objects.get(id=id).delete()
    return HttpResponse('''<script>alert('Deleted successfully');window.location='/admin_view_assigned_lab#stats'</script>''')

def admin_add_lab_assistant(request):
    ob = login_table.objects.all()
    labasst=lab_assistant_table.objects.all()
    return render(request,'admin/add_lab_assistant.html',{'asst':ob,'lab':labasst})

def admin_add_lab_assistant_post(request):
    name = request.POST['textfield']
    gender = request.POST['lab']
    phoneno = request.POST['textfield2']
    post = request.POST['textfield5']
    email = request.POST['textfield1']
    place = request.POST['textfield6']
    pin = request.POST['textfield7']
    qualif = request.POST['textfield9']
    image = request.POST['file2']
    dob = request.POST['textfield8']

    a = login_table()
    a.username = email
    a.password = phoneno
    a.type = 'lab assistant'
    a.save()

    labasst = lab_assistant_table()

    labasst.LOGIN = a
    labasst.name = name
    labasst.gender = gender
    labasst.phone_no = phoneno
    labasst.post = post
    labasst.email = email
    labasst.place = place
    labasst.pin = pin
    labasst.qualification = qualif
    labasst.image = image
    labasst.dob = dob
    labasst.save()
    return HttpResponse('''<script>alert('Lab assistant Added');window.location='/admin_view_lab_assistant#stats'</script>''')

def admin_view_lab_assistant(request):
    ob=lab_assistant_table.objects.all()
    return render(request,'admin/view lab assistant.html',{'data': ob})

def admin_view_lab_assistant_post(request):
    a = request.POST['textfield']
    ob = lab_assistant_table.objects.filter(name__icontains=a)
    return render(request,'admin/view lab assistant.html', {'data': ob, "s": a})

def delete_lab_assistant(request,id):
    labasst=lab_assistant_table.objects.get(id=id).delete()
    return HttpResponse('''<script>alert('Deleted successfully');window.location='/admin_view_lab_assistant#stats'</script>''')

def edit_lab_assistant(request,id):
    request.session['id'] = id
    ob=lab_assistant_table.objects.get(id=id)
    return render(request,'admin/edit lab assistant.html', {"labasst":ob})

def edit_lab_assistant_post(request):
    studname = request.POST['textfield']
    image = request.POST['file2']
    phoneno = request.POST['textfield2']
    email = request.POST['textfield1']
    gender = request.POST['lab']
    post = request.POST['textfield5']
    place = request.POST['textfield6']
    pin = request.POST['textfield7']
    dob = request.POST['textfield8']
    qualif = request.POST['textfield9']

    ob = lab_assistant_table.objects.get(id=request.session['id'])

    ob.studname = studname
    ob.image = image
    ob.phone_no = phoneno
    ob.email = email
    ob.gender = gender
    ob.post = post
    ob.place = place
    ob.pin = pin
    ob.dob = dob
    ob.qualification = qualif
    ob.save()
    return HttpResponse('''<script>alert('Edited successfully');window.location='/admin_view_lab_assistant#stats'</script>''')


def admin_add_exam_schedule(request):
    ob=subject_table.objects.all()
    ob1=staff_table.objects.all()
    return render(request,'admin/add exam schedule.html',{"sub":ob,"stf":ob1})

def admin_add_exam_schedule_post(request):
    subject=request.POST['subject']
    staff=request.POST['staff']
    date = request.POST['textfield']
    time=request.POST['textfield2']
    exmn=request.POST['textfield3']
    dur=request.POST['textfield4']
    details=request.POST['textfield5']
    syll=request.FILES['file2']

    fs = FileSystemStorage()
    fp = fs.save(syll.name, syll)

    exam=exam_schedule_table()
    exam.SUBJECT=subject_table.objects.get(id=subject)
    exam.STAFF=staff_table.objects.get(id=staff)
    exam.date=date
    exam.time=time
    exam.exam_name=exmn
    exam.duration=dur
    exam.details=details
    exam.syllabus=fp
    exam.save()
    return HttpResponse('''<script>alert('Exam schedule added');window.location='/admin_view_exam_schedule#stats'</script>''')

def admin_view_exam_schedule(request):
    ob = exam_schedule_table.objects.all()
    return render(request,'admin/view exam sched.html',{'data':ob})

def admin_view_exam_schedule_post(request):
    a = request.POST['textfield']
    ob = exam_schedule_table.objects.filter(exam_name__icontains=a)
    return render(request, 'admin/view exam sched.html', {'data': ob,"s": a})

def edit_exam_schedule(request, id):
    ob=subject_table.objects.all()
    ob1=staff_table.objects.all()
    ob2=exam_schedule_table.objects.get(id=id)
    time = str(ob2.time)
    return render(request,'admin/edit_exam_schedule.html',{"sub":ob,"stf":ob1,"exam":ob2,'time':time})

def edit_exam_schedule_post(request):
    id= request.POST['id']
    date= request.POST['textfield']
    time= request.POST['textfield2']
    exam_name=request.POST['textfield3']
    duration=request.POST['textfield4']
    details=request.POST['textfield5']
    if 'file2' in request.FILES:
        syll = request.FILES['file2']
        fs = FileSystemStorage()
        fsave = fs.save(syll.name, syll)

        ob = exam_schedule_table.objects.get(id=id)
        ob.date=date
        ob.time=time
        ob.exam_name=exam_name
        ob. duration=duration
        ob.details=details
        ob.syllabus = fsave
        ob.save()
        return HttpResponse(
            '''<script>alert('Edited successfully');window.location='/admin_view_exam_schedule#stats'</script>''')
    else:
        ob =exam_schedule_table.objects.get(id=id)
        ob.date = date
        ob.time = time
        ob.exam_name = exam_name
        ob.duration = duration
        ob.details = details
        ob.save()
        return HttpResponse(
            '''<script>alert('Edited successfully');window.location='/admin_view_exam_schedule#stats'</script>''')

        # ob=exam_schedule_table.objects.get(id=id)
        # ob.department_name=dep
        # ob.details = detail
        # ob.save()
        #
        # return HttpResponse('''<script>alert('Edited successfully');window.location='/admin_view_dept'</script>''')

def delete_exam_schedule(request,id):
    exam=exam_schedule_table.objects.get(id=id).delete()
    return HttpResponse('''<script>alert('Deleted successfully');window.location='/admin_view_exam_schedule#stats'</script>''')


def admin_view_system_details(request):
    ob=system_table.objects.all()
    return render(request,'admin/view system details.html',{'data':ob})

def admin_view_system_details_post(request):
    a = request.POST['textfield']
    ob = system_table.objects.filter(system_no__icontains=a)
    return render(request, 'admin/view system details.html', {'data': ob, "s": a})

def admin_add_student(request):
    course=course_table.objects.all()
    stud=student_table.objects.all()
    return render(request,'admin/add student.html',{'cour':course,"stud":stud})

def admin_add_student_post(request):
    course = request.POST['course_name']
    studname=request.POST['textfield1']
    rollno=request.POST['textfield3']
    image=request.FILES['file2']
    phoneno=request.POST['textfield5']
    email=request.POST['textfield4']
    sem=request.POST['textfield6']
    gender=request.POST['stud']
    post=request.POST['textfield8']
    place=request.POST['textfield9']
    pin=request.POST['textfield10']
    dob=request.POST['textfield11']
    qualif=request.POST['textfield12']

    fs=FileSystemStorage()
    path=fs.save(image.name,image)

    ob=login_table()
    ob.username=email
    ob.password=phoneno
    ob.type='student'
    ob.save()
    stud=student_table()

    stud.LOGIN=ob
    stud.COURSE=course_table.objects.get(id=course)
    stud.studname=studname
    stud.roll_no=rollno
    stud.image=path
    stud.phone_no=phoneno
    stud.email=email
    stud.semester=sem
    stud.gender=gender
    stud.post=post
    stud.place=place
    stud.pin=pin
    stud.dob=dob
    stud.qualification=qualif
    stud.save()
    return HttpResponse('''<script>alert('Student Added');window.location='/admin_view_student#stats'</script>''')

def admin_view_student(request):
    ob=student_table.objects.all()
    print(ob)
    return render(request,'admin/view student.html',{'data':ob})

def admin_view_student_post(request):
    a=request.POST["textfield13"]
    ob=student_table.objects.filter(studname__icontains=a)
    return render(request,'admin/view student.html', {'data': ob,"s":a})

def edit_student(request,id):
    ob =course_table.objects.all()
    ob1= student_table.objects.get(id=id)
    return render(request,'admin/edit_student.html',{"cour":ob,"stud":ob1})

def edit_student_post(request):
    id = request.POST['id']
    course = request.POST['course_name']
    studname = request.POST['textfield1']
    rollno = request.POST['textfield3']
    image = request.POST['file2']
    phoneno = request.POST['textfield5']
    email = request.POST['textfield4']
    sem = request.POST['textfield6']
    gender = request.POST['lab']
    post = request.POST['textfield8']
    place = request.POST['textfield9']
    pin = request.POST['textfield10']
    dob = request.POST['textfield11']
    qualif = request.POST['textfield12']

    ob=student_table.objects.get(id=id)

    ob2 = course_table.objects.get(id=course)

    ob.studname=studname
    ob.COURSE=ob2
    ob.roll_no=rollno
    ob.image=image
    ob.phone_no=phoneno
    ob.email=email
    ob.semester=sem
    ob.gender=gender
    ob.post=post
    ob.place=place
    ob.pin=pin
    ob.dob=dob
    ob.qualification=qualif
    ob.save()
    return HttpResponse('''<script>alert('Edited successfully');window.location='/admin_view_student#stats'</script>''')

def delete_student(request,id):
    stud=student_table.objects.get(id=id).delete()
    return HttpResponse('''<script>alert('Deleted successfully');window.location='/admin_view_student#stats'</script>''')

def admin_add_staff(request):
    ob = login_table.objects.all()
    course = course_table.objects.all()
    dept=department_table.objects.all()
    staf=staff_table.objects.all()
    return render(request,'admin/add staff.html',{'stf':ob,'cour':course,'dep':dept,"staf":staf })

def admin_add_staff_post(request):
    course = request.POST['course_name']
    name = request.POST['textfield']
    prolang = request.POST['textfield10']
    image = request.POST['file2']
    phoneno = request.POST['textfield2']
    email = request.POST['textfield1']
    sem = request.POST['textfield3']
    gender = request.POST['lab']
    post = request.POST['textfield5']
    place = request.POST['textfield6']
    pin = request.POST['textfield7']
    dob = request.POST['textfield8']
    qualif = request.POST['textfield9']

    a=login_table()
    a.username=email
    a.password=phoneno
    a.type='staff'
    a.save()

    staff = staff_table()

    staff.LOGIN =a
    staff.COURSE = course_table.objects.get(id=course)
    staff.name = name
    staff.program_language = prolang
    staff.image = image
    staff.phone_no = phoneno
    staff.email = email
    staff.semester = sem
    staff.gender = gender
    staff.post = post
    staff.place = place
    staff.pin = pin
    staff.dob = dob
    staff.qualification = qualif
    staff.save()
    return HttpResponse('''<script>alert('Staff Added');window.location='/admin_view_staff#stats'</script>''')

def edit_staff(request,id):
    ob=course_table.objects.all()
    ob1=staff_table.objects.get(id=id)
    return render(request,'admin/edit_staff.html', {"cour": ob,"stf": ob1})


def edit_staff_post(request):
     id = request.POST['id']
     course = request.POST['course_name']
     name = request.POST['textfield']
     prolang = request.POST['textfield10']
     image = request.POST['file2']
     phoneno = request.POST['textfield2']
     email = request.POST['textfield1']
     sem = request.POST['textfield3']
     gender = request.POST['lab']
     post = request.POST['textfield5']
     place = request.POST['textfield6']
     pin = request.POST['textfield7']
     dob = request.POST['textfield8']
     qualif = request.POST['textfield9']

     ob=staff_table.objects.get(id=id)
     ob2=course_table.objects.get(id=course)


     ob.COURSE = ob2
     ob.name = name
     ob.program_language = prolang
     ob.image = image
     ob.phone_no = phoneno
     ob.email = email
     ob.semester = sem
     ob.gender = gender
     ob.post = post
     ob.place = place
     ob.pin = pin
     ob.dob = dob
     ob.qualification = qualif
     ob.save()
     return HttpResponse('''<script>alert('Edited successfully');window.location='/admin_view_staff#stats'</script>''')

def delete_staff(request,id):
    ob=staff_table.objects.get(id=id).delete()
    return HttpResponse('''<script>alert('Deleted successfully');window.location='/admin_view_staff#stats'</script>''')


def admin_view_staff(request):
    ob=staff_table.objects.all()
    return render(request,'admin/view staff.html',{'data':ob})

def admin_view_staff_post(request):
    a=request.POST['textfield']
    ob = staff_table.objects.filter(name__icontains=a)
    return render(request, 'admin/view staff.html', {'data': ob,"s":a})


def admin_subject_allocation(request):
    ob=subject_table.objects.all()
    ob1=staff_table.objects.all()
    return render(request,'admin/subject allocation.html',{'sub':ob,'stf':ob1})

def admin_subject_allocation_post(request):
    subject=request.POST['subject']
    staff=request.POST['name']
    date = request.POST['textfield']

    sub=subject_allocation_to_staff_table()
    sub.SUBJECT=subject_table.objects.get(id=subject)
    sub.STAFF=staff_table.objects.get(id=staff)
    sub.date=date
    sub.save()
    return HttpResponse('''<script>alert('Subject allocated');window.location='admin_subject_allocation#stats'</script>''')

def admin_view_complaint(request):
    ob=complaint_student_table.objects.all()
    return render(request, 'admin/view complaint.html', {'data':ob})

# def admin_view_feedback(request):
#     ob=feedback_table.objects.all()
#     return render(request, 'admin/view feedback.html', {'data':ob})


def send_reply(request,id):
    com = complaint_student_table.objects.get(id=id)
    request.session['cmp'] = id
    return render(request, 'admin/send reply.html', {'com':com})

def send_reply_post(request):
    reply = request.POST['textfield2']
    com = complaint_student_table.objects.get(id=request.session['cmp'])
    com.reply = reply
    com.save()
    return HttpResponse('''<script>alert('Replied');window.location='/admin_view_complaint#stats'</script>''')

def admin_home_page(request):
    return render(request,'admin/indexadmin.html')

def admin_home_page_post(request):
    return HttpResponse("ok")

def lab_assistant_home_page(request):
    return render(request,'Lab assisstant/indexla.html')

def lab_assistant_home_page_post(request):
    return HttpResponse("ok")

def lab_assistant_add_system(request):
    ob = assign_lab_table.objects.filter(LAB_ASST__LOGIN__id=request.session['lid'])
    return render(request,'Lab assisstant/Add system.html',{"data":ob})

def lab_assistant_add_system_post(request):
    lab=request.POST['select']
    sys=request.POST['textfield']
    pas=request.POST['textfield1']
    pro=request.POST['textfield2']
    ram=request.POST['textfield3']
    ssd = request.POST['textfield4']
    hdd = request.POST['textfield5']
    date=request.POST['textfield6']

    system=system_table()
    system.LAB=lab_table.objects.get(id=lab)
    system.system_no=sys
    system.password=pas
    system.processor=pro
    system.RAM =ram
    system.SSD=ssd
    system.HDD=hdd
    system.date=date
    system.save()
    return HttpResponse('''<script>alert('System Added');window.location='/lab_assistant_view_system_in_lab#stats'</script>''')

def edit_system(request,id):
   sys=system_table.objects.get(id=id)
   request.session["id"]=id
   ob=assign_lab_table.objects.filter(LAB_ASST__LOGIN__id=request.session['lid'])
   return render(request,'Lab assisstant/edit system.html',{'sys':sys,'data':ob})

def edit_system_post(request):
    lab = request.POST['select']
    sys = request.POST['textfield']
    pas = request.POST['textfield1']
    pro = request.POST['textfield2']
    ram = request.POST['textfield3']
    ssd = request.POST['textfield4']
    hdd = request.POST['textfield5']
    date = request.POST['textfield6']

    system = system_table.objects.get(id=request.session["id"])
    system.LAB = lab_table.objects.get(id=lab)
    system.system_no = sys
    system.password = pas
    system.processor = pro
    system.RAM = ram
    system.SSD = ssd
    system.HDD = hdd
    system.date = date
    system.save()
    return HttpResponse('''<script>alert('Edited successfully');window.location='/lab_assistant_view_system_in_lab#stats'</script>''')

def delete_system(request,id):
    sys=system_table.objects.get(id=id).delete()
    return HttpResponse('''<script>alert('Deleted successfully');window.location='/lab_assistant_view_system_in_lab#stats'</script>''')

def lab_assistant_view_system_in_lab(request):
    ob = assign_lab_table.objects.filter(LAB_ASST__LOGIN__id=request.session['lid'])
    labids=[]
    for i in ob:
        labids.append(i.LAB.id)
    ob1=system_table.objects.filter(LAB__id__in=labids)
    return render(request,'Lab assisstant/view system in lab.html',{"data":ob1})

def lab_assistant_view_system_in_lab_post(request):
    a = request.POST['textfield']
    ob = system_table.objects.filter(system_no__icontains=a)
    return render(request, 'Lab assisstant/view system in lab.html', {'data': ob, "s": a})

def lab_assistant_system_allocation(request):
    ob=student_system_allocate.objects.all()
    ids=[]
    for i in ob:
        ids.append(i.STUD_ID.id)
    ob = student_table.objects.exclude(id__in=ids)
    return render(request, 'Lab assisstant/system allocation.html', {'data': ob})

def lab_assistant_system_allocation_post(request):
    ob = student_system_allocate.objects.all()
    ids = []
    for i in ob:
        ids.append(i.STUD_ID.id)
    a = request.POST["textfield"]
    ob = student_table.objects.filter(studname__icontains=a).exclude(id__in=ids)
    return render(request, 'Lab assisstant/system allocation.html', {'data': ob, "s": a})

def allocate_system(request,id):
    request.session["studid"]=id
    ob=assign_lab_table.objects.filter(LAB_ASST__LOGIN=request.session["lid"])
    if len(ob)>0:
        obb=assign_lab_table.objects.get(LAB_ASST__LOGIN=request.session["lid"])

        sys=system_table.objects.filter(LAB=obb.LAB.id)
    return render(request,'Lab assisstant/allocate system.html',{"sys":sys})
    # return HttpResponse('''<script>alert('System allocated');window.location='/lab_assistant_system_allocation'</script>''')

def allocate_system_post(request):
    systemid=request.POST['system']
    ob1=student_system_allocate()
    ob1.SYSTEM_ID_id=systemid
    ob1.STUD_ID_id=request.session["studid"]
    ob1.date=datetime.datetime.now().date()
    ob1.save()
    return HttpResponse('''<script>alert('System allocated');window.location='/lab_assistant_system_allocation#stats'</script>''')

def lab_assistant_view_allocated_system(request):
    ob = assign_lab_table.objects.filter(LAB_ASST__LOGIN=request.session["lid"])
    if len(ob) > 0:
        obb = assign_lab_table.objects.get(LAB_ASST__LOGIN=request.session["lid"])

    ob=student_system_allocate.objects.filter(SYSTEM_ID__LAB=obb.LAB.id)
    return render(request,'Lab assisstant/view allocated system.html', {'data': ob})


def lab_assistant_view_allocated_lab(request):
    ob=assign_lab_table.objects.filter(LAB_ASST__LOGIN__id=request.session['lid'])
    return render(request,'Lab assisstant/view allocated lab.html',{"data":ob})

def lab_assistant_view_allocated_lab_post(request):
    a = request.POST['textfield']
    ob = assign_lab_table.objects.filter(LAB__Lab_no__icontains=a)
    return render(request, 'Lab assisstant/view allocated lab.html',{'data': ob,"s": a})


def lab_assistant_view_assigned_lab_subject_to_staff(request):
    return render(request,'admin/view system details.html')
def lab_assistant_view_assigned_lab_subject_to_staff_post(request):
    return HttpResponse("ok")

def lab_assistant_view_exam_schedule(request):
    ob=exam_schedule_table.objects.all()
    return render(request,'Lab assisstant/view exam schedule.html',{'data':ob})

def lab_assistant_view_exam_schedule_post(request):
    a = request.POST['textfield']
    ob = exam_schedule_table.objects.filter(exam_name__icontains=a)
    return render(request, 'Lab assisstant/view exam schedule.html', {'data': ob, "s": a})

def lab_assistant_view_student(request):
    ob = student_table.objects.all()
    return render(request,'Lab assisstant/View Student.html',{'data':ob})

def lab_assistant_view_student_post(request):
    a = request.POST["textfield"]
    ob = student_table.objects.filter(studname__icontains=a)
    return render(request, 'Lab assisstant/View Student.html',{'data': ob, "s": a})

def staff_home_page(request):
    return render(request,'staff/indexstaff.html')

def staff_home_page_post(request):
    return HttpResponse("ok")

def staff_add_reply(request,id):
    request.session['cid']=id
    return render(request, 'staff/stf add reply.html')

def staff_add_reply_post(request):

    reply=request.POST['textfield2']

    rep=complaint_student_table.objects.get(id=request.session['cid'])

    rep.reply=reply
    rep.save()
    return HttpResponse('''<script>alert('Reply Added');window.location='/staff_view_complaints#stats'</script>''')

def staff_add_student(request):
    course = course_table.objects.all()
    stud = student_table.objects.all()
    return render(request, 'staff/stf add student.html', {'cour': course, "stud": stud})

def staff_add_student_post(request):
    course = request.POST['course_name']
    studname = request.POST['textfield1']
    rollno = request.POST['textfield3']
    image = request.FILES['file2']
    phoneno = request.POST['textfield5']
    email = request.POST['textfield4']
    sem = request.POST['textfield6']
    gender = request.POST['lab']
    post = request.POST['textfield8']
    place = request.POST['textfield9']
    pin = request.POST['textfield10']
    dob = request.POST['textfield11']
    qualif = request.POST['textfield12']

    ob = login_table()
    ob.username = email
    ob.password = phoneno
    ob.type='student'
    ob.save()
    stud = student_table()

    stud.LOGIN = ob
    stud.COURSE = course_table.objects.get(id=course)
    stud.studname = studname
    stud.roll_no = rollno
    stud.image = image
    stud.phone_no = phoneno
    stud.email = email
    stud.semester = sem
    stud.gender =gender
    stud.post = post
    stud.place = place
    stud.pin = pin
    stud.dob = dob
    stud.qualification = qualif
    stud.save()
    return HttpResponse('''<script>alert('Student Added');window.location='/staff_view_student#stats'</script>''')

def staff_view_student(request):
    ob = student_table.objects.all()
    return render(request, 'staff/stf view student.html', {'data': ob})

def staff_view_student_post(request):
    a = request.POST["textfield13"]
    ob = student_table.objects.filter(studname__icontains=a)
    return render(request, 'staff/stf view student.html', {'data': ob, "s": a})

def staff_edit_student(request,id):
    ob = course_table.objects.all()
    ob1 = student_table.objects.get(id=id)
    return render(request,'staff/staff edit student.html',{"cour": ob, "stud": ob1})

def staff_edit_student_post(request):
    id = request.POST['id']
    course = request.POST['course_name']
    studname = request.POST['textfield1']
    rollno = request.POST['textfield3']
    image = request.POST['file2']
    phoneno = request.POST['textfield5']
    email = request.POST['textfield4']
    sem = request.POST['textfield6']
    gender = request.POST['lab']
    post = request.POST['textfield8']
    place = request.POST['textfield9']
    pin = request.POST['textfield10']
    dob = request.POST['textfield11']
    qualif = request.POST['textfield12']

    ob = student_table.objects.get(id=id)

    ob2 = course_table.objects.get(id=course)

    ob.studname = studname
    ob.COURSE = ob2
    ob.roll_no = rollno
    ob.image = image
    ob.phone_no = phoneno
    ob.email = email
    ob.semester = sem
    ob.gender = gender
    ob.post = post
    ob.place = place
    ob.pin = pin
    ob.dob = dob
    ob.qualification = qualif
    ob.save()
    return HttpResponse('''<script>alert('Edited successfully');window.location='/staff_view_student#stats'</script>''')

def staff_delete_student(request,id):
    stud=student_table.objects.get(id=id).delete()
    return HttpResponse('''<script>alert('Deleted successfully');window.location='/staff_view_student#stats'</script>''')

def staff_view_allocated_subject(request):
    ob=subject_allocation_to_staff_table.objects.filter(STAFF__LOGIN__id=request.session['lid'])
    return render(request,'staff/view allocated subject.html',{"data":ob})

def staff_view_allocated_subject_post(request):
    a = request.POST["textfield"]
    ob = subject_allocation_to_staff_table.objects.filter(STAFF__LOGIN__id=request.session['lid'],SUBJECT__subject__icontains=a)
    return render(request,'staff/view allocated subject.html',{'data': ob,"s": a})

def staff_view_complaints(request):
    ob=complaint_student_table.objects.all()
    return render(request,'staff/view complaints.html',{'data': ob})

def staff_view_complaints_post(request):
    a = request.POST['textfield']
    ob = lab_assistant_table.objects.filter(name__icontains=a)
    return render(request, 'staff/view complaints.html', {'data': ob, "s": a})

def staff_view_feedback(request):
    ob=feedback_table.objects.all()
    return render(request,'staff/view feedbacks.html',{'data': ob})

def staff_view_feedback_post(request):
    a = request.POST['textfield']
    ob = lab_assistant_table.objects.filter(name__icontains=a)
    return render(request, 'staff/view feedbacks.html', {'data': ob, "s": a})


def staff_view_exam_schedule(request):
    ob = exam_schedule_table.objects.all()
    return render(request,'staff/view exam sched.html', {'data': ob})

def staff_view_exam_schedule_post(request):
    a = request.POST['textfield']
    ob = exam_schedule_table.objects.filter(exam_name__icontains=a)
    return render(request,'staff/view exam sched.html',{'data': ob, "s": a})

def system_no(request):
    return render(request,'Lab assisstant/systemno.html')
#
#
def system_no_code(request):
    btn = request.POST['btn']
    a = request.POST['textfield']
    if btn == "Start":

        ob=system_table.objects.get(system_no=a)
        get_memory_info(ob.id)
        return  redirect('/system_no')
    elif btn== "View":
        ob = memory.objects.all()
        return render(request,'Lab assisstant/ViewSystemUtil.html',{'data': ob})


#
#
# requests.get(
#     "http://" + ip + "/insert_memmory?id=" + str(a) + "&tm=" + str(tm) + "&am=" + am + "&um=" + um + "&mu=" + mu)


def insert_memory(request):
    a = request.GET['id']
    tm = request.GET['tm']
    am = request.GET['am']
    um = request.GET['um']
    mu = request.GET['mu']
    # get_memory_info(a)
    ob=memory()
    ob.total_memory=tm
    ob.avail_memory=am
    ob.used_memory=um
    ob.memory_percent=mu
    ob.SYSTEM=system_table.objects.get(id=a)
    ob.save()

    return  JsonResponse({"task":"ok"})



def index():
    return HttpResponse("okk")


def dw(request):
    path = request.GET["p"]
    file_path = "static/" + path
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{path}"'
        return response

def select(request):
    path = request.GET["p"]
    result = screenshot_table.objects.get(sid=path)

    if result:
        result.delete()
        return HttpResponse("ok")
    else:
        return HttpResponse("na")

def insprocess(request):
    lis = ['System Idle Process', 'System', 'Registry', 'smss.exe', 'wininit.exe', 'services.exe', 'lsass.exe', 'wsc_proxy.exe', 'Memory Compression', 'igfxCUIService.exe', 'AvastSvc.exe', 'aswToolsSvc.exe', 'dasHost.exe', 'spoolsv.exe', 'IntelCpHDCPSvc.exe', 'novapdfs.exe', 'SecurityHealthService.exe']
    sid = request.GET["p"]
    pr = request.GET["pr"]

    if pr not in lis:
        process_table.objects.filter(SYSTEM__id=sid, process=pr).delete()
        # Process.objects.create(sid=sid, process=pr)
        ob=process_table()
        ob.SYSTEM=system_table.objects.get(id=sid)
        ob.process=pr
        ob.save()
        return HttpResponse("ok")
    return HttpResponse("ok")



def process(request):
    path = request.GET["p"]
    ob=log_table.objects.filter(SYSTEM_ID__id=path,date=datetime.datetime.today())

    print(ob,"------")
    if len(ob)==0:
        ob=log_table()
        ob.SYSTEM_ID=system_table.objects.get(id=path)
        ob.login_time=datetime.datetime.today()
        ob.logout_time=datetime.datetime.today()
        ob.date = datetime.datetime.today()
        ob.save()
    else:
        ob=ob[0]
        ob.logout_time=datetime.datetime.today()
        ob.save()
    result = command_table.objects.filter(SYSTEM__id=path)
    res = "#".join([item.process for item in result])

    command_table.objects.filter(SYSTEM__id=path).delete()
    return HttpResponse(res)

def sd(request):
    path = request.GET["p"]
    result = command_table.objects.filter(sid=path).first()
    res_str = "#".join(result.process)

    command_table.objects.filter(sid=path).delete()
    return HttpResponse(res_str)

def rs(request):
    path = request.GET["p"]
    result = command_table.objects.filter(sid=path).first()
    res_str = "#".join(result.process)

    command_table.objects.filter(sid=path).delete()
    return HttpResponse(res_str)

def bgp(request):
    path = request.GET["p"]
    result = command_table.objects.filter(sid=path).first()
    res_str = "#".join(result.process)

    command_table.objects.filter(sid=path).delete()
    return HttpResponse(res_str)

def up(request):
    fn = request.GET["cp"]
    path = request.GET["sc"]
    id = request.GET["id"]






    ob=screenshot_table()
    ob.SYSTEM=system_table.objects.get(id=id)
    ob.screenshot=path
    ob.campic=fn
    ob.date=datetime.datetime.today()
    ob.status='pending'
    ob.save()

    return HttpResponse("ok")

def upn(request):
    fn = request.GET["cp"]
    path = request.GET["sc"]
    id = request.GET["id"]
    p = request.GET["p"]



    ob=notification_table.objects.filter(SYSTEM__id=id,date=datetime.datetime.today(),status='pending',process=p)

    if len(ob)==0:
        import winsound
        frequency = 2500  # Set Frequency To 2500 Hertz
        duration = 1000  # Set Duration To 1000 ms == 1 second
        winsound.Beep(frequency, duration)

        ob=notification_table()
        ob.SYSTEM=system_table.objects.get(id=id)
        ob.screenshot=path
        ob.camera_image=fn
        ob.process=p
        ob.date=datetime.datetime.today()
        ob.status='pending'
        ob.save()

    return HttpResponse("ok")


def notification_details(request):
    ob = notification_table.objects.all()
    return render(request, 'Lab assisstant/notifdetails.html', {'data': ob})

def log_details(request):
    ob = log_table.objects.all()
    return render(request, 'Lab assisstant/logdetails.html', {'data': ob})


def up1(request):
    # fn = request.GET["fn"]x
    # path = request.GET["p"]
    #
    # image_string = path.decode('base64')
    # file_path = "static/media/" + fn
    #
    # with open(file_path, "wb") as fh:
    #     fh.write(image_string)
    img=request.FILES['image']
    fs=FileSystemStorage()
    fs.save(img.name,img)

    return HttpResponse("ok")

def delete_memory(request):
    ob=memory.objects.all().delete()
    return HttpResponse('''<script>alert('success');window.location='/system_no#stats'</script>''')


def bgprocess(request,id):
    request.session['bid']=id

    ob = process_table.objects.filter(SYSTEM__id=id)
    for i in ob:
        i.delete()
    ob=command_table()
    ob.SYSTEM=system_table.objects.get(id=id)
    ob.process="bgp"
    ob.save()
    return redirect("/r_bgprocess/"+str(id))

def search(request):
    a = request.POST["textfield"]
    ob = process_table.objects.filter(process__icontains=a,SYSTEM__id=request.session['sid'])
    return render(request, 'lab assisstant/bgprocess.html', {'data': ob,"a":a})



def r_bgprocess(request,id):
    request.session['bid']=id

    ob = process_table.objects.filter(SYSTEM__id=request.session['sid'])
    return render(request,'lab assisstant/bgprocess.html', {'data': ob})

def closefn(request,id):
    try:
        ob = process_table.objects.get(SYSTEM__id=request.session['sid'],process=id)
        ob.delete()
    except:
        pass
    ob = command_table()
    ob.SYSTEM = system_table.objects.get(id=request.session['sid'])
    ob.process = id
    ob.save()
    return HttpResponse('''<script>alert('success');window.location="/r_bgprocess/'''+str(request.session['sid'])+ '''#stats"</script>''')


def manage(request,id):
    request.session['sid']=id
    return render(request,'lab assisstant/manage.html')

def screenshot(request,id):
    request.session['bid'] = id
    ob = command_table()
    ob.SYSTEM = system_table.objects.get(id=id)
    ob.process = "sc"
    ob.save()
    ob = screenshot_table.objects.filter(SYSTEM__id=id).order_by("-id")
    print(ob)
    return render(request, 'lab assisstant/screenshot.html', {'data': ob})


def r_screenshot(request,id):
    request.session['bid']=id

    ob = screenshot_table.objects.filter(SYSTEM__id=id).order_by("-id")
    print(ob)
    return render(request, 'lab assisstant/screenshot.html', {'data': ob})

def shutdown(request,id):
    request.session['bid'] = id
    ob = command_table()
    ob.SYSTEM = system_table.objects.get(id=id)
    ob.process = "sd"
    ob.save()
    return HttpResponse(
        '''<script>alert('success');window.location="/manage/''' + str(request.session['sid']) + '''#stats"</script>''')

def restart(request,id):
    request.session['bid'] = id
    ob = command_table()
    ob.SYSTEM = system_table.objects.get(id=id)
    ob.process = "rs"
    ob.save()
    return HttpResponse(
        '''<script>alert('success');window.location="/manage/''' + str(request.session['sid']) + '''#stats"</script>''')










# --------------------------------------------------------------------
def android_login(request):
    un=request.POST['username']
    pwd=request.POST['password']
    a = login_table.objects.filter(username=un, password=pwd)
    if a.exists():
        var = login_table.objects.get(username=un, password=pwd)
        print(un, pwd)
        if var.type == 'student':
            return JsonResponse({"status":'ok','lid':str(var.id),'type':var.type})
        else:
            return JsonResponse({'status':'notok'})

    else:
        return JsonResponse({'status': 'notok'})


def student_view_profile(request):
    lid = request.POST['lid']
    profile = student_table.objects.get(LOGIN=lid)
    data = {
        'id':profile.id,
        'studname':profile.studname,
        'course_name':profile.COURSE.course_name,
        'roll_no':str(profile.roll_no),
        'image':profile.image.url,
        'phone_no':str(profile.phone_no),
        'email':profile.email,
        'semester':profile.semester,
        'gender':profile.gender,
        'post':profile.post,
        'place':profile.place,
        'pin':str(profile.pin),
        'dob':str(profile.dob),
        'qualification':profile.qualification,
    }
    return JsonResponse({
        'status':'ok','profile':[data]
    })


def view_lab(request):
    lab = lab_table.objects.all()
    labs = []
    for i in lab:
        labs.append({
            'id':i.id,
            'Lab_no':str(i.Lab_no),
            'Floor_no':str(i.Floor_no),
        })
    print(labs)
    return JsonResponse({'status':'ok','labs':labs})

#
# def view_subject(request):
#     sub = subject_table.objects.all()
#     subs = []
#     for i in sub:
#         subs.append({
#             'id': i.id,
#             'course_name': i.COURSE.course_name,
#             'subject': i.subject,
#             'semester': i.semester,
#             'syllabus': i.syllabus.url if i.syllabus else None,
#         })
#     return JsonResponse({'status': 'ok', 'subs': subs})
def view_subject(request):
    sub = subject_table.objects.all()
    subs = []
    for i in sub:
        subs.append({
            'id': i.id,
            'course_name': i.COURSE.course_name,
            'subject': i.subject,
            'semester': i.semester,
            'syllabus': i.syllabus.url[1:] if i.syllabus else None,
        })
    return JsonResponse({'status': 'ok', 'subs': subs})



def view_exam_details(request):
    exm = exam_schedule_table.objects.all()
    exms = []
    for i in exm:
        exms.append({
            'id': i.id,
            'name': i.STAFF.name,
            'subject': i.SUBJECT.subject,
            'date': str(i.date),
            'time': str(i.time),
            'exam_name': i.exam_name,
            'duration': i.duration,
            'details': i.details,
            'syllabus': i.syllabus.url[1:] if i.syllabus else None,
        })
        print(exms)
    return JsonResponse({'status': 'ok', 'exms': exms})


def view_system_info(request):
    sys = system_table.objects.all()
    syss = []
    for i in sys:
        syss.append({
            'id': i.id,
            'system_no': str(i.system_no),
            'password': i.password,
            'LAB': str(i.LAB.Lab_no),
            'processor': i.processor,
            'RAM': i.RAM,
            'SSD': i.SSD,
            'HDD': i.HDD,
            'date': str(i.date),
        })
        print(syss)
    return JsonResponse({'status': 'ok', 'data': syss})


def view_reply(request):
    lid=request.POST['lid']
    cmp = complaint_student_table.objects.filter(STUDENT__LOGIN_id=lid)
    cmps = []
    for i in cmp:
        cmps.append({
            'id': i.id,
            'name': i.STAFF.name,
            'complaint': i.complaint,
            'reply': i.reply,
            'date': str(i.date),
        })
    return JsonResponse({'status': 'ok', 'cmps': cmps})


def send_complaint(request):
    lid=request.POST['lid']
    sid=request.POST['sid']
    complaint=request.POST['complaint']
    a=complaint_student_table()
    a.complaint=complaint
    a.reply='pending'
    a.date=datetime.datetime.now().today()
    a.STAFF=staff_table.objects.get(id=sid)
    a.STUDENT=student_table.objects.get(LOGIN_id=lid)
    a.save()
    return JsonResponse({'status':'ok'})

def viewstaff(request):
    ob=staff_table.objects.all()
    print(ob,"HHHHHHHHHHHHHHH")
    mdata=[]
    for i in ob:
        data={'name':i.name,'id':i.id}
        mdata.append(data)
        print(mdata)
    return JsonResponse({"status":"ok","data":mdata})



def send_feedback(request):
    fbk=feedback_table.objects.all()
    fbks=[]
    for i in fbk:
        fbks.append({
            'id': i.id,
            'studname': i.STUDENT.studname,
            'feedback': i.feedback.name,
            'name': i.STAFF.name,
            'date': str(i.date),
        })
    return JsonResponse({'status': 'ok', 'fbks': fbks})



def student_send_feedback(request):
    lid=request.POST['lid']
    sid=request.POST['sid']
    feedback=request.POST['feedback']
    date=datetime.datetime.now().today()

    a=feedback_table()
    a.STUDENT=student_table.objects.get(LOGIN_id=lid)
    a.date=date
    a.feedback=feedback
    a.STAFF=staff_table.objects.get(id=sid)
    a.save()
    return JsonResponse({'status': 'ok'})

def user_view_profile(request):
    lid=request.POST['lid']
    ob=student_table.objects.get(LOGIN__id=lid)

    return JsonResponse({'status': 'ok',"name":ob.studname,"COURSE":ob.COURSE.course_name,"roll_no":ob.roll_no,"image":ob.image.url[1:],"phone_no":ob.phone_no,"email":ob.email,"semester":ob.semester,"gender":ob.gender,"post":ob.post,"place":ob.place,"pin":ob.pin,"dob":ob.dob,"qualification":ob.qualification})

def update_profile(request):
    lid = request.POST['lid']
    studname = request.POST['name']
    phone_no = request.POST['phone_no']
    email = request.POST['email']

    a= student_table.objects.get(LOGIN_id=lid)
    a.studname = studname
    a.phone_no = phone_no
    a.email = email
    a.save()
    return JsonResponse({'status': 'ok'})

def forgot_password(request):
    print(request.POST)
    try:
        username = request.POST['username']
        s = login_table.objects.get(username=username)

        # If user is not found or doesn't exist, return an invalid response
        if s is None:
            return JsonResponse({"status": "Invalid username"})
        else:
            # Fetch the Organization associated with the Login object
            try:
                student = student_table.objects.get(LOGIN=s)
                email_address = student.email  # Assuming email is in Organization model
            except student_table.DoesNotExist:
                return JsonResponse({"status": "Email not available in Organization"})

            if not email_address:
                return JsonResponse({"status": "Email not available"})

            # Create the email content
            subject = 'SMART LAB Password'
            message = f"Your password: {s.password}"
            from_email = 'anniet5745@gmail.com'

            try:
                # Send the email with the password to the user's email address
                send_mail(subject, message, from_email, [email_address])
                return JsonResponse({"status": "ok"})
            except Exception as e:
                print(f"Error sending email: {str(e)}")
                return JsonResponse({"status": "Email sending failed"})
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({"status": "Error occurred"})

def view_coursename(request):
    ob = course_table.objects.all()
    mdata = []
    for i in ob:
        data = {'course_name': i.course_name, 'id': i.id}
        mdata.append(data)
    return JsonResponse({"status": "ok", "data": mdata})


def view_gender(request):
    ob = student_table.objects.all()
    mdata = []
    for i in ob:
        data = {'gender': i.gender, 'id': i.id}
        mdata.append(data)
    return JsonResponse({"status": "ok", "data": mdata})


# def Androidregistration(request):
#     print(request.POST,"jjjjjjj")
#     print(request.FILES,"jjjjjjj")
#     username = request.POST['username']
#     password = request.POST['password']
#     name = request.POST['studname']
#     email = request.POST['email']
#     phone = request.POST['phone_no']
#     place = request.POST['place']
#     pin = request.POST['pin']
#     COURSE = request.POST['course']
#     roll_no = request.POST['roll_no']
#     semester = request.POST['semester']
#     gender = request.POST['gender']
#     post = request.POST['post']
#     dob = request.POST['dob']
#     qualification = request.POST['qualification']
#     image = request.FILES['image']
#     fs = FileSystemStorage()
#     fp = fs.save(image.name,image)
#
#
#     log = login_table()
#     log.username = username
#     log.password = password
#     log.type = 'student'
#     log.save()
#
#     u_obj = student_table()
#     u_obj.studname = name
#     u_obj.email = email
#     u_obj.phone_no = phone
#     u_obj.place = place
#     u_obj.pin = pin
#     u_obj.COURSE = course_table.objects.get(course_name=COURSE)
#
#     u_obj.roll_no = roll_no
#     u_obj.image = fp
#     u_obj.semester = semester
#     u_obj.gender = gender
#     u_obj.post = post
#     u_obj.dob = dob
#     u_obj.qualification = qualification
#
#     u_obj.LOGIN = log
#     u_obj.save()
#     print('uuuuuuuuuuuuuuuu')
#     return JsonResponse({'status':'ok'})
#


def Androidregistration(request):
    print(request.POST, "jjjjjjj")
    print(request.FILES, "jjjjjjj")

    # username = request.POST['username']
    password = request.POST['password']
    name = request.POST['studname']
    email = request.POST['email']
    phone = request.POST['phone_no']
    place = request.POST['place']
    pin = request.POST['pin']
    COURSE = request.POST['course']
    roll_no = request.POST['roll_no']
    semester = request.POST['semester']
    gender = request.POST['gender']
    post = request.POST['post']
    dob = request.POST['dob']
    qualification = request.POST['qualification']
    image = request.FILES['image']

    obxx=student_table.objects.filter(roll_no__icontains=roll_no)

    print(obxx)

    print(roll_no,"=============")
    if obxx.exists():
        return JsonResponse({'status': 'error', 'message': 'Roll number already registered'})



    fs = FileSystemStorage()
    fp = fs.save(image.name, image)

    log = login_table()
    log.username = email
    log.password = password
    log.type = 'student'
    log.save()

    # Create and save student entry
    u_obj = student_table()
    u_obj.studname = name
    u_obj.email = email
    u_obj.phone_no = phone
    u_obj.place = place
    u_obj.pin = pin
    u_obj.COURSE = course_table.objects.get(course_name=COURSE)
    u_obj.roll_no = roll_no
    u_obj.image = fp
    u_obj.semester = semester
    u_obj.gender = gender
    u_obj.post = post
    u_obj.dob = dob
    u_obj.qualification = qualification
    u_obj.LOGIN = log
    u_obj.save()

    print('uuuuuuuuuuuuuuuu')
    return JsonResponse({'status': 'ok'})

















