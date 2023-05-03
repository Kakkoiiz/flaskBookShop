const avatarUpload = document.querySelector('#avatar-upload');
const avatarPreview = document.querySelector('#avatar-preview');
var addBook = document.getElementById('addBook')
var showAddBook = document.getElementById('btn_add');
var closeAddBook = document.getElementById('close_add')

function showAdd () {
    if (addBook.style.display == 'block') {
      addBook.style.display = 'none'
    } else {
      addBook.style.display = 'block'
    }
}

showAddBook.addEventListener('click', showAdd)
closeAddBook.addEventListener('click', showAdd)

avatarUpload.addEventListener('change', function() {
    const reader = new FileReader();
  
    reader.addEventListener('load', function(){
      avatarPreview.setAttribute('src', reader.result);
    });
  
    reader.readAsDataURL(this.files[0]);
  });
  
  