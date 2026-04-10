# Requirements Document

## Project Description (Input)
ファイルの重複チェックを行い、同一ファイルに関してはひとつのファイルに統合するコマンドラインツールを作成します。

下記の過程で得られるファイルパスやハッシュ値、同一ファイルのパスといった中間データはSQLite（以下、DB）に保存します。

以下、同一のファイルが複数ある場合、ファイルパスで昇順ソートしファイルパスが一番最初のファイルを「幹ファイル」、それ以外を「枝ファイル」と表現しています。

1. ユーザーから引数として与えるのは以下のとおり。
    - 探索するディレクトリ
    - 探索するファイルパターン（デフォルトは `*.mp4` ）
    - 枝ファイルを移動する先のディレクトリ（デフォルトは、「探索するディレクトリ」と同じ階層の `.dup_trash` ）
    - 統合を実行するかのスイッチ（デフォルトはoff）
2. 指定したディレクトリ配下から、指定したファイルパターンに該当するファイル群を探索する。
3. 各ファイルのハッシュ値を計算し、ファイルパスと紐付ける。
    - このハッシュ値が同一のファイルを「同一ファイル」として判定する。
    - ファイルパスとハッシュ値がDBに保存されている場合は、ハッシュ値の計算はスキップする。
4. 同一のファイルがある場合は、ファイルパスに関連する情報として列挙する。
5. これを該当するファイル群すべてに適用する。
6. 終わったらユーザーに終わった旨を伝える。その際、下記の情報も表示する。
    - 探索したファイルの総数
    - スキップしたファイルの総数
    - 今回処理したファイルの総数（=探索したファイルの総数 - スキップしたファイルの総数）
    - ユニークなファイルの総数（=探索したファイルの総数から枝ファイルの総数を引いた値）
7. 統合を実行するかのスイッチがonの場合は、後述する処理を行う。


統合を実行するかのスイッチがonの場合の処理

1. 幹ファイルのみを残し、枝ファイルを「枝ファイルを移動する先のディレクトリ」に移動する。
    - この際、ディレクトリ構造を残したまま移動する。
        - 例： `${探索するディレクトリ}/foo/baa/john.mp4`  → `${枝ファイルを移動する先のディレクトリ}/foo/baa/john.mp4` 

2. 終わったらユーザーに終わった旨を伝える。その際、下記の情報も表示する。
    - 今回移動したファイルの総数


ルール

1. python 3.14で実装する。
2. なるべく標準のライブラリを用いる。
3. サードパーティ製のライブラリを用いる場合は開発者に確認する。
4. loggingライブラリを用いてログファイルへの出力、コンソールへの出力をする。
    - 処理するファイルのパスはログおよびコンソールへ出力する。
5. CLIのライブラリとしては、Typerを使用する。
6. パッケージマネージャーとしては、uvを使用する。

## Requirements

### Requirement 1: ファイル探索機能
**Objective:** ユーザーは指定したディレクトリからファイルパターンに一致するファイルを探索できる。

#### Acceptance Criteria
1. When ユーザーが探索ディレクトリとファイルパターンを指定したとき、duplicate-file-checker は指定ディレクトリ配下からパターンに該当するファイル群を再起的に探索する。
2. If 探索ディレクトリが存在しない場合、duplicate-file-checker はエラーメッセージを表示する。
3. The duplicate-file-checker はデフォルトで `*.mp4` パターンを適用する。
4. The duplicate-file-checker は指定ディレクトリのサブディレクトリを再起的に辿る。

### Requirement 2: ハッシュ計算と重複判定機能
**Objective:** システムはファイルのハッシュを計算し、重複を判定できる。

#### Acceptance Criteria
1. When ファイルが探索されたとき、duplicate-file-checker は各ファイルのハッシュ値を計算し、ファイルパスと紐付ける。
2. If ファイルパスとハッシュ値がDBに保存されている場合、duplicate-file-checker はハッシュ値の計算をスキップする。
3. The duplicate-file-checker は同一ハッシュ値を持つファイルを同一ファイルとして判定する。

### Requirement 3: データ保存機能
**Objective:** 中間データをSQLite DBに保存する。

#### Acceptance Criteria
1. The duplicate-file-checker はファイルパス、ハッシュ値、同一ファイルのパスをSQLite DBに保存する。
2. When 処理が完了したとき、duplicate-file-checker はDBを更新する。

### Requirement 4: レポート表示機能
**Objective:** 処理完了時に統計情報を表示する。

#### Acceptance Criteria
1. When 処理が完了したとき、duplicate-file-checker は探索したファイルの総数、スキップしたファイルの総数、今回処理したファイルの総数、ユニークなファイルの総数を表示する。
2. If 統合スイッチがonの場合、duplicate-file-checker は移動したファイルの総数を表示する。

### Requirement 5: ファイル統合機能
**Objective:** オプションで重複ファイルを統合する。

#### Acceptance Criteria
1. Where 統合スイッチがonの場合、duplicate-file-checker は幹ファイルを残し、枝ファイルを指定ディレクトリに移動する。
2. While 統合処理中、duplicate-file-checker はディレクトリ構造を維持する。
3. The duplicate-file-checker はデフォルトで統合スイッチをoffにする。

### Requirement 6: ログ出力機能
**Objective:** 処理中のログをファイルとコンソールに出力する。

#### Acceptance Criteria
1. The duplicate-file-checker はloggingライブラリを用いてログファイルとコンソールに出力する。
2. When ファイルが処理されたとき、duplicate-file-checker はファイルパスをログとコンソールに出力する。
3. The duplicate-file-checker はログファイルを `logs` ディレクトリに出力する。ディレクトリが存在しない場合は作成する。
4. The duplicate-file-checker はログファイルをデイリーでローテーションし、上限は7日分の保持とする。

### Requirement 7: CLIインターフェース
**Objective:** Typerを用いたコマンドラインインターフェースを提供する。

#### Acceptance Criteria
1. The duplicate-file-checker はTyperライブラリを使用してCLIを実装する。
2. When ユーザーが引数を指定したとき、duplicate-file-checker は引数を正しく解析する。
3. The duplicate-file-checker は枝ファイルを移動する先のディレクトリのデフォルト値を「探索するディレクトリ」と同じ階層の `.dup_trash` にする。