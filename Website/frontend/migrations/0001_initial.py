# Generated by Django 4.1.1 on 2023-04-25 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('classname', models.CharField(db_column='ClassName', max_length=50)),
                ('classid', models.IntegerField(db_column='ClassID', primary_key=True, serialize=False)),
                ('sectionnumber', models.IntegerField(db_column='sectionNumber')),
                ('size', models.IntegerField(db_column='Size')),
                ('classnumber', models.CharField(db_column='ClassNumber', max_length=10)),
            ],
            options={
                'db_table': 'Class',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('idenrollment', models.AutoField(db_column='idEnrollment', primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'Enrollment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('filename', models.CharField(db_column='FileName', max_length=45)),
                ('filetype', models.CharField(db_column='FileType', max_length=45)),
                ('filecontent', models.TextField(db_column='FileContent')),
                ('fileid', models.AutoField(db_column='fileID', primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'File',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('professornetid', models.CharField(db_column='ProfessorNetID', max_length=15, primary_key=True, serialize=False)),
                ('firstname', models.CharField(db_column='FirstName', max_length=15)),
                ('lastname', models.CharField(db_column='LastName', max_length=15)),
                ('email', models.CharField(max_length=45)),
                ('password', models.CharField(blank=True, db_column='Password', max_length=18, null=True)),
            ],
            options={
                'db_table': 'Professor',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('creationdate', models.DateTimeField(db_column='CreationDate')),
                ('content', models.TextField(db_column='Content')),
                ('replyid', models.AutoField(db_column='ReplyID', primary_key=True, serialize=False)),
                ('parent_replyid', models.IntegerField(db_column='Parent_ReplyID')),
            ],
            options={
                'db_table': 'Reply',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('permissions', models.IntegerField(db_column='Permissions')),
                ('netid', models.CharField(db_column='NetID', max_length=11, primary_key=True, serialize=False)),
                ('firstname', models.CharField(db_column='FirstName', max_length=15)),
                ('lastname', models.CharField(db_column='LastName', max_length=15)),
                ('email', models.CharField(max_length=45)),
                ('password', models.CharField(blank=True, db_column='Password', max_length=18, null=True)),
            ],
            options={
                'db_table': 'Student',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('threadid', models.AutoField(db_column='ThreadID', primary_key=True, serialize=False)),
                ('creationdate', models.DateTimeField(db_column='CreationDate')),
                ('threadcontent', models.TextField(db_column='ThreadContent')),
                ('threadtitle', models.CharField(db_column='ThreadTitle', max_length=45)),
            ],
            options={
                'db_table': 'Thread',
                'managed': False,
            },
        ),
    ]