# Generated by Django 4.1.10 on 2023-11-06 06:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("data_sci", "0002_rename_awa_team_footballmatches_away_team"),
    ]

    operations = [
        migrations.DeleteModel(
            name="FootballMatches",
        ),
    ]
