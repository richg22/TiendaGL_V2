document.addEventListener('DOMContentLoaded', function() {
    get_cart_data();
  });
  
  function get_cart_data() {
    var nroprod = document.getElementById('nroprod');
    var cantidad = localStorage.getItem('cantidad');

    nroprod.textContent = cantidad;

    var totalp = document.getElementById('total');
    var total = localStorage.getItem('total');
    console.log(total);
    
    totalp.textContent = 'Total (CLP) - $'+total;

    document.getElementById('cantidad_productos').value = cantidad;
    document.getElementById('totalv').setAttribute('value', total);


    var prod_det_boleta = [];

    for (var i = 1; i <= cantidad; i++) {
        var value = localStorage.getItem(i);
      
        prod_det_boleta.push(value); 
        
        var listItem = document.createElement('p');
        listItem.textContent = value;
      
        var productosContainer = document.getElementById('productos');
        productosContainer.appendChild(listItem);
      
        console.log('Clave:', i);
        console.log('Valor:', value);
      }
      
      document.getElementById('productos_list').value = JSON.stringify(prod_det_boleta);
  }
  