var total=0;
var contprod=0;
var cant = 0;

function addToCart(event) {
    event.preventDefault();
    
    // Obtener los detalles del producto
    var card = event.target.closest('.card');
    var title = card.querySelector('.card-text').textContent;
    var price = card.querySelector('.andes-money-amount__fraction').textContent;

   //var id = event.target.dataset.id;
   
   contprod++;
   var id = contprod;
   // Crear un elemento para mostrar los detalles del producto en el carrito

  var product = document.createElement('div');
  product.classList.add('product-item');
  product.innerHTML = `
    <h3>${title} - $${Math.floor(parseFloat(price))}</h3>
    <button class="btn btn-sm btn-outline-secondary remove-from-cart" data-id="${id}">Eliminar</button>
  `;

  // Obtener el valor actual del contador del localStorage
  var contador = localStorage.getItem('contador');
  
  // Verificar si el contador existe
  if (contador) {
    // Si el contador existe, incrementar su valor
    contador = parseInt(contador) + 1;
  } else {
    // Si el contador no existe, establecerlo en 1
    contador = 1;
  }

  // Guardar el nuevo valor del contador en el localStorage
  localStorage.setItem('contador', contador);

  // Agregar el nuevo elemento al localStorage con una clave única
  var nuevoElemento = title;
  localStorage.setItem( contador , nuevoElemento +' - '+Math.floor(parseFloat(price)) );
  
   // Agregar el producto al carrito
   var carrito = document.getElementById('carrito');
   carrito.appendChild(product);

   total += parseFloat(price);
   var totalCarrito = document.getElementById('total-carrito');
   totalCarrito.textContent = 'Total: $' + parseFloat(total).toFixed(0);
   
   // Actualizar el contador de productos
   var contador = document.getElementById('contador-productos');
   contador.textContent = parseInt(contador.textContent) + 1;
   
   // Asignar el evento click al botón de eliminación
   var removeButtons = document.getElementsByClassName('remove-from-cart');
   for (var i = 0; i < removeButtons.length; i++) {
     removeButtons[i].addEventListener('click', removeFromCart);
   }
   
   cant++
   console.log("cont suma"+cant);

  }
  
  // Función para eliminar un producto del carrito
  function removeFromCart(event) {
    event.preventDefault();
    
    var id = event.target.dataset.id;
    console.log(id)
    
    // Eliminar el producto del carrito
    var product = event.target.closest('.product-item');
    var price = product.querySelector('h3').textContent.split('$')[1];
    product.remove();
    
    //xd

    var contador = localStorage.getItem('contador');
    //console.log(contador)
    if (contador) {
      localStorage.removeItem(id);
    }

    //xd

    // Actualizar el contador de productos
    var contador = document.getElementById('contador-productos');
    contador.textContent = parseInt(contador.textContent) - 1;

    total -= parseFloat(price);
    var totalCarrito = document.getElementById('total-carrito');
    totalCarrito.textContent = 'Total: $' + parseFloat(total).toFixed(0);

    if(total === 0){
    totalCarrito.textContent = 'Carrito Vacío'}
    
    cant--
    console.log('cont resta'+cant);
  }
  
  // Obtener todos los enlaces "Añadir a carrito"
  var addToCartLinks = document.getElementsByClassName('add-to-cart');
  // Asignar el evento click a cada enlace
  for (var i = 0; i < addToCartLinks.length; i++) {
    addToCartLinks[i].addEventListener('click', addToCart);
  }


function CantLocalStorage(){
  localStorage.setItem("cantidad",cant)
  localStorage.setItem("total",total)
}

