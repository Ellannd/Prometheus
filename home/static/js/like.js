
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('comment-button').addEventListener('click', function() {
    console.log("Button has been pressed (Comment Button)");
    var commentForm = document.getElementById('comment-form-container');
    commentForm.scrollIntoView({ behavior: 'smooth' });
    commentForm.querySelector('textarea').focus(); });

  document.getElementById('like-button').addEventListener('click', function() {
    console.log('El botón de like ha sido presionado.');

    var pk = this.getAttribute('data-artwork-id');

    fetch(`/artworks/${pk}/like/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        'Content-Type': 'application/json',
      }
    })
    .then(response => response.json())
    .then(data => {
      document.getElementById('like-count').innerText = data.likes;
    })
    .catch(error => console.error('Error:', error));
  });
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
