#!/usr/bin/perl



# �t���p�X
eval{ $path1 = `pwd`; };
if ($@ || !$path1) { $path1 = 'error'; }

print "Content-type: text/html\n\n";
print <<"EOM";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
<title>$ver</title></head>
<body bgcolor="#FFFFFF" text="#000000">
<h3>���́u�f�B���N�g���v�̃t���p�X�͈ȉ��̂Ƃ���ł��B</h3>

<P>
<DL>
<DT>�T�[�o�[���t���p�X
<DD><font color="#0000A0" size="+1"><tt>$path1</tt></font><br><br>

</div>
</body>
</html>
EOM

exit;






