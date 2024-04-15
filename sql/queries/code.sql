-- name: GetCode :one
SELECT * FROM codes
WHERE code = $1;

-- name: ListCode :many
SELECT * FROM codes
ORDER BY code;

-- name: CreateCode :one
INSERT INTO codes (code, version, school, subject, course, goal_group, grade, goal, detail, status, text)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
RETURNING *;

-- name: UpdateCode :one
UPDATE codes
SET code = $2, version = $3, school = $4, subject = $5, course = $6, goal_group = $7, grade = $8, goal = $9, detail = $10, status = $11, text = $12
WHERE id = $1
RETURNING *;

-- name: DeleteCode :one
DELETE FROM codes
WHERE id = $1
RETURNING *;
