var d = window.document;
if(navigator.userAgent.indexOf('iPhone') > -1)
	d.write('<meta name="viewport" content="width=device-width, maximum-scale=0.5; initial-scale=0.3;" />');
else if(navigator.userAgent.indexOf('iPad') > -1)
	d.write('<meta name="viewport" content="width=device-width, maximum-scale=1.0; initial-scale=0.6;"/>');
	
	
	
		
