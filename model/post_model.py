from typing import Any, Dict, Optional, Tuple
from pymysql import MySQLError as Error
import pymysql
from pymysql.cursors import DictCursor

def get_connection():
    return pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="bazzi625",
        database="practice_paging",
        cursorclass=DictCursor,
        autocommit=False,
    )

async def posts(requestData: Dict[str, Any]) -> Optional[Tuple[Dict[str, Any], ...]]:
    """
    게시글 목록 조회 모델
    - DB에서 posts 테이블을 페이징 단위로 조회합니다.
    """
    offset = requestData.get("offset")
    limit = requestData.get("limit")

    conn = None
    try:
        conn = get_connection()
        with conn.cursor(DictCursor) as cur:
            cur.execute(
                """
                SELECT id, title, author, created_at
                FROM posts
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
                """,
                (limit, offset),
            )
            rows = cur.fetchall()
        conn.commit()
        return rows
    except Error as e:
        if conn:
            conn.rollback()
        print("MySQL error in posts:", e)
        return None
    finally:
        if conn:
            conn.close()