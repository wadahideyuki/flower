# モジュール宣言/変数初期化
use strict;
my %cf;
#┌─────────────────────────────────
#│ CLIP-MAIL : init.cgi - 2015/02/28
#│ copyright (c) KentWeb, 1997-2015
#│ http://www.kent-web.com/
#└─────────────────────────────────
$cf{version} = 'clipmail v5.02';
#┌─────────────────────────────────
#│ [注意事項]
#│ 1. このプログラムはフリーソフトです。このプログラムを使用した
#│    いかなる損害に対して作者は一切の責任を負いません。
#│ 2. 送信フォームのHTMLページの作成に関しては、HTML文法の範疇
#│    となるため、サポート対象外となります。
#│ 3. 設置に関する質問はサポート掲示板にお願いいたします。
#│    直接メールによる質問はお受けいたしておりません。
#└─────────────────────────────────
#
# [ 送信フォーム (HTML) の記述例 ]
#
# ・タグの記述例 (1)
#   おなまえ <input type="text" name="name" size="25">
#   → このフォームに「山田太郎」と入力して送信すると、
#      「name = 山田太郎」という形式で受信します
#
# ・タグの記述例 (2)
#   お好きな色 <input type="radio" name="color" value="青">
#   → このラジオボックスにチェックして送信すると、
#      「color = 青」という形式で受信します
#
# ・タグの記述例 (3)
#   E-mail <input type="text" name="email" size="25">
#   → name値に「email」という文字を使うとこれはメールアドレス
#      と認識し、アドレスの書式を簡易チェックします
#   → (○) abc@xxx.co.jp
#   → (×) abc.xxx.co.jp → 入力エラーとなります
#
# ・タグの記述例 (4)
#   E-mail <input type="text" name="_email" size="25">
#   → name値の先頭に「アンダーバー 」を付けると、その入力値は
#     「入力必須」となります。
#      上記の例では、「メールアドレスは入力必須」となります。
#
# ・name値への「全角文字」の使用は可能です
#  (例) <input type="radio" name="年齢" value="20歳代">
#  → 上記のラジオボックスにチェックを入れて送信すると、
#     「年齢 = 20歳代」という書式で受け取ることができます。
#
# ・name値を「name」とするとこれを「送信者名」と認識して送信元の
#   メールアドレスを「送信者 <メールアドレス>」というフォーマットに
#   自動変換します。
#  (フォーム記述例)  <input type="text" name="name">
#  (送信元アドレス)  太郎 <taro@email.xx.jp>
#
# ・タグの記述例 (5)
#   ＜添付メール許可の場合＞
#   <input type="file" name="clip-1" size="40">
#   → name値を「clip-」+「数字」にしてください。
#   → 「数字」を変えることで、参照用フィールドを複数用意することが
#      できます。
#
# ・制御タグ-1
#   → 入力必須項目を強制指定する（半角スペースで複数指定可）
#   → ラジオボタン、チェックボックス対策
#   → name値を「need」、value値を「必須項目1 + 半角スペース +必須項目2 + 半角スペース ...」
#   (例) <input type="hidden" name="need" value="名前 メールアドレス 性別" />
#
# ・制御タグ-2
#   → 2つの入力内容が同一かをチェックする
#   → name値を「match」、value値を「項目1 + 半角スペース + 項目2」
#   (例) <input type="hidden" name="match" value="email email2" />
#
# ・制御タグ-3
#   → name値の並び順を指定する（半角スペースで複数指定）
#   → 入力エラー画面及びメール本文の並びを指定します
#   (例) <input type="hidden" name="sort" value="name email メッセージ" />

#===========================================================
#  ▼基本設定
#===========================================================

# このプログラムの文字コード (utf8 or sjis)
# utf8 : UTF-8
# sjis : Shift-JIS
$cf{kcode} = 'sjis';

# 管理者用パスワード
$cf{password} = 'japanflower';

# 送信先メールアドレス
$cf{mailto} = 'info@ikebana-atrium.com, yasuka_o@ikebana-atrium.com';

# sendmailのパス【サーバパス】
$cf{sendmail} = '/usr/lib/sendmail';

# sendmailへの-fコマンド（プロバイダの仕様確認）
# 0 : no
# 1 : yes
$cf{send_fcmd} = 0;

# 文字コード自動判別（0=no 1=yes）
# → フォームからの文字コード自動判別を行う場合
# → 通常は、「0」のほうが望ましい
$cf{conv_code} = 0;

