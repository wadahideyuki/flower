#!/usr/local/bin/perl

#┌─────────────────────────────────
#│ POST-MAIL v4.31 (2010/06/27)
#│ copyright (c) KentWeb
#│ webmaster@kent-web.com
#│ http://www.kent-web.com/
#└─────────────────────────────────
$ver = 'postmail v4.31';
#┌─────────────────────────────────
#│ [注意事項]
#│ 1. このスクリプトはフリーソフトです。このスクリプトを使用した
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
#   おなまえ <input type="text" name="name">
#   → このフォームに「山田太郎」と入力して送信すると、
#      「name = 山田太郎」という形式で受信します
#
# ・タグの記述例 (2)
#   お好きな色 <input type="radio" name="color" value="青">
#   → このラジオボックスにチェックして送信すると、
#      「color = 青」という形式で受信します
#
# ・タグの記述例 (3)
#   E-mail <input type="text" name="email">
#   → name値に「email」という文字を使うとこれはメールアドレス
#      と認識し、アドレスの書式を簡易チェックします
#   → (○) abc@xxx.co.jp
#   → (×) abc.xxx.co.jp → 入力エラーとなります
#
# ・タグの記述例 (4)
#   E-mail <input type="text" name="_email">
#   → name値の先頭に「アンダーバー 」を付けると、その入力値は
#     「入力必須」となります。
#      上記の例では、「メールアドレスは入力必須」となります。
#
# ・name値への「全角文字」の使用は可能です
#  (例) <input type="radio" name="年齢" value="20歳代">
#  → 上記のラジオボックスにチェックを入れて送信すると、
#     「年齢 = 20歳代」という書式で受け取ることができます。
#
# ・mimew.pl使用時、name値を「name」とするとこれを「送信者名」と認識
#   して送信元のメールアドレスを「送信者 <メールアドレス>」という
#   フォーマットに自動変換します。
#  (フォーム記述例)  <input type="text" name="name">
#  (送信元アドレス)  太郎 <taro@email.xx.jp>
#
# ・コマンドタグ (1)
#   → 入力必須項目を強制指定する（半角スペースで複数指定可）
#   → ラジオボタン、チェックボックス対策
#   → name値を「need」、value値を「必須項目1 + 半角スペース +必須項目2 + 半角スペース ...」
#   (例) <input type="hidden" name="need" value="名前 メールアドレス 性別">
#
# ・コマンドタグ (2)
#   → 2つの入力内容が同一かをチェックする
#   → name値を「match」、value値を「項目1 + 半角スペース + 項目2」
#   (例) <input type="hidden" name="match" value="email email2">
#
# ・コマンドタグ (3)
#   → メール件名を指定する
#   → この場合、設定で指定する $subject より優先されます。
#   (例) <input type="hidden" name="subject" value="メールタイトル○○">
#
#  [ 簡易チェック ]
#   http://～～/postmail.cgi?mode=check
#
#  [ 設置例 ]
#
#  public_html / index.html (トップページ等）
#       |
#       +-- postmail / postmail.cgi  [705]
#             |        postmail.html
#             |
#             +-- lib / jcode.pl     [604]
#             |         mimew.pl     [604] ... 任意
#             |         io-socket.pl [604]
#             |
#             +-- data / log.cgi     [606]
#             |
#             +-- tmpl / body.txt
#                        conf.html
#                        err1.html
#                        err2.html
#                        thx.html

#-------------------------------------------------
#  ▼基本設定
#-------------------------------------------------

# 文字コード変換ライブラリ【サーバパス】
require './lib/jcode.pl';

# MIMEエンコードライブラリを使う場合（推奨）【サーバパス】
#  → メールヘッダの全角文字をBASE64変換する機能
#  → mimew.plを指定
$mimew = './lib/mimew.pl';

# 送信先メールアドレス
$mailto = 'info@st-george.co.jp,terasaka@st-george.co.jp,kusaka@st-george.co.jp';

# 入力フィールドあたりの最大容量（バイト）
# ＊参考 : 全角1文字 = 2バイト
$max_field = 500;

# 送信前確認
# 0 : no
# 1 : yes
$preview = 1;

# メールタイトル
$subject = '仙台セント・ジョージ教会 お問い合わせ';

# 本体プログラム【URLパス】
$script = './form02.cgi';

# ログファイル【サーバパス】
$logfile = './data/log.cgi';

