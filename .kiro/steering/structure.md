# Project Structure

## Organization Philosophy

モジュール分割は責務ベース。CLI オーケストレーションと、スキャン・ハッシュ・DB・移動・保守を分離し、変更時に波及しにくい構造を維持する。

## Directory Patterns

### Application Package
Location: /duplicate_filechecker/
Purpose: 実行ロジックの中核。CLI と各サービスクラスを配置する。
Example: cli.py が Scanner/Hasher/Database/Merger/MaintenanceService を組み合わせる。

### Tests by Behavior
Location: /tests/
Purpose: モジュール単位で挙動を検証し、I/O を伴う処理を tmp_path と monkeypatch で再現する。
Example: test_merger.py で移動先競合時のリネームを検証する。

### Operational Artifacts
Location: /logs/
Purpose: 実行ログとメンテナンス監査ログを配置する。
Example: purged_entry.csv に purge 実行履歴を追記する。

## Naming Conventions

- Files: snake_case.py
- Classes: CapWords
- Functions/Methods: snake_case
- Tests: test_<module>.py と test_<behavior>

## Import Organization

- パッケージ内部: 相対 import を基本とする (例: from .database import Database)
- テスト側: アプリの公開モジュールを絶対 import する (例: from duplicate_filechecker.scanner import Scanner)

## Code Organization Principles

- CLI はフロー制御に専念し、業務処理はサービスへ委譲する。
- 共有状態は必要最小限にし、ファイル/DB の副作用は専用モジュール内に閉じる。
- 破壊的操作 (移動・削除) はログまたは監査証跡を残し、後追い可能性を確保する。

---
ディレクトリの完全列挙ではなく、拡張時に維持すべき構造パターンを記述する。
