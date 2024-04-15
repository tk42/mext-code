import dataclasses


@dataclasses.dataclass
class RawRecord:
    code: str
    text: str


@dataclasses.dataclass
class Record:
    code: str
    version: str
    school: str
    subject: str
    course: str
    goal_group: str
    grade: str
    goal: str
    detail: str
    status: str
    text: str

    def to_dict(self):
        return {
            "code": self.code,
            "version": self.version,
            "school": self.school,
            "subject": self.subject,
            "course": self.course,
            "goal_group": self.goal_group,
            "grade": self.grade,
            "goal": self.goal,
            "detail": self.detail,
            "status": self.status,
            "text": self.text,
        }
