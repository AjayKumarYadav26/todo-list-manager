import uuid
from datetime import datetime, date


VALID_STATUSES = ("pending", "in_progress", "completed")
VALID_PRIORITIES = ("high", "medium", "low")
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}
STATUS_ORDER = {"pending": 0, "in_progress": 1, "completed": 2}


def _utc_now_iso() -> str:
    return datetime.utcnow().isoformat()


def create_todo(data: dict) -> dict:
    title = (data.get("title") or "").strip()
    if not title:
        raise ValueError("Title is required")
    if len(title) > 200:
        raise ValueError("Title must be 200 characters or less")

    priority = data.get("priority", "medium")
    if priority not in VALID_PRIORITIES:
        raise ValueError(f"Priority must be one of: {', '.join(VALID_PRIORITIES)}")

    due_date = data.get("due_date") or None
    if due_date:
        try:
            date.fromisoformat(due_date)
        except (ValueError, TypeError):
            raise ValueError("Due date must be in YYYY-MM-DD format")

    now = _utc_now_iso()
    return {
        "id": str(uuid.uuid4()),
        "title": title,
        "description": (data.get("description") or "").strip(),
        "status": "pending",
        "priority": priority,
        "category": (data.get("category") or "").strip(),
        "due_date": due_date,
        "created_at": now,
        "updated_at": now,
        "completed_at": None,
    }


def validate_update(data: dict) -> dict:
    cleaned = {}

    if "title" in data:
        title = (data["title"] or "").strip()
        if not title:
            raise ValueError("Title is required")
        if len(title) > 200:
            raise ValueError("Title must be 200 characters or less")
        cleaned["title"] = title

    if "description" in data:
        cleaned["description"] = (data["description"] or "").strip()

    if "status" in data:
        if data["status"] not in VALID_STATUSES:
            raise ValueError(f"Status must be one of: {', '.join(VALID_STATUSES)}")
        cleaned["status"] = data["status"]

    if "priority" in data:
        if data["priority"] not in VALID_PRIORITIES:
            raise ValueError(f"Priority must be one of: {', '.join(VALID_PRIORITIES)}")
        cleaned["priority"] = data["priority"]

    if "category" in data:
        cleaned["category"] = (data["category"] or "").strip()

    if "due_date" in data:
        due_date = data["due_date"] or None
        if due_date:
            try:
                date.fromisoformat(due_date)
            except (ValueError, TypeError):
                raise ValueError("Due date must be in YYYY-MM-DD format")
        cleaned["due_date"] = due_date

    if not cleaned:
        raise ValueError("No valid fields to update")

    cleaned["updated_at"] = _utc_now_iso()

    if "status" in cleaned:
        if cleaned["status"] == "completed":
            cleaned["completed_at"] = _utc_now_iso()
        else:
            cleaned["completed_at"] = None

    return cleaned


def matches_filters(todo: dict, filters: dict) -> bool:
    if "status" in filters and filters["status"]:
        statuses = [s.strip() for s in filters["status"].split(",")]
        if todo["status"] not in statuses:
            return False

    if "priority" in filters and filters["priority"]:
        priorities = [p.strip() for p in filters["priority"].split(",")]
        if todo["priority"] not in priorities:
            return False

    if "category" in filters and filters["category"]:
        if todo.get("category", "").lower() != filters["category"].lower():
            return False

    if "search" in filters and filters["search"]:
        query = filters["search"].lower()
        title = (todo.get("title") or "").lower()
        desc = (todo.get("description") or "").lower()
        if query not in title and query not in desc:
            return False

    return True


def sort_todos(todos: list, sort_by: str = "created_at", sort_order: str = "desc") -> list:
    reverse = sort_order == "desc"

    if sort_by == "priority":
        key = lambda t: PRIORITY_ORDER.get(t.get("priority", "medium"), 1)
        reverse = not reverse
    elif sort_by == "status":
        key = lambda t: STATUS_ORDER.get(t.get("status", "pending"), 0)
    elif sort_by == "due_date":
        key = lambda t: t.get("due_date") or "9999-12-31"
    elif sort_by == "title":
        key = lambda t: (t.get("title") or "").lower()
    else:
        key = lambda t: t.get("created_at", "")

    return sorted(todos, key=key, reverse=reverse)


def compute_stats(todos: list) -> dict:
    total = len(todos)
    by_status = {"pending": 0, "in_progress": 0, "completed": 0}
    by_priority = {"high": 0, "medium": 0, "low": 0}
    by_category = {}
    overdue_count = 0
    completed_today = 0
    created_this_week = 0
    today = date.today()
    week_ago = today.toordinal() - 7

    for t in todos:
        by_status[t.get("status", "pending")] = by_status.get(t.get("status", "pending"), 0) + 1
        by_priority[t.get("priority", "medium")] = by_priority.get(t.get("priority", "medium"), 0) + 1

        cat = t.get("category") or "Uncategorized"
        by_category[cat] = by_category.get(cat, 0) + 1

        if t.get("due_date") and t.get("status") != "completed":
            try:
                if date.fromisoformat(t["due_date"]) < today:
                    overdue_count += 1
            except ValueError:
                pass

        if t.get("completed_at"):
            try:
                comp_date = datetime.fromisoformat(t["completed_at"]).date()
                if comp_date == today:
                    completed_today += 1
            except ValueError:
                pass

        if t.get("created_at"):
            try:
                created_date = datetime.fromisoformat(t["created_at"]).date()
                if created_date.toordinal() >= week_ago:
                    created_this_week += 1
            except ValueError:
                pass

    completion_rate = round((by_status["completed"] / total * 100), 1) if total > 0 else 0

    return {
        "total": total,
        "by_status": by_status,
        "by_priority": by_priority,
        "by_category": by_category,
        "overdue_count": overdue_count,
        "completion_rate": completion_rate,
        "completed_today": completed_today,
        "created_this_week": created_this_week,
    }
