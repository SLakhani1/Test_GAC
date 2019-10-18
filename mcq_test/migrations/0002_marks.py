# Generated by Django 2.2.6 on 2019-10-18 05:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mcq_test', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Marks',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('marks', models.IntegerField(default=0)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mcq_test.Users')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mcq_test.Test')),
            ],
        ),
    ]