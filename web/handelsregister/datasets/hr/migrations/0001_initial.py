# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-08-18 08:29
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activiteit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activiteitsomschrijving', models.CharField(blank=True, help_text='De omschrijving van de activiteiten die de Vestiging of Rechtspersoon uitoefent', max_length=300, null=True)),
                ('sbi_code', models.CharField(blank=True, help_text='De codering van de activiteit conform de SBI2008', max_length=3, null=True)),
                ('omschrijving', models.CharField(blank=True, help_text='Omschrijving van de activiteit', max_length=300, null=True)),
                ('hoofdactiviteit', models.NullBooleanField(help_text='Indicatie die aangeeft welke van de activiteiten de hoofdactiviteit is')),
            ],
        ),
        migrations.CreateModel(
            name='BinnenlandseNietNatuurlijkPersoon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='BuitenlandseVennootschap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Communicatiegegevens',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('domeinnaam', models.URLField(blank=True, help_text='Het internetadres (URL)', max_length=300, null=True)),
                ('emailadres', models.EmailField(blank=True, help_text='Het e-mailadres waar op de onderneming gemaild kan worden', max_length=200, null=True)),
                ('toegangscode', models.CharField(blank=True, help_text="De internationale toegangscode van het land waarop het nummer (telefoon of fax) betrekking heeft'", max_length=10, null=True)),
                ('communicatie_nummer', models.CharField(blank=True, help_text='Nummer is het telefoon- of faxnummer zonder opmaak', max_length=15, null=True)),
                ('soort_communicatie_nummer', models.CharField(blank=True, choices=[('Telefoon', 'Telefoon'), ('Fax', 'Fax')], max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Functievervulling',
            fields=[
                ('fvvid', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('functietitel', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Handelsnaam',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('handelsnaam', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Kapitaal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Locatie',
            fields=[
                ('id', models.CharField(max_length=18, primary_key=True, serialize=False)),
                ('volledig_adres', models.CharField(blank=True, help_text='Samengesteld adres ', max_length=550, null=True)),
                ('toevoeging_adres', models.TextField(blank=True, help_text='Vrije tekst om een Adres nader aan te kunnen duiden', null=True)),
                ('afgeschermd', models.BooleanField(help_text='Geeft aan of het adres afgeschermd is of niet')),
                ('postbus_nummer', models.CharField(blank=True, max_length=10, null=True)),
                ('bag_nummeraanduiding', models.URLField(blank=True, help_text='Link naar de BAG Nummeraanduiding', null=True)),
                ('bag_adresseerbaar_object', models.URLField(blank=True, help_text='Link naar het BAG Adresseerbaar object', null=True)),
                ('straat_huisnummer', models.CharField(blank=True, max_length=220, null=True)),
                ('postcode_woonplaats', models.CharField(blank=True, max_length=220, null=True)),
                ('regio', models.CharField(blank=True, max_length=170, null=True)),
                ('land', models.CharField(blank=True, max_length=50, null=True)),
                ('geometry', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=28992)),
            ],
        ),
        migrations.CreateModel(
            name='MaatschappelijkeActiviteit',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('naam', models.CharField(blank=True, help_text='De (statutaire) naam of eerste handelsnaam van de inschrijving', max_length=600, null=True)),
                ('kvk_nummer', models.CharField(blank=True, help_text='Betreft het identificerende gegeven voor de {MaatschappelijkeActiviteit}, het KvK-nummer', max_length=8, null=True, unique=True)),
                ('datum_aanvang', models.DateField(blank=True, help_text='De datum van aanvang van de {MaatschappelijkeActiviteit}', max_length=8, null=True)),
                ('datum_einde', models.DateField(blank=True, help_text='De datum van beëindiging van de {MaatschappelijkeActiviteit}', max_length=8, null=True)),
                ('incidenteel_uitlenen_arbeidskrachten', models.NullBooleanField(help_text="Indicatie die aangeeft of de ondernemer tijdelijk arbeidskrachten ter beschikking stelt en dit niet onderdeel is van zijn 'reguliere' activiteiten.")),
                ('non_mailing', models.NullBooleanField(help_text='Indicator die aangeeft of de inschrijving haar adresgegevens beschikbaar stelt voor mailing-doeleinden.')),
                ('activiteiten', models.ManyToManyField(help_text='De SBI-activiteiten van de MaatschappelijkeActiviteit is het totaal van alle SBI-activiteiten die voorkomen bij de MaatschappelijkeActiviteit behorende NietCommercieleVestigingen en bij de Rechtspersoon', to='hr.Activiteit')),
                ('bezoekadres', models.ForeignKey(blank=True, help_text='bezoekadres', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='hr.Locatie')),
                ('communicatiegegevens', models.ManyToManyField(help_text='Afgeleid van communicatiegegevens van inschrijving', to='hr.Communicatiegegevens')),
            ],
        ),
        migrations.CreateModel(
            name='MaatschappelijkeActiviteitVestiging',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datum_aanvang', models.CharField(blank=True, max_length=8, null=True)),
                ('datum_einde', models.CharField(blank=True, max_length=8, null=True)),
                ('maatschappelijke_activiteit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr.MaatschappelijkeActiviteit')),
            ],
        ),
        migrations.CreateModel(
            name='NatuurlijkPersoon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geboortedatum', models.CharField(blank=True, max_length=8, null=True)),
                ('geboorteplaats', models.CharField(blank=True, max_length=240, null=True)),
                ('geboorteland', models.CharField(blank=True, max_length=50, null=True)),
                ('naam', models.CharField(blank=True, max_length=600, null=True)),
                ('geslachtsnaam', models.CharField(blank=True, max_length=240, null=True)),
                ('geslachtsaanduiding', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='NietNatuurlijkPersoon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Onderneming',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('totaal_werkzame_personen', models.DecimalField(blank=True, decimal_places=0, max_digits=8, null=True)),
                ('fulltime_werkzame_personen', models.DecimalField(blank=True, decimal_places=0, max_digits=8, null=True)),
                ('parttime_werkzame_personen', models.DecimalField(blank=True, decimal_places=0, max_digits=8, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Persoon',
            fields=[
                ('prsid', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('rechtsvorm', models.CharField(blank=True, max_length=50, null=True)),
                ('uitgebreide_rechtsvorm', models.CharField(blank=True, max_length=240, null=True)),
                ('volledige_naam', models.CharField(blank=True, max_length=240, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RechterlijkeUitspraak',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Vestiging',
            fields=[
                ('vesid', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('vestigingsnummer', models.CharField(max_length=12)),
                ('sbicode_hoofdactiviteit', models.CharField(blank=True, max_length=20, null=True)),
                ('sbicode_nevenactiviteit1', models.CharField(blank=True, max_length=20, null=True)),
                ('sbicode_nevenactiviteit2', models.CharField(blank=True, max_length=20, null=True)),
                ('sbicode_nevenactiviteit3', models.CharField(blank=True, max_length=20, null=True)),
                ('sbi_omschrijving_hoofdact', models.CharField(blank=True, max_length=180, null=True)),
                ('sbi_omschrijving_nevenact1', models.CharField(blank=True, max_length=180, null=True)),
                ('sbi_omschrijving_nevenact2', models.CharField(blank=True, max_length=180, null=True)),
                ('sbi_omschrijving_nevenact3', models.CharField(blank=True, max_length=180, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='maatschappelijkeactiviteitvestiging',
            name='vestiging',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr.Vestiging'),
        ),
        migrations.AddField(
            model_name='maatschappelijkeactiviteit',
            name='eigenaar',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hr.Persoon'),
        ),
        migrations.AddField(
            model_name='maatschappelijkeactiviteit',
            name='hoofdvestiging',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='hr.Vestiging'),
        ),
        migrations.AddField(
            model_name='maatschappelijkeactiviteit',
            name='onderneming',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hr.Onderneming'),
        ),
        migrations.AddField(
            model_name='maatschappelijkeactiviteit',
            name='postadres',
            field=models.ForeignKey(blank=True, help_text='postadres', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='hr.Locatie'),
        ),
        migrations.AddField(
            model_name='handelsnaam',
            name='onderneming',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='handelsnamen', to='hr.Onderneming'),
        ),
    ]
