
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
from teams.models import Team

class Lead(models.Model):
    LEAD_STAGE_CHOICES = (
        ('lead', 'Lead'),
        ('prospect', 'Prospect'),
        ('high_prospect', 'High Prospect'),
        ('sold_onboard', 'Sold/On-board'),
        ('hold', 'Hold'),
        ('lost', 'Lost'),
        ('junk', 'Junk'),
    )

    PROFESSION_CHOICES = (
        ('doctor', 'Doctor'),
        ('artist', 'Artist'),
        ('engineer', 'Engineer'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('other', 'Other'),
    )

    PROJECT_CHOICES = (
        ('grand', 'Grand'),
        ('majestic', 'Majestic'),
        ('skyvilla', 'Skyvilla'),
        ('maxus', 'Maxus'),
        ('other', 'Other'),
    )

    PROPERTY_STATUS_CHOICES = (
        ('ready', 'Ready'),
        ('initial', 'Initial'),
        ('going', 'Going'),
    )

    PREFERRED_LOCATION_CHOICES = (
        ('banani', 'Banani'),
        ('gulshan', 'Gulshan'),
        ('badda', 'Badda'),
        ('dhanmondi', 'Dhanmondi'),
        ('other', 'Other'),
    )

    COMPANY_CHOICES = (
        ('rupayanhousing', 'Rupayan Housing'),
        ('rupayancityuttara', 'Rupayan City Uttara'),
        ('other', 'Other'),
    )

    INTERESTED_PROJECT_BUILDING_CHOICES = (
        ('grand-building-12', 'Grand Building 12'),
        ('majestic-building-5', 'Majestic Building 5'),
        ('skyvilla-building-3', 'Skyvilla Building 3'),
        ('maxus-building-8', 'Maxus Building 8'),
        ('other', 'Other'),
    )

    UNIT_SIZE_CHOICES = (
        ('2000-2500', '2000-2500 sqft'),
        ('200-300', '200-300 sqft'),
        ('300-400', '300-400 sqft'),
        ('2500-3000', '2500-3000 sqft'),
        ('3000-3500', '3000-3500 sqft'),
        ('3500-4000', '3500-4000 sqft'),
        ('4000+', '4000+ sqft'),
        ('other', 'Other'),
    )

    PREFERENCE_FLOOR = (
        ('1st', '1st Floor'),
        ('2nd', '2nd Floor'),
        ('3rd', '3rd Floor'),
        ('4th', '4th Floor'),
        ('5th', '5th Floor'),
        ('6th', '6th Floor'),
        ('7th', '7th Floor'),
        ('8th', '8th Floor'),
        ('9th', '9th Floor'),
        ('10th', '10th Floor'),
        ('11th', '11th Floor'),
        ('12th', '12th Floor'),
        ('13th', '13th Floor'),
        ('14th', '14th Floor'),
        ('15th', '15th Floor'),
    )

    FACING_CHOICES = (
        ('east', 'East'),
        ('west', 'West'),
        ('north', 'North'),
        ('south', 'South'),
        ('north-east', 'North-East'),
        ('north-west', 'North-West'),
        ('south-east', 'South-East'),
        ('south-west', 'South-West'),
        ('other', 'Other'),
    )

    VIEW_CHOICES = (
        ('road', 'Road'),
        ('park', 'Park'),
        ('lake', 'Lake'),
        ('city', 'City'),
        ('other', 'Other'),
    )

    BUDGET_CHOICES = (
        ('less-than-50-lakh', 'Less than 50 Lakh'),
        ('less-than-1-crore', 'Less than 1 Crore'),
        ('1-crore-to-2-crore', '1 Crore to 2 Crore'),
        ('2-crore-to-3-crore', '2 Crore to 3 Crore'),
        ('3-crore-to-4-crore', '3 Crore to 4 Crore'),
        ('4-crore-to-5-crore', '4 Crore to 5 Crore'),
        ('more-than-5-crore', 'More than 5 Crore'),
        ('other', 'Other'),
    )

    LEAD_SOURCE_CHOICES = (
        ('sgl', 'SGL'),
        ('walkin', 'Walk-in'),
        ('other', 'Other'),
    )

    SUB_SOURCE_CHOICES = (
        ('ownsource', 'Own Source'),
        ('referral', 'Referral'),
        ('doorto-door', 'Door to Door'),
        ('social-media', 'Social Media'),
        ('online-advertisement', 'Online Advertisement'),
        ('other', 'Other'),
    )

    TEAM_LEADER_CHOICES = (
        ('iktadul', 'Iktadul'),
        ('salman', 'Salman'),
        ('other', 'Other'),
    )

    FOLLOWUP_STATUS_CHOICES = (
        ('call', 'Call'),
        ('email', 'Email'),
        ('int Meeting', 'Int Meeting'),
        ('Ext Meeting', 'Ext Meeting'),
        ('project visit', 'Project Visit'),
        ('sold', 'Sold'),
        ('onboard', 'On-board'),
        ('junk', 'Junk'),
    )

    name = models.CharField("Name", max_length=50)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField(
    "Phone",
        max_length=11,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{11}$',
                message='Phone number must contain only numbers.',
                code='invalid_phone'
            )
        ]
    )
    present_address = models.CharField("Present Address", max_length=20, choices=PREFERRED_LOCATION_CHOICES, blank=True, null=True)
    primaryemail = models.EmailField("Primary Email", blank=True, null=True)
    secondaryemail = models.EmailField("Secondary Email", blank=True, null=True)
    profession = models.CharField("Profession", max_length=20, choices=PROFESSION_CHOICES, blank=True, null=True)
    resident = models.CharField("Resident", max_length=100, blank=True, null=True)
    notes = models.TextField("Notes", blank=True, null=True)
    projecttype = models.CharField("Project Type", max_length=20, choices=PROJECT_CHOICES, blank=True, null=True)
    projectstatus = models.CharField("Project Status", max_length=20, choices=PROPERTY_STATUS_CHOICES, default='ready', blank=True, null=True)
    preferred_location = models.CharField("Preferred Location", max_length=20, choices=PREFERRED_LOCATION_CHOICES, blank=True, null=True)
    company = models.CharField("Company", max_length=20, choices=COMPANY_CHOICES, default="rupayancityuttara", null=True)
    interested_project_building = models.CharField("Interested Project Building", max_length=30, choices=INTERESTED_PROJECT_BUILDING_CHOICES, blank=True, null=True)
    unit_size = models.CharField("Unit Size", max_length=20, choices=UNIT_SIZE_CHOICES, blank=True, null=True)
    preference_floor = models.CharField("Preference Floor", max_length=20, choices=PREFERENCE_FLOOR, blank=True, null=True)
    facing = models.CharField("Facing", max_length=20, choices=FACING_CHOICES, blank=True, null=True)
    view = models.CharField("View", max_length=20, choices=VIEW_CHOICES, blank=True, null=True)
    budget = models.CharField("Budget", max_length=20, choices=BUDGET_CHOICES, blank=True, null=True)
    leadsource = models.CharField("Lead Source", max_length=20, choices=LEAD_SOURCE_CHOICES, default='sgl', blank=True, null=True)
    subsource = models.CharField("Sub Source", max_length=20, choices=SUB_SOURCE_CHOICES, default='ownsource',blank=True, null=True)
    teamleader = models.CharField("Team Leader", max_length=20, choices=TEAM_LEADER_CHOICES, default='iktadul',blank=True, null=True)
    description = models.TextField("Description", blank=True, null=True)
    converted_to_client = models.BooleanField("Converted to Client", default=False)
    created_by = models.ForeignKey(User, related_name='leads', on_delete=models.CASCADE)
    created_at = models.DateTimeField("Created At", auto_now_add=True)
    modified_at = models.DateTimeField("Modified At", auto_now=True)
    followup_by = models.CharField("Follow Up By", max_length=50, choices=FOLLOWUP_STATUS_CHOICES, blank=True, null=True)
    lead_status = models.CharField("Lead Status", max_length=20, choices=LEAD_STAGE_CHOICES, default="lead", null=True)
    next_followup_by = models.CharField(max_length=20, choices=FOLLOWUP_STATUS_CHOICES, blank=True, null=True)
    next_followup_date = models.DateField("Next Follow Up Date", blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True)
    

    unique_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)  # Save to get pk

        if is_new and not self.unique_id:
            self.unique_id = f"P-{self.pk:04d}"
            # Update unique_id without causing recursion
            Lead.objects.filter(pk=self.pk).update(unique_id=self.unique_id)



class LeadChangeLog(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='change_logs')
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    change_date = models.DateTimeField(auto_now_add=True)
    field_name = models.CharField(max_length=100)
    old_value = models.TextField(blank=True, null=True)
    new_value = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.lead} changed {self.field_name} on {self.change_date.strftime('%Y-%m-%d %H:%M:%S')}"
    


