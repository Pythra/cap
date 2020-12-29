# Generated by Django 3.1.3 on 2020-12-02 13:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('not_status', models.CharField(choices=[('unseen', 'unseen'), ('present', 'present'), ('seen', 'seen')], default='unseen', max_length=10)),
                ('body', models.TextField()),
                ('dp', models.ImageField(null=True, upload_to='comment_dp')),
                ('comment_pic', models.ImageField(blank=True, null=True, upload_to='comment_pics/')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('visits', models.IntegerField(default=0)),
                ('likes', models.ManyToManyField(blank=True, related_name='comment_likes', to=settings.AUTH_USER_MODEL)),
                ('name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created_on'],
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('dp', models.ImageField(null=True, upload_to='comment_dp')),
                ('comment_pic', models.ImageField(blank=True, null=True, upload_to='comment_pics/')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('not_status', models.CharField(choices=[('unseen', 'unseen'), ('present', 'present'), ('seen', 'seen')], default='unseen', max_length=10)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='capping.comment')),
                ('likes', models.ManyToManyField(blank=True, related_name='reply_likes', to=settings.AUTH_USER_MODEL)),
                ('name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dp', models.ImageField(blank=True, default='default.jpeg', null=True, upload_to='')),
                ('first_name', models.CharField(blank=True, max_length=20, null=True)),
                ('last_name', models.CharField(blank=True, max_length=20, null=True)),
                ('birthday', models.CharField(blank=True, max_length=20, null=True)),
                ('job', models.CharField(blank=True, max_length=20, null=True)),
                ('balance', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=8, null=True)),
                ('email_confirmed', models.BooleanField(default=False)),
                ('joined', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['joined'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70, unique=True)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('content', models.TextField()),
                ('post_pic', models.ImageField(blank=True, null=True, upload_to='post_pics/')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(choices=[(0, 'Draft'), (1, 'Publish')], default=1)),
                ('not_status', models.CharField(choices=[('unseen', 'unseen'), ('present', 'present'), ('seen', 'seen')], default='unseen', max_length=10)),
                ('visits', models.IntegerField(default=0)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('like', models.ManyToManyField(blank=True, related_name='post_likes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('not_status', models.CharField(choices=[('unseen', 'unseen'), ('present', 'present'), ('seen', 'seen')], default='unseen', max_length=10)),
                ('created_on', models.TimeField(auto_now_add=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='capping.comment')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='capping.post')),
                ('reply', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='capping.reply')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='capping.post'),
        ),
    ]
