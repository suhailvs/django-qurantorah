# Generated by Django 2.1.3 on 2018-11-25 22:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aya',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Aya Number')),
                ('text', models.TextField()),
            ],
            options={
                'ordering': ['sura', 'number'],
            },
        ),
        migrations.CreateModel(
            name='Lemma',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'ordering': ['token'],
            },
        ),
        migrations.CreateModel(
            name='QuranTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('translator', models.CharField(max_length=50)),
                ('source_name', models.CharField(max_length=50)),
                ('source_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Root',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('letters', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sura',
            fields=[
                ('number', models.IntegerField(primary_key=True, serialize=False, verbose_name='Sura Number')),
                ('name', models.CharField(max_length=50, verbose_name='Sura Name')),
                ('tname', models.CharField(max_length=50, verbose_name='English Transliterated Name')),
                ('ename', models.CharField(max_length=50, verbose_name='English Name')),
                ('order', models.IntegerField(verbose_name='Revelation Order')),
                ('type', models.CharField(choices=[('Meccan', 'Meccan'), ('Medinan', 'Medinan')], max_length=7, verbose_name='')),
                ('rukus', models.IntegerField(verbose_name='Number of Rukus')),
                ('bismillah', models.CharField(blank=True, max_length=50, verbose_name='Bismillah')),
            ],
            options={
                'ordering': ['number'],
            },
        ),
        migrations.CreateModel(
            name='TranslatedAya',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('aya', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='quran.Aya')),
                ('sura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='quran.Sura')),
                ('translation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quran.QuranTranslation')),
            ],
            options={
                'ordering': ['aya'],
            },
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('token', models.CharField(max_length=50)),
                ('ename', models.CharField(blank=True, max_length=50)),
                ('translation', models.CharField(blank=True, max_length=200)),
                ('aya', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='words', to='quran.Aya')),
                ('lemma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quran.Lemma')),
                ('root', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='words', to='quran.Root')),
                ('sura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='words', to='quran.Sura')),
            ],
            options={
                'ordering': ['number'],
            },
        ),
        migrations.AddField(
            model_name='root',
            name='ayas',
            field=models.ManyToManyField(through='quran.Word', to='quran.Aya'),
        ),
        migrations.AddField(
            model_name='lemma',
            name='ayas',
            field=models.ManyToManyField(through='quran.Word', to='quran.Aya'),
        ),
        migrations.AddField(
            model_name='lemma',
            name='root',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lemmas', to='quran.Root'),
        ),
        migrations.AddField(
            model_name='aya',
            name='sura',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ayas', to='quran.Sura'),
        ),
        migrations.AlterUniqueTogether(
            name='word',
            unique_together={('aya', 'number')},
        ),
        migrations.AlterUniqueTogether(
            name='translatedaya',
            unique_together={('aya', 'translation')},
        ),
        migrations.AlterUniqueTogether(
            name='aya',
            unique_together={('number', 'sura')},
        ),
    ]
