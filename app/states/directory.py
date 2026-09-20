import reflex as rx

import logging
from string import ascii_uppercase
from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from app.models import Username


SAMPLE_USERNAMES = (
    "amber",
    "boon",
    "clover",
    "drift",
    "ember",
    "fern",
    "grove",
    "harbor",
    "indigo",
    "juniper",
    "kestrel",
    "linden",
    "moss",
    "north",
    "olive",
    "paper",
    "quill",
    "river",
    "sage",
    "timber",
    "umber",
    "violet",
    "willow",
    "xenon",
    "yarrow",
    "zephyr",
)


class DirectoryState(rx.State):
    search: str = ""
    initial: str = "All"
    letters: list[str] = list(ascii_uppercase)
    rows: list[dict[str, str]] = []
    total: int = 0
    indexed: int = 0
    loading: bool = True
    error: str = ""

    @rx.var
    def result_count(self) -> int:
        return len(self.rows)

    @rx.var
    def filtered(self) -> bool:
        return bool(self.search or self.initial != "All")

    @rx.var
    def display_state(self) -> str:
        if self.loading:
            return "loading"
        if self.error:
            return "error"
        if not self.rows:
            return "empty"
        return "ready"

    def _query(self):
        try:
            with rx.session() as session:
                statement = select(Username)
                if self.search.strip():
                    statement = statement.where(
                        Username.username.icontains(
                            self.search.strip(), autoescape=True
                        )
                    )
                if self.initial != "All":
                    statement = statement.where(
                        func.upper(Username.initial_letter) == self.initial
                    )
                records = session.scalars(
                    statement.order_by(
                        func.lower(Username.username),
                        Username.username,
                        Username.id,
                    )
                ).all()
                self.rows = [
                    {
                        "username": row.username,
                        "initial": row.initial_letter.upper(),
                        "number": f"{row.id:03d}",
                    }
                    for row in records
                ]
                self.total = (
                    session.scalar(select(func.count()).select_from(Username))
                    or 0
                )
                self.indexed = (
                    session.scalar(
                        select(
                            func.count(func.distinct(Username.initial_letter))
                        )
                    )
                    or 0
                )
            self.error = ""
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.rows = []
            self.total = 0
            self.indexed = 0
            self.error = "The directory couldn't be loaded. Please try again."
        finally:
            self.loading = False

    @rx.event
    def load(self):
        self.loading = True
        self.error = ""
        yield
        try:
            with rx.session() as session:
                existing = session.scalars(select(Username)).all()
                names = {row.username.casefold() for row in existing}
                initials = {row.initial_letter.upper() for row in existing}
                samples = [
                    {"username": name, "initial_letter": name[0].upper()}
                    for name in SAMPLE_USERNAMES
                    if name.casefold() not in names
                    and name[0].upper() not in initials
                ]
                if samples:
                    session.execute(
                        insert(Username)
                        .values(samples)
                        .on_conflict_do_nothing()
                    )
                    session.commit()
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.rows = []
            self.error = (
                "The directory couldn't be initialized. Please try again."
            )
            self.loading = False
            return
        self._query()

    @rx.event
    def search_changed(self, value: str):
        self.search = value
        self.loading = True
        yield
        self._query()

    @rx.event
    def select_initial(self, value: str):
        if value not in self.letters and value != "All":
            return
        self.initial = value
        self.loading = True
        yield
        self._query()

    @rx.event
    def clear_filters(self):
        self.search = ""
        self.initial = "All"
        self.loading = True
        yield
        self._query()
