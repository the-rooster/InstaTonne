# Generated by Django 4.1.6 on 2023-02-20 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InstaTonneApis', '0010_remove_author_id_alter_author_userid'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='id',
            field=models.BigAutoField(auto_created=True, default=2, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='author',
            name='userID',
            field=models.TextField(),
        ),
    ]
