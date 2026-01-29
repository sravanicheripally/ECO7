"""
Migration script to normalize existing role and permission codes to uppercase format.
Run this BEFORE deploying the new validation rules to the database.

Usage:
    python scripts/normalize_role_codes.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.core.database import engine, SessionLocal
from app.models.user_role import UserRole
from app.models.user_permission import UserPermission


def normalize_role_codes():
    """Normalize all UserRole codes to uppercase format"""
    db: Session = SessionLocal()
    
    try:
        roles = db.query(UserRole).all()
        updated_count = 0
        errors = []
        
        print(f"Found {len(roles)} roles to check...")
        
        for role in roles:
            original_code = role.code
            normalized_code = original_code.strip().upper()
            
            if original_code != normalized_code:
                # Check if normalized code already exists
                existing = db.query(UserRole).filter(
                    UserRole.code == normalized_code,
                    UserRole.id != role.id
                ).first()
                
                if existing:
                    errors.append(
                        f"⚠️  CONFLICT: Role '{role.name}' (code: {original_code}) "
                        f"conflicts with existing code {normalized_code}. "
                        f"Please manually resolve before applying validation."
                    )
                else:
                    role.code = normalized_code
                    updated_count += 1
                    print(f"✓ Updated: {original_code} → {normalized_code}")
        
        if errors:
            print("\n⚠️  CONFLICTS FOUND - Fix these before proceeding:")
            for error in errors:
                print(f"  {error}")
            db.rollback()
            return False
        
        if updated_count > 0:
            db.commit()
            print(f"\n✅ Successfully updated {updated_count} role codes")
        else:
            print("\n✅ All role codes are already in correct format")
        
        return True
        
    except Exception as e:
        print(f"❌ Error normalizing roles: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def normalize_permission_codes():
    """Normalize all UserPermission codes to uppercase format"""
    db: Session = SessionLocal()
    
    try:
        permissions = db.query(UserPermission).all()
        updated_count = 0
        errors = []
        
        print(f"\nFound {len(permissions)} permissions to check...")
        
        for permission in permissions:
            original_code = permission.code
            normalized_code = original_code.strip().upper()
            
            if original_code != normalized_code:
                # Check if normalized code already exists
                existing = db.query(UserPermission).filter(
                    UserPermission.code == normalized_code,
                    UserPermission.id != permission.id
                ).first()
                
                if existing:
                    errors.append(
                        f"⚠️  CONFLICT: Permission '{permission.name}' (code: {original_code}) "
                        f"conflicts with existing code {normalized_code}. "
                        f"Please manually resolve before applying validation."
                    )
                else:
                    permission.code = normalized_code
                    updated_count += 1
                    print(f"✓ Updated: {original_code} → {normalized_code}")
        
        if errors:
            print("\n⚠️  CONFLICTS FOUND - Fix these before proceeding:")
            for error in errors:
                print(f"  {error}")
            db.rollback()
            return False
        
        if updated_count > 0:
            db.commit()
            print(f"\n✅ Successfully updated {updated_count} permission codes")
        else:
            print("\n✅ All permission codes are already in correct format")
        
        return True
        
    except Exception as e:
        print(f"❌ Error normalizing permissions: {e}")
        db.rollback()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("Role & Permission Code Normalization Script")
    print("=" * 60)
    
    roles_ok = normalize_role_codes()
    perms_ok = normalize_permission_codes()
    
    print("\n" + "=" * 60)
    if roles_ok and perms_ok:
        print("✅ All codes normalized successfully!")
        print("\nYou can now safely apply the validation constraints.")
    else:
        print("❌ Fix the conflicts above before proceeding")
    print("=" * 60)
