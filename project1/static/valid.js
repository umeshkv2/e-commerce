function A(f)
{ 
	if(check_text(f.name,"Enter correct name")==false)
		{
			f.name.focus();
			return false;
		}
	else if(onlyalpha(f.name,"Only alphabets allowed")==false)
	{
			f.name.focus();
			return false;
	}
	else if(mobile_range(f.mobileno,"Incorrect mobile number")==false)
	{
		f.mobileno.focus();
		return false;
	}
	else if(check_pass(f.pass,"password must be atleast of length 8 character ")==false)
	{
		f.pass.focus();
		return false;
	}
	else if(match_pass(f.pass,f.cpass,"Password Doesn't Match")==false)
	{
		f.pass.focus();
		f.pass.value="";
		f.cpass.value="";
		return false;
	}
	
}


function B(f)
{ 
	if(check_pass(f.oldpass,"old password must be atleast of length 8 character ")==false)
	{
		f.oldpass.focus();
		return false;
	}
	if(check_pass(f.newpass,"new password must be atleast of length 8 character ")==false)
	{
		f.newpass.focus();
		return false;
	}
	else if(match_pass(f.newpass,f.cpass,"Password Doesn't Match")==false)
	{
		f.oldpass.focus();
		f.oldpass.value="";
		f.newpass.value="";
		f.cpass.value="";
		return false;
	}
	
}



function check_text(e,m)
{
	if(e.value==null||e.value=="")
		{
			alert(m);
			return false;
		}
	else
		{
			return true;
		}
}
function onlyalpha(e,m)
{
	var letter=/^[A-Z a-z]+$/ ;
	if(e.value.match(letter))
		{
			return true;
		}
	else
	{
		alert(m);
		return false;
	}
}

function mobile_range(e,m)
{
	var mx=9999999999;
	var mn=6000000000;
	if(e.value>mx||e.value<mn)
		{
			alert(m);
			return false;
		}
	else
		{
			return true;
		}
}

function check_pass(e,m)
{	
	if ( e.value.length >= 8) 
		{
			return true;
		}
	else
	{
		alert(m);
		return false;
	}
}

function match_pass(e1,e2,m)
{
	if(e1.value!=e2.value)
		{
			alert(m);
			return false;
		}
	else
	{
		return true;
	}
	
}