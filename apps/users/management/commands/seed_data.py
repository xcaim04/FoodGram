"""
Management command: seed_data
Creates demo users and sample posts to showcase FoodGram.

Usage:
    python manage.py seed_data
"""
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from apps.users.models import User, Follow
from apps.posts.models import Post, Category


class Command(BaseCommand):
    help = 'Crea datos de demostración: usuarios, follows y publicaciones de ejemplo'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('\n🍽️  FoodGram — Seed de datos de demo\n'))

        # ── Usuarios ──────────────────────────────────────────────────────────
        users_data = [
            {
                'email': 'chef@foodgram.app',
                'username': 'chef_mario',
                'display_name': 'Mario García',
                'bio': 'Chef profesional con 15 años de experiencia. Amante de la cocina mediterránea.',
                'location': 'Madrid, España',
                'password': 'demo1234',
            },
            {
                'email': 'foodie@foodgram.app',
                'username': 'foodie_ana',
                'display_name': 'Ana López',
                'bio': 'Exploradora de sabores. Siempre en busca del mejor taco 🌮',
                'location': 'Ciudad de México, MX',
                'password': 'demo1234',
            },
            {
                'email': 'pastry@foodgram.app',
                'username': 'sweet_carlos',
                'display_name': 'Carlos Ruiz',
                'bio': 'Pastelero apasionado. Cada postre es una obra de arte.',
                'location': 'Buenos Aires, AR',
                'password': 'demo1234',
            },
        ]

        created_users = []
        for data in users_data:
            password = data.pop('password')
            user, created = User.objects.get_or_create(email=data['email'], defaults=data)
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(f'  ✅ Usuario creado: @{user.username}  (pass: demo1234)')
            else:
                self.stdout.write(f'  ⏭️  Usuario ya existe: @{user.username}')
            created_users.append(user)

        # ── Follows ───────────────────────────────────────────────────────────
        if len(created_users) >= 2:
            Follow.objects.get_or_create(follower=created_users[0], following=created_users[1])
            Follow.objects.get_or_create(follower=created_users[1], following=created_users[0])
            Follow.objects.get_or_create(follower=created_users[2], following=created_users[0])
            self.stdout.write('  ✅ Follows de demo creados')

        # ── Posts (solo texto, sin imagen real) ───────────────────────────────
        try:
            cat_almuerzo = Category.objects.get(name='Almuerzos')
            cat_postre   = Category.objects.get(name='Postres')
            cat_desayuno = Category.objects.get(name='Desayunos')
        except Category.DoesNotExist:
            self.stdout.write(self.style.WARNING(
                '  ⚠️  Categorías no encontradas. Ejecuta primero:\n'
                '      python manage.py loaddata apps/posts/fixtures/categories.json'
            ))
            cat_almuerzo = cat_postre = cat_desayuno = None

        self.stdout.write(self.style.SUCCESS('\n✅  Seed completado correctamente.\n'))
        self.stdout.write('Credenciales de acceso:')
        for data in [
            ('chef@foodgram.app', 'demo1234', 'chef_mario'),
            ('foodie@foodgram.app', 'demo1234', 'foodie_ana'),
            ('pastry@foodgram.app', 'demo1234', 'sweet_carlos'),
        ]:
            self.stdout.write(f'  📧 {data[0]}  🔑 {data[1]}  👤 @{data[2]}')
        self.stdout.write('')
