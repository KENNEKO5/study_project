
# Snowflake 基礎ガイド（業務活用向け）

Snowflake の基本概念・アーキテクチャ・主要機能を体系的にまとめたノートです。  
業務でよく使う操作を中心に整理しています。

---

# 1. Snowflake とは

- **クラウドネイティブ**のデータウェアハウス（DWH）サービス
- AWS / Azure / GCP 上で動作
- ストレージとコンピュートが**完全分離**されている
- SQL ベースで操作可能

---

# 2. アーキテクチャ（3層構造）

```
┌──────────────────────────┐
│   クラウドサービス層       │  ← メタデータ管理、認証、最適化
├──────────────────────────┤
│   コンピュート層           │  ← 仮想ウェアハウス（クエリ実行）
├──────────────────────────┤
│   ストレージ層            │  ← データの永続保存（圧縮・暗号化）
└──────────────────────────┘
```

| 層 | 役割 |
|---|---|
| クラウドサービス層 | 認証、メタデータ管理、クエリ最適化、トランザクション管理 |
| コンピュート層 | 仮想ウェアハウスによるクエリ実行（スケールアップ/アウト可能） |
| ストレージ層 | データを列指向フォーマットで圧縮・暗号化して保存 |

---

# 3. オブジェクト階層

```
アカウント
  └── データベース (DATABASE)
        └── スキーマ (SCHEMA)
              ├── テーブル (TABLE)
              ├── ビュー (VIEW)
              ├── ステージ (STAGE)
              ├── パイプ (PIPE)
              ├── ストリーム (STREAM)
              ├── タスク (TASK)
              ├── ファイルフォーマット (FILE FORMAT)
              └── UDF / プロシージャ
```

---

# 4. 仮想ウェアハウス（Virtual Warehouse）

クエリを実行するためのコンピュートリソース。使った分だけ課金される。

## ウェアハウスの作成
```sql
CREATE WAREHOUSE my_wh
  WAREHOUSE_SIZE = 'X-SMALL'
  AUTO_SUSPEND = 300
  AUTO_RESUME = TRUE;
```

## サイズ一覧

| サイズ | クレジット/時間 |
|---|---|
| X-Small | 1 |
| Small | 2 |
| Medium | 4 |
| Large | 8 |
| X-Large | 16 |

## ウェアハウスの操作
```sql
-- 使用するウェアハウスの指定
USE WAREHOUSE my_wh;

-- サイズ変更
ALTER WAREHOUSE my_wh SET WAREHOUSE_SIZE = 'MEDIUM';

-- 一時停止 / 再開
ALTER WAREHOUSE my_wh SUSPEND;
ALTER WAREHOUSE my_wh RESUME;

-- 削除
DROP WAREHOUSE my_wh;
```

## マルチクラスター（Enterprise以上）
```sql
CREATE WAREHOUSE my_wh
  WAREHOUSE_SIZE = 'SMALL'
  MIN_CLUSTER_COUNT = 1
  MAX_CLUSTER_COUNT = 3
  SCALING_POLICY = 'STANDARD';
```

---

# 5. データベース・スキーマ操作

## データベース
```sql
CREATE DATABASE my_db;
DROP DATABASE my_db;
USE DATABASE my_db;
SHOW DATABASES;
```

## スキーマ
```sql
CREATE SCHEMA my_schema;
DROP SCHEMA my_schema;
USE SCHEMA my_schema;
SHOW SCHEMAS;
```

## コンテキスト設定（まとめて指定）
```sql
USE ROLE sysadmin;
USE WAREHOUSE my_wh;
USE DATABASE my_db;
USE SCHEMA my_schema;
```

---

# 6. テーブル操作

## CREATE TABLE
```sql
CREATE TABLE users (
    id INT AUTOINCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(255),
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);
```

## テーブルの種類

| 種類 | 特徴 |
|---|---|
| 永続テーブル | デフォルト。Time Travel・Fail-safe あり |
| 一時テーブル (TEMPORARY) | セッション終了時に自動削除 |
| トランジェントテーブル (TRANSIENT) | Fail-safe なし。一時的なデータ向け |

