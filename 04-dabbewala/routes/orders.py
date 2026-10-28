from fastapi import APIRouter, Depends, HTTPException, Query
from database import get_session
from sqlmodel import Session, select
from models import Order, OrderCreate, OrderUpdate, StatusLog, OrderStatus
from datetime import datetime, timezone

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=Order)
def create_order(order: OrderCreate, session: Session = Depends(get_session)):
    db_order = Order(**order.model_dump())
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order


@router.get("/", response_model=list[Order])
def list_orders(
    status: OrderStatus | None = Query(default=None, description="Filter by order status"),
    created_date: datetime | None = Query(default=None, description="Filter by creation date (YYYY-MM-DD)"),
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=20, ge=1, le=100, description="Maximum number of records to return"),
    session: Session = Depends(get_session)
):
    query = select(Order)

    if status:
        query = query.where(Order.status == status)
    if created_date:
        start = datetime.combine(created_date, datetime.min.time()).replace(tzinfo=timezone.utc)
        end = datetime.combine(created_date, datetime.max.time()).replace(tzinfo=timezone.utc)
        query = query.where(Order.created_at >= start, Order.created_at <= end)

    query = query.offset(skip).limit(limit)

    orders = session.exec(query).all()
    return orders
