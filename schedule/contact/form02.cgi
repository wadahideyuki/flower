#!/usr/local/bin/perl

#��������������������������������������������������������������������
#�� POST-MAIL v4.31 (2010/06/27)
#�� copyright (c) KentWeb
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#��������������������������������������������������������������������
$ver = 'postmail v4.31';
#��������������������������������������������������������������������
#�� [���ӎ���]
#�� 1. ���̃X�N���v�g�̓t���[�\�t�g�ł��B���̃X�N���v�g���g�p����
#��    �����Ȃ鑹�Q�ɑ΂��č�҂͈�؂̐ӔC�𕉂��܂���B
#�� 2. ���M�t�H�[����HTML�y�[�W�̍쐬�Ɋւ��ẮAHTML���@�̔��e
#��    �ƂȂ邽�߁A�T�|�[�g�ΏۊO�ƂȂ�܂��B
#�� 3. �ݒu�Ɋւ��鎿��̓T�|�[�g�f���ɂ��肢�������܂��B
#��    ���ڃ��[���ɂ�鎿��͂��󂯂������Ă���܂���B
#��������������������������������������������������������������������
#
# [ ���M�t�H�[�� (HTML) �̋L�q�� ]
#
# �E�^�O�̋L�q�� (1)
#   ���Ȃ܂� <input type="text" name="name">
#   �� ���̃t�H�[���Ɂu�R�c���Y�v�Ɠ��͂��đ��M����ƁA
#      �uname = �R�c���Y�v�Ƃ����`���Ŏ�M���܂�
#
# �E�^�O�̋L�q�� (2)
#   ���D���ȐF <input type="radio" name="color" value="��">
#   �� ���̃��W�I�{�b�N�X�Ƀ`�F�b�N���đ��M����ƁA
#      �ucolor = �v�Ƃ����`���Ŏ�M���܂�
#
# �E�^�O�̋L�q�� (3)
#   E-mail <input type="text" name="email">
#   �� name�l�Ɂuemail�v�Ƃ����������g���Ƃ���̓��[���A�h���X
#      �ƔF�����A�A�h���X�̏������ȈՃ`�F�b�N���܂�
#   �� (��) abc@xxx.co.jp
#   �� (�~) abc.xxx.co.jp �� ���̓G���[�ƂȂ�܂�
#
# �E�^�O�̋L�q�� (4)
#   E-mail <input type="text" name="_email">
#   �� name�l�̐擪�Ɂu�A���_�[�o�[ �v��t����ƁA���̓��͒l��
#     �u���͕K�{�v�ƂȂ�܂��B
#      ��L�̗�ł́A�u���[���A�h���X�͓��͕K�{�v�ƂȂ�܂��B
#
# �Ename�l�ւ́u�S�p�����v�̎g�p�͉\�ł�
#  (��) <input type="radio" name="�N��" value="20�Α�">
#  �� ��L�̃��W�I�{�b�N�X�Ƀ`�F�b�N�����đ��M����ƁA
#     �u�N�� = 20�Α�v�Ƃ��������Ŏ󂯎�邱�Ƃ��ł��܂��B
#
# �Emimew.pl�g�p���Aname�l���uname�v�Ƃ���Ƃ�����u���M�Җ��v�ƔF��
#   ���đ��M���̃��[���A�h���X���u���M�� <���[���A�h���X>�v�Ƃ���
#   �t�H�[�}�b�g�Ɏ����ϊ����܂��B
#  (�t�H�[���L�q��)  <input type="text" name="name">
#  (���M���A�h���X)  ���Y <taro@email.xx.jp>
#
# �E�R�}���h�^�O (1)
#   �� ���͕K�{���ڂ������w�肷��i���p�X�y�[�X�ŕ����w��j
#   �� ���W�I�{�^���A�`�F�b�N�{�b�N�X�΍�
#   �� name�l���uneed�v�Avalue�l���u�K�{����1 + ���p�X�y�[�X +�K�{����2 + ���p�X�y�[�X ...�v
#   (��) <input type="hidden" name="need" value="���O ���[���A�h���X ����">
#
# �E�R�}���h�^�O (2)
#   �� 2�̓��͓��e�����ꂩ���`�F�b�N����
#   �� name�l���umatch�v�Avalue�l���u����1 + ���p�X�y�[�X + ����2�v
#   (��) <input type="hidden" name="match" value="email email2">
#
# �E�R�}���h�^�O (3)
#   �� ���[���������w�肷��
#   �� ���̏ꍇ�A�ݒ�Ŏw�肷�� $subject ���D�悳��܂��B
#   (��) <input type="hidden" name="subject" value="���[���^�C�g������">
#
#  [ �ȈՃ`�F�b�N ]
#   http://�`�`/postmail.cgi?mode=check
#
#  [ �ݒu�� ]
#
#  public_html / index.html (�g�b�v�y�[�W���j
#       |
#       +-- postmail / postmail.cgi  [705]
#             |        postmail.html
#             |
#             +-- lib / jcode.pl     [604]
#             |         mimew.pl     [604] ... �C��
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
#  ����{�ݒ�
#-------------------------------------------------

