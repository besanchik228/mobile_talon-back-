from datetime import date, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth import require_teacher
from database import get_db
from models import Ticket
from schemas import TicketCreate, TicketOut

# Роутер для работы с талонами (учительская часть)
router = APIRouter(prefix="/teacher", tags=["talon-teacher"])


@router.post("/submit", response_model=TicketOut)
def submit_ticket(
    payload: TicketCreate,                 # Данные, которые передаёт учитель (кол-во талонов, дата)
    db: Session = Depends(get_db),        # Сессия базы данных
    teacher = Depends(require_teacher),   # Проверка, что запрос делает именно учитель
):
    """
    Эндпоинт для подачи талонов учителем.
    - Если дата не указана — используется текущая.
    - Проверяется, что на эту дату учитель ещё не подавал талон.
    - Создаётся новая запись Ticket и сохраняется в БД.
    """

    # Если дата не указана — берём сегодняшнюю
    target_date = payload.date or date.today()

    # Проверяем, не существует ли уже талон на эту дату от этого учителя
    existing = db.query(Ticket).filter(
        Ticket.teacher_id == teacher.id,
        Ticket.date == target_date
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Ticket for this date already submitted")

    # Создаём новый талон
    ticket = Ticket(
        date=target_date,
        paid_count=payload.paid_count,
        free_count=payload.free_count,   # льготные (free) талоны
        class_name=teacher.class_name or "N/A",
        teacher_id=teacher.id,
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    # Возвращаем данные в формате схемы TicketOut
    return TicketOut(
        id=ticket.id,
        date=ticket.date,
        class_name=ticket.class_name,
        paid_count=ticket.paid_count,
        free_count=ticket.free_count,  # поле в модели
        total=ticket.paid_count + ticket.free_count
    )


@router.get("/week", response_model=list[TicketOut])
def get_teacher_week(
    db: Session = Depends(get_db),
    teacher = Depends(require_teacher),
):
    """
    Эндпоинт для получения списка талонов учителя за последние 7 дней.
    - Формируется диапазон дат: сегодня и 6 предыдущих дней.
    - Выбираются все талоны учителя за этот период.
    - Результат сортируется по дате (от новых к старым).
    """

    # Определяем диапазон дат (последние 7 дней)
    end = date.today()
    start = end - timedelta(days=6)

    # Получаем все талоны учителя за неделю
    tickets = db.query(Ticket).filter(
        Ticket.teacher_id == teacher.id,
        Ticket.date.between(start, end)
    ).order_by(Ticket.date.desc()).all()

    # Преобразуем объекты в список схем