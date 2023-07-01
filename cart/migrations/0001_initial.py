# Generated by Django 3.2 on 2023-04-17 08:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('number', models.SmallIntegerField(blank=True, default=1, help_text='商品数量', verbose_name='商品数量')),
                ('is_checked', models.BooleanField(blank=True, default=True, help_text='是否选中', verbose_name='是否选中')),
                ('goods', models.ForeignKey(help_text='商品ID', on_delete=django.db.models.deletion.CASCADE, to='goods.goods', verbose_name='商品ID')),
                ('user', models.ForeignKey(blank=True, help_text='用户ID', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户ID')),
            ],
            options={
                'verbose_name': '购物车',
                'verbose_name_plural': '购物车',
                'db_table': 'cart',
            },
        ),
    ]
