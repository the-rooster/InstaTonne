# Generated by Django 4.1.6 on 2023-02-21 00:20

import InstaTonneApis.models
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
                ('id', models.TextField(default=InstaTonneApis.models.default_id_generator, editable=False, primary_key=True, serialize=False)),
                ('type', models.TextField()),
                ('id_url', models.TextField()),
                ('url', models.TextField()),
                ('host', models.TextField()),
                ('displayName', models.TextField()),
                ('github', models.TextField()),
                ('profileImage', models.TextField()),
                ('userID', models.TextField()),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=InstaTonneApis.models.default_id_generator, editable=False, primary_key=True, serialize=False)),
                ('type', models.TextField()),
                ('url', models.TextField()),
                ('contentType', models.TextField()),
                ('comment', models.TextField()),
                ('published', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InstaTonneApis.author')),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.TextField()),
                ('summary', models.TextField()),
                ('published', models.DateTimeField(auto_now_add=True)),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requester', to='InstaTonneApis.author')),
                ('object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requestee', to='InstaTonneApis.author')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.TextField(default=InstaTonneApis.models.default_id_generator, editable=False, primary_key=True, serialize=False)),
                ('type', models.TextField()),
                ('url', models.TextField()),
                ('title', models.TextField()),
                ('source', models.TextField()),
                ('origin', models.TextField()),
                ('description', models.TextField()),
                ('contentType', models.TextField()),
                ('content', models.TextField()),
                ('visibility', models.TextField()),
                ('categories', models.CharField(max_length=100)),
                ('unlisted', models.BooleanField(default=False)),
                ('published', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='InstaTonneApis.author')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.TextField(default=InstaTonneApis.models.default_id_generator, editable=False, primary_key=True, serialize=False)),
                ('type', models.TextField()),
                ('context', models.TextField()),
                ('summary', models.TextField()),
                ('published', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InstaTonneApis.author')),
                ('comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='InstaTonneApis.comment')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='InstaTonneApis.post')),
            ],
        ),
        migrations.CreateModel(
            name='Inbox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='InstaTonneApis.comment')),
                ('like', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='InstaTonneApis.like')),
                ('ownerId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InstaTonneApis.author')),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='InstaTonneApis.post')),
                ('request', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='InstaTonneApis.request')),
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
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='InstaTonneApis.post'),
        ),
    ]
