# Generated by Django 5.1.7 on 2025-05-26 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lead', '0004_alter_lead_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lead',
            name='email',
        ),
        migrations.AddField(
            model_name='lead',
            name='budget',
            field=models.CharField(choices=[('less-than-50-lakh', 'Less than 50 Lakh'), ('less-than-1-crore', 'Less than 1 Crore'), ('1-crore-to-2-crore', '1 Crore to 2 Crore'), ('2-crore-to-3-crore', '2 Crore to 3 Crore'), ('3-crore-to-4-crore', '3 Crore to 4 Crore'), ('4-crore-to-5-crore', '4 Crore to 5 Crore'), ('more-than-5-crore', 'More than 5 Crore'), ('other', 'Other')], default='other', max_length=20),
        ),
        migrations.AddField(
            model_name='lead',
            name='company',
            field=models.CharField(choices=[('rupayanhousing', 'Rupayan Housing'), ('rupayancityuttara', 'Rupayan City Uttara'), ('other', 'Other')], default='other', max_length=20),
        ),
        migrations.AddField(
            model_name='lead',
            name='facing',
            field=models.CharField(choices=[('east', 'East'), ('west', 'West'), ('north', 'North'), ('south', 'South'), ('north-east', 'North-East'), ('north-west', 'North-West'), ('south-east', 'South-East'), ('south-west', 'South-West'), ('other', 'Other')], default='other', max_length=20),
        ),
        migrations.AddField(
            model_name='lead',
            name='interestedprojectbuilding',
            field=models.CharField(choices=[('grand-building-12', 'Grand Building 12'), ('majestic-building-5', 'Majestic Building 5'), ('skyvilla-building-3', 'Skyvilla Building 3'), ('maxus-building-8', 'Maxus Building 8'), ('other', 'Other')], default='other', max_length=30),
        ),
        migrations.AddField(
            model_name='lead',
            name='leadsource',
            field=models.CharField(choices=[('sgl', 'SGL'), ('walkin', 'Walk-in'), ('other', 'Other')], default='other', max_length=20),
        ),
        migrations.AddField(
            model_name='lead',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lead',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='lead',
            name='preference_floor',
            field=models.CharField(choices=[('1st', '1st Floor'), ('2nd', '2nd Floor'), ('3rd', '3rd Floor'), ('4th', '4th Floor'), ('5th', '5th Floor'), ('6th', '6th Floor'), ('7th', '7th Floor'), ('8th', '8th Floor'), ('9th', '9th Floor'), ('10th', '10th Floor'), ('11th', '11th Floor'), ('12th', '12th Floor'), ('13th', '13th Floor'), ('14th', '14th Floor'), ('15th', '15th Floor')], default='1st', max_length=20),
        ),
        migrations.AddField(
            model_name='lead',
            name='prefferatedlocation',
            field=models.CharField(choices=[('banani', 'Banani'), ('gulshan', 'Gulshan'), ('badda', 'Badda'), ('dhanmondi', 'Dhanmondi'), ('other', 'Other')], default='other', max_length=20),
        ),
        migrations.AddField(
            model_name='lead',
            name='presentaddress',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='lead',
            name='primaryemail',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='lead',
            name='proffession',
            field=models.CharField(choices=[('doctor', 'Doctor'), ('engineer', 'Engineer'), ('teacher', 'Teacher'), ('student', 'Student'), ('other', 'Other')], default='null', max_length=20),
        ),
        migrations.AddField(
            model_name='lead',
            name='projectstatus',
            field=models.CharField(choices=[('ready', 'Ready'), ('initial', 'Initial'), ('going', 'Going')], default='ready', max_length=20),
        ),
        migrations.AddField(
            model_name='lead',
            name='projecttype',
            field=models.CharField(choices=[('grand', 'Grand'), ('majestic', 'Majestic'), ('skyvilla', 'Skyvilla'), ('maxus', 'Maxus'), ('other', 'Other')], default='other', max_length=20),
        ),
        migrations.AddField(
            model_name='lead',
            name='propertystatus',
            field=models.CharField(choices=[('ready', 'Ready'), ('initial', 'Initial'), ('going', 'Going')], default='ready', max_length=20),
        ),
        migrations.AddField(
            model_name='lead',
            name='resident',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='lead',
            name='secondaryemail',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='lead',
            name='subsource',
            field=models.CharField(choices=[('ownsource', 'Own Source'), ('referral', 'Referral'), ('doorto-door', 'Door to Door'), ('social-media', 'Social Media'), ('online-advertisement', 'Online Advertisement'), ('other', 'Other')], default='other', max_length=20),
        ),
        migrations.AddField(
            model_name='lead',
            name='teamleader',
            field=models.CharField(choices=[('IKTADUL', 'Iktadul'), ('salman', 'Salman'), ('other', 'Other')], default='other', max_length=20),
        ),
        migrations.AddField(
            model_name='lead',
            name='unit_size',
            field=models.CharField(choices=[('2000-2500', '2000-2500 sqft'), ('200-300', '200-300 sqft'), ('300-400', '300-400 sqft'), ('2500-3000', '2500-3000 sqft'), ('3000-3500', '3000-3500 sqft'), ('3500-4000', '3500-4000 sqft'), ('4000+', '4000+ sqft'), ('other', 'Other')], default='other', max_length=20),
        ),
        migrations.AddField(
            model_name='lead',
            name='view',
            field=models.CharField(choices=[('road', 'Road'), ('park', 'Park'), ('lake', 'Lake'), ('city', 'City'), ('other', 'Other')], default='other', max_length=20),
        ),
    ]
