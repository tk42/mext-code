import os
import httpx
from datatypes.record import Record

HASURA_URL = os.getenv("HASURA_URL")
HASURA_SECRET = os.getenv("HASURA_SECRET")


def read_by_subject(subject: str, goal: list[str], limit: int = 10):
    headers = {
        "Content-Type": "application/json",
        "x-hasura-admin-secret": HASURA_SECRET,
    }
    query = """
    query MyQuery($subject: bpchar!, $goal: [bpchar!]!, $limit: Int!) {
        codes (
            where: {
                version: {
                    _eq: "8"
                },
                school: {
                    _eq: "3"
                },
                subject: {
                    _eq: $subject
                },
                goal: {
                    _in: $goal
                }
            },
            limit: $limit,
            order_by: {
                code: asc
            }
        ) {
            code
            text
        }
    }
    """
    variables = {"subject": subject, "goal": goal, "limit": limit}
    result = httpx.post(
        HASURA_URL, json={"query": query, "variables": variables}, headers=headers
    )
    return result.json()


def insert_data(records: list[Record]):
    headers = {
        "Content-Type": "application/json",
        "x-hasura-admin-secret": HASURA_SECRET,
    }
    query = """
    mutation MyMutation($objects: [codes_insert_input!]!){
        insert_codes(objects: $objects) {
            returning {
                id
                code
            }
            affected_rows
        }
    }
    """
    variables = {"objects": records}
    result = httpx.post(
        HASURA_URL, json={"query": query, "variables": variables}, headers=headers
    )
    return result.json()
