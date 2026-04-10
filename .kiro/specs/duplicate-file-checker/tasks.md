# Implementation Plan

## Task Format Template

Use whichever pattern fits the work breakdown:

### Major task only
- [ ] {{NUMBER}}. {{TASK_DESCRIPTION}}{{PARALLEL_MARK}}
  - {{DETAIL_ITEM_1}} *(Include details only when needed. If the task stands alone, omit bullet items.)*
  - _Requirements: {{REQUIREMENT_IDS}}_

### Major + Sub-task structure
- [ ] {{MAJOR_NUMBER}}. {{MAJOR_TASK_SUMMARY}}
- [ ] {{MAJOR_NUMBER}}.{{SUB_NUMBER}} {{SUB_TASK_DESCRIPTION}}{{SUB_PARALLEL_MARK}}
  - {{DETAIL_ITEM_1}}
  - {{DETAIL_ITEM_2}}
  - {{OBSERVABLE_COMPLETION_ITEM}} *(At least one detail item should state the observable completion condition for this task.)*
  - _Requirements: {{REQUIREMENT_IDS}}_ *(IDs only; do not add descriptions or parentheses.)*
  - _Boundary: {{COMPONENT_NAMES}}_ *(Only for (P) tasks. Omit when scope is obvious.)*
  - _Depends: {{TASK_IDS}}_ *(Only for non-obvious cross-boundary dependencies. Most tasks omit this.)*

> **Parallel marker**: Append ` (P)` only to tasks that can be executed in parallel. Omit the marker when running in `--sequential` mode.
>
> **Optional test coverage**: When a sub-task is deferrable test work tied to acceptance criteria, mark the checkbox as `- [ ]*` and explain the referenced requirements in the detail bullets.

- [ ] 1. 環境とインフラのセットアップ
- [x] 1.1 プロジェクト構造の作成
  - duplicate_filechecker パッケージディレクトリを作成
  - __init__.py ファイルを追加
  - 必要なファイル構造を準備
  - ディレクトリ構造が設計通りになっていることを確認
  - _Requirements: 1.1, 3.1, 6.1, 7.1_

- [x] 1.2 依存関係の確認
  - Python 3.14 が利用可能であることを確認
  - Typer がインストールされていることを確認
  - 標準ライブラリ (sqlite3, hashlib, logging, pathlib, shutil) が利用可能であることを確認
  - 環境が実装に適していることを確認
  - _Requirements: 1.1, 2.1, 3.1, 6.1, 7.1_

- [ ] 2. コアコンポーネントの実装
- [x] 2.1 (P) Scanner コンポーネントの実装
  - 指定ディレクトリからファイルパターンマッチングでファイルを探索する機能を実装
  - ディレクトリが存在しない場合のエラーハンドリングを実装
  - デフォルトパターン *.mp4 を適用する機能を実装
  - ファイルリストを返すインターフェースを提供
  - ファイル探索が正常に動作することを確認
  - _Requirements: 1.1, 1.2, 1.3_
  - _Boundary: Scanner_

- [x] 2.2 (P) Hasher コンポーネントの実装
  - ファイルのハッシュ値を計算する機能を実装
  - DBに保存されているハッシュ値をチェックしてスキップする機能を実装
  - 同一ハッシュ値のファイルを判定する機能を実装
  - ハッシュ計算結果を返すインターフェースを提供
  - ハッシュ計算が正確に行われることを確認
  - _Requirements: 2.1, 2.2, 2.3_
  - _Boundary: Hasher_

- [x] 2.3 (P) Database コンポーネントの実装
  - SQLite DBへの接続とテーブル作成機能を実装
  - ファイルパスとハッシュ値の保存・取得機能を実装
  - DB更新処理を実装
  - データ保存が正常に行われることを確認
  - _Requirements: 3.1, 3.2_
  - _Boundary: Database_

- [x] 2.4 (P) Merger コンポーネントの実装
  - 幹ファイルを残し枝ファイルを移動する機能を実装
  - ディレクトリ構造を維持した移動を実装
  - 統合スイッチのデフォルトoffを実装
  - ファイル移動が正常に行われることを確認
  - _Requirements: 5.1, 5.2, 5.3_
  - _Boundary: Merger_

- [x] 2.5 (P) Logger コンポーネントの実装
  - loggingライブラリを使用したログ設定を実装
  - ファイルとコンソールへの出力機能を実装
  - 処理中のファイルパスをログに出力する機能を実装
  - ログ出力が正常に行われることを確認
  - _Requirements: 6.1, 6.2_
  - _Boundary: Logger_

- [ ] 3. CLIインターフェースの実装
- [x] 3.1 CLI 引数解析の実装
  - Typer を使用したコマンドラインインターフェースを実装
  - ディレクトリ、ファイルパターン、trash_dir、mergeスイッチの引数を実装
  - trash_dir のデフォルト値を探索ディレクトリと同じ階層の .dup_trash に設定
  - 引数解析が正常に行われることを確認
  - _Requirements: 7.1, 7.2, 7.3_

- [ ] 4. 統合とテスト
- [x] 4.1 コンポーネント統合
  - CLI から各コンポーネントを呼び出す統合処理を実装
  - ファイル探索からレポート表示までの全体フローを実装
  - 統合スイッチon時のファイル移動処理を実装
  - 全体処理が正常に動作することを確認
  - _Requirements: 1.1, 2.1, 3.1, 4.1, 4.2, 5.1, 6.1, 7.1_

- [x] 4.2 統計レポートの実装
  - 探索したファイル総数、スキップ数、処理数、ユニーク数を計算して表示
  - 統合on時の移動ファイル数を表示
  - レポート表示が正確であることを確認
  - _Requirements: 4.1, 4.2_

- [x] 4.3 エンドツーエンドテスト
  - サンプルファイルを使用して全体処理をテスト
  - 重複ファイルの検出と統合を検証
  - エラーハンドリングをテスト
  - 全ての要件が満たされていることを確認
  - _Requirements: 1.1, 1.2, 1.3, 2.1, 2.2, 2.3, 3.1, 3.2, 4.1, 4.2, 5.1, 5.2, 5.3, 6.1, 6.2, 7.1, 7.2, 7.3_

- [ ] 5. 要件追加への対応
- [x] 5.1 (P) Scanner を再起探索に更新
  - os.walk を使用してディレクトリを再起的に辿る実装に変更
  - fnmatch を使用してパターンマッチングを実装
  - 既存テストより再起探索対応を確認
  - _Requirements: 1.4_
  - _Boundary: Scanner_

- [x] 5.2 (P) Logger にログローテーション機能を追加
  - RotatingFileHandler を使用してデイリーローテーション実装
  - backupCount=7 で7日分保持
  - maxBytes=0 でサイズベース回転を無効化
  - ログローテーション機能が正常に動作することを確認
  - _Requirements: 6.3, 6.4_
  - _Boundary: Logger_