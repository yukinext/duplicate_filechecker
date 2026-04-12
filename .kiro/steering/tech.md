# Technology Stack

## Architecture

単一 CLI エントリからサービスクラスを組み合わせる軽量レイヤ構成。CLI 層が処理フローを制御し、各モジュールは単一責務で実装する。

## Core Technologies

- Language: Python 3.14+
- Framework: Typer (CLI)
- Runtime: CPython
- Storage: SQLite (標準ライブラリ sqlite3)

## Key Libraries

- typer: コマンド定義と引数解釈。
- sqlite3/hashlib/logging/pathlib/os/shutil: 永続化、ハッシュ計算、ログ、ファイル操作の基盤。
- pytest + unittest.mock: 単体テストと依存差し替え。

## Development Standards

### Type Safety

- 主要関数は型ヒントを付与し、戻り値に tuple や dataclass を用いて意図を明確化する。
- mypy を導入し、未設定検査や未型付け関数の実行時チェックを有効化する。

### Code Quality

- Ruff を lint/format の基準として利用する。
- import の first-party 境界は duplicate_filechecker として整理する。
- 1行 120 文字を上限にする。

### Testing

- pytest を中心に、tmp_path/monkeypatch を使ったファイルシステム依存テストを行う。
- CLI は typer.testing.CliRunner で実行し、副作用のある依存は mock で隔離する。

## Development Environment

### Required Tools

- Python 3.14 以上
- 仮想環境 (.venv 推奨)
- pytest, ruff, mypy

### Common Commands

```bash
python main.py check <directory> --pattern "*.mp4"
python main.py maint purge-missing --db-path duplicates.db
pytest
ruff check .
mypy .
```

## Key Technical Decisions

- ハッシュキャッシュを DB に保存し、再スキャン時のコストを抑える。
- 重複移動時は source からの相対パスを trash に保持し、復元や追跡を容易にする。
- 保守処理は専用サービスとして分離し、通常スキャン経路と責務を混在させない。

---
全依存の列挙ではなく、開発判断に影響する標準と設計選択を記述する。
