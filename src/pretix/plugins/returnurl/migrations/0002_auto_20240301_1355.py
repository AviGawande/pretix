# Generated by Django 4.2.10 on 2024-03-01 13:55
import re

from django.core.cache import cache
from django.db import migrations

MISSING_SLASH = re.compile(r"^https?://[^/]*$")


def force_slash_after_hostname(prefix):
    prefix = prefix.strip()
    if MISSING_SLASH.match(prefix):
        return prefix + "/"
    else:
        return prefix


def update_returnurl_prefixes(app, schema_editor):
    EventSettingsStore = app.get_model('pretixbase', 'Event_SettingsStore')

    for setting in EventSettingsStore.objects.filter(key='returnurl_prefix'):
        prefixes = setting.value.split("\n")
        new_prefixes = [force_slash_after_hostname(prefix) for prefix in prefixes]
        new_value = "\n".join(new_prefixes)
        setting.value = new_value
        cache.delete('hierarkey_{}_{}'.format('event', setting.object_id))
        setting.save()


class Migration(migrations.Migration):

    dependencies = [
        ('returnurl', '0001_initial'),
        ('pretixbase', '0257_item_default_price_not_null'),
    ]

    operations = [
        migrations.RunPython(update_returnurl_prefixes, migrations.RunPython.noop)
    ]