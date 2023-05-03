const avatarUpload = document.querySelector('#avatar-upload');
const avatarPreview = document.querySelector('#avatar-preview');
const avatarUpdate = document.querySelector('#avatar_update');
const avatarUpdatePreview = document.querySelector('#avatar-update-preview');
var product = document.getElementById('product');
var btn_add = document.getElementById('btn_add')
var btn_close = document.getElementById('btn_close')
var product_update = document.getElementById('product_update');
var btn_update = document.querySelectorAll('.js_show_product');
var btn_update_close = document.querySelectorAll('.js_update_close');
var btn_show_products = document.getElementById('btn_show_products');
var btn_show_users = document.getElementById('btn_show_users');

avatarUpload.addEventListener('change', function() {
  const reader = new FileReader();

  reader.addEventListener('load', function(){
    avatarPreview.setAttribute('src', reader.result);
  });

  reader.readAsDataURL(this.files[0]);
});


    
avatarUpdate.addEventListener('change', function() {
  const reader = new FileReader();

  reader.addEventListener('load', function(){
    avatarUpdatePreview.setAttribute('src', reader.result);
  });

  reader.readAsDataURL(this.files[0]);
});


function showListProducts() {
  if (product_content.style.display == 'block') {
    product_content.style.display = 'none'
  } else {
    product_content.style.display = 'block'
  }
}

btn_show_products.addEventListener('click', showListProducts)
btn_show_users.addEventListener('click',showListProducts)




function showProduct(){
  if( product.style.display == 'block'){
    product.style.display = 'none'
  }else{
    product.style.display = 'block'
  }
}

btn_close.addEventListener('click', showProduct);
btn_add.addEventListener('click', showProduct)

function showUpdateProduct(){
  if ( product_update.style.display == 'block'){
    product_update.style.display = 'none'
  } else {
    product_update.style.display = 'block'
  }
}



for (var i = 0; i < btn_update.length; i++) {
  btn_update[i].addEventListener('click', showUpdateProduct);
}
for (var i = 0; i < btn_update_close.length; i++) {
  btn_update_close[i].addEventListener('click', showUpdateProduct);
}




function onUpdateProduct(product_string) {
  product_string = product_string.replaceAll("'", "").replaceAll('(', '').replaceAll(')', '').trim();
  var product = product_string.split(',')
  var avatar_upload = document.getElementById('avatar_upload');
  var u_id = document.getElementById('u_id');
  var u_name = document.getElementById('u_name');
  var u_description = document.getElementById('u_description');
  var u_price = document.getElementById('u_price');
  var u_quantity = document.getElementById('u_quantity');

  u_id.value = product[0].trim();
  u_name.value = product[1].trim();
  u_description.value = product[2].trim();
  u_price.value = product[3].trim();
  u_quantity.value = product[5].trim();
}