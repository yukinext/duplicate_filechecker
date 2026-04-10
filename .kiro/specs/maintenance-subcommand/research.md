# Research & Design Decisions

## Summary
- **Feature**: `maintenance-subcommand`
- **Discovery Scope**: Extension
- **Key Findings**:
  - 既存CLIはTyperの単一コマンド構成であり、サブコマンド追加時はコマンド境界の分離が必要。
  - DB層は `save/get_hash/get_stem_file` のみで、全件取得・削除APIが未定義。
  - 既存Loggerは `logs` ディレクトリを生成するため、監査CSVの出力先と整合する。

## Research Log

### CLI拡張ポイント
- **Context**: メンテナンス処理を既存重複検出と分離する必要がある。
- **Sources Consulted**: 既存コード [duplicate_filechecker/cli.py](duplicate_filechecker/cli.py)
- **Findings**:
  - Typerアプリは `main` コマンド中心。
  - 新規サブコマンドを同居させる場合、既存引数と副作用を混在させない設計が必要。
- **Implications**:
  - `main` と `maintenance purge-missing` を明示分離する。

### DB整合性処理
- **Context**: DB内パス存在チェックと削除が新規要件。
- **Sources Consulted**: 既存コード [duplicate_filechecker/database.py](duplicate_filechecker/database.py)
- **Findings**:
  - `files(path PRIMARY KEY, hash)` テーブルは削除キーが明確。
  - 全件読み出しAPIと削除APIを追加すれば要件を満たせる。
- **Implications**:
  - `list_entries()` と `delete_entry(path)` の明示契約を追加する。

### 監査CSV出力
- **Context**: 削除エントリーを `logs/purged_entry.csv` にタブ区切り追記する要件。
- **Sources Consulted**: 既存コード [duplicate_filechecker/logger.py](duplicate_filechecker/logger.py)
- **Findings**:
  - 既存ログ運用は `logs` ディレクトリ前提。
  - CSV追記は標準ライブラリで十分実装可能。
- **Implications**:
  - `MaintenanceReporter` 相当の責務を追加し、UTC ISO 8601を統一フォーマット化する。

## Architecture Pattern Evaluation

| Option | Description | Strengths | Risks / Limitations | Notes |
|--------|-------------|-----------|---------------------|-------|
| CLI内直接実装 | コマンド内でDB/FS/CSVを直接処理 | 実装量が少ない | 責務過多でテストしづらい | 小規模でも保守性が低い |
| サービス分離 | CLIはオーケストレーションのみ、DB/監査出力は別責務 | テスト容易、拡張しやすい | クラス追加の初期コスト | 採用 |

## Design Decisions

### Decision: メンテナンス処理を専用サービスへ分離
- **Context**: 既存 `main` の責務拡大を避ける必要。
- **Alternatives Considered**:
  1. `cli.py` に全処理を直書き
  2. `MaintenanceService` を導入
- **Selected Approach**: `MaintenanceService` に走査・削除・監査出力を集約し、CLIは呼び出しのみ担当。
- **Rationale**: 既存アーキテクチャに沿って責務分離し、テスト容易性を維持できるため。
- **Trade-offs**: ファイル追加が必要だが、長期保守性が向上。
- **Follow-up**: 単体テストで削除条件とCSV列順を固定化する。

### Decision: 監査CSVはタブ区切り・UTC ISO 8601固定
- **Context**: 監査の再処理・機械可読性を担保したい。
- **Alternatives Considered**:
  1. カンマ区切りCSV
  2. タブ区切りTSV相当
- **Selected Approach**: 拡張子は `.csv` のまま、区切り文字はタブ `\t` を使用。
- **Rationale**: パス文字列内カンマ影響を避けつつ要件準拠できるため。
- **Trade-offs**: 一般的CSV想定ツールでは明示設定が必要。
- **Follow-up**: READMEに区切り仕様を明記。

## Risks & Mitigations
- 既存コマンドとの引数競合リスク — サブコマンド配下に限定した引数設計にする。
- 大量エントリー時の処理時間増大 — 逐次処理とストリーム追記でメモリ使用を固定化する。
- 監査ファイル破損リスク — 1行単位追記と例外ログで再実行可能性を確保する。

## References
- Python `pathlib` / `datetime` / `csv` 標準ライブラリ
- 既存実装: [duplicate_filechecker/cli.py](duplicate_filechecker/cli.py), [duplicate_filechecker/database.py](duplicate_filechecker/database.py), [duplicate_filechecker/logger.py](duplicate_filechecker/logger.py)
