from datetime import date, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth import require_teacher
from database import get_db
from models import Ticket
from schemas import TicketCreate, TicketOut

router = APIRouter(prefix="/tickets", tags=["tickets-teacher"])


@router.post("/submit", response_model=TicketOut)
def submit_ticket(
    payload: TicketCreate,
    db: Session = Depends(get_db),
    teacher = Depends(require_teacher),
):
    target_date = payload.date or date.today()

    existing = db.query(Ticket).filter(
        Ticket.teacher_id == teacher.id,
        Ticket.date == target_date
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Ticket for this date already submitted")

    ticket = Ticket(
        date=target_date,
        paid_count=payload.paid_count,
        benefit_count=payload.benefit_count,
        class_name=teacher.class_name or "N/A",
        teacher_id=teacher.id,
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return TicketOut(
        id=ticket.id,
        date=ticket.date,
        class_name=ticket.class_name,
        paid_count=ticket.paid_count,
        free_count=ticket.free_count,
        total=ticket.paid_count + ticket.benefit_count
    )


@router.get("/teacher/week", response_model=list[TicketOut])
def get_teacher_week(
    db: Session = Depends(get_db),
    teacher = Depends(require_teacher),
):
    end = date.today()
    start = end - timedelta(days=6)

    tickets = db.query(Ticket).filter(
        Ticket.teacher_id == teacher.id,
        Ticket.date.between(start, end)
    ).order_by(Ticket.date.desc()).all()

    return [
        TicketOut(
            id=t.id,
            date=t.date,
            class_name=t.class_name,
            paid_count=t.paid_count,
            free_count=t.free_count,
            total=t.paid_count + t.free_count
        ) for t in tickets
    ]
