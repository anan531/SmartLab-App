from django.db import models

# Create your models here.

class login_table(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    type=models.CharField(max_length=100)

class department_table(models.Model):
    department_name=models.CharField(max_length=100)
    details=models.CharField(max_length=500)


class course_table(models.Model):
    DEPT=models.ForeignKey(department_table,on_delete=models.CASCADE)
    course_name=models.CharField(max_length=100)
    details=models.CharField(max_length=500)

class staff_table(models.Model):
    LOGIN = models.ForeignKey(login_table, on_delete=models.CASCADE)
    COURSE=models.ForeignKey(course_table,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    # DEPT=models.ForeignKey(department_table,on_delete=models.CASCADE)
    email=models.CharField(max_length=100)
    phone_no=models.BigIntegerField()
    image=models.FileField()
    semester=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    post=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    pin=models.IntegerField()
    dob=models.DateField()
    qualification=models.CharField(max_length=100)
    program_language = models.CharField(max_length=100)


class lab_table(models.Model):
    Lab_no=models.IntegerField()
    Floor_no=models.IntegerField()


class subject_table(models.Model):
    COURSE=models.ForeignKey(course_table,on_delete=models.CASCADE)
    subject=models.CharField(max_length=100)
    semester=models.CharField(max_length=100)
    syllabus=models.FileField()

class lab_assistant_table(models.Model):
    LOGIN=models.ForeignKey(login_table,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    phone_no=models.BigIntegerField()
    post=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    pin=models.IntegerField()
    qualification=models.CharField(max_length=100)
    image=models.FileField()
    dob=models.DateField(max_length=100)


class assign_lab_table(models.Model):
    LAB_ASST=models.ForeignKey(lab_assistant_table,on_delete=models.CASCADE)
    LAB=models.ForeignKey(lab_table,on_delete=models.CASCADE)
    date=models.DateField()


class exam_schedule_table(models.Model):
    SUBJECT=models.ForeignKey(subject_table,on_delete=models.CASCADE)
    STAFF=models.ForeignKey(staff_table,on_delete=models.CASCADE)
    date=models.DateField()
    time=models.TimeField()
    exam_name=models.CharField(max_length=100)
    duration=models.CharField(max_length=100)
    details=models.CharField(max_length=500)
    syllabus=models.FileField()


class system_table(models.Model):
    system_no=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    LAB=models.ForeignKey(lab_table,on_delete=models.CASCADE)
    processor=models.CharField(max_length=100)
    RAM=models.CharField(max_length=100)
    SSD=models.CharField(max_length=100)
    HDD=models.CharField(max_length=100)
    date=models.DateField()


class student_table(models.Model):
    LOGIN=models.ForeignKey(login_table,on_delete=models.CASCADE)
    studname=models.CharField(max_length=100)
    COURSE=models.ForeignKey(course_table,on_delete=models.CASCADE)
    roll_no=models.CharField(max_length=100)
    image=models.FileField()
    phone_no=models.BigIntegerField()
    email=models.CharField(max_length=100)
    semester=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    post=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    pin=models.IntegerField()
    dob=models.DateField()
    qualification=models.CharField(max_length=100)



class subject_allocation_to_staff_table(models.Model):
    SUBJECT=models.ForeignKey(subject_table,on_delete=models.CASCADE)
    STAFF=models.ForeignKey(staff_table,on_delete=models.CASCADE)
    date=models.DateField()



class complaint_student_table(models.Model):
    STUDENT=models.ForeignKey(student_table,on_delete=models.CASCADE)
    STAFF=models.ForeignKey(staff_table,on_delete=models.CASCADE)
    complaint=models.CharField(max_length=500)
    reply=models.CharField(max_length=500)
    date=models.DateField()


class feedback_table(models.Model):
    STUDENT=models.ForeignKey(student_table,on_delete=models.CASCADE)
    feedback=models.CharField(max_length=500)
    date=models.DateField()
    STAFF=models.ForeignKey(staff_table,on_delete=models.CASCADE)


class doubt_table(models.Model):
    STUDENT=models.ForeignKey(complaint_student_table,on_delete=models.CASCADE)
    STAFF=models.ForeignKey(staff_table,on_delete=models.CASCADE)
    doubt=models.CharField(max_length=100)
    date=models.DateField()
    reply=models.CharField(max_length=100)
    image=models.FileField()


class notification_table(models.Model):
    SYSTEM=models.ForeignKey(system_table,on_delete=models.CASCADE)
    screenshot=models.FileField()
    camera_image=models.FileField()
    process=models.CharField(max_length=100)
    date=models.DateField()
    status=models.CharField(max_length=100)


class command_table(models.Model):
    SYSTEM=models.ForeignKey(system_table,on_delete=models.CASCADE)
    process=models.CharField(max_length=100)


class process_table(models.Model):
    SYSTEM=models.ForeignKey(system_table,on_delete=models.CASCADE)
    process=models.CharField(max_length=100)

class screenshot_table(models.Model):
    SYSTEM=models.ForeignKey(system_table,on_delete=models.CASCADE)
    screenshot=models.FileField()
    campic=models.FileField()
    date=models.DateField()
    status=models.CharField(max_length=100)

class student_system_allocate(models.Model):
    SYSTEM_ID=models.ForeignKey(system_table,on_delete=models.CASCADE)
    STUD_ID=models.ForeignKey(student_table,on_delete=models.CASCADE)
    date=models.DateField()

class memory(models.Model):
    SYSTEM = models.ForeignKey(system_table, on_delete=models.CASCADE)
    total_memory=models.CharField(max_length=500)
    avail_memory=models.CharField(max_length=500)
    used_memory=models.CharField(max_length=500)
    memory_percent=models.CharField(max_length=500)

class log_table(models.Model):
    SYSTEM_ID=models.ForeignKey(system_table,on_delete=models.CASCADE)
    login_time=models.TimeField()
    logout_time=models.TimeField()
    date=models.DateField()

