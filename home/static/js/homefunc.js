// static/js/like.js

// Función para obtener el valor del token CSRF de las cookies
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

// Obtener el token CSRF
const csrftoken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded', function() {
  // Seleccionar todos los botones de like
  const likeButtons = document.querySelectorAll('.like-button');

  // Agregar un manejador de eventos a cada botón de like
  likeButtons.forEach(function(button) {
    button.addEventListener('click', function() {
      console.log('El botón de like ha sido presionado.');

      var artworkId = this.getAttribute('data-artwork-id');

      fetch(`/artworks/${artworkId}/like/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrftoken,
          'Content-Type': 'application/json',
        }
      })
      .then(response => response.json())
      .then(data => {
        console.log(data);  // Verificar los datos devueltos por el servidor
        if (data.error) {
          console.error('Error:', data.error);
        } else {
          document.getElementById(`like-button-${artworkId}`).innerText = data.likes;  // Actualizar solo el número de likes
        }
      })
      .catch(error => console.error('Error:', error));
    });
  });
});
