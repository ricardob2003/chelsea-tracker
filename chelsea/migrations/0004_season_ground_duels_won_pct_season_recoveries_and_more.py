# Generated by Django 5.1.6 on 2025-02-18 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chelsea', '0003_remove_vote_unique_vote_per_player_or_manager_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='ground_duels_won_pct',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='season',
            name='recoveries',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='season',
            name='tackles',
            field=models.IntegerField(default=0),
        ),
    ]
