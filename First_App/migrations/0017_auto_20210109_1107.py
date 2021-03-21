# Generated by Django 3.1.5 on 2021-01-09 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('First_App', '0016_auto_20210108_1749'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='key_course',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='attendent',
            name='url_image',
            field=models.URLField(max_length=1000, null=True),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_user', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=100)),
                ('major', models.CharField(max_length=100)),
                ('user_type', models.CharField(max_length=10)),
                ('courses', models.ManyToManyField(to='First_App.Course')),
            ],
        ),
    ]