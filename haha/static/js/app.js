const avatarUpload = document.querySelector('#avatar-upload');
const avatarPreview = document.querySelector('#avatar-preview');
var product = document.getElementById('product');
var btn_add = document.getElementById('btn_add')
var btn_close = document.getElementById('btn_close')


avatarUpload.addEventListener('change', function() {
  const file = this.files[0];
  if (file) {
    const reader = new FileReader();
    reader.addEventListener('load', function() {
      avatarPreview.setAttribute('src', this.result);
    });
    reader.readAsDataURL(file);
  }
});



function showProduct(){
  if( product.style.display == 'none'){
    product.style.display = 'block'
  }else{
    product.style.display = 'none'
  }
}

btn_close.addEventListener('click', showProduct);

btn_add.addEventListener('click', showProduct)