const avatarUpload = document.querySelector('#avatar-upload');
const avatarPreview = document.querySelector('#avatar-preview');
const avatarUpdate = document.querySelector('#avatar_update');
const avatarUpdatePreview = document.querySelector('#avatar-update-preview');
var addBook = document.getElementById('add_book');
var showAddBook = document.getElementById('btn_add');
var closeAddBook = document.getElementById('close_add')
var updateBook = document.getElementById('update_book');
var showUpdateBook = document.querySelectorAll('.js_update_book');
var closeUpdateBook = document.querySelectorAll('.js_close_update');


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


function showAdd () {
  if (addBook.style.display == 'block') {
    addBook.style.display = 'none'
  } else {
    addBook.style.display = 'block'
  }
}
showAddBook.addEventListener('click', showAdd)
closeAddBook.addEventListener('click', showAdd)


function showUpdate() {
  if (updateBook.style.display == 'block') {
      updateBook.style.display = 'none'
  } else {
      updateBook.style.display = 'block'
  }
}

for (var i = 0; i < showUpdateBook.length; i++){
  showUpdateBook[i].addEventListener('click', showUpdate)
}

for (var i = 0; i < closeUpdateBook.length; i++){
  closeUpdateBook[i].addEventListener('click', showUpdate)
}


function onUpdateBook(book_string) {
  book_string = book_string.replaceAll("'", "").replaceAll('(', '').replaceAll(')', '').replaceAll("Decimal", "").trim();
  var book = book_string.split(",");
  var u_book_id = document.getElementById("u_book_id");
  var u_title = document.getElementById("u_title");
  var u_author = document.getElementById("u_author");
  var u_genre = document.getElementById("u_genre");
  var u_year = document.getElementById("u_year");
  var u_price = document.getElementById("u_price");
  var avatar_update = document.getElementById("avatar_update");

  u_book_id.value = book[0].trim();
  u_title.value = book[1].trim();
  u_author.value = book[2].trim();
  u_genre.value = book[3].trim();
  u_year.value = book[4].trim();
  u_price.value = book[5].trim();
  avatar_update = book[6].trim();
  
}

// ---------Author----------