# �����R�[�h�ϊ����C�u�����y�T�[�o�p�X�z
require './lib/jcode.pl';

# MIME�G���R�[�h���C�u�������g���ꍇ�i�����j�y�T�[�o�p�X�z
#  �� ���[���w�b�_�̑S�p������BASE64�ϊ�����@�\
#  �� mimew.pl���w��
$mimew = './lib/mimew.pl';

# ���M�惁�[���A�h���X
$mailto = 'info@st-george.co.jp,terasaka@st-george.co.jp,kusaka@st-george.co.jp';

# ���̓t�B�[���h������̍ő�e�ʁi�o�C�g�j
# ���Q�l : �S�p1���� = 2�o�C�g
$max_field = 500;

# ���M�O�m�F
# 0 : no
# 1 : yes
$preview = 1;

# ���[���^�C�g��
$subject = '���Z���g�E�W���[�W���� ���₢���킹';

# �{�̃v���O�����yURL�p�X�z
$script = './form02.cgi';

# ���O�t�@�C���y�T�[�o�p�X�z
$logfile = './data/log.cgi';

# �m�F��ʃe���v���[�g�y�T�[�o�p�X�z
$tmp_conf = './tmpl02/conf.html';

# ��ʃG���[��ʃe���v���[�g�y�T�[�o�p�X�z
$tmp_err1 = './tmpl02/err1.html';

# ���̓G���[��ʃe���v���[�g�y�T�[�o�p�X�z
$tmp_err2 = './tmpl02/err2.html';

# ���M���ʃe���v���[�g�y�T�[�o�p�X�z
$tmp_thx = './tmpl02/thx.html';

# ���M�u�{���v�e���v���[�g�y�T�[�o�p�X�z
$tmp_body = './tmpl02/body.txt';

# ���M�u�{���v�e���v���[�g�y�T�[�o�p�X�z
$tmp_body2 = './tmpl02/body2.txt';

# ���[���̑��M�Җ�
$master_name = '���Z���g�E�W���[�W����';

# ���M��̌`��
# 0 : �������b�Z�[�W���o��.
# 1 : �߂�� ($back) �֎����W�����v������.
$reload = 0;

# ���M��̖߂��yURL�p�X�z
#  �� http://����L�q����
$back = 'http://www.st-george.co.jp';

# ����IP�A�h���X����̘A�����M����
# �� ������Ԋu��b���Ŏw��i0�ɂ���Ƃ��̋@�\�͖����j
$block_post = 60;

# ���M�� method=POST ���� (0=no 1=yes)
#  �� �Z�L�����e�B�΍�
$postonly = 1;

# �A���[���F
$alm_col = "#dd0000";

# �z�X�g�擾���@
# 0 : gethostbyaddr�֐����g��Ȃ�
# 1 : gethostbyaddr�֐����g��
$gethostbyaddr = 0;

# �A�N�Z�X�����i��������Δ��p�X�y�[�X�ŋ�؂�A�A�X�^���X�N�j
# �� ���ۃz�X�g������IP�A�h���X�̋L�q��
#   �i�O����v�͐擪�� ^ ������j�y��z^210.12.345.*
#   �i�����v�͖����� $ ������j�y��z*.anonymizer.com$
$denyhost = '';

# �֎~���[�h
# �� ���e���֎~���郏�[�h���R���}�ŋ�؂�
$no_wd = '';

# ���M���֍T�� (CC) �𑗂�
# 0=no 1=yes
# ���Z�L�����e�B�ケ�̋@�\�͐������܂���.
# ��name="email" �̃t�B�[���h�ւ̓��͂��K�{�ƂȂ�܂�.
$cc_mail = 0;

# ���[�����M�`��
# 1 : sendmail���M�isendmail�����p�\�ȃT�[�o�j
# 2 : IO:Socket���W���[�����M�i�\�P�b�g�֘A�̃��W���[�������p�\�ȃT�[�o�j
$send_type = 1;

## sendmail���M�̂Ƃ� ##
# sendmail�̃p�X
$sendmail = '/usr/lib/sendmail';

##�y���zsendmail���M�̕��͐ݒ�͂����܂łŏI���B�����艺�͐ݒ�s�v�ł��B

