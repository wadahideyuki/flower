//�܂肽���݃��j���[�N�b�L�[
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//�Z�b�g�N�b�L�[�擾
function setCookie (ListId, theValue) {
	if ( (ListId != null) && (theValue != null) ) {
		/*
		//�Ō�ɃA�N�Z�X����������1�N�ԗL��
		var kigen = 360;
		var expDay = new Date();
		expDay.setTime ( expDay.getTime () + (kigen*60*60*24*1000) );
		expDay = expDay.toGMTString ();
		*/
		document.cookie = ListId + "=" + escape (theValue) + "; path=/;";
		return true;
	}
	return false;
}
//�N�b�L�[�擾
function getCookie (ListId) {
	ListId += "=" // =��ǉ����Č����̎����������
	var theCookie = document.cookie + ";";//�������ŏI���ڂ�-1�ɂȂ�̂�h��
	var start = theCookie.indexOf (ListId);//�w�肳�ꂽ���O����������
	if (start != -1) {
		end = theCookie.indexOf ( ";", start );
		return unescape ( theCookie.substring (start + ListId.length, end) );
	}
	return false;
}
//���j���[��\��+�\��
function ListVisible (ListId) {
	var getValue = getCookie (ListId);
	if ( getValue == "block" ) {
		setCookie (ListId,"none");
		getValue = getCookie (ListId);
		document.getElementById(ListId).style.display = getValue;
	} else if ( getValue == "none" ) {
		setCookie (ListId,"block");
		getValue = getCookie (ListId);
		document.getElementById(ListId).style.display = getValue;
	}
}
//�N�b�L�[�ۑ�����Ă��Ȃ���Ώ����l��ۑ�
function ListDefault () {
	var checkCookie = navigator.cookieEnabled;
	if (checkCookie != true) {
		alert ("���̃T�C�g�̓��j���[�\����Cookie���g�p���Ă���܂��B\n�u���E�U��Cookie�ݒ��on�ɂ��Ă��������B");
	}
	//�e�N�b�L�[���擾�����l
	var gvArray = new Array (
		"gbExhibition",
		"gbOutline",
		"gbEvaSystem",
		"gbEventEdu",
		"gbVisitors",
		"gbCommunity",
		"gbCollection",
		"gbRestaurantShop",
		"gbAccess"
	);
	var gvLength = gvArray.length;
	for (i=0; i<gvLength; i++) {
		var getValue = new Array ();
		getValue[i] = getCookie (gvArray[i]);
		if ( getValue[i] == false ) {
			setCookie (gvArray[i],"none");
			document.getElementById(gvArray[i]).style.display = "none";
		} else {
			document.getElementById(gvArray[i]).style.display = getValue[i];
		}
	}
}
function ListDefault_English () {
	var checkCookie = navigator.cookieEnabled;
	if (checkCookie != true) {
		alert ("���̃T�C�g�̓��j���[�\����Cookie���g�p���Ă���܂��B\n�u���E�U��Cookie�ݒ��on�ɂ��Ă��������B");
	}
	//�e�N�b�L�[���擾�����l
	var gvArray = new Array (
		"gbExhibition",
		"gbOutline",
		"gbVisitors",
		"gbCollection",
		"gbAccess"
	);
	var gvLength = gvArray.length;
	for (i=0; i<gvLength; i++) {
		var getValue = new Array ();
		getValue[i] = getCookie (gvArray[i]);
		if ( getValue[i] == false ) {
			setCookie (gvArray[i],"none");
			document.getElementById(gvArray[i]).style.display = "none";
		} else {
			document.getElementById(gvArray[i]).style.display = getValue[i];
		}
	}
}


function smartRollover() {
	if(document.getElementsByTagName) {
		var images = document.getElementsByTagName("img");
		for(var i=0; i < images.length; i++) {
			if(images[i].getAttribute("src").match("_of."))
			{
				images[i].onmouseover = function() {
					this.setAttribute("src", this.getAttribute("src").replace("_of.", "_on."));
				}
				images[i].onmouseout = function() {
					this.setAttribute("src", this.getAttribute("src").replace("_on.", "_of."));
				}
			}
		}
	}
}
if(window.addEventListener) {
	window.addEventListener("load", smartRollover, false);
}
else if(window.attachEvent) {
	window.attachEvent("onload", smartRollover);
}



//�I�[�v���T�u�E�B���h�E
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
function OpenWin (FN,W,H) {
	var WO;
	WO = window.open (FN,'OpenWin','location=no,menubar=no,toolbar=no,scrollbars=yes,status=no,width=' + W + ',height=' + H + ',resizable=yes');
	WO.focus();
}


//�N���[�Y�T�u�E�B���h�E
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
function CloseWin () {
	window.close();
}


//���[���I�[�o�[
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
function MM_preloadImages() { //v3.0
	var d=document; if(d.images){ if(!d.MM_p) d.MM_p=new Array();
	var i,j=d.MM_p.length,a=MM_preloadImages.arguments; for(i=0; i<a.length; i++)
	if (a[i].indexOf("#")!=0){ d.MM_p[j]=new Image; d.MM_p[j++].src=a[i];}}
}

function MM_swapImgRestore() { //v3.0
	var i,x,a=document.MM_sr; for(i=0;a&&i<a.length&&(x=a[i])&&x.oSrc;i++) x.src=x.oSrc;
}

function MM_findObj(n, d) { //v4.01
	var p,i,x;  if(!d) d=document; if((p=n.indexOf("?"))>0&&parent.frames.length) {
	d=parent.frames[n.substring(p+1)].document; n=n.substring(0,p);}
	if(!(x=d[n])&&d.all) x=d.all[n]; for (i=0;!x&&i<d.forms.length;i++) x=d.forms[i][n];
	for(i=0;!x&&d.layers&&i<d.layers.length;i++) x=MM_findObj(n,d.layers[i].document);
	if(!x && d.getElementById) x=d.getElementById(n); return x;
}

function MM_swapImage() { //v3.0
	var i,j=0,x,a=MM_swapImage.arguments; document.MM_sr=new Array; for(i=0;i<(a.length-2);i+=3)
	if ((x=MM_findObj(a[i]))!=null){document.MM_sr[j++]=x; if(!x.oSrc) x.oSrc=x.src; x.src=a[i+2];}
}



