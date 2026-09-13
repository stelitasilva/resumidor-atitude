import sqlite3
import json
import uuid
from datetime import datetime
from typing import Dict, Any, List

class SummaryRepository:
    def __init__(self, db_path: str = "resultados/summaries.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS executions (
                    id TEXT PRIMARY KEY,
                    case_id TEXT NOT NULL,
                    entry_id TEXT NOT NULL,
                    selected_record_ids TEXT NOT NULL,
                    model TEXT NOT NULL,
                    prompt_version TEXT NOT NULL,
                    generated_json TEXT NOT NULL,
                    validation_errors TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    total_seconds REAL,
                    load_seconds REAL,
                    generation_seconds REAL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS reviews (
                    id TEXT PRIMARY KEY,
                    summary_id TEXT NOT NULL,
                    reviewer TEXT NOT NULL,
                    revised_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(summary_id) REFERENCES executions(id)
                )
            """)

    def save_execution(self, data: Dict[str, Any]) -> str:
        exec_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO executions (id, case_id, entry_id, selected_record_ids, model, prompt_version, generated_json, validation_errors, created_at, total_seconds, load_seconds, generation_seconds)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                exec_id,
                data["case_id"],
                data["entry_id"],
                json.dumps(data["selected_record_ids"]),
                data["model"],
                data["prompt_version"],
                json.dumps(data["generated_json"], ensure_ascii=False),
                json.dumps(data["validation_errors"], ensure_ascii=False),
                now,
                data.get("total_seconds", 0.0),
                data.get("load_seconds", 0.0),
                data.get("generation_seconds", 0.0)
            ))
        return exec_id

    def save_review(self, summary_id: str, reviewer: str, revised_json: dict) -> str:
        review_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO reviews (id, summary_id, reviewer, revised_json, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                review_id,
                summary_id,
                reviewer,
                json.dumps(revised_json, ensure_ascii=False),
                now
            ))
        return review_id

    def get_summary(self, summary_id: str) -> Dict[str, Any]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute("SELECT * FROM executions WHERE id = ?", (summary_id,)).fetchone()
            if not row:
                return None
            
            reviews = conn.execute("SELECT * FROM reviews WHERE summary_id = ? ORDER BY created_at DESC", (summary_id,)).fetchall()
            
            return {
                "id": row["id"],
                "case_id": row["case_id"],
                "entry_id": row["entry_id"],
                "selected_record_ids": json.loads(row["selected_record_ids"]),
                "model": row["model"],
                "prompt_version": row["prompt_version"],
                "generated_json": json.loads(row["generated_json"]),
                "validation_errors": json.loads(row["validation_errors"]),
                "created_at": row["created_at"],
                "total_seconds": row["total_seconds"],
                "load_seconds": row["load_seconds"],
                "generation_seconds": row["generation_seconds"],
                "reviews": [{
                    "id": r["id"],
                    "reviewer": r["reviewer"],
                    "revised_json": json.loads(r["revised_json"]),
                    "created_at": r["created_at"]
                } for r in reviews]
            }

    def find_by_selection(self, case_id: str, entry_id: str, record_ids: List[str]) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM executions WHERE case_id = ? AND entry_id = ? ORDER BY created_at DESC", 
                (case_id, entry_id)
            ).fetchall()
            
            results = []
            target_set = set(record_ids)
            for row in rows:
                saved_ids = set(json.loads(row["selected_record_ids"]))
                if saved_ids == target_set:
                    reviews = conn.execute("SELECT * FROM reviews WHERE summary_id = ? ORDER BY created_at DESC", (row["id"],)).fetchall()
                    results.append({
                        "id": row["id"],
                        "created_at": row["created_at"],
                        "generated_json": json.loads(row["generated_json"]),
                        "reviews": [{
                            "reviewer": r["reviewer"],
                            "created_at": r["created_at"],
                            "revised_json": json.loads(r["revised_json"])
                        } for r in reviews]
                    })
            return results
