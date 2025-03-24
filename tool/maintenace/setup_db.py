#!/usr/bin/env python
from tool.models import *
from tool import db, app
import sys


def initialize_database():
    try:
        print("Initializing database...")
        
        # user flask app context
        with app.app_context():
            # Create all database tables
            db.create_all()
            print("Database tables created successfully!")
            
            # You can add initial data here if needed
            # Example:
            # if not User.query.first():
            #     admin = User(username='admin', email='admin@example.com')
            #     db.session.add(admin)
            #     db.session.commit()
            #     print("Initial admin user created")
            
        return True
    except Exception as e:
        print(f"Error initializing database: {str(e)}", file=sys.stderr)
        return False

if __name__ == '__main__':
    if initialize_database():
        print("Database initialization completed successfully!")
        sys.exit(0)
    else:
        print("Database initialization failed!", file=sys.stderr)
        sys.exit(1)