# メール本文をBase64で送る
# → 機種依存文字等を扱う場合や、UTF-8版で海外との送信時に有効。
# 0 : no
# 1 : yes
$cf{send_b64} = 0;

# フォームのname値の置き換えをする場合（任意オプション）
# → 英字のname値を日本語に自動的に置き換えます。
# 例: 「email = xx@xx.xx」→「メールアドレス = xx@xx.xx」
$cf{replace} = {
		'name'    => 'お名前',
		'email'   => 'メール・アドレス',
		'comment' => 'コメント',
	};

# 添付メールを許可する
# 0 : no
# 1 : yes
$cf{attach} = 1;

# 添付メール許可のとき添付ファイルの「拡張子」を指定する場合
# → ドットなしで、コンマで区切る（小文字で記述）。
# → すべての拡張子をOKにするときは、$cf{extension} = ""; とする。
$cf{extension} = "gif,jpg,jpeg,png,bmp,doc,docx,xls,xlsx,pdf";

# 画像プレビューの時の表示サイズ
# → 画像はGIF/JPEG/PNG/BMPのみ
# → 順に横幅、縦幅
$cf{img_max_w} = 200;
$cf{img_max_h} = 150;

# 最大受信サイズ（Byte）
# → 例 : 102400Bytes = 100KB
$cf{maxdata} = 1024000;

# 自動返信
# 0 : no
# 1 : yes
$cf{auto_res} = 1;

# ログ蓄積の最大保存数
# → 0 にすると機能無効
$cf{keep_log} = 1000;

# メールタイトル
$cf{subject} = 'FlowerJapan 2018 | 出展申し込みフォーム';

# メール件名の外部指定（任意オプション）
# → 複数のフォームメールで運用する場合、タグで件名指定する
$cf{multi_sub} = {
		1 => '資料請求フォーム',
		2 => 'ご注文フォーム',
		3 => 'ご感想連絡フォーム',
	};

# 返信向けメールタイトル
$cf{sub_reply} = '「FlowerJapan 2018 | 出展申し込みフォーム」にご協力いただきありがとうございます';

# 本体プログラム【URLパス】
$cf{mail_cgi} = './clipmail.cgi';

# 管理プログラム【URLパス】
$cf{admin_cgi} = './admin.cgi';

# ログファイル【サーバパス】
$cf{logfile} = './data/log.cgi';

# セッションファイル【サーバパス】
$cf{sesfile} = './data/ses.cgi';

# 一時ディレクトリ
# → 順に【URLパス】【サーバパス】
$cf{uplurl} = './upl';
$cf{upldir} = './upl';

# テンプレートディレクトリ【サーバパス】
$cf{tmpldir} = './tmpl';

# セッションの許容時間（分単位）
# → 確認画面表示後、送信ボタンを押すまでの時間
$cf{sestime} = 5;

# 送信後の形態
# 0 : 完了メッセージを出す.
# 1 : 戻り先 ($back) へ自動ジャンプさせる.
$cf{reload} = 0;

# 送信後の戻り先【URLパス】
$cf{back} = 'index.html';

# フォームのname値の正当性をチェックする
# → 半角文字は英数字、アンダーバー、ハイフンはOK。全角は全てOK
# 0 : no
# 1 : yes
$cf{check_key} = 1;

# 送信は method=POST 限定 (0=no 1=yes)
# → セキュリティ対策
$cf{postonly} = 1;

# アクセス制限（複数あれば半角スペースで区切る、アスタリスク可）
# → 拒否ホスト名又はIPアドレスの記述例
#   （前方一致は先頭に ^ をつける）【例】^210.12.345.*
#   （後方一致は末尾に $ をつける）【例】*.anonymizer.com$
$cf{denyhost} = '';

# 禁止ワード
# → 投稿時禁止するワードをコンマで区切る
$cf{no_wd} = '';

# ホスト取得方法
# 0 : gethostbyaddr関数を使わない
# 1 : gethostbyaddr関数を使う
$cf{gethostbyaddr} = 0;

#===========================================================
#  ▲設定完了
#===========================================================

# for content-type charset
$cf{charset} = $cf{kcode} eq 'utf8' ? 'utf-8' : 'shift_jis';

# 文字コード変換モジュール
if ($] < 5.006) {
	require './lib/jacode.pl';
	$cf{conv_pm} = 'j';
} else {
	require Unicode::Japanese;
	$cf{conv_pm} = 'u';
}

# 設定値を返す
sub set_init {
	return %cf;
}


1;