# 確認画面テンプレート【サーバパス】
$tmp_conf = './tmpl02/conf.html';

# 一般エラー画面テンプレート【サーバパス】
$tmp_err1 = './tmpl02/err1.html';

# 入力エラー画面テンプレート【サーバパス】
$tmp_err2 = './tmpl02/err2.html';

# 送信後画面テンプレート【サーバパス】
$tmp_thx = './tmpl02/thx.html';

# 送信「本文」テンプレート【サーバパス】
$tmp_body = './tmpl02/body.txt';

# 送信「本文」テンプレート【サーバパス】
$tmp_body2 = './tmpl02/body2.txt';

# メールの送信者名
$master_name = '仙台セント・ジョージ教会';

# 送信後の形態
# 0 : 完了メッセージを出す.
# 1 : 戻り先 ($back) へ自動ジャンプさせる.
$reload = 0;

# 送信後の戻り先【URLパス】
#  → http://から記述する
$back = 'http://www.st-george.co.jp';

# 同一IPアドレスからの連続送信制御
# → 許可する間隔を秒数で指定（0にするとこの機能は無効）
$block_post = 60;

# 送信は method=POST 限定 (0=no 1=yes)
#  → セキュリティ対策
$postonly = 1;

# アラーム色
$alm_col = "#dd0000";

# ホスト取得方法
# 0 : gethostbyaddr関数を使わない
# 1 : gethostbyaddr関数を使う
$gethostbyaddr = 0;

# アクセス制限（複数あれば半角スペースで区切る、アスタリスク可）
# → 拒否ホスト名又はIPアドレスの記述例
#   （前方一致は先頭に ^ をつける）【例】^210.12.345.*
#   （後方一致は末尾に $ をつける）【例】*.anonymizer.com$
$denyhost = '';

# 禁止ワード
# → 投稿時禁止するワードをコンマで区切る
$no_wd = '';

# 送信元へ控え (CC) を送る
# 0=no 1=yes
# ＊セキュリティ上この機能は推奨しません.
# ＊name="email" のフィールドへの入力が必須となります.
$cc_mail = 0;

# メール送信形式
# 1 : sendmail送信（sendmailが利用可能なサーバ）
# 2 : IO:Socketモジュール送信（ソケット関連のモジュールが利用可能なサーバ）
$send_type = 1;

## sendmail送信のとき ##
# sendmailのパス
$sendmail = '/usr/lib/sendmail';

##【注】sendmail送信の方は設定はここまでで終了。これより下は設定不要です。

## IO:Socketモジュール送信のとき ##
# io-socket.plのパス
$io_socket = './lib/io-socket.pl';

# SMTPサーバ
$server = "mail.server.xx.jp";

# SMTPポート番号（通常は25）
$port = 25;

# POP before SMTPを使用する
# 0 : no
# 1 : yes
$pop_bef_smtp = 0;

# POP3サーバ【POP before SMTPのとき】
$pop3sv = 'mail.server.xx.jp';

# POP3ポート番号（通常は110）【POP before SMTPのとき】
$pop3port = 110;

# 接続ID【POP before SMTPのとき】
$user = 'user_id';

# 接続パスワード【POP before SMTPのとき】
$pass = 'password';

## ↑SMTPサーバへの接続情報ここまで

#-------------------------------------------------
#  ▲設定完了
#-------------------------------------------------

# フォームデコード
$ret = &decode;

# 基本処理
if (!$ret) { &error("不明な処理です"); }
elsif ($in{'mode'} eq "check") { &check; }

# POSTチェック
if ($postonly && !$postflag) { &error("不正なアクセスです"); }

# 汚染チェック
if ($in{'subject'} =~ /\r|\n/) { &error("メール件名が不正です"); }
$in{'subject'} =~ s/\@/＠/g;
$in{'subject'} =~ s/\./．/g;
$in{'subject'} =~ s/\+/＋/g;
$in{'subject'} =~ s/\-/－/g;
$in{'subject'} =~ s/\:/：/g;
$in{'subject'} =~ s/\;/；/g;
$in{'subject'} =~ s/\|/｜/g;

# 著作権表記（削除不可）
$copy = <<EOM;
EOM

# 禁止ワード
if ($no_wd) {
	local($flg);
	foreach (@key) {
		foreach $nowd ( split(/,/, $no_wd) ) {
			if (index($in{$_},$nowd) >= 0) {
				$flg = 1; last;
			}
		}
		if ($flg) { &error("禁止ワードが含まれています"); }
	}
}

