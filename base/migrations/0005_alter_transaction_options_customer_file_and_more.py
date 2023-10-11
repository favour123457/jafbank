# Generated by Django 4.1.4 on 2023-09-27 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_transaction_receiver_alter_transaction_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['-time']},
        ),
        migrations.AddField(
            model_name='customer',
            name='file',
            field=models.FileField(null=True, upload_to='files/'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='recv_no',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='account',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.customer'),
        ),
    ]