## IO:Socket���W���[�����M�̂Ƃ� ##
# io-socket.pl�̃p�X
$io_socket = './lib/io-socket.pl';

# SMTP�T�[�o
$server = "mail.server.xx.jp";

# SMTP�|�[�g�ԍ��i�ʏ��25�j
$port = 25;

# POP before SMTP���g�p����
# 0 : no
# 1 : yes
$pop_bef_smtp = 0;

# POP3�T�[�o�yPOP before SMTP�̂Ƃ��z
$pop3sv = 'mail.server.xx.jp';

# POP3�|�[�g�ԍ��i�ʏ��110�j�yPOP before SMTP�̂Ƃ��z
$pop3port = 110;

# �ڑ�ID�yPOP before SMTP�̂Ƃ��z
$user = 'user_id';

# �ڑ��p�X���[�h�yPOP before SMTP�̂Ƃ��z
$pass = 'password';

## ��SMTP�T�[�o�ւ̐ڑ���񂱂��܂�

#-------------------------------------------------
#  ���ݒ芮��
#-------------------------------------------------

# �t�H�[���f�R�[�h
$ret = &decode;

# ��{����
if (!$ret) { &error("�s���ȏ����ł�"); }
elsif ($in{'mode'} eq "check") { &check; }

# POST�`�F�b�N
if ($postonly && !$postflag) { &error("�s���ȃA�N�Z�X�ł�"); }

