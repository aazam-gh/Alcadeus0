from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.account import Account, AccountCreate, AccountUpdate
from app.models.account import Account as AccountModel
from app.database.engine import get_db

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("", response_model=Account)
def create_account(account: AccountCreate, db: Session = Depends(get_db)) -> Account:
    """Create a new account."""
    db_account = AccountModel(**account.model_dump())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


@router.get("/{account_id}", response_model=Account)
def get_account(account_id: int, db: Session = Depends(get_db)) -> Account:
    """Get an account by ID."""
    account = db.query(AccountModel).filter(AccountModel.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.get("", response_model=list[Account])
def list_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[Account]:
    """List all accounts."""
    accounts = db.query(AccountModel).offset(skip).limit(limit).all()
    return accounts


@router.patch("/{account_id}", response_model=Account)
def update_account(
    account_id: int,
    account_update: AccountUpdate,
    db: Session = Depends(get_db)
) -> Account:
    """Update an account."""
    db_account = db.query(AccountModel).filter(AccountModel.id == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    update_data = account_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_account, field, value)
    
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


@router.delete("/{account_id}")
def delete_account(account_id: int, db: Session = Depends(get_db)):
    """Delete an account."""
    db_account = db.query(AccountModel).filter(AccountModel.id == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    db.delete(db_account)
    db.commit()
    return {"detail": "Account deleted successfully"}
