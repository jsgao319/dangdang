# Generated by Django 2.0.6 on 2019-04-15 21:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=20)),
                ('m_phone', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=20)),
                ('postcode', models.CharField(max_length=20)),
                ('ship_man', models.CharField(default='username', max_length=20)),
            ],
            options={
                'db_table': 't_address',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('parent_id', models.IntegerField()),
            ],
            options={
                'db_table': 't_category',
            },
        ),
        migrations.CreateModel(
            name='ConfirmString',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=256, verbose_name='邮箱注册码')),
                ('c_time', models.DateTimeField(auto_now_add=True, verbose_name='注册码的生成时间')),
            ],
            options={
                'db_table': 't_confirmString',
            },
        ),
        migrations.CreateModel(
            name='HistoryOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_num', models.IntegerField()),
                ('address', models.CharField(max_length=100)),
                ('content', models.TextField()),
            ],
            options={
                'db_table': 't_history_order',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=50)),
                ('time', models.DateTimeField()),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mainapp.Address')),
            ],
            options={
                'db_table': 't_order',
            },
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='mainapp.Order')),
            ],
            options={
                'db_table': 't_order_info',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('author', models.CharField(max_length=50)),
                ('face', models.CharField(max_length=100)),
                ('publishing_house', models.CharField(max_length=50)),
                ('edition', models.SmallIntegerField()),
                ('publishing_time', models.DateTimeField()),
                ('print_time', models.SmallIntegerField()),
                ('isbn', models.CharField(max_length=30)),
                ('word', models.CharField(max_length=20)),
                ('number_of_page', models.IntegerField()),
                ('format_of_book', models.CharField(max_length=20)),
                ('paper', models.CharField(max_length=20)),
                ('packagin', models.CharField(max_length=20)),
                ('emboitement', models.CharField(max_length=10)),
                ('sales', models.CharField(max_length=20)),
                ('price', models.FloatField()),
                ('dangdang_price', models.FloatField()),
                ('review', models.BigIntegerField()),
                ('issue', models.DateTimeField()),
                ('score', models.FloatField()),
                ('sold_out', models.CharField(max_length=10)),
                ('recommand', models.CharField(max_length=10)),
                ('extend', models.CharField(max_length=50)),
                ('menus', models.ForeignKey(db_column='menus', on_delete=django.db.models.deletion.DO_NOTHING, to='mainapp.Category')),
            ],
            options={
                'db_table': 't_product',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=100)),
                ('salt', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('c_time', models.DateTimeField(auto_now_add=True, verbose_name='用户的创建时间')),
                ('has_confirm', models.BooleanField(default=False, verbose_name='邮箱是否确认')),
            ],
            options={
                'db_table': 't_user',
            },
        ),
        migrations.AddField(
            model_name='orderinfo',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mainapp.Product'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mainapp.User'),
        ),
        migrations.AddField(
            model_name='historyorder',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mainapp.User'),
        ),
        migrations.AddField(
            model_name='confirmstring',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mainapp.User', verbose_name='关联的用户'),
        ),
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.ForeignKey(db_column='user', on_delete=django.db.models.deletion.DO_NOTHING, to='mainapp.User'),
        ),
    ]