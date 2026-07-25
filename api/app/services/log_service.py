from app.database.connection import SessionLocal
from app.models.log import Log
from app.schemas.log import LogSchema
from sqlalchemy import func, text, or_
from datetime import datetime, timedelta, timezone

class LogService:


    @staticmethod
    async def create(log: LogSchema):

        db = SessionLocal()

        try:

            novo_log = Log(
                application=log.application,
                service=log.service,
                level=log.level,
                message=log.message,
                environment=log.environment,
                request_id=log.request_id,
                context=log.context
            )

            db.add(novo_log)
            db.commit()
            db.refresh(novo_log)

            return {
                "message": "Log recebido",
                "id": novo_log.id
            }

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()



    @staticmethod
    async def list(
        level=None,
        service=None,
        application=None,
        environment=None,
        search=None,
        start_date=None,
        end_date=None,
        page=1,
        limit=50
    ):

        db = SessionLocal()

        try:

            query = db.query(Log)


            if level:
                query = query.filter(Log.level == level.upper())

            if service:
                query = query.filter(Log.service == service)

            if application:
                query = query.filter(Log.application == application)

            if environment:
                query = query.filter(Log.environment == environment)

            if search:
                query = query.filter(
                    or_(
                        Log.message.ilike(f"%{search}%"),
                        Log.request_id.ilike(f"%{search}%")
                    )
                )

            if start_date:
                query = query.filter(
                    Log.created_at >= datetime.fromisoformat(start_date)
                )

            if end_date:
                query = query.filter(
                    Log.created_at <= datetime.fromisoformat(end_date)
                )


            total = query.count()


            logs = (
                query
                .order_by(Log.created_at.desc())
                .offset((page - 1) * limit)
                .limit(limit)
                .all()
            )


            return {
                "total": total,
                "page": page,
                "limit": limit,
                "data": logs
            }


        finally:
            db.close()



    @staticmethod
    async def timeline(minutes=60):

        db = SessionLocal()

        try:

            agora = datetime.now(timezone.utc)

            inicio = agora - timedelta(
                minutes=minutes
            )


            minutos = (
                func.generate_series(
                    inicio,
                    agora,
                    text("interval '1 minute'")
                )
                .table_valued(
                    "minutos"
                )
                .alias("minutos")
            )


            logs = (
                db.query(
                    func.date_trunc(
                        "minute",
                        Log.created_at
                    ).label("time"),

                    func.count(Log.id).label("total")
                )
                .filter(
                    Log.created_at >= inicio
                )
                .group_by(
                    func.date_trunc(
                        "minute",
                        Log.created_at
                    )
                )
                .subquery()
            )


            result = (
                db.query(
                    func.to_char(
                        minutos.c.minutos,
                        "HH24:MI"
                    ).label("time"),

                    func.coalesce(
                        logs.c.total,
                        0
                    ).label("total")
                )
                .select_from(
                    minutos
                )
                .outerjoin(
                    logs,
                    logs.c.time == minutos.c.minutos
                )
                .order_by(
                    minutos.c.minutos
                )
                .all()
            )


            return [
                {
                    "time": item.time,
                    "total": item.total
                }
                for item in result
            ]


        finally:
            db.close()


    @staticmethod
    async def stats():

        db = SessionLocal()

        try:

            total = db.query(Log).count()


            levels = (
                db.query(
                    Log.level,
                    func.count(Log.id)
                )
                .group_by(Log.level)
                .all()
            )


            services = (
                db.query(
                    Log.service,
                    func.count(Log.id)
                )
                .group_by(Log.service)
                .all()
            )


            applications = (
                db.query(
                    Log.application,
                    func.count(Log.id)
                )
                .group_by(Log.application)
                .all()
            )


            return {
                "total": total,
                "levels": dict(levels),
                "services": dict(services),
                "applications": dict(applications)
            }


        finally:
            db.close()

    @staticmethod
    async def create_bulk(logs):

        db = SessionLocal()

        try:

            novos_logs = []


            for log in logs:

                novos_logs.append(
                    Log(
                        application=log.application,
                        service=log.service,
                        level=log.level,
                        message=log.message,
                        environment=log.environment,
                        request_id=log.request_id,
                        context=log.context
                    )
                )


            db.bulk_save_objects(novos_logs)
            db.commit()


            return {
                "message": "Logs recebidos",
                "total": len(novos_logs)
            }


        except Exception:
            db.rollback()
            raise


        finally:
            db.close()