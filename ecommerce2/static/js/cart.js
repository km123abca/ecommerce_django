console.log('cart.js in operational in this page');
let cart =JSON.parse(getCookie('cart'));
// console.log('cart:'+cart)
if(!cart)
	{
		cart={};
		console.log('new cart was created');
		document.cookie='cart='+JSON.stringify(cart)+";domain=;path=/";
		console.log(cart);
	}

var updateBtns=document.getElementsByClassName('update-cart');

for(i=0;i<updateBtns.length;i++)
	{
		updateBtns[i].addEventListener('click',
											   function()
											   	{
											   	  var productId=this.dataset.product;
											   	  var action=this.dataset.action;
											   	  console.log(`productId:${productId},action:${action}`)
											   	  if(user=='AnonymousUser')
											   	  	{
											   	  		// console.log('user is not authenticated');
											   	  		addCookieItem(productId,action);
											   	  	}
											   	  else
											   	  	{
											   	  		updateUserOrder(productId,action);
											   	  	}
											   	}
		 							  );
	}
function updateUserOrder(productId,action)
	{
		 // console.log(`productId:${productId},action:${action}`)
		// console.log('User was authenticated data was sent');
		var url='/update_item/';
		fetch(url,
				  {
				  	method:'POST',
				  	headers:{
				  			  'Content-Type':'application/json',
				  			   "X-CSRFToken":getCookie('csrftoken'),
				  			},
				  	body: JSON.stringify(
				  						  {
				  						  	"productId":productId,
				  						  	"action"   :action,
				  						  }
				  		                )
				  }
			 )
		.then(
			  response=>response.json()
			 )
		.then(
			  (data)=>
			  		  {
			  		  	console.log("data:"+data);
			  		  	location.reload();
			  		  }
			 );
	}

function getCookie(name) 
   	{
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') 
    	{
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) 
        	{
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) 
            	{
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            	}
        	}
    	}
    	return cookieValue;
	}

function getCookieCustom(name)
	{
		
		for(var cookiex of document.cookie.split(';'))
		{
			let key_val=cookiex.split('=');
			if(key_val[0].trim()==name)
				return decodeURIComponent(key_val[1].trim());
		}
		return null;
	}

function addCookieItem(productId,action)
	{
		// console.log('user is not authenticated');
		if(action=='add')
			{
				if(!cart[productId])
					{
						cart[productId]={'quantity':1};
					}
				else
					{
						cart[productId]['quantity']+=1;
					}
			}
		else if(action=='remove')
			{
				cart[productId]['quantity']-=1;
				if(cart[productId]['quantity']<=0)
				{
					delete cart[productId];
				}
			}
		document.cookie='cart='+JSON.stringify(cart)+";domain=;path=/";
		location.reload();
	}


function showImagexx(imgx){
document.getElementsByTagName("body")[0].style.backgroundImage=`url('/uploads/${imgx}')`;
document.getElementsByTagName("body")[0].style.backgroundRepeat="no-repeat";
document.getElementsByTagName("body")[0].style.backgroundSize="cover";
}