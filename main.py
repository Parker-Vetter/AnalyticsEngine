from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas
import logging
from database import engine, get_db, USE_DB

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(name)s:%(message)s"
)

logger = logging.getLogger(__name__)

# Only create tables if DB is enabled
if USE_DB and engine is not None:
    models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {
        "message": "AnalyticsEngine is running",
        "database": "connected" if USE_DB else "disabled"
    }

@app.post("/stats/kills")
def submit_kills(stat: schemas.StatSubmit, db: Session = Depends(get_db)):
    if not USE_DB or db is None:
        logger.info(f"[DB DISABLED] Received stat submission: player_id={stat.player_id}, kills={stat.kills}")
        return {"message": "DB is disabled, stat not saved"}
    
    player = db.query(models.PlayerStats).filter(
        models.PlayerStats.player_id == stat.player_id
    ).first()

    if player:
        player.total_kills += stat.kills
    else:
        player = models.PlayerStats(player_id=stat.player_id, total_kills=stat.kills)
        db.add(player)

    db.commit()
    db.refresh(player)
    return {"player_id": player.player_id, "total_kills": player.total_kills}