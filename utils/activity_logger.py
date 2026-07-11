from models import ActivityLog, db


def record_activity(
    user_id,
    action,
    entity_type,
    entity_name,
    description,
):
    activity = ActivityLog(
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_name=entity_name,
        description=description,
    )

    db.session.add(activity)