from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer_profile', to='users.user'),
        ),
        migrations.AddField(
            model_name='professional',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='professional',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='professional_profile', to='users.user'),
        ),
        migrations.AddField(
            model_name='service',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='availability',
            name='day_of_week',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Segunda-feira'), (1, 'Terça-feira'), (2, 'Quarta-feira'), (3, 'Quinta-feira'), (4, 'Sexta-feira'), (5, 'Sábado'), (6, 'Domingo')]),
        ),
        migrations.AlterUniqueTogether(
            name='availability',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='availability',
            constraint=models.UniqueConstraint(fields=('professional', 'day_of_week'), name='unique_professional_weekday'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='accounts.customer'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='accounts.service'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='notes',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddIndex(
            model_name='appointment',
            index=models.Index(fields=('start_time', 'status'), name='accounts_ap_start_t_5a0b3a_idx'),
        ),
        migrations.AddIndex(
            model_name='appointment',
            index=models.Index(fields=('customer', 'start_time'), name='accounts_ap_customer_7b1f77_idx'),
        ),
    ]
