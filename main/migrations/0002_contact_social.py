from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='facebook_url',
            field=models.URLField(blank=True, verbose_name='Facebook'),
        ),
        migrations.AddField(
            model_name='contact',
            name='instagram_url',
            field=models.URLField(blank=True, verbose_name='Instagram'),
        ),
        migrations.AddField(
            model_name='contact',
            name='youtube_url',
            field=models.URLField(blank=True, verbose_name='YouTube'),
        ),
    ]