```sql
CREATE TEMPORARY TABLE tmp_data (id INT, val STRING);
CREATE TRANSIENT TABLE staging_data (id INT, val STRING);
```

## CTAS（SELECT から作成）
```sql
CREATE TABLE new_table AS
SELECT * FROM existing_table WHERE status = 'active';
```

## クローン（ゼロコピークローン）
```sql
CREATE TABLE users_clone CLONE users;
CREATE DATABASE dev_db CLONE prod_db;
```

---

# 7. データ型

| カテゴリ | 型 |
|---|---|
| 数値 | NUMBER, INT, FLOAT, DECIMAL |
| 文字列 | VARCHAR, STRING, TEXT, CHAR |
| 日付・時刻 | DATE, TIME, TIMESTAMP_NTZ, TIMESTAMP_LTZ, TIMESTAMP_TZ |
| 論理 | BOOLEAN |
| 半構造化 | VARIANT, OBJECT, ARRAY |
| バイナリ | BINARY |

## VARIANT 型（半構造化データ）
```sql
CREATE TABLE events (
    id INT,
    data VARIANT
);

-- JSON を直接挿入
INSERT INTO events SELECT 1, PARSE_JSON('{"name": "test", "value": 100}');

-- アクセス
SELECT data:name::STRING, data:value::INT FROM events;
```

---

# 8. データロード（COPY INTO）

## ステージの種類

| 種類 | 説明 |
|---|---|
| 内部ステージ (@~, @%table, @stage) | Snowflake 内部のストレージ |
| 外部ステージ | S3 / Azure Blob / GCS を参照 |

## 内部ステージにファイルアップロード
```sql
PUT file://C:/data/users.csv @my_stage;
```

## ファイルフォーマット
```sql
CREATE FILE FORMAT my_csv_format
  TYPE = 'CSV'
  FIELD_DELIMITER = ','
  SKIP_HEADER = 1
  FIELD_OPTIONALLY_ENCLOSED_BY = '"';

CREATE FILE FORMAT my_json_format
  TYPE = 'JSON'
  STRIP_OUTER_ARRAY = TRUE;
```

## COPY INTO（ロード）
```sql
COPY INTO my_table
FROM @my_stage/users.csv
FILE_FORMAT = (FORMAT_NAME = 'my_csv_format')
ON_ERROR = 'CONTINUE';
```

## 外部ステージ（S3 の例）
```sql
CREATE STAGE my_s3_stage
  URL = 's3://my-bucket/data/'
  CREDENTIALS = (AWS_KEY_ID = '...' AWS_SECRET_KEY = '...');

COPY INTO my_table
FROM @my_s3_stage
FILE_FORMAT = (TYPE = 'CSV');
```

## ON_ERROR オプション

| オプション | 動作 |
|---|---|
| CONTINUE | エラー行をスキップして続行 |
| SKIP_FILE | エラーのあるファイルをスキップ |
| ABORT_STATEMENT | エラー発生時に中止（デフォルト） |

---

# 9. データアンロード

```sql
COPY INTO @my_stage/export/
FROM my_table
FILE_FORMAT = (TYPE = 'CSV' HEADER = TRUE)
OVERWRITE = TRUE;

-- S3 へ直接出力
COPY INTO 's3://my-bucket/export/'
FROM my_table
FILE_FORMAT = (TYPE = 'PARQUET')
CREDENTIALS = (AWS_KEY_ID = '...' AWS_SECRET_KEY = '...');
```

---

# 10. Snowpipe（自動データ取り込み）

ファイルがステージに到着すると自動でロードする仕組み。

```sql
CREATE PIPE my_pipe
  AUTO_INGEST = TRUE
AS
COPY INTO my_table
FROM @my_s3_stage
FILE_FORMAT = (TYPE = 'CSV');
```

```sql
-- パイプの状態確認
SELECT SYSTEM$PIPE_STATUS('my_pipe');

-- 手動でリフレッシュ
ALTER PIPE my_pipe REFRESH;
```

---

# 11. Time Travel（タイムトラベル）

過去のデータにアクセスできる機能（最大90日、エディションによる）。

