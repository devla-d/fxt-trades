
function isEmail(str) {
	var re = new RegExp(/^[\w\.+-]*[a-zA-Z0-9+]@[a-zA-Z0-9][\w\.-]*[a-zA-Z0-9]\.[a-zA-Z][a-zA-Z\.]*[a-zA-Z]$/);
	return re.test(str);
}

function isRealPhoneNumber(str){
	var prefix = str.substring(0,3);
	if(prefix!='111'&&prefix!='222'&&prefix!='333'&&prefix!='444'&&prefix!='555'&&prefix!='666'&&prefix!='777'&&prefix!='999'){
		var myRegxp = /^([2-9]{1}[0-8]{1}[0-9]{1}[-][2-9]{1}[0-9]{1}[0-9]{1}[-][0-9]{1}[0-9]{1}[0-9]{1}[0-9]{1})$/;
		return myRegxp.test(str);
	}
	else{
		return false;
	}
}

function trim(str){
   return str.replace(/^\s*|\s*$/g,"");
}

function cleanupPhoneNumber(phoneNumber){
	var reg = new RegExp("^(1[ .-]*)?[ (]*([2-9][0-9]{2})[) .-]*([0-9]{3})[ .-]*([0-9]{4})$", "i");
	var m = reg.exec(phoneNumber);
	if (m != null) {
		return m[2]+'-'+m[3]+'-'+m[4];
	}
	return phoneNumber;
}

function encode(str){
	// simple one way encryption (checksum)
	// created: September 30, 2009
	// modified: December 14, 2009
	// author: Jamie Beck <jbeck@terabit.ca>
	
	var l = str.length;
	var i;
	var sum = 0;
	for(i = 0; i < l-1; i++){
		sum = sum + Math.pow(str.charCodeAt(i), i+1);
	}
	return sum;
}

function setCookie(c_name,value,expiredays){
	var exdate=new Date();
	exdate.setDate(exdate.getDate()+expiredays);
	document.cookie=c_name+ "=" +escape(value)+((expiredays==null) ? "" : ";expires="+exdate.toGMTString());
}

function getCookie(c_name){
	if (document.cookie.length>0){
	  c_start=document.cookie.indexOf(c_name + "=");
	  if (c_start!=-1){
		c_start=c_start + c_name.length+1;
		c_end=document.cookie.indexOf(";",c_start);
		if (c_end==-1) c_end=document.cookie.length;
			return unescape(document.cookie.substring(c_start,c_end));
		}
	  }
	return "";
}

$(function(){
	if(typeof $.fancybox != 'undefined'){

		$(".overlay").fancybox({
			maxWidth	: 800,
			maxHeight	: 450,
			fitToView	: false,
			width		: '70%',
			height		: '70%',
			autoSize	: false,
			closeClick	: false,
			openEffect	: 'none',
			closeEffect	: 'none'
		});
	}

});