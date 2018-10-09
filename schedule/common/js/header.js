// JavaScript Document

////////////////////////////////////////////////////////////////////////////////
/// 座標制御
////////////////////////////////////////////////////////////////////////////////

function setHeader(){
	var myScroll;
	var a=0;
	function loaded(){
		setHeight();
		myScroll=new iScroll('content_inner',{desktopCompatibility:true});
	}
	function setHeight(){
		var headerH=document.getElementById('header').offsetHeight;
		var wrapperH=window.innerHeight-headerH;
		document.getElementById('content').style.height=wrapperH+'px';
	}
	window.addEventListener('onorientationchange' in window?'orientationchange':'resize',setHeight,false);
	document.addEventListener('touchmove',function(e){e.preventDefault();},false);
	document.addEventListener('DOMContentLoaded',loaded,false);
}

////////////////////////////////////////////////////////////////////////////////
/// スマートフォンブラウザ判定
////////////////////////////////////////////////////////////////////////////////

var nUa=navigator.userAgent;
var uaAr=nUa.indexOf('Linux; U; Android ')!=-1;
var uaIPo=nUa.indexOf('iPod; U')!=-1;
var uaIPh=nUa.indexOf('iPhone; U')!=-1;
var uaIPa=nUa.indexOf('iPad; U')!=-1;

////////////////////////////////////////////////////////////////////////////////
/// ロード
////////////////////////////////////////////////////////////////////////////////

if(uaIPo||uaIPh||uaIPa) setFooter();



