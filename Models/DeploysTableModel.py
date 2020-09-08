from dataclasses import dataclass, field
import datetime


@dataclass
class DeploysTableModel:
    start_changeset_id: int
    end_changeset_id: int
    deployment_date: datetime

    def __iter__(self):
        yield self.start_changeset_id
        yield self.end_changeset_id
        yield self.deployment_date
