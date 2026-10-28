from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.user import User, AuditLog
from backend.app.schemas.auth import UserRegister, UserLogin, UserResponse, TokenResponse, PasswordChange
from backend.app.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    # Validate email uniqueness
    existing_user = db.query(User).filter(User.email == user_data.email.lower().strip()).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email address already exists"
        )
    
    if len(user_data.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long"
        )

    user = User(
        email=user_data.email.lower().strip(),
        full_name=user_data.full_name.strip(),
        hashed_password=hash_password(user_data.password),
        role="user",
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Log audit
    db.add(AuditLog(
        user_id=user.id,
        action="USER_REGISTERED",
        target_type="user",
        target_id=user.id,
        details=f"User {user.email} registered account"
    ))
    db.commit()

    token = create_access_token(data={"sub": str(user.id), "email": user.email, "role": user.role})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }

@router.post("/login", response_model=TokenResponse)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.email.lower().strip()).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account is deactivated. Please contact support."
        )

    token = create_access_token(data={"sub": str(user.id), "email": user.email, "role": user.role})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/change-password")
def change_password(data: PasswordChange, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not verify_password(data.old_password, current_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")
    
    if len(data.new_password) < 8:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New password must be at least 8 characters")

    current_user.hashed_password = hash_password(data.new_password)
    db.commit()
    return {"message": "Password updated successfully"}

@router.delete("/delete-account")
def delete_account(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user.id
    email = current_user.email
    db.delete(current_user)
    db.commit()

    db.add(AuditLog(
        user_id=None,
        action="USER_DELETED_ACCOUNT",
        target_type="user",
        target_id=user_id,
        details=f"User {email} deleted their account and all personal records"
    ))
    db.commit()
    return {"message": "Account and all associated private records have been permanently deleted"}
