# Generated by Django 2.2.6 on 2019-10-11 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mcq_test', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='test',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='mcq_test.Test'),
            preserve_default=False,
        ),
    ]