```sql
-- 5分前のデータを取得
SELECT * FROM my_table AT(OFFSET => -60*5);

-- 特定の日時のデータを取得
SELECT * FROM my_table AT(TIMESTAMP => '2024-01-15 10:00:00'::TIMESTAMP);

-- 特定クエリ実行前のデータを取得
SELECT * FROM my_table BEFORE(STATEMENT => '<query_id>');

-- 誤って削除したテーブルの復元
UNDROP TABLE my_table;
UNDROP DATABASE my_db;
UNDROP SCHEMA my_schema;
```

## 保持期間の設定
```sql
ALTER TABLE my_table SET DATA_RETENTION_TIME_IN_DAYS = 7;
```

---

# 12. ストリーム & タスク（変更データキャプチャ）

## ストリーム（変更追跡）
```sql
CREATE STREAM my_stream ON TABLE source_table;

-- 変更データの確認
SELECT * FROM my_stream;
-- METADATA$ACTION: INSERT / DELETE
-- METADATA$ISUPDATE: TRUE / FALSE
```

## タスク（スケジュール実行）
```sql
CREATE TASK my_task
  WAREHOUSE = my_wh
  SCHEDULE = 'USING CRON 0 * * * * UTC'  -- 毎時実行
AS
INSERT INTO target_table
SELECT * FROM my_stream WHERE METADATA$ACTION = 'INSERT';
```

```sql
-- タスクの有効化（作成直後は SUSPENDED）
ALTER TASK my_task RESUME;

-- タスクの一時停止
ALTER TASK my_task SUSPEND;

-- 手動実行
EXECUTE TASK my_task;

-- 実行履歴
SELECT * FROM TABLE(INFORMATION_SCHEMA.TASK_HISTORY())
ORDER BY SCHEDULED_TIME DESC;
```

---

# 13. ロール & アクセス制御（RBAC）

## デフォルトロール

```
ACCOUNTADMIN
  ├── SYSADMIN        ← DB・ウェアハウスの管理
  ├── SECURITYADMIN   ← ユーザー・ロールの管理
  └── USERADMIN       ← ユーザーの作成
PUBLIC                ← 全ユーザーに自動付与
```

## よく使う操作
```sql
-- ロールの作成
CREATE ROLE analyst_role;

-- 権限の付与
GRANT USAGE ON DATABASE my_db TO ROLE analyst_role;
GRANT USAGE ON SCHEMA my_db.my_schema TO ROLE analyst_role;
GRANT SELECT ON ALL TABLES IN SCHEMA my_db.my_schema TO ROLE analyst_role;

-- ロールをユーザーに付与
GRANT ROLE analyst_role TO USER john;

-- ロールの切り替え
USE ROLE analyst_role;
```

## 将来のオブジェクトへの権限付与
```sql
GRANT SELECT ON FUTURE TABLES IN SCHEMA my_db.my_schema TO ROLE analyst_role;
```

---

# 14. Snowflake 独自の便利関数

## 半構造化データ操作
```sql
-- JSON パース
PARSE_JSON('{"key": "value"}')

-- パス指定でアクセス
data:customer.name::STRING

-- 配列の展開
SELECT value FROM my_table, LATERAL FLATTEN(input => data:items);
```

## FLATTEN（ネスト展開）
```sql
SELECT
  f.value:name::STRING AS item_name,
  f.value:price::NUMBER AS item_price
FROM orders,
LATERAL FLATTEN(input => order_data:items) f;
```

## その他よく使う関数
```sql
-- 型変換
TO_DATE('2024-01-15')
TO_TIMESTAMP('2024-01-15 10:00:00')
TO_VARCHAR(column_name, 'YYYY-MM-DD')

-- NULL 処理
NVL(col, 'default')
COALESCE(col1, col2, 'default')
IFF(condition, true_val, false_val)
NULLIF(col, '')

-- 文字列
SPLIT_PART('a-b-c', '-', 2)  -- 結果: 'b'
REGEXP_LIKE(col, '^[0-9]+$')

-- 日付
DATEADD(DAY, 7, CURRENT_DATE())
DATEDIFF(DAY, start_date, end_date)
DATE_TRUNC('MONTH', created_at)
```

---

# 15. ウィンドウ関数