# ホスト取得＆チェック
&get_host;

# 必須入力チェック
if ($in{'need'}) {
	local(@tmp, @uniq, %seen);

	# needフィールドの値を必須配列に加える
	@tmp = split(/\s+/, $in{'need'});
	push(@need,@tmp);

	# 必須配列の重複要素を排除する
	foreach (@need) {
		push(@uniq,$_) unless $seen{$_}++;
	}

	# 必須項目の入力値をチェックする
	foreach (@uniq) {

		# フィールドの値が投げられてこないもの（ラジオボタン等）
		if (!defined($in{$_})) {
			$check++;
			push(@key,$_);
			push(@err,$_);

		# 入力なしの場合
		} elsif ($in{$_} eq "") {
			$check++;
			push(@err,$_);
		}
	}
}

# 入力内容マッチ
if ($in{'match'}) {
	($match1,$match2) = split(/\s+/, $in{'match'}, 2);

	if ($in{$match1} ne $in{$match2}) {
		&error("$match1と$match2の再入力内容が異なります");
	}
}

# 入力チェック確認画面
if ($check || $max_flg) { &err_check; }

# E-Mail書式チェック
if ($in{'email'} =~ /\,/) {
	&error("メールアドレスにコンマ ( , ) が含まれています");
}
if ($in{'email'} && $in{'email'} !~ /^[\w\.\-]+\@[\w\.\-]+\.[a-zA-Z]{2,6}$/) {
	&error("メールアドレスの書式が不正です");
}

# プレビュー
if ($preview && $in{'mode'} ne "send") {

	# 連続送信チェック
	&check_post('view');

	local($cp_flag,$flag,$cell,$tmp,$hidden);
	open(IN,"$tmp_conf") || &error("Open Error: $tmp_conf");
	print "Content-type: text/html\n\n";
	while (<IN>) {
		if (/<!-- cell_begin -->/) {
			$flag = 1;
			next;
		}
		if (/<!-- cell_end -->/) {
			$flag = 0;

			local($key,$bef,$tmp);

			$hidden .= "<input type=\"hidden\" name=\"mode\" value=\"send\" />\n";

			foreach $key (@key) {
				next if ($bef eq $key);

				if ($key eq "need" || $key eq "match" || ($in{'match'} && $key eq $match2)) {
					next;
				} elsif ($key eq "subject") {
					$hidden .= "<input type=\"hidden\" name=\"$key\" value=\"$in{$key}\" />\n";
					next;
				}

				$in{$key} =~ s/\0/ /g;
				$in{$key} =~ s/\r\n/<br \/>/g;
				$in{$key} =~ s/\r/<br \/>/g;
				$in{$key} =~ s/\n/<br \/>/g;
				if ($in{$key} =~ /<br \/>$/) {
					while ($in{$key} =~ /<br \/>$/) {
						$in{$key} =~ s/<br \/>$//g;
					}
				}

				$tmp = $cell;
				$tmp =~ s/\$left/$key/;
				$tmp =~ s/\$right/$in{$key}/;

				print "$tmp\n";
				$hidden .= "<input type=\"hidden\" name=\"$key\" value=\"$in{$key}\" />\n";

				$bef = $key;
			}
			next;
		}
		if ($flag) {
			$cell .= $_;
			next;
		}

		s/\$script/$script/;
		s/<!-- hidden -->/$hidden/;

		if (/(<\/body([^>]*)>)/i) {
			$cp_flag = 1;
			$tmp = $1;
			s/$tmp/$copy\n$tmp/;
		}

		print;
	}
	close(IN);

	if (!$cp_flag) { print "$copy\n</body></html>\n"; }

	exit;
}

# 連続送信チェック
&check_post('send');

# 時間取得
($date1, $date2) = &get_time;

# コマンドタグで件名指定あり
if ($in{'subject'}) {
	$in{'subject'} =~ s/\|/｜/g;
	$in{'subject'} =~ s/;/；/g;
	$subject = $in{'subject'};
}

# ブラウザ情報
$agent = $ENV{'HTTP_USER_AGENT'};
$agent =~ s/<//g;
$agent =~ s/>//g;
$agent =~ s/"//g;
$agent =~ s/&//g;
$agent =~ s/'//g;

local($bef, $mbody, $email, $subject2, $tbody);

