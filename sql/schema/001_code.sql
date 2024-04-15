-- +goose Up
CREATE TABLE IF NOT EXISTS codes (
    id BIGSERIAL PRIMARY KEY,
    code CHAR(16) NOT NULL,
    version CHAR(1) NOT NULL,
    school CHAR(1) NOT NULL,
    subject CHAR(1) NOT NULL,
    course CHAR(1) NOT NULL,
    goal_group CHAR(1) NOT NULL,
    grade CHAR(1) NOT NULL,
    goal CHAR(1) NOT NULL,
    detail CHAR(8) NOT NULL,
    status CHAR(1) NOT NULL,
    text TEXT NOT NULL
);

-- +goose Down
DROP TABLE IF EXISTS codes;
