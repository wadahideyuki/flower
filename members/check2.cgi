#!/usr/local/bin/perl

#��������������������������������������������������������������������
#�� CLIP MAIL : check.cgi - 2015/01/29
#�� copyright (c) KentWeb, 1997-2015
#�� http://www.kent-web.com/
#��������������������������������������������������������������������

# ���W���[���錾
use strict;
use CGI::Carp qw(fatalsToBrowser);
use lib './lib2';

# �O���t�@�C����荞��
require './init2.cgi';
my %cf = set_init();

print <<EOM;
Content-type: text/html; charset=$cf{charset}

<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=$cf{charset}">
<title>Check Mode</title>
</head>
<body>
<b>Check Mode: [ $cf{version} ]</b>
<ul>
<li>Perl�o�[�W���� : $]
EOM

# sendmail�`�F�b�N
print "<li>sendmail�p�X : ";
if (-e $cf{sendmail}) {
	print "OK\n";
} else {
	print "NG �� $cf{sendmail}\n";
}

# �f�B���N�g��
if (-d $cf{upldir}) {
	print "<li>�ꎞ�f�B���N�g���p�X : OK\n";

	if (-r $cf{upldir} && -w $cf{upldir} && -x $cf{upldir}) {
		print "<li>�ꎞ�f�B���N�g���p�[�~�b�V���� : OK\n";
	} else {
		print "<li>�ꎞ�f�B���N�g���p�[�~�b�V���� : NG\n";
	}
} else {
	print "<li>�ꎞ�f�B���N�g���p�X : NG\n";
}

# ���O�t�@�C��
my %log = (logfile => '���O�t�@�C��', sesfile => '�Z�b�V�����t�@�C��');
foreach ( keys %log ) {
	if (-f $cf{$_}) {
		print "<li>$log{$_}�p�X : OK\n";

		if ($_ ne 'base64') {
			if (-r $cf{$_} && -w $cf{$_}) {
				print "<li>$log{$_}�p�[�~�b�V���� : OK\n";
			} else {
				print "<li>$log{$_}�p�[�~�b�V���� : NG\n";
			}
		}
	} else {
		print "<li>$log{$_}�p�X : NG\n";
	}
}

# �e���v���[�g
foreach (qw(conf.html error.html thanks.html mail.txt reply.txt)) {
	print "<li>�e���v���[�g�p�X ( $_ ) : ";

	if (-f "$cf{tmpldir}/$_") {
		print "OK\n";
	} else {
		print "NG\n";
	}
}

print <<EOM;
</ul>
</body>
</html>
EOM
exit;