# 本文テンプレ読み込み
open(IN,"$tmp_body");
while (<IN>) {
	s/\r\n/\n/;

	$tbody .= $_;
}
close(IN);

# 返信用テンプレ読み込み
open(IN,"$tmp_body2");
while (<IN>) {
s/\r\n/\n/;

$tbody2 .= $_;
}
close(IN);

# テンプレ変数変換
$tbody =~ s/\$date/$date1/;
$tbody2 =~ s/\$date/$date1/; 
$tbody =~ s/\$agent/$agent/;
$tbody =~ s/\$host/$host/;
&jcode::convert(\$tbody, 'jis');
&jcode'convert(*tbody2, 'jis'); 

# 本文のキーを展開
foreach (@key) {
	# 本文に含めない部分を排除
	next if ($_ eq "mode");
	next if ($_ eq "need");
	next if ($_ eq "match");
	next if ($_ eq "subject");
	next if ($in{'match'} && $_ eq $match2);
	next if ($bef eq $_);

	# エスケープ
	$in{$_} =~ s/\0/ /g;
	$in{$_} =~ s/＜br＞/\n/g;
	$in{$_} =~ s/\.\n/\. \n/g;

	# 添付ファイル拒否
	$in{$_} =~ s/Content-Disposition:\s*attachment;.*//ig;
	$in{$_} =~ s/Content-Transfer-Encoding:.*//ig;
	$in{$_} =~ s/Content-Type:\s*multipart\/mixed;\s*boundary=.*//ig;

	# 本文内容
	local($tmp);
	if ($in{$_} =~ /\n/) {
		$tmp = "$_ = \n\n$in{$_}\n";
	} else {
		$tmp = "$_ = $in{$_}\n";
	}
	&jcode::convert(\$tmp, 'jis', 'sjis');
	$mbody .= $tmp;

	$bef = $_;
}

# 本文テンプレ内の変数を置き換え
$tbody =~ s/\$message/$mbody/;
$tbody2 =~ s/\$message/$mbody/;

# メールアドレスがない場合は送信先に置き換え
if ($in{'email'} eq "") { $email = $mailto; }
else { $email = $in{'email'}; }

# MIMEエンコード

if (-e $mimew) {
require $mimew;
$subject2 = &mimeencode($subject);
$from = &mimeencode("\"$master_name\" <$mailto>");
} else {
$subject2 = &base64($subject);
$from = &base64("\"$master_name\"") . " <$mailto>";
}


# 送信内容フォーマット化
$body = "To: $mailto\n";
$body .= "From: $from\n";
if ($cc_mail && $email) { $body .= "Cc: $email\n"; }
$body .= "Subject: $subject2\n";
$body .= "MIME-Version: 1.0\n";
$body .= "Content-type: text/plain; charset=iso-2022-jp\n";
$body .= "Content-Transfer-Encoding: 7bit\n";
$body .= "Date: $date2\n";
$body .= "X-Mailer: $ver\n\n";
$body .= "$tbody\n";

$body2 = "To: $email\n";
$body2 .= "From: $from\n";
$body2 .= "Subject: $subject2\n";
$body2 .= "MIME-Version: 1.0\n";
$body2 .= "Content-type: text/plain; charset=iso-2022-jp\n";
$body2 .= "Content-Transfer-Encoding: 7bit\n";
$body2 .= "Date: $date2\n";
$body2 .= "X-Mailer: $ver\n\n";
$body2 .= "$tbody2\n";


# IO:Socketモジュール送信
if ($send_type == 2) {
	require $io_socket;
	&sendmail($email, $mailto, $body);

# sendmail送信
} else {
	open(MAIL,"| $sendmail -t -i") || &error("メール送信失敗");
	print MAIL "$body\n";
	close(MAIL);
}

open(MAIL,"| $sendmail -t -i") || &error("メール送信失敗");
print MAIL "$body2\n";
close(MAIL);


####### お客様控え用

# リロード
if ($reload) {
	if ($ENV{'PERLXS'} eq "PerlIS") {
		print "HTTP/1.0 302 Temporary Redirection\r\n";
		print "Content-type: text/html\n";
	}
	print "Location: $back\n\n";
	exit;

# 完了メッセージ
} else {
	local($cp_flag,$tmp);
	open(IN,"$tmp_thx") || &error("Open Error: $tmp_thx");
	print "Content-type: text/html\n\n";
	while (<IN>) {
		s/\$back/$back/;

		if (/(<\/body([^>]*)>)/i) {
			$cp_flag=1;
			$tmp = $1;
			s/$tmp/$copy\n$tmp/;
		}

		print;
	}
	close(IN);

	if (!$cp_flag) { print "$copy\n</body></html>\n"; }

	exit;
}


