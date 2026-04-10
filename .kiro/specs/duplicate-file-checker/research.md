# Research & Design Decisions Template

---
**Purpose**: Capture discovery findings, architectural investigations, and rationale that inform the technical design.

**Usage**:
- Log research activities and outcomes during the discovery phase.
- Document design decision trade-offs that are too detailed for `design.md`.
- Provide references and evidence for future audits or reuse.
---

## Summary
- **Feature**: duplicate-file-checker
- **Discovery Scope**: New Feature
- **Key Findings**:
  - Python 3.14は安定版で、標準ライブラリを使用可能
  - SQLiteはPython標準ライブラリで利用可能
  - TyperはCLIライブラリとして適切

## Research Log
Document notable investigation steps and their outcomes. Group entries by topic for readability.

### Python 3.14 Compatibility
- **Context**: プロジェクトがPython 3.14を使用
- **Sources Consulted**: Python公式ドキュメント
- **Findings**: Python 3.14は最新安定版、hashlib, sqlite3, logging, pathlibなどの標準ライブラリが利用可能
- **Implications**: 標準ライブラリを優先的に使用可能

### SQLite Usage
- **Context**: DB保存機能の実装
- **Sources Consulted**: Python sqlite3ドキュメント
- **Findings**: sqlite3モジュールで簡単にDB操作可能、トランザクション対応
- **Implications**: 軽量DBとして適切

### Typer CLI Library
- **Context**: CLIインターフェースの実装
- **Sources Consulted**: Typer公式ドキュメント
- **Findings**: TyperはPython CLIライブラリ、デコレータベースで使いやすい
- **Implications**: CLI実装に適する

### ログ出力拡張の実現性
- **Context**: ログ出力機能の拡張（スキップログ、移動ログ、処理時間ログ）
- **Sources Consulted**: 既存のdesign.md、logger.pyの実装、Python loggingドキュメント
- **Findings**: 既存のlogging設定を拡張可能。ログディレクトリ作成とローテーションは既に実装済み。新しいログメソッドを追加することで要件を満たせる。
- **Implications**: 実装コストが低く、既存アーキテクチャに適合。

### コンポーネント間連携
- **Context**: HasherとMergerからLoggerを呼び出す統合方法
- **Sources Consulted**: 既存のコンポーネントインターフェース、design.mdのDependencies
- **Findings**: Hasherのcalculate_hashでスキップ判定時にLogger.log_skipを呼び出し可能。Mergerのmergeで移動時にLogger.log_moveを呼び出し可能。CLIで処理開始・終了時にtimeモジュールで計測し、Logger.log_durationを呼び出し。
- **Implications**: インターフェース変更が最小限で済む。

### 処理時間計測
- **Context**: 処理時間の計測方法
- **Sources Consulted**: Python timeモジュールドキュメント
- **Findings**: time.time()を使用して開始・終了時間を記録し、差分を計算可能。
- **Implications**: 標準ライブラリのみで実現可能。

## Architecture Pattern Evaluation
List candidate patterns or approaches that were considered. Use the table format where helpful.

| Option | Description | Strengths | Risks / Limitations | Notes |
|--------|-------------|-----------|---------------------|-------|
| シンプルスクリプト | 単一ファイルで全て処理 | シンプル | 保守性低い | 却下 |
| モジュール化 | 機能をモジュールに分離 | 保守性高い | 複雑さ増加 | 採用 |

## Design Decisions
Record major decisions that influence `design.md`. Focus on choices with significant trade-offs.

### Decision: 標準ライブラリ優先
- **Context**: サードパーティライブラリを最小限に
- **Alternatives Considered**:
  1. Clickライブラリ — 人気だがTyperが指定
  2. SQLAlchemy — ORMだがsqlite3で十分
- **Selected Approach**: sqlite3, hashlib, loggingを使用
- **Rationale**: 標準ライブラリで十分機能する
- **Trade-offs**: 機能制限 vs 依存削減
- **Follow-up**: 実装で検証

## Risks & Mitigations
- ファイルハッシュ計算の性能 — 大ファイル対応で最適化
- DBロック — トランザクションで対応
- CLI引数解析 — Typerで堅牢

## References
Provide canonical links and citations (official docs, standards, ADRs, internal guidelines).
- [Python 3.14 Documentation](https://docs.python.org/3.14/) — 標準ライブラリ確認
- [Typer Documentation](https://typer.tiangolo.com/) — CLIライブラリ仕様