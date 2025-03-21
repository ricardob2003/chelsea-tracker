# Generated by Django 5.1.5 on 2025-02-07 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chelsea', '0002_manager_trophies_won_player_aerial_duels_won_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='vote',
            name='unique_vote_per_player_or_manager',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='votes_count',
        ),
        migrations.AddConstraint(
            model_name='vote',
            constraint=models.CheckConstraint(condition=models.Q(models.Q(('manager__isnull', True), ('player__isnull', False)), models.Q(('manager__isnull', False), ('player__isnull', True)), _connector='OR'), name='only_one_of_player_or_manager'),
        ),
    ]
