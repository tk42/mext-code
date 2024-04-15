import csv
from datatypes.record import RawRecord, Record
from hasura import insert_data


def read_csv(file_path: str) -> list[RawRecord]:
    reader = csv.reader(open(file_path, "r"))
    recs = []
    for i, r in enumerate(reader):
        if i < 2:
            continue
        recs += [RawRecord(code=r[3], text=r[2])]
    return recs


def convert_record(raw: RawRecord) -> Record:
    return Record(
        code=raw.code,
        version=raw.code[0],
        school=raw.code[1],
        subject=raw.code[2],
        course=raw.code[3],
        goal_group=raw.code[4],
        grade=raw.code[5],
        goal=raw.code[6],
        detail=raw.code[7:15],
        status=raw.code[15],
        text=raw.text,
    )


if __name__ == "__main__":
    recs = read_csv("./sample/20230901-mxt_syoto01-000013115_37.csv")
    recs = [convert_record(r).to_dict() for r in recs]
    result = insert_data(recs)
    try:
        print(result["data"]["insert_codes"]["affected_rows"])
    except Exception as e:
        print(e)
        print(result)