#-------------------------------------------------
#  入力チェック
#-------------------------------------------------
sub err_check {
	local($cp_flag, $flag, $cell);
	open(IN,"$tmp_err2") || &error("Open Error: $tmp_err2");
	print "Content-type: text/html\n\n";
	while (<IN>) {
		if (/<!-- cell_begin -->/) {
			$flag = 1;
		}
		if (/<!-- cell_end -->/) {
			$flag = 0;

			my $bef;
			foreach $key (@key) {
				next if ($key eq "need");
				next if ($key eq "subject");
				next if ($key eq "match");
				next if ($in{'match'} && $key eq $match2);
				next if ($_ eq "match");
				next if ($bef eq $key);

				my $tmp = $cell;
				$tmp =~ s/\$left/$key/;

				my $flg;
				foreach $err (@err) {
					if ($err eq $key) { $flg++; last; }
				}
				if ($flg) {
					$tmp =~ s|\$right|<span style="color:$alm_col">$keyは入力必須です</span>|;
				} elsif (defined($err{$key})) {
					$tmp =~ s|\$right|<span style="color:$alm_col">$keyの入力内容が大きすぎます</span>|;
				} else {
					$in{$key} =~ s/\r\n/<br>/g;
					$in{$key} =~ s/\r/<br>/g;
					$in{$key} =~ s/\n/<br>/g;
					$in{$key} =~ s/\0/ /g;

					$tmp =~ s/\$right/$in{$key}/;
				}

				print "$tmp\n";

				$bef = $key;
			}
		}
		if ($flag) {
			$cell .= $_;
			next;
		}

		if (/(<\/body([^>]*)>)/i) {
			$cp_flag = 1;
			$tmp = $1;
			s/$tmp/$copy\n$tmp/;
		}

		print;
	}
	close(IN);

	if (!$cp_flag) { print "$copy\n</body></html>\n"; }

	exit;
}

#-------------------------------------------------
#  フォームデコード
#-------------------------------------------------
sub decode {
	my $buf;
	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		$postflag = 1;
		read(STDIN, $buf, $ENV{'CONTENT_LENGTH'});
	} else {
		$postflag = 0;
		$buf = $ENV{'QUERY_STRING'};
	}

	undef(%in); undef(%err);
	@key = (); @need = (); @err = ();
	$check = 0; $max_flg = 0;
	foreach ( split(/&/, $buf) ) {
		my ($key, $val) = split(/=/);
		$key =~ tr/+/ /;
		$key =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("H2", $1)/eg;
		$val =~ tr/+/ /;
		$val =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("H2", $1)/eg;

		# コード変換
		&jcode::convert(\$key, 'sjis');
		&jcode::convert(\$val, 'sjis');

		# エスケープ
		$key =~ s/&/＆/g;
		$key =~ s/"/”/g;
		$key =~ s/</＜/g;
		$key =~ s/>/＞/g;
		$key =~ s/'/’/g;
		$val =~ s/&/＆/g;
		$val =~ s/"/”/g;
		$val =~ s/</＜/g;
		$val =~ s/>/＞/g;
		$val =~ s/'/’/g;

		if (length($key) > $max_field || length($val) > $max_field) {
			$max_flg = 1;
			$err{$key} = $val;
		}

		# 必須入力項目
		if ($key =~ /^_(.+)/) {
			$key = $1;
			push(@need,$key);

			if ($val eq "") { $check++; push(@err,$key); }
		}

		$in{$key} .= "\0" if (defined($in{$key}));
		$in{$key} .= $val;

		push(@key,$key);
	}

	# 返り値
	if ($buf) { return 1; } else { return 0; }
}

#-------------------------------------------------
#  エラー処理
#-------------------------------------------------
sub error {
	print "Content-type: text/html\n\n";
	open(IN,"$tmp_err1");
	while (<IN>) {
		s/\$error/$_[0]/;

		print;
	}
	close(IN);

	exit;
}

