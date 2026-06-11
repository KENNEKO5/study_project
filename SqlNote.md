
# SQL 構文一覧（学習・開発支援用）

SQL の主要構文を体系的にまとめたチートシートです。  
主要 DB（MySQL / PostgreSQL / SQL Server / Oracle）で共通して使える構文を網羅しています。

---

# 1. データベース操作（DDL）

## CREATE DATABASE
```sql
CREATE DATABASE db_name;
```

## DROP DATABASE
```sql
DROP DATABASE db_name;
```

## USE（DB選択）
```sql
USE db_name;
```

---

# 2. テーブル操作（DDL）

## CREATE TABLE
```sql
CREATE TABLE table_name (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    created_at TIMESTAMP
);
```

## DROP TABLE
```sql
DROP TABLE table_name;
```

## ALTER TABLE
```sql
ALTER TABLE table_name ADD column_name datatype;
ALTER TABLE table_name DROP COLUMN column_name;
ALTER TABLE table_name RENAME TO new_table_name;
ALTER TABLE table_name MODIFY column_name datatype;
```

## TRUNCATE TABLE
```sql
TRUNCATE TABLE table_name;
```

---

# 3. データ操作（DML）

## INSERT
```sql
INSERT INTO table_name (col1, col2) VALUES ('A', 123);
INSERT INTO table_name VALUES ('A', 123, NOW());
```

## UPDATE
```sql
UPDATE table_name SET col1 = 'B' WHERE id = 1;
```

## DELETE
```sql
DELETE FROM table_name WHERE id = 1;
```

---

# 4. データ取得（SELECT）

## 基本 SELECT
```sql
SELECT * FROM table_name;
SELECT col1, col2 FROM table_name;
```

## DISTINCT
```sql
SELECT DISTINCT col1 FROM table_name;
```

## WHERE
```sql
SELECT * FROM table_name WHERE col1 = 'A';
```

## 比較演算子
```sql
=   <>   !=   >   <   >=   <=
```

## BETWEEN
```sql
SELECT * FROM table_name WHERE price BETWEEN 100 AND 200;
```

## IN
```sql
SELECT * FROM table_name WHERE status IN ('A', 'B');
```

## LIKE
```sql
SELECT * FROM table_name WHERE name LIKE 'A%';
```

## IS NULL
```sql
SELECT * FROM table_name WHERE deleted_at IS NULL;
```

---

# 5. 集計（GROUP BY / HAVING）

## GROUP BY
```sql
SELECT category, COUNT(*) FROM items GROUP BY category;
```

## HAVING（集計後の条件）
```sql
SELECT category, COUNT(*) 
FROM items 
GROUP BY category
HAVING COUNT(*) > 10;
```

---

# 6. 並び替え（ORDER BY）

```sql
SELECT * FROM table_name ORDER BY created_at DESC;
```

---

# 7. LIMIT / OFFSET

```sql
SELECT * FROM table_name LIMIT 10 OFFSET 20;
```

---

# 8. JOIN（結合）

## INNER JOIN
```sql
SELECT * 
FROM users u
INNER JOIN orders o ON u.id = o.user_id;
```

## LEFT JOIN
```sql
SELECT * 
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;
```

## RIGHT JOIN
```sql
SELECT * 
FROM users u
RIGHT JOIN orders o ON u.id = o.user_id;
```

## FULL OUTER JOIN
```sql
SELECT * 
FROM users u
FULL OUTER JOIN orders o ON u.id = o.user_id;
```

---

# 9. サブクエリ

## SELECT 内
```sql
SELECT name, (SELECT COUNT(*) FROM orders WHERE user_id = u.id) AS order_count
FROM users u;
```

## WHERE 内
```sql
SELECT * FROM users WHERE id IN (SELECT user_id FROM orders);
```

---

# 10. ビュー（VIEW）

## CREATE VIEW
```sql
CREATE VIEW active_users AS
SELECT * FROM users WHERE status = 'active';
```

## DROP VIEW
```sql
DROP VIEW active_users;
```

---

# 11. インデックス（INDEX）

## CREATE INDEX
```sql
CREATE INDEX idx_users_name ON users(name);
```

## DROP INDEX
```sql
DROP INDEX idx_users_name;
```

---

# 12. トランザクション（TRANSACTION）

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
-- ROLLBACK;
```

---

# 13. 制約（CONSTRAINT）

## PRIMARY KEY
```sql
id INT PRIMARY KEY
```

## FOREIGN KEY
```sql
FOREIGN KEY (user_id) REFERENCES users(id)
```

## UNIQUE
```sql
email VARCHAR(255) UNIQUE
```

## CHECK
```sql
CHECK (age >= 18)
```

---

# 14. 関数（組み込み）

## 文字列
```sql
UPPER(), LOWER(), LENGTH(), CONCAT(), SUBSTRING()
```

## 数値
```sql
ABS(), ROUND(), CEIL(), FLOOR(), MOD()
```

## 日付
```sql
NOW(), CURRENT_DATE, CURRENT_TIMESTAMP, DATE_ADD(), DATE_SUB()
```

## 集計
```sql
COUNT(), SUM(), AVG(), MIN(), MAX()
```

---

# 15. CASE 式

```sql
SELECT
  id,
  CASE 
    WHEN score >= 80 THEN 'A'
    WHEN score >= 60 THEN 'B'
    ELSE 'C'
  END AS grade
FROM students;
```

---

# 16. UNION / UNION ALL

```sql
SELECT name FROM users
UNION
SELECT name FROM admins;

SELECT name FROM users
UNION ALL
SELECT name FROM admins;
```

---

# 17. ストアドプロシージャ（DB依存）

```sql
CREATE PROCEDURE get_users()
BEGIN
    SELECT * FROM users;
END;
```

---

# 18. トリガー（TRIGGER）

```sql
CREATE TRIGGER update_timestamp
BEFORE UPDATE ON users
FOR EACH ROW
SET NEW.updated_at = NOW();
```

---

# 19. 権限（GRANT / REVOKE）

```sql
GRANT SELECT, INSERT ON db.* TO 'user'@'%';
REVOKE INSERT ON db.* FROM 'user'@'%';
```

---

# 20. その他便利構文

## EXPLAIN（実行計画）
```sql
EXPLAIN SELECT * FROM users;
```

## COMMENT（コメント）
```sql
-- 1行コメント
/* 複数行コメント */
```
