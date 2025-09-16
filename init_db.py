# init_db.py - initialize database and create seed users and sample data
import os
from app import create_app, db
from app.models import User, Role, Order, OrderItem
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

app = create_app()
app.app_context().push()

def seed():
    db.create_all()

    # Create roles if not present
    for r in ['admin', 'cse', 'pe', 'customer', 'management']:
        if not Role.query.filter_by(name=r).first():
            db.session.add(Role(name=r))
    db.session.commit()

    def create_user(email, password, role_name, name=None):
        if User.query.filter_by(email=email).first():
            return
        role = Role.query.filter_by(name=role_name).first()
        u = User(
            email=email,
            name=name or email.split('@')[0],
            password_hash=generate_password_hash(password)
        )
        u.roles.append(role)
        db.session.add(u)
        return u

    create_user("admin@example.com", "adminpass", "admin", "Admin")
    create_user("cse@example.com", "csepass", "cse", "CSE User")
    create_user("pe@example.com", "pepass", "pe", "PE User")
    create_user("customer@example.com", "custpass", "customer", "Customer")
    create_user("mgmt@example.com", "mgmtpass", "management", "Management")

    # sample order
    if not Order.query.first():
        order = Order(
            order_number="ORD-1001",
            customer_name="Acme Corp",
            status="approved",
            created_by_email="cse@example.com",
            delivery_date=datetime.utcnow() + timedelta(days=7)
        )
        item = OrderItem(
            material="Steel Rod",
            quantity=100,
            unit="pcs",
            supplier="SteelSuppliers Ltd",
            payment_terms="Net 30"
        )
        order.items.append(item)
        db.session.add(order)

    db.session.commit()
    print("Database initialized and seeded.")

if __name__ == "__main__":
    seed()