#-------------------------------------------------
#  時間取得
#-------------------------------------------------
sub get_time {
	$ENV{'TZ'} = "JST-9";
	my ($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime(time);
	my @w = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');
	my @m = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');

	# 日時のフォーマット
	my $date1 = sprintf("%04d/%02d/%02d(%s) %02d:%02d",
			$year+1900,$mon+1,$mday,$w[$wday],$hour,$min);
	my $date2 = sprintf("%s, %02d %s %04d %02d:%02d:%02d",
			$w[$wday],$mday,$m[$mon],$year+1900,$hour,$min,$sec) . " +0900";

	return ($date1, $date2);
}

#-------------------------------------------------
#  ホスト名取得
#-------------------------------------------------
sub get_host {
	# ホスト名取得
	$host = $ENV{'REMOTE_HOST'};
	$addr = $ENV{'REMOTE_ADDR'};

	if ($gethostbyaddr && ($host eq "" || $host eq $addr)) {
		$host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2);
	}
	if ($host eq "") { $host = $addr; }

	# チェック
	if ($denyhost) {
		my $flg;
		foreach ( split(/\s+/, $denyhost) ) {
			s/\./\\\./g;
			s/\*/\.\*/g;

			if ($host =~ /$_/i) { $flg = 1; last; }
		}
		if ($flg) { &error("アクセスを許可されていません"); }
	}
}

#-------------------------------------------------
#  送信チェック
#-------------------------------------------------
sub check_post {
	my $job = shift;

	# IP及び時間取得
	my $addr = $ENV{'REMOTE_ADDR'};
	my $now  = time;

	# ログオープン
	open(DAT,"+< $logfile");
	eval "flock(DAT, 2);";
	my $data = <DAT>;

	# 分解
	my ($ip, $time) = split(/<>/, $data);

	# IP及び時間をチェック
	if ($ip eq $addr && $now - $time <= $block_post) {
		close(DAT);
		&error("連続送信は$block_post秒間お待ちください");
	}

	if ($job eq "send") {
		seek(DAT, 0, 0);
		print DAT "$addr<>$now";
		truncate(DAT, tell(DAT));
	}
	close(DAT);
}

#-------------------------------------------------
#  チェックモード
#-------------------------------------------------
sub check {
	print "Content-type: text/html\n\n";
	print <<EOM;
<html><head>
<meta http-equiv="content-type" content="text/html; charset=shift_jis">
<title>チェックモード</title></head>
<body>
<h3>チェックモード</h3>
<ul>
EOM

	# ログファイル
	if (-e $logfile) {
		print "<li>ログファイル：パスOK!\n";

		if (-r $logfile && -w $logfile) {
			print "<li>ログファイル：パーミッションOK!\n";
		} else {
			print "<li>ログファイル：パーミッションNG\n";
		}

	} else {
		print "<li>ログファイルパスNG → $logfile\n";
	}

	# メールソフトチェック
	print "<li>メールソ\フトパス：";
	if (-e $sendmail) {
		print "OK\n";
	} else {
		print "NG → $sendmail\n";
	}

	# jcode.pl バージョンチェック
	print "<li>jcode.plバージョンチェック：";

	if ($jcode'version < 2.13) {
		print "バージョンが低いようです。→ v$jcode::version\n";
	} else {
		print "バージョンOK (v$jcode'version)\n";
	}

	# テンプレート
	foreach ( $tmp_body, $tmp_conf, $tmp_err1, $tmp_err2, $tmp_thx ) {
		print "<li>テンプレート ( $_ ) ：";
		if (-e $_) {
			print "パスOK!\n";
		} else {
			print "パスNG → $_\n";
		}
	}

	print <<EOM;
<li>バージョン：$ver
</ul>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  BASE64変換
#-------------------------------------------------
#　とほほのWWW入門で公開されているルーチンを参考にしました。
#　http://www.tohoho-web.com/
sub base64 {
	local($sub) = @_;
	&jcode::convert(\$sub, 'jis');

	$sub =~ s/\x1b\x28\x42/\x1b\x28\x4a/g;
	$sub = "=?iso-2022-jp?B?" . &b64enc($sub) . "?=";
	$sub;
}
sub b64enc {
	local($ch) = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
	local($x, $y, $z, $i);
	$x = unpack("B*", $_[0]);
	for ( $i = 0; $y = substr($x,$i,6); $i += 6 ) {
		$z .= substr($ch, ord(pack("B*", "00" . $y)), 1);
		if (length($y) == 2) {
			$z .= "==";
		} elsif (length($y) == 4) {
			$z .= "=";
		}
	}
	$z;
}