```sql
SELECT
  name,
  department,
  salary,
  ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS rank,
  SUM(salary) OVER (PARTITION BY department) AS dept_total,
  LAG(salary) OVER (ORDER BY hire_date) AS prev_salary,
  LEAD(salary) OVER (ORDER BY hire_date) AS next_salary
FROM employees;
```

## QUALIFY（ウィンドウ関数の結果でフィルタ）
```sql
SELECT *
FROM employees
QUALIFY ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) = 1;
```

---

# 16. パフォーマンス最適化

## クラスタリングキー
```sql
ALTER TABLE my_table CLUSTER BY (date_column, region);

-- クラスタリング状態の確認
SELECT SYSTEM$CLUSTERING_INFORMATION('my_table');
```

## クエリプロファイル
```sql
-- 直近のクエリ履歴
SELECT * FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY())
ORDER BY START_TIME DESC LIMIT 10;

-- クエリ ID で確認
SELECT * FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY())
WHERE QUERY_ID = '<query_id>';
```

## リザルトキャッシュ
- 同一クエリは24時間キャッシュされる（無料）
- ウェアハウスが停止中でもキャッシュから返る

## ベストプラクティス
- `SELECT *` を避け、必要な列だけ取得
- 適切なウェアハウスサイズを選ぶ（大きすぎない）
- AUTO_SUSPEND を短め（60〜300秒）に設定
- 頻繁に結合するカラムにクラスタリングキーを設定

---

# 17. データ共有（Data Sharing）

```sql
-- 共有の作成（プロバイダー側）
CREATE SHARE my_share;
GRANT USAGE ON DATABASE my_db TO SHARE my_share;
GRANT USAGE ON SCHEMA my_db.public TO SHARE my_share;
GRANT SELECT ON TABLE my_db.public.shared_table TO SHARE my_share;

-- 共有先アカウントの設定
ALTER SHARE my_share ADD ACCOUNTS = org1.consumer_account;

-- 共有データの利用（コンシューマー側）
CREATE DATABASE shared_db FROM SHARE provider_account.my_share;
```

---

# 18. よく使う管理コマンド

```sql
-- 現在のコンテキスト確認
SELECT CURRENT_WAREHOUSE(), CURRENT_DATABASE(), CURRENT_SCHEMA(), CURRENT_ROLE();

-- オブジェクト一覧
SHOW TABLES;
SHOW VIEWS;
SHOW STAGES;
SHOW PIPES;
SHOW TASKS;
SHOW WAREHOUSES;

-- テーブル定義確認
DESCRIBE TABLE my_table;
-- または
DESC TABLE my_table;

-- DDL の取得
SELECT GET_DDL('TABLE', 'my_table');

-- ストレージ使用量
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.TABLE_STORAGE_METRICS
WHERE TABLE_NAME = 'MY_TABLE';

-- クレジット使用量
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE START_TIME >= DATEADD(DAY, -7, CURRENT_TIMESTAMP())
ORDER BY START_TIME DESC;
```

---

# 19. コスト管理

## リソースモニター
```sql
CREATE RESOURCE MONITOR my_monitor
  WITH CREDIT_QUOTA = 100
  FREQUENCY = MONTHLY
  START_TIMESTAMP = IMMEDIATELY
  TRIGGERS
    ON 75 PERCENT DO NOTIFY
    ON 100 PERCENT DO SUSPEND;

ALTER WAREHOUSE my_wh SET RESOURCE_MONITOR = my_monitor;
```

## コスト削減のポイント
- 使わないウェアハウスは AUTO_SUSPEND で自動停止
- TRANSIENT / TEMPORARY テーブルを活用して Fail-safe コストを削減
- リソースモニターでクレジット使用量を監視
- 不要な Time Travel 期間を短縮

---

# 20. Snowflake エディション比較

| 機能 | Standard | Enterprise | Business Critical |
|---|---|---|---|
| Time Travel 最大日数 | 1日 | 90日 | 90日 |
| マルチクラスター WH | - | ○ | ○ |
| マテリアライズドビュー | - | ○ | ○ |
| 行アクセスポリシー | - | ○ | ○ |
| データマスキング | - | ○ | ○ |
| Tri-Secret Secure | - | - | ○ |
| HIPAA / PCI DSS | - | - | ○ |