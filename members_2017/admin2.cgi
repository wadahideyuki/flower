#!/usr/local/bin/perl

#��������������������������������������������������������������������
#�� Clip Mail : admin2.cgi - 2015/01/04
#�� copyright (c) KentWeb, 1997-2015
#�� http://www.kent-web.com/
#��������������������������������������������������������������������

# ���W���[�����s
use strict;
use CGI::Carp qw(fatalsToBrowser);
use lib './lib2';
use CGI::Minimal;

# �O���t�@�C����荞��
require './init2.cgi';
my %cf = set_init();

# �f�[�^��
CGI::Minimal::max_read_size($cf{maxdata});
my $cgi = CGI::Minimal->new;
error('�e�ʃI�[�o�[') if ($cgi->truncated);

# �t�H�[���f�R�[�h
my %in = parse_form();

# ��{����
pwd_check();
menu_list();

#-----------------------------------------------------------
#  ���O�_�E�����[�h
#-----------------------------------------------------------
sub menu_list {
	# �_�E�����[�h���s
	if ($in{downld}) {

		# �I���`�F�b�N
		if (!$in{br}) { error("�I�v�V�����ɖ��I��������܂�"); }

		# ���s�R�[�h��`
		my %br = ( win => "\r\n", mac => "\r", unix => "\n" );

		# ���O���I�[�v��
		my ($i,@item,%key,%head,%csv);
		open(IN,"$cf{logfile}") or error("open err: $cf{logfile}");
		while(<IN>) {
			chomp;
			$i++;
			my @log = split(/<>/);

			my $csv;
			foreach my $n (0 .. $#log) {
				my ($key,$val) = split(/=/,$log[$n]);

				if ($n <= 1) {
					$head{$i} .= "$val,";
					next;
				}

				if (!defined($key{$key})) {
					$key{$key}++;
					push(@item,$key);
				}

				# HTML�ϊ�
				$val =~ s/&lt;/</g;
				$val =~ s/&gt;/>/g;
				$val =~ s/&quot;/"/g;
				$val =~ s/&#39;/'/g;
				$val =~ s/&amp;/&/g;

				$csv{"$i<>$key"} = $val;
			}
		}
		close(IN);

		# �_�E�����[�h�p�w�b�_�[
		print "Content-type: application/octet-stream\n";
		print "Content-Disposition: attachment; filename=data.csv\n\n";
		binmode(STDOUT);

		# ����
		print qq|Date,IP,|, join(',', @item), $br{$in{br}};

		# CSV
		foreach (1 .. $i) {
			my $csv;
			foreach my $key (@item) {
				$csv .= qq|$csv{"$_<>$key"},|;
			}
			$csv =~ s/,$//;

			print "$head{$_}$csv$br{$in{br}}";
		}

		exit;
	}

	# ���O���𐔂���
	my $i = 0;
	open(IN,"$cf{logfile}");
	++$i while(<IN>);
	close(IN);

	# �_�E�����[�h���
	header("CSV�_�E�����[�h");
	back_button();
	print <<EOM;
<blockquote>
�E ���݂̃��O���F <b>$i</b>��<br>
�E ���s�`����I�����āA�_�E�����[�h�{�^���������Ă��������B<br>
<form action="$cf{admin_cgi}" method="post">
<input type="hidden" name="pass" value="$in{pass}">
<table class="menu">
<tr>
	<th>���s�`��</th>
	<td>
		<input type="radio" name="br" value="win">Windows�`�� �iCR+LF�j<br>
		<input type="radio" name="br" value="unix">Macintosh/UNIX�`�� �iLF�j<br>
		<input type="radio" name="br" value="mac">Macintosh���`�� �iCR�j<br>
	</td>
</tr>
</table>
<input type="submit" name="downld" value="�_�E�����[�h">
</form>
</blockquote>
</body>
</html>
EOM
	exit;
}

#-----------------------------------------------------------
#  �F��
#-----------------------------------------------------------
sub pwd_check {
	# �������
	if ($in{pass} eq "") {
		enter_form();

	# �F��
	} elsif ($in{pass} ne $cf{password}) {
		error("�F�؂ł��܂���");
	}
}

#-----------------------------------------------------------
#  �������
#-----------------------------------------------------------
sub enter_form {
	header("�������");
	print <<EOM;
<blockquote>
<form action="$cf{admin_cgi}" method="post">
<table width="380">
<tr>
	<td height="40" align="center">
		<fieldset><legend>�Ǘ��p�X���[�h����</legend><br>
		<input type="password" name="pass" size="20">
		<input type="submit" value=" �F�� "><br><br>
		</fieldset>
	</td>
</tr>
</table>
</form>
</blockquote>
<script language="javascript">
<!--
self.document.forms[0].pass.focus();
//-->
</script>
</body>
</html>
EOM
	exit;
}

#-----------------------------------------------------------
#  HTML�w�b�_
#-----------------------------------------------------------
sub header {
	my $ttl = shift;

	print <<EOM;
Content-type: text/html; charset=$cf{charset}

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
<meta http-equiv="content-type" content="text/html; charset=$cf{charset}">
<meta http-equiv="content-style-type" content="text/css">
<style type="text/css">
<!--
body,td,th { font-size:80%; font-family:Verdana,"MS PGothic","Osaka",Arial,sans-serif; }
table.head { width:100%; background:#8080c0; }
td.obi { padding:7px; color:#fff; font-weight:bold; }
table.menu { width:350px; background:#8080c0; border-collapse:collapse; margin:1em 0; }
table.menu th, table.menu td { border:1px solid #8080c0; padding:8px; white-space:nowrap; }
table.menu th { background:#c8c8e3; }
table.menu td { background:#fff;  }
.wid-300 { width:300px; }
p.red { color:#dd0000; }
-->
</style>
<title>$ttl</title>
</head>
<table class="head">
<tr>
	<td class="obi">$ttl</td>
</tr>
</table>
EOM
}

#-----------------------------------------------------------
#  �G���[����
#-----------------------------------------------------------
sub error {
	my $err = shift;

	header("ERROR");
	print <<EOM;
<blockquote>
<h3>ERROR !</h3>
<p class="red">$err<p>
<form>
<input type="button" value="�O��ʂɖ߂�" onclick="history.back()">
</form>
</blockquote>
</body>
</html>
EOM
	exit;
}

#-----------------------------------------------------------
#  ���O�A�E�g
#-----------------------------------------------------------
sub back_button {
	print <<EOM;
<div style="text-align:right;">
<form action="$cf{admin_cgi}">
<input type="submit" value="�~ LOGOUT">
</form>
</div>
EOM
}

#-----------------------------------------------------------
#  �t�H�[���f�R�[�h
#-----------------------------------------------------------
sub parse_form {
	my %in;
	foreach ( $cgi->param() ) {
		my $val = $cgi->param($_);

		$val =~ s/&/&amp;/g;
		$val =~ s/</&lt;/g;
		$val =~ s/>/&gt;/g;
		$val =~ s/"/&quot;/g;
		$val =~ s/'/&#39;/g;
		$val =~ s/[\r\n]/\t/g;

		$in{$_} = $val;
	}
	return %in;
}

