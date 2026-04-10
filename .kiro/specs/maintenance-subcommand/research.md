# Research & Design Decisions

## Summary
- **Feature**: `maintenance-subcommand`
- **Discovery Scope**: Extension
- **Key Findings**:
  - 現在のCLIは `main` ベースの単一コマンド設計で、`main.py` 側の手動ディスパッチが混在している。
  - Typerのネストサブコマンド構成へ統一することで、`check` と `maint` の責務境界を明確化できる。
  - 既存のメンテナンス処理（DB走査・削除・監査出力）はサービス層を維持し、CLIルーティングのみ再設計するのが最小変更。

## Research Log

### CLIルーティングの整合性
- **Context**: 既存機能も含めてTyperサブコマンドへ統一する要求が追加された。
- **Sources Consulted**: 既存コード [duplicate_filechecker/cli.py](duplicate_filechecker/cli.py), [main.py](main.py)
- **Findings**:
  - 既存重複チェックは `main` 関数直結。
  - メンテナンスは `main.py` 側で引数分岐して呼び出しており、Typerルーティング外にある。
- **Implications**:
  - Typerアプリに `check` と `maint` の2系統を定義し、`main.py` は `app()` 呼び出しのみに戻す必要がある。

### 既存機能保全
- **Context**: 既存重複チェック挙動を維持したままコマンド名のみを `check` へ変更する必要がある。
- **Sources Consulted**: 既存コード [duplicate_filechecker/cli.py](duplicate_filechecker/cli.py)
- **Findings**:
  - 重複チェック処理は独立関数として分離しやすい。
  - `check` サブコマンドへ移しても内部依存は維持可能。
- **Implications**:
  - 処理本体をサービスまたはコマンド関数へ残し、CLI定義のみ命名変更する。

### メンテナンス機能との統合
- **Context**: `maint` サブコマンドで既存の purge 処理を提供する必要がある。
- **Sources Consulted**: 既存コード [duplicate_filechecker/maintenance.py](duplicate_filechecker/maintenance.py)
- **Findings**:
  - `MaintenanceService` と `PurgeAuditWriter` は既に分離されている。
  - ルーティングをTyperへ寄せてもサービス層は変更最小で済む。
- **Implications**:
  - `maint` 配下に `purge-missing` を定義し、`--db-path` などの引数をTyper管理に移す。

## Architecture Pattern Evaluation

| Option | Description | Strengths | Risks / Limitations | Notes |
|--------|-------------|-----------|---------------------|-------|
| main.py手動分岐維持 | 既存ディスパッチを継続 | 変更が少ない | Typer一貫性要件に非準拠 | 不採用 |
| Typer単層2コマンド | `check` / `maint` を直下定義 | シンプル | `maint` 将来拡張時に整理不足 | 採用候補 |
| Typer階層構成 | `maint purge-missing` をネスト | 拡張容易、責務明確 | 初期定義がやや増える | 採用 |

## Design Decisions

### Decision: Typer階層サブコマンドへ統一
- **Context**: `check` と `maint` の明示的な操作境界を必要とする。
- **Alternatives Considered**:
  1. `main.py` で手動分岐
  2. Typerで階層サブコマンド化
- **Selected Approach**: ルートTyper配下で `check` と `maint` を提供し、`maint` に保守操作を収容する。
- **Rationale**: 要件5.1-5.3を満たしつつ、CLI設計を単一責務に統一できるため。
- **Trade-offs**: 既存利用者の呼び出し名が変わるため、移行案内が必要。
- **Follow-up**: CLI統合テストで旧ルートと新コマンドの期待動作を検証する。

### Decision: 重複チェック本体は再利用し、エントリポイントのみ再配線
- **Context**: 挙動回帰を最小化したい。
- **Alternatives Considered**:
  1. 重複チェック処理を全面再設計
  2. 既存処理を `check` コマンドへ移すのみ
- **Selected Approach**: 処理本体は維持し、Typerデコレータと呼び出し導線を変更する。
- **Rationale**: 変更範囲をCLI層へ限定できるため。
- **Trade-offs**: 関数命名整理は別途必要。
- **Follow-up**: 既存テスト更新で互換範囲を固定化する。

## Risks & Mitigations
- 既存運用スクリプトが旧呼び出し形式を使用するリスク — `README` とヘルプ出力で新コマンド名を明示し、必要なら互換エイリアス期間を設ける。
- ルーティング変更による回帰リスク — CLI統合テストで `check` と `maint purge-missing` の両方を検証する。
- 手動分岐コード残存リスク — `main.py` を `app()` のみへ戻し、二重ルーティングを禁止する。

## References
- 既存実装: [duplicate_filechecker/cli.py](duplicate_filechecker/cli.py), [duplicate_filechecker/maintenance.py](duplicate_filechecker/maintenance.py), [main.py](main.py)
- Typer公式ドキュメント（サブコマンド設計）
