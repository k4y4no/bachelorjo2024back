# scripts/seed.py
from datetime import date
from sqlalchemy.orm import Session
from src.model.event import Sport, Location, Event
from src.model.user import Role, User
from src.config.hash import pwd_context
import secrets

def seed(db: Session):
    # évite de doubler le seed
    if db.query(Sport).first():
        return

    natation = Sport(name='Natation')
    course = Sport(name='Course')
    saut = Sport(name='Saut')

    piscine = Location(name='Piscine', nb_places=75)
    terrain = Location(name='Terrain', nb_places=60)
    terrain2 = Location(name='Terrain 2', nb_places=100)

    admin_role = Role(name='admin')
    user_role = Role(name='user')

    db.add_all([natation, course, saut, piscine, terrain, terrain2, admin_role, user_role])
    db.flush()  # pour avoir les IDs si tu veux passer par *_id

    # Version RELATIONNELLE (recommandée)
    event1 = Event(sport=natation, location=piscine,  date_event=date.today())
    event2 = Event(sport=course,   location=terrain,  date_event=date.today())
    event3 = Event(sport=course,   location=terrain2, date_event=date.today())
    event4 = Event(sport=saut,     location=terrain,  date_event=date.today())

    db.add_all([event1, event2, event3, event4])

        # Ajout des utilisateurs
    # Vérifie s'il y a déjà un admin
    admin_exists = db.query(User).join(User.roles).filter(Role.name == "admin").first()
    roles = db.query(Role).all()
    admin_role_obj = next((r for r in roles if r.name == "admin"), None)
    user_role_obj = next((r for r in roles if r.name == "user"), None)

    # Premier user : admin si aucun admin existe
    first_user_roles = [admin_role_obj] if not admin_exists else [user_role_obj]
    user1 = User(
        name="Doe",
        firstname="John",
        email="john.doe@example.com",
        phone="0600000001",
        password=pwd_context.hash("password1"),
        hidden_key=secrets.token_urlsafe(32),
        roles=first_user_roles
    )
    # Second user : user
    user2 = User(
        name="Smith",
        firstname="Jane",
        email="jane.smith@example.com",
        phone="0600000002",
        password=pwd_context.hash("password2"),
        hidden_key=secrets.token_urlsafe(32),
        roles=[user_role_obj]
    )

    db.add_all([user1, user2])
    db.commit()
