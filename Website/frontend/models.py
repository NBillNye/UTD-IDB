# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Class(models.Model):
    classname = models.CharField(db_column='ClassName', max_length=50)  # Field name made lowercase.
    classid = models.IntegerField(db_column='ClassID', primary_key=True)  # Field name made lowercase.
    sectionnumber = models.IntegerField(db_column='sectionNumber')  # Field name made lowercase.
    size = models.IntegerField(db_column='Size')  # Field name made lowercase.
    professor_professornetid = models.ForeignKey('Professor', models.DO_NOTHING, db_column='Professor_ProfessorNetID')  # Field name made lowercase.
    classnumber = models.CharField(db_column='ClassNumber', max_length=10)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Class'


class Enrollment(models.Model):
    idenrollment = models.AutoField(db_column='idEnrollment', primary_key=True)  # Field name made lowercase.
    student_netid = models.ForeignKey('Student', models.DO_NOTHING, db_column='Student_NetID')  # Field name made lowercase.
    class_classid = models.ForeignKey(Class, models.DO_NOTHING, db_column='Class_ClassID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Enrollment'


class File(models.Model):
    filename = models.CharField(db_column='FileName', max_length=45)  # Field name made lowercase.
    filetype = models.CharField(db_column='FileType', max_length=45)  # Field name made lowercase.
    filecontent = models.TextField(db_column='FileContent')  # Field name made lowercase.
    class_classid = models.ForeignKey(Class, models.DO_NOTHING, db_column='Class_ClassID')  # Field name made lowercase.
    fileid = models.AutoField(db_column='fileID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'File'


class Professor(models.Model):
    professornetid = models.CharField(db_column='ProfessorNetID', primary_key=True, max_length=15)  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=15)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=15)  # Field name made lowercase.
    email = models.CharField(max_length=45)
    password = models.CharField(db_column='Password', max_length=18, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Professor'


class Reply(models.Model):
    thread_threadid = models.ForeignKey('Thread', models.DO_NOTHING, db_column='Thread_ThreadID')  # Field name made lowercase.
    creationdate = models.DateTimeField(db_column='CreationDate')  # Field name made lowercase.
    content = models.TextField(db_column='Content')  # Field name made lowercase.
    student_netid = models.ForeignKey('Student', models.DO_NOTHING, db_column='Student_NetID')  # Field name made lowercase.
    replyid = models.AutoField(db_column='ReplyID', primary_key=True)  # Field name made lowercase.
    parent_replyid = models.IntegerField(db_column='Parent_ReplyID')

    class Meta:
        managed = False
        db_table = 'Reply'


class Student(models.Model):
    permissions = models.IntegerField(db_column='Permissions', null=True)  # Field name made lowercase.
    netid = models.CharField(db_column='NetID', primary_key=True, max_length=11)  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=15)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=15)  # Field name made lowercase.
    email = models.CharField(max_length=50)
    password = models.CharField(db_column='Password', max_length=20, blank=True, null=True)  # Field name made lowercase.
        
    class Meta:
        managed = False
        db_table = 'Student'


class Thread(models.Model):
    class_classid = models.ForeignKey(Class, models.DO_NOTHING, db_column='Class_ClassID')  # Field name made lowercase.
    threadid = models.AutoField(db_column='ThreadID', primary_key=True)  # Field name made lowercase.
    creationdate = models.DateTimeField(db_column='CreationDate')  # Field name made lowercase.
    threadcontent = models.TextField(db_column='ThreadContent')  # Field name made lowercase.
    student_netid = models.ForeignKey(Student, models.DO_NOTHING, db_column='Student_NetID')  # Field name made lowercase.
    threadtitle = models.CharField(db_column='ThreadTitle', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Thread'
