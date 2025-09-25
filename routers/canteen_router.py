from datetime import date, timedelta
from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from auth import require_canteen
from database import get_db
from models import User, UserRole, Ticket
from schemas import (
    CanteenDayRow, CanteenDaySummary, CanteenDayResponse,
    CanteenWeekDay, CanteenWeekResponse
)

router = APIRouter(prefix="/talon", tags=["talon-canteen"])


@router.get("/canteen/day", response_model=CanteenDayResponse)
def daily_view(
    dt: date = Query(default=date.today()),
    db: Session = Depends(get_db),
    canteen = Depends(require_canteen),
):
    teacher_ids = db.query(User.id).filter(
        User.role == UserRole.teacher,
        User.canteen_id == canteen.id
    ).subquery()
    rows_raw = db.query(
        Ticket.class_name.label("class_name"),
        func.coalesce(func.sum(Ticket.paid_count), 0).label("paid"),
        func.coalesce(func.sum(Ticket.free_count), 0).label("free"),
    ).filter(
        Ticket.teacher_id.in_(teacher_ids),
        Ticket.date == dt
    ).group_by(Ticket.class_name).order_by(Ticket.class_name).all()

    rows: List[CanteenDayRow] = []
    total_paid = 0
    total_free = 0

    for r in rows_raw:
        paid = int(r.paid or 0)
        free = int(r.free or 0)
        total = paid + free
        rows.append(CanteenDayRow(
            class_name=r.class_name,
            paid_count=paid,
            free_count=free,
            total=total
        ))
        total_paid += paid
        total_free += free

    summary = CanteenDaySummary(
        total_paid=total_paid,
        total_free=total_free,
        total_all=total_paid + total_free
    )

    return CanteenDayResponse(date=dt, rows=rows, summary=summary)


@router.get("/canteen/week", response_model=CanteenWeekResponse)
def weekly_view(
    start: date = Query(default=None),
    db: Session = Depends(get_db),
    canteen = Depends(require_canteen),
):
    if start is None:
        end_default = date.today()
        start = end_default - timedelta(days=6)

    end = start + timedelta(days=6)

    teacher_ids = db.query(User.id).filter(
        User.role == UserRole.teacher,
        User.canteen_id == canteen.id
    ).subquery()
    days_map = {start + timedelta(days=i): {"paid": 0, "free": 0} for i in range(7)}

    agg = db.query(
        Ticket.date.label("d"),
        func.coalesce(func.sum(Ticket.paid_count), 0).label("paid"),
        func.coalesce(func.sum(Ticket.free_count), 0).label("free"),
    ).filter(
        Ticket.teacher_id.in_(teacher_ids),
        Ticket.date.between(start, end)
    ).group_by(Ticket.date).all()

    for row in agg:
        d = row.d
        days_map[d]["paid"] = int(row.paid or 0)
        days_map[d]["free"] = int(row.free or 0)

    days: List[CanteenWeekDay] = []
    grand_paid = 0
    grand_free = 0

    for i in range(7):
        d = start + timedelta(days=i)
        paid = days_map[d]["paid"]
        free = days_map[d]["free"]
        total = paid + free
        days.append(CanteenWeekDay(
            date=d, total_paid=paid, total_free=free, total_all=total
        ))
        grand_paid += paid
        grand_free += free

    return CanteenWeekResponse(
        start_date=start,
        end_date=end,
        days=days,
        grand_total_paid=grand_paid,
        grand_total_free=grand_free,
        grand_total_all=grand_paid + grand_free
    )
