#┌─────────────────────────────────
#│ POST-MAIL v4
#│ io-socket.pl - 2007/04/23
#│ copyright (c) KentWeb
#│ webmaster@kent-web.com
#│ http://www.kent-web.com/
#└─────────────────────────────────

#-------------------------------------------------
#  ソケット送信
#-------------------------------------------------
sub sendmail {
	my ($from, $to, $body) = @_;
	local($sock);

	# モジュール宣言
	use IO::Socket;
	use CGI::Carp qw(carpout fatalsToBrowser);

	# バイナリモード（Windows用）
	binmode(STDOUT);

	# POP before SMTP
	if ($pop_bef_smtp) {

		# ソケット接続（プロトコル、接続ホスト、接続ポート）
		$sock = IO::Socket::INET->new(
						Proto => "tcp",
						PeerAddr => $pop3sv,
						PeerPort => $pop3port,
						) || die "接続失敗";

		# バッファクリア
		$sock -> autoflush(1);
		&res('\+OK', 'flush失敗');

		# USERコマンド
		print $sock "USER $user\r\n";
		&res('\+OK', "USER失敗");

		# PASSコマンド
		print $sock "PASS $pass\r\n";
		&res('\+OK', "PASS失敗");

		# QUITコマンド
		print $sock "QUIT\r\n";
		&res('\+OK', "QUIT失敗");

		# ソケット完了
		$sock -> close();
	}

	# 本文改行調整
	$body =~ s/\n/\r\n/g;

	# ソケット接続（プロトコル、接続ホスト、接続ポート）
	$sock = IO::Socket::INET->new(
					Proto => "tcp",
					PeerAddr => $server,
					PeerPort => $port,
					) || die "接続失敗";

	# バッファクリア
	$sock -> autoflush(1);
	&res(220, 'flush失敗');

	# HELOコマンド
	print $sock "HELO $server\r\n";
	&res(250, 'HELO失敗');

	# MAILコマンド
	print $sock "MAIL FROM: <$from>\r\n";
	&res(250, 'MAIL失敗');

	# RCPTコマンド
	print $sock "RCPT TO: <$to>\r\n";
	&res("250|251", 'RCPT失敗');

	# RCPTコマンド
	if ($cc_mail) {
		print $sock "RCPT TO: <$from>\r\n";
		&res("250|251", 'RCPT(CC)失敗');
	}

	# DATAコマンド
	print $sock "DATA\r\n";
	&res(354, 'DATA失敗');

	# 本文送信
	print $sock "$body\r\n.\r\n";
	&res(250, '本文送信失敗');

	# QUITコマンド
	print $sock "QUIT\r\n";

	# ソケット完了
	$sock -> close();
}

#-------------------------------------------------
#  レスポンスチェック
#-------------------------------------------------
sub res {
	my ($str, $err) = @_;

	my $res = <$sock>;
	if ($res !~ /^$str/) {
		$sock -> close();
		die "$err : $res\n";
	}
}



1;

