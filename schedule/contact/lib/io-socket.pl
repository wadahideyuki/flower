#��������������������������������������������������������������������
#�� POST-MAIL v4
#�� io-socket.pl - 2007/04/23
#�� copyright (c) KentWeb
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#��������������������������������������������������������������������

#-------------------------------------------------
#  �\�P�b�g���M
#-------------------------------------------------
sub sendmail {
	my ($from, $to, $body) = @_;
	local($sock);

	# ���W���[���錾
	use IO::Socket;
	use CGI::Carp qw(carpout fatalsToBrowser);

	# �o�C�i�����[�h�iWindows�p�j
	binmode(STDOUT);

	# POP before SMTP
	if ($pop_bef_smtp) {

		# �\�P�b�g�ڑ��i�v���g�R���A�ڑ��z�X�g�A�ڑ��|�[�g�j
		$sock = IO::Socket::INET->new(
						Proto => "tcp",
						PeerAddr => $pop3sv,
						PeerPort => $pop3port,
						) || die "�ڑ����s";

		# �o�b�t�@�N���A
		$sock -> autoflush(1);
		&res('\+OK', 'flush���s');

		# USER�R�}���h
		print $sock "USER $user\r\n";
		&res('\+OK', "USER���s");

		# PASS�R�}���h
		print $sock "PASS $pass\r\n";
		&res('\+OK', "PASS���s");

		# QUIT�R�}���h
		print $sock "QUIT\r\n";
		&res('\+OK', "QUIT���s");

		# �\�P�b�g����
		$sock -> close();
	}

	# �{�����s����
	$body =~ s/\n/\r\n/g;

	# �\�P�b�g�ڑ��i�v���g�R���A�ڑ��z�X�g�A�ڑ��|�[�g�j
	$sock = IO::Socket::INET->new(
					Proto => "tcp",
					PeerAddr => $server,
					PeerPort => $port,
					) || die "�ڑ����s";

	# �o�b�t�@�N���A
	$sock -> autoflush(1);
	&res(220, 'flush���s');

	# HELO�R�}���h
	print $sock "HELO $server\r\n";
	&res(250, 'HELO���s');

	# MAIL�R�}���h
	print $sock "MAIL FROM: <$from>\r\n";
	&res(250, 'MAIL���s');

	# RCPT�R�}���h
	print $sock "RCPT TO: <$to>\r\n";
	&res("250|251", 'RCPT���s');

	# RCPT�R�}���h
	if ($cc_mail) {
		print $sock "RCPT TO: <$from>\r\n";
		&res("250|251", 'RCPT(CC)���s');
	}

	# DATA�R�}���h
	print $sock "DATA\r\n";
	&res(354, 'DATA���s');

	# �{�����M
	print $sock "$body\r\n.\r\n";
	&res(250, '�{�����M���s');

	# QUIT�R�}���h
	print $sock "QUIT\r\n";

	# �\�P�b�g����
	$sock -> close();
}

#-------------------------------------------------
#  ���X�|���X�`�F�b�N
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

