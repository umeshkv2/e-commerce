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
	else if(match_pass(f.password,f.cpassword,"Password Doesn't Match")==false)
	{
		f.password.focus();
		f.password.value="";
		f.cpassword.value="";
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
