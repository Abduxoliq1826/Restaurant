# Generated by Django 4.0.5 on 2022-10-07 17:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='order',
            field=models.ForeignKey(default=59, on_delete=django.db.models.deletion.CASCADE, to='api.order'),
            preserve_default=False,
        ),
    ]