# �����`�F�b�N
if ($in{'subject'} =~ /\r|\n/) { &error("���[���������s���ł�"); }
$in{'subject'} =~ s/\@/��/g;
$in{'subject'} =~ s/\./�D/g;
$in{'subject'} =~ s/\+/�{/g;
$in{'subject'} =~ s/\-/�|/g;
$in{'subject'} =~ s/\:/�F/g;
$in{'subject'} =~ s/\;/�G/g;
$in{'subject'} =~ s/\|/�b/g;

# ���쌠�\�L�i�폜�s�j
$copy = <<EOM;
EOM

# �֎~���[�h
if ($no_wd) {
	local($flg);
	foreach (@key) {
		foreach $nowd ( split(/,/, $no_wd) ) {
			if (index($in{$_},$nowd) >= 0) {
				$flg = 1; last;
			}
		}
		if ($flg) { &error("�֎~���[�h���܂܂�Ă��܂�"); }
	}
}

# �z�X�g�擾���`�F�b�N
&get_host;

# �K�{���̓`�F�b�N
if ($in{'need'}) {
	local(@tmp, @uniq, %seen);

	# need�t�B�[���h�̒l��K�{�z��ɉ�����
	@tmp = split(/\s+/, $in{'need'});
	push(@need,@tmp);

	# �K�{�z��̏d���v�f��r������
	foreach (@need) {
		push(@uniq,$_) unless $seen{$_}++;
	}

	# �K�{���ڂ̓��͒l���`�F�b�N����
	foreach (@uniq) {

		# �t�B�[���h�̒l���������Ă��Ȃ����́i���W�I�{�^�����j
		if (!defined($in{$_})) {
			$check++;
			push(@key,$_);
			push(@err,$_);

		# ���͂Ȃ��̏ꍇ
		} elsif ($in{$_} eq "") {
			$check++;
			push(@err,$_);
		}
	}
}

# ���͓��e�}�b�`
if ($in{'match'}) {
	($match1,$match2) = split(/\s+/, $in{'match'}, 2);

	if ($in{$match1} ne $in{$match2}) {
		&error("$match1��$match2�̍ē��͓��e���قȂ�܂�");
	}
}

# ���̓`�F�b�N�m�F���
if ($check || $max_flg) { &err_check; }

# E-Mail�����`�F�b�N
if ($in{'email'} =~ /\,/) {
	&error("���[���A�h���X�ɃR���} ( , ) ���܂܂�Ă��܂�");
}
if ($in{'email'} && $in{'email'} !~ /^[\w\.\-]+\@[\w\.\-]+\.[a-zA-Z]{2,6}$/) {
	&error("���[���A�h���X�̏������s���ł�");
}

# �v���r���[
if ($preview && $in{'mode'} ne "send") {

	# �A�����M�`�F�b�N
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

# �A�����M�`�F�b�N
&check_post('send');

# ���Ԏ擾
($date1, $date2) = &get_time;

# �R�}���h�^�O�Ō����w�肠��
if ($in{'subject'}) {
	$in{'subject'} =~ s/\|/�b/g;
	$in{'subject'} =~ s/;/�G/g;
	$subject = $in{'subject'};
}

# �u���E�U���
$agent = $ENV{'HTTP_USER_AGENT'};
$agent =~ s/<//g;
$agent =~ s/>//g;
$agent =~ s/"//g;
$agent =~ s/&//g;
$agent =~ s/'//g;

local($bef, $mbody, $email, $subject2, $tbody);

# �{���e���v���ǂݍ���
open(IN,"$tmp_body");
while (<IN>) {
	s/\r\n/\n/;

	$tbody .= $_;
}
close(IN);

# �ԐM�p�e���v���ǂݍ���
open(IN,"$tmp_body2");
while (<IN>) {
s/\r\n/\n/;

$tbody2 .= $_;
}
close(IN);

# �e���v���ϐ��ϊ�
$tbody =~ s/\$date/$date1/;
$tbody2 =~ s/\$date/$date1/; 
$tbody =~ s/\$agent/$agent/;
$tbody =~ s/\$host/$host/;
&jcode::convert(\$tbody, 'jis');
&jcode'convert(*tbody2, 'jis'); 

# �{���̃L�[��W�J
foreach (@key) {
	# �{���Ɋ܂߂Ȃ�������r��
	next if ($_ eq "mode");
	next if ($_ eq "need");
	next if ($_ eq "match");
	next if ($_ eq "subject");
	next if ($in{'match'} && $_ eq $match2);
	next if ($bef eq $_);

	# �G�X�P�[�v
	$in{$_} =~ s/\0/ /g;
	$in{$_} =~ s/��br��/\n/g;
	$in{$_} =~ s/\.\n/\. \n/g;

	# �Y�t�t�@�C������
	$in{$_} =~ s/Content-Disposition:\s*attachment;.*//ig;
	$in{$_} =~ s/Content-Transfer-Encoding:.*//ig;
	$in{$_} =~ s/Content-Type:\s*multipart\/mixed;\s*boundary=.*//ig;

	# �{�����e
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

# �{���e���v�����̕ϐ���u������
$tbody =~ s/\$message/$mbody/;
$tbody2 =~ s/\$message/$mbody/;

# ���[���A�h���X���Ȃ��ꍇ�͑��M��ɒu������
if ($in{'email'} eq "") { $email = $mailto; }
else { $email = $in{'email'}; }

# MIME�G���R�[�h

if (-e $mimew) {
require $mimew;
$subject2 = &mimeencode($subject);
$from = &mimeencode("\"$master_name\" <$mailto>");
} else {
$subject2 = &base64($subject);
$from = &base64("\"$master_name\"") . " <$mailto>";
}


# ���M���e�t�H�[�}�b�g��
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


# IO:Socket���W���[�����M
if ($send_type == 2) {
	require $io_socket;
	&sendmail($email, $mailto, $body);

# sendmail���M
} else {
	open(MAIL,"| $sendmail -t -i") || &error("���[�����M���s");
	print MAIL "$body\n";
	close(MAIL);
}

open(MAIL,"| $sendmail -t -i") || &error("���[�����M���s");
print MAIL "$body2\n";
close(MAIL);


####### ���q�l�T���p

# �����[�h
if ($reload) {
	if ($ENV{'PERLXS'} eq "PerlIS") {
		print "HTTP/1.0 302 Temporary Redirection\r\n";
		print "Content-type: text/html\n";
	}
	print "Location: $back\n\n";
	exit;

# �������b�Z�[�W
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
#  ���̓`�F�b�N
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
					$tmp =~ s|\$right|<span style="color:$alm_col">$key�͓��͕K�{�ł�</span>|;
				} elsif (defined($err{$key})) {
					$tmp =~ s|\$right|<span style="color:$alm_col">$key�̓��͓��e���傫�����܂�</span>|;
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
#  �t�H�[���f�R�[�h
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

		# �R�[�h�ϊ�
		&jcode::convert(\$key, 'sjis');
		&jcode::convert(\$val, 'sjis');

		# �G�X�P�[�v
		$key =~ s/&/��/g;
		$key =~ s/"/�h/g;
		$key =~ s/</��/g;
		$key =~ s/>/��/g;
		$key =~ s/'/�f/g;
		$val =~ s/&/��/g;
		$val =~ s/"/�h/g;
		$val =~ s/</��/g;
		$val =~ s/>/��/g;
		$val =~ s/'/�f/g;

		if (length($key) > $max_field || length($val) > $max_field) {
			$max_flg = 1;
			$err{$key} = $val;
		}

		# �K�{���͍���
		if ($key =~ /^_(.+)/) {
			$key = $1;
			push(@need,$key);

			if ($val eq "") { $check++; push(@err,$key); }
		}

		$in{$key} .= "\0" if (defined($in{$key}));
		$in{$key} .= $val;

		push(@key,$key);
	}

	# �Ԃ�l
	if ($buf) { return 1; } else { return 0; }
}

#-------------------------------------------------
#  �G���[����
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
#  ���Ԏ擾
#-------------------------------------------------
sub get_time {
	$ENV{'TZ'} = "JST-9";
	my ($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime(time);
	my @w = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');
	my @m = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');

	# �����̃t�H�[�}�b�g
	my $date1 = sprintf("%04d/%02d/%02d(%s) %02d:%02d",
			$year+1900,$mon+1,$mday,$w[$wday],$hour,$min);
	my $date2 = sprintf("%s, %02d %s %04d %02d:%02d:%02d",
			$w[$wday],$mday,$m[$mon],$year+1900,$hour,$min,$sec) . " +0900";

	return ($date1, $date2);
}

#-------------------------------------------------
#  �z�X�g���擾
#-------------------------------------------------
sub get_host {
	# �z�X�g���擾
	$host = $ENV{'REMOTE_HOST'};
	$addr = $ENV{'REMOTE_ADDR'};

	if ($gethostbyaddr && ($host eq "" || $host eq $addr)) {
		$host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2);
	}
	if ($host eq "") { $host = $addr; }

	# �`�F�b�N
	if ($denyhost) {
		my $flg;
		foreach ( split(/\s+/, $denyhost) ) {
			s/\./\\\./g;
			s/\*/\.\*/g;

			if ($host =~ /$_/i) { $flg = 1; last; }
		}
		if ($flg) { &error("�A�N�Z�X��������Ă��܂���"); }
	}
}

#-------------------------------------------------
#  ���M�`�F�b�N
#-------------------------------------------------
sub check_post {
	my $job = shift;

	# IP�y�ю��Ԏ擾
	my $addr = $ENV{'REMOTE_ADDR'};
	my $now  = time;

	# ���O�I�[�v��
	open(DAT,"+< $logfile");
	eval "flock(DAT, 2);";
	my $data = <DAT>;

	# ����
	my ($ip, $time) = split(/<>/, $data);

	# IP�y�ю��Ԃ��`�F�b�N
	if ($ip eq $addr && $now - $time <= $block_post) {
		close(DAT);
		&error("�A�����M��$block_post�b�Ԃ��҂���������");
	}

	if ($job eq "send") {
		seek(DAT, 0, 0);
		print DAT "$addr<>$now";
		truncate(DAT, tell(DAT));
	}
	close(DAT);
}

#-------------------------------------------------
#  �`�F�b�N���[�h
#-------------------------------------------------
sub check {
	print "Content-type: text/html\n\n";
	print <<EOM;
<html><head>
<meta http-equiv="content-type" content="text/html; charset=shift_jis">
<title>�`�F�b�N���[�h</title></head>
<body>
<h3>�`�F�b�N���[�h</h3>
<ul>
EOM

	# ���O�t�@�C��
	if (-e $logfile) {
		print "<li>���O�t�@�C���F�p�XOK!\n";

		if (-r $logfile && -w $logfile) {
			print "<li>���O�t�@�C���F�p�[�~�b�V����OK!\n";
		} else {
			print "<li>���O�t�@�C���F�p�[�~�b�V����NG\n";
		}

	} else {
		print "<li>���O�t�@�C���p�XNG �� $logfile\n";
	}

	# ���[���\�t�g�`�F�b�N
	print "<li>���[���\\�t�g�p�X�F";
	if (-e $sendmail) {
		print "OK\n";
	} else {
		print "NG �� $sendmail\n";
	}

	# jcode.pl �o�[�W�����`�F�b�N
	print "<li>jcode.pl�o�[�W�����`�F�b�N�F";

	if ($jcode'version < 2.13) {
		print "�o�[�W�������Ⴂ�悤�ł��B�� v$jcode::version\n";
	} else {
		print "�o�[�W����OK (v$jcode'version)\n";
	}

	# �e���v���[�g
	foreach ( $tmp_body, $tmp_conf, $tmp_err1, $tmp_err2, $tmp_thx ) {
		print "<li>�e���v���[�g ( $_ ) �F";
		if (-e $_) {
			print "�p�XOK!\n";
		} else {
			print "�p�XNG �� $_\n";
		}
	}

	print <<EOM;
<li>�o�[�W�����F$ver
</ul>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  BASE64�ϊ�
#-------------------------------------------------
#�@�Ƃقق�WWW����Ō��J����Ă��郋�[�`�����Q�l�ɂ��܂����B
#�@http://www.tohoho-web.com/
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


