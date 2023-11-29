from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from models.purchase_history_model import PurchaseHistoryModel
from models.user_model import UserModel
from schemas.purchase_history_schema import PurchaseHistorySchema
from core.deps import get_session, get_current_user

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED,
             response_model=PurchaseHistorySchema)
async def post_article(logged_user: UserModel = Depends(get_current_user),
                       db: AsyncSession = Depends(get_session)):

    new_purchase: PurchaseHistoryModel = PurchaseHistoryModel(
        customer=logged_user.id)

    db.add(new_purchase)
    await db.commit()

    return new_purchase
