# Requirements Document

## Project Description (Input)
メンテナンス用のサブコマンドを追加する。

1. DBに格納されているパスを確認する。
2. パスのファイルが存在しない場合はそのエントリーを削除する。
3. 削除したエントリーは、`logs/purged_entry.csv` に出力する。
   - 出力内容はタブ区切りで以下を出力する。
     - ファイルパス
     - ハッシュ値
     - 処理日時（UTC）のISOフォーマット

## Requirements

### Requirement 1: DBエントリー確認機能
**Objective:** ユーザーはメンテナンス用サブコマンドでDBに保存されているパスを確認できる。

#### Acceptance Criteria
1.1 When ユーザーがメンテナンス用サブコマンドを実行したとき、duplicate-file-checker はDBの全エントリー（ファイルパスとハッシュ値）を走査対象として取得する。
1.2 The duplicate-file-checker は既存の重複チェックコマンドとは独立したサブコマンドとしてこの機能を提供する。

### Requirement 2: 不正エントリー削除機能
**Objective:** ファイルが存在しないDBエントリーを削除できる。

#### Acceptance Criteria
2.1 When DBに保存されたファイルパスがファイルシステム上に存在しない場合、duplicate-file-checker は該当エントリーをDBから削除する。
2.2 The duplicate-file-checker はファイルが存在するエントリーを削除しない。

### Requirement 3: 削除エントリー監査ログ出力機能
**Objective:** 削除したエントリー情報を監査可能な形式で出力する。

#### Acceptance Criteria
3.1 When エントリーを削除した場合、duplicate-file-checker は `logs/purged_entry.csv` に追記出力する。
3.2 The duplicate-file-checker は出力フォーマットをタブ区切りとし、1行につき「ファイルパス」「ハッシュ値」「処理日時（UTC ISO 8601）」の3列を出力する。
3.3 The duplicate-file-checker は `logs` ディレクトリが存在しない場合に作成する。

### Requirement 4: 障害耐性と可観測性
**Objective:** メンテナンス処理中の障害を記録しつつ継続可能にする。

#### Acceptance Criteria
4.1 When エントリー処理中に例外が発生した場合、duplicate-file-checker は対象パスと例外内容をログに出力する。
4.2 The duplicate-file-checker は例外が発生したエントリー以外の処理を継続する。
