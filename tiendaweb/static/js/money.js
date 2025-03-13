$(function(){

	$("#btn-dolar").click(function() {

		$.get('https://openexchangerates.org/api/latest.json', {app_id: '002dee0d0c5a40ed9a0f1423fc812714', base: 'USD'}, function(data) {
			console.log("1 USD equals " + data.rates.CLP + " PESOSXDS");
			$("#dolar").text("A $"+data.rates.CLP+" EL DÓLAR PAPITO")
		});
		
	});

})

$(document).ready(function() {

		$.get('https://openexchangerates.org/api/latest.json', {app_id: '002dee0d0c5a40ed9a0f1423fc812714', base: 'USD'}, function(data) {
			console.log("1 USD equals " + data.rates.CLP + " PESOSXDS");
			$("#dolar").text("A $"+data.rates.CLP+" EL DÓLAR PAPITO")
		});
		
		let fecha = new Date(),
		formateada = fecha.toLocaleDateString('es-ES', {
		  year: 'numeric',
		  month: 'numeric',
		  day: 'numeric'
		});
		console.log(formateada);
		$("#fecha_ac").text("( "+ formateada +" )")


	});

