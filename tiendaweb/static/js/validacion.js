function validarNombre(Nombre,Nombrelabel) {
    
    if ( Nombre.length >=15) {
        alert("Error: El nombre " + Nombre + "es demasiado largo.");
        document.getElementById("Nombrelabel").style.color = "black";
        document.getElementById("Nombrelabel").innerHTML="Nombre"
    } else {
        document.getElementById("Nombrelabel").style.color = "green";
        document.getElementById("Nombrelabel").innerHTML="Nombre Valido"
        
    }
    
}


function validarCorreo(Correo,Correolabel) {

    expr = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    if ( !expr.test(Correo) ) {
        alert("Error: La dirección de correo " + Correo + "es incorrecta.");
        document.getElementById("Correolabel").style.color = "black";
        document.getElementById("Correolabel").innerHTML="Email"
    } else {
        document.getElementById("Correolabel").style.color = "green";
        document.getElementById("Correolabel").innerHTML="Email Valido"
        
    }

}

function validarContraseña(Contraseña1,Contraseña1label,Contraseña2,Contraseña2label) {
    var Contraseña1label = document.getElementById("Contraseña1label").value;
    var Contraseña2label = document.getElementById("Contraseña2label").value;

    if ( Contraseña1.length < 8 ) {
        alert("Error: La contraseña es muy corta");
    }
    
    /*if(Contraseña1 != "" && Contraseña2 != ""){      
       alert("Error: Las contraseñas no coinciden");
    }*/
    
    if(Contraseña1 != Contraseña2){
        alert("Error: Las contraseñas no coinciden");
        document.getElementById("Contraseña1label").style.color = "black";
        document.getElementById("Contraseña1label").innerHTML="Contraseña"
        document.getElementById("Contraseña2label").style.color = "black";
        document.getElementById("Contraseña2label").innerHTML="Confirmar Contraseña"
    }else{
        document.getElementById("Contraseña1label").style.color = "green";
        document.getElementById("Contraseña1label").innerHTML="Contraseña Valida"
        document.getElementById("Contraseña2label").style.color = "green";
        document.getElementById("Contraseña2label").innerHTML="Contraseña Valida"
    }

}
/*function validarCheckbox(Check) {
    if(Check){
        document.getElementById("Checklabel").innerHTML = Check
        alert("Debe aceptar los terminos y condiciones")
    } else {
        caja = true
    }
    
  }*/


/*function evento(){
    if ( Nombre.length >=15 ) {
        document.getElementById("Nombrelabel").style.color = "green";
        document.getElementById("Nombrelabel").innerHTML="Nombre Valido"
    } else {
    document.getElementById("Nombrelabel").style.color = "green";
        document.getElementById("Nombrelabel").innerHTML="Nombre Valido"    
        
    }

}*/
