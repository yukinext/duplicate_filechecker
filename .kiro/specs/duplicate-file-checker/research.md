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