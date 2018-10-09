//折りたたみメニュークッキー
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//セットクッキー取得
function setCookie (ListId, theValue) {
	if ( (ListId != null) && (theValue != null) ) {
		/*
		//最後にアクセスした日から1年間有効
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
//クッキー取得
function getCookie (ListId) {
	ListId += "=" // =を追加して検索の手引きをする
	var theCookie = document.cookie + ";";//検索時最終項目で-1になるのを防ぐ
	var start = theCookie.indexOf (ListId);//指定された名前を検索する
	if (start != -1) {
		end = theCookie.indexOf ( ";", start );
		return unescape ( theCookie.substring (start + ListId.length, end) );
	}
	return false;
}
//メニュー非表示+表示
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
//クッキー保存されていなければ初期値を保存
function ListDefault () {
	var checkCookie = navigator.cookieEnabled;
	if (checkCookie != true) {
		alert ("このサイトはメニュー表示にCookieを使用しております。\nブラウザのCookie設定をonにしてください。");
	}
	//各クッキーを取得した値
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
		alert ("このサイトはメニュー表示にCookieを使用しております。\nブラウザのCookie設定をonにしてください。");
	}
	//各クッキーを取得した値
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



//オープンサブウィンドウ
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
function OpenWin (FN,W,H) {
	var WO;
	WO = window.open (FN,'OpenWin','location=no,menubar=no,toolbar=no,scrollbars=yes,status=no,width=' + W + ',height=' + H + ',resizable=yes');
	WO.focus();
}


//クローズサブウィンドウ
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
function CloseWin () {
	window.close();
}


//ロールオーバー
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



