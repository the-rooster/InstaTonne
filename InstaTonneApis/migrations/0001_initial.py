# Generated by Django 4.1.6 on 2023-02-12 05:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.TextField()),
                ('url', models.TextField()),
                ('host', models.TextField()),
                ('displayName', models.TextField()),
                ('github', models.TextField()),
                ('profileImage', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.TextField()),
                ('published', models.DateTimeField(auto_now_add=True)),
                ('requestee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requestee', to='InstaTonneApis.author')),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requester', to='InstaTonneApis.author')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField()),
                ('title', models.TextField()),
                ('source', models.TextField()),
                ('origin', models.TextField()),
                ('description', models.TextField()),
                ('contentType', models.TextField()),
                ('content', models.TextField()),
                ('visibility', models.TextField()),
                ('catagories', models.CharField(max_length=100)),
                ('unlisted', models.BooleanField(default=False)),
                ('published', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InstaTonneApis.author')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField()),
                ('summary', models.TextField()),
                ('published', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InstaTonneApis.author')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InstaTonneApis.post')),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followeeAuthorId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followeeAuthorId', to='InstaTonneApis.author')),
                ('followerAuthorId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followerAuthorId', to='InstaTonneApis.author')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField()),
                ('contentType', models.TextField()),
                ('content', models.TextField()),
                ('published', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InstaTonneApis.author')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InstaTonneApis.post')),
            ],
        ),
    ]
