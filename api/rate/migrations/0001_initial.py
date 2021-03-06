# Generated by Django 2.2.1 on 2019-06-17 06:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Port',
            fields=[
                ('code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('slug', models.CharField(max_length=55, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('parent_slug', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='rate.Region')),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField()),
                ('price', models.IntegerField()),
                ('dest_code', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='destin_code', to='rate.Port')),
                ('orig_code', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='origin_code', to='rate.Port')),
            ],
        ),
        migrations.AddField(
            model_name='port',
            name='parent_slug',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rate.Region'),
        ),
    ]
