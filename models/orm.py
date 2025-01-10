import logging
from db.connect import cur, conn

logging.basicConfig(level=logging.INFO)

def execute_query(query, params=None, fetchone=False, fetchall=False, commit=False):
    """
    General function to execute SQL queries.
    """
    try:
        cur.execute(query, params or ())
        if commit:
            conn.commit()
        if fetchone:
            return cur.fetchone()
        if fetchall:
            return cur.fetchall()
    except Exception as e:
        logging.error(f"Query failed: {query} | Error: {e}")
        raise e

class Base:
    def __init__(self, table):
        self.table = table

    def create(self, **kwargs):
        keys = ', '.join(kwargs.keys())
        values = ', '.join(['%s'] * len(kwargs))
        query = f"INSERT INTO {self.table}({keys}) VALUES ({values})"
        execute_query(query, tuple(kwargs.values()), commit=True)

    def get(self, **conditions):
        keys = ' AND '.join([f"{key} = %s" for key in conditions.keys()])
        query = f"SELECT * FROM {self.table} WHERE {keys}"
        return execute_query(query, tuple(conditions.values()), fetchone=True)

    def get_all(self, **conditions):
        if conditions:
            keys = ' AND '.join([f"{key} = %s" for key in conditions.keys()])
            query = f"SELECT * FROM {self.table} WHERE {keys}"
            return execute_query(query, tuple(conditions.values()), fetchall=True)
        query = f"SELECT * FROM {self.table}"
        return execute_query(query, fetchall=True)

    def delete(self, **conditions):
        keys = ' AND '.join([f"{key} = %s" for key in conditions.keys()])
        query = f"DELETE FROM {self.table} WHERE {keys}"
        execute_query(query, tuple(conditions.values()), commit=True)

    def statistika(self):
        """
        Retrieve statistics for the last day, week, and month.
        """
        intervals = {
            "day": "1 day",
            "week": "1 week",
            "month": "1 month"
        }
        stats = {}
        for key, interval in intervals.items():
            query = f"SELECT * FROM {self.table} WHERE created_at >= NOW() - INTERVAL %s"
            stats[key] = execute_query(query, (interval,), fetchall=True)
        return stats

class MediaClass(Base):
    def create_data(self, file_id: str, caption: str, post_id: int, url: str):
        self.create(file_id=file_id, caption=caption, post_id=post_id, url=url)

    def delete_movie(self, post_id: int):
        self.delete(post_id=post_id)

    def get_max_id(self):
        query = f"SELECT max(id) FROM {self.table}"
        return execute_query(query, fetchone=True)

class ChannelClass(Base):
    def create_data(self, username: str, channel_id: str, is_order: bool):
        self.create(username=username, channel_id=channel_id, is_order=is_order)

    def delete_data(self, channel_id: str):
        try:
            conn.begin()
            self.delete(channel_id=channel_id)
            query_request = "DELETE FROM join_requests WHERE channel_id = %s"
            execute_query(query_request, (channel_id,), commit=False)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e

class LinkClass(Base):
    def create_data(self, link: str):
        self.create(link=link)

class JoinRequest(Base):
    def create_data(self, channel_id: str, user_id: str):
        self.create(channel_id=channel_id, user_id=user_id)
