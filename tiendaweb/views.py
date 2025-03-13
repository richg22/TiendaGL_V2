from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto
from django.views.decorators.http import require_POST
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
import json
from .forms import MiFormulario
from django.contrib.auth import views as auth_views

from flask import render_template, request
from transbank.error.transbank_error import TransbankError
from transbank.webpay.webpay_plus.transaction import Transaction
import random
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import datetime as dt
from django.contrib.auth import authenticate, login, logout
#IP de los formularios
from .forms import ClienteCreationForm , LoginForm


#from webpay_plus import bp


# Create your views here.

def home(request):
    return render(request, 'index.html')

def productos(request):
    return render(request, 'prod.html')
  

def dproductos(request, id):
    producto = get_object_or_404(Producto, id=id)
    print(producto)
    context = { "productos" : producto}
    return render(request, 'dpro.html', context)

def productos(request):
    return render(request, 'dpro.html')
  

def productos(request):
    productos = Producto.objects.all()
    print("Cantidad de productos:", len(productos))
    context = {"productos": productos}
    return render(request, 'prod.html', context)

def venta(request):
      return render(request, 'venta.html')


def confirmar_venta(request):

    print("Webpay Plus Transaction.create")
    buy_order = str(random.randrange(1000000, 99999999))
    session_id = str(random.randrange(1000000, 99999999))
    amount = request.POST.get('totalv')

    nombre_apellido = request.POST.get('firstName')
    rut = request.POST.get('rut')
    email = request.POST.get('email')
    direccion = request.POST.get('address')
    totalv = request.POST.get('totalv')
    cantidad_productos = request.POST.get('cantidad_productos')
    productos_list = json.loads(request.POST.get('productos_list'))

    request.session['nombre'] = nombre_apellido
    request.session['rut'] = rut
    request.session['email'] = email
    request.session['direccion'] = direccion
    request.session['totalv'] = totalv
    request.session['cantidad_productios'] = cantidad_productos
    request.session['productos_list'] = productos_list


    return_url = request.build_absolute_uri(location='commit-pay/')

    print('buy_order: {0}'.format(buy_order))
    print('session_id: {0}'.format(session_id))
    print('amount: {0}'.format(amount))
    print('return_url: {0}'.format(return_url))
    print('request.headers: {0}'.format(request.headers))

    response = (Transaction().create)(buy_order, session_id, amount, return_url) 
    print('response: {0}'.format(response))
    print('Token generado: {0}'.format(response['token']))

    return render(request, 'inter.html', {'response': response, 'amount': amount})    


    if request.method == 'POST':
     
        nombre_apellido = request.POST.get('firstName')
        rut = request.POST.get('rut')
        email = request.POST.get('email')
        direccion = request.POST.get('address')
        totalv = request.POST.get('totalv')
        cantidad_productos = request.POST.get('cantidad_productos')
        productos_list = json.loads(request.POST.get('productos_list'))

        cliente, created = Cliente.objects.get_or_create(rut=rut)

        cliente.nombre = nombre_apellido
        cliente.email = email
        cliente.direccion = direccion
        cliente.save()

        boleta = Boleta(total=totalv, cant_productos=cantidad_productos, rut_cliente=cliente)
        boleta.save()

        for producto in productos_list:
            detalle = Detalle_Boleta(producto=producto, id_boleta=boleta)
            detalle.save()
  
        return render(request, 'confirmacion.html')
    else:
        return HttpResponse('Error: Se requiere una solicitud POST')
    

@csrf_exempt 
def commitpay(request):
    print('commitpay')
    print("request: {0}".format(request.POST))    
    token = request.GET.get('token_ws')

    print('TOKEEN')
    print(token)
    TBK_TOKEN = request.POST.get('TBK_TOKEN')
    TBK_ID_SESION = request.POST.get('TBK_ID_SESION')
    TBK_ORDEN_COMPRA = request.POST.get('TBK_ORDEN_COMPRA')

    #TRANSACCIÓN REALIZADA
    if TBK_TOKEN is None and TBK_ID_SESION is None and TBK_ORDEN_COMPRA is None and token is not None:

        #APROBAR TRANSACCIÓN
        transaction = Transaction()
        response = transaction.commit(token=token)
        #response = Transaction.commit(token=token)
        print("response: {}".format(response)) 

        status = response['status']
        print("status: {0}".format(status))
        response_code = response['response_code']
        print("response_code: {0}".format(response_code)) 

        #TRANSACCIÓN APROBADA
        if status == 'AUTHORIZED' and response_code == 0:

            state = ''
            if response['status'] == 'AUTHORIZED':
                state = 'Aceptado'
            pay_type = ''
            if response['payment_type_code'] == 'VD':
                pay_type = 'T_Débito'
            elif response['payment_type_code'] == 'VN':
                pay_type = 'T_Crédito'
            elif response['payment_type_code'] == 'VP':
                pay_type = 'T_Prepago'    
            amount = int(response['amount'])
            amount = f'{amount:,.0f}'.replace(',', '.')
            transaction_date = dt.datetime.strptime(response['transaction_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
            transaction_date = '{:%d-%m-%Y %H:%M:%S}'.format(transaction_date)
            transaction_detail = {  'card_number': response['card_detail']['card_number'],
                                    'transaction_date': transaction_date,
                                    'state': state,
                                    'pay_type': pay_type,
                                    'amount': amount,
                                    'authorization_code': response['authorization_code'],
                                    'buy_order': response['buy_order'], }
            

            nombre = request.session.get('nombre')
            rut = request.session.get('rut')
            email = request.session.get('email')
            direccion = request.session.get('direccion')
            totalv = request.session.get('totalv')
            cantidad_productos= request.session.get('cantidad_productios')
            productos_list = request.session.get('productos_list', [])

            nro_orden = response['authorization_code']

            cliente, created = Cliente.objects.get_or_create(rut=rut)

            cliente.nombre = nombre
            cliente.email = email
            cliente.direccion = direccion
            cliente.save()

            boleta = Boleta(total=totalv, cant_productos=cantidad_productos, rut_cliente=cliente, fecha=transaction_date,tipo_pago=pay_type, nro_orden=nro_orden)
            boleta.save()

            for producto in productos_list:
                detalle = Detalle_Boleta(producto=producto, id_boleta=boleta)
                detalle.save()

            request.session.clear()
            return render(request, 'confirmacion.html', {'transaction_detail': transaction_detail})
        else:
        #TRANSACCIÓN RECHAZADA            
            return HttpResponse('ERROR EN LA TRANSACCIÓN, SE RECHAZA LA TRANSACCIÓN.')
    else:
    #TRANSACCIÓN CANCELADA            
        return HttpResponse('ERROR EN LA TRANSACCIÓN, SE CANCELO EL PAGO.')

    

def admin(request):
    productos = Producto.objects.all()
    context = {"productos": productos}
    return render(request, 'adminpro.html', context)
    

def aproducto(request):
    return render(request, 'addpro.html')



def add_producto(request):
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        desc = request.POST.get('desc')
        anio = request.POST.get('anio')
        clas = request.POST.get('clas')
        dess = request.POST.get('dess')
        gen = request.POST.get('gen')
        idv = request.POST.get('idvid')
        imagen = request.FILES['imagen']

        producto = Producto(
            nombre=nombre,
            precio=precio,
            descripcion=desc,
            anno_lanzamiento=anio,
            clasificacion=clas,
            desarrollador=dess,
            genero=gen,
            id_video=idv,
            imagen=imagen
        )
        producto.save()

        return redirect('administrador') 
    else:
        return HttpResponse('Error: Se requiere una solicitud POST')

    return render(request, 'addpro.html')




def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'GET':

        producto.delete()
        return redirect('administrador')
    else:
        return HttpResponse('Error: Se requiere una solicitud GET')

def add_cliente(request):
    
    if request.method == 'POST':
       
        nombre_apellido = request.POST.get('firstName')
        rut = request.POST.get('rut')
        email = request.POST.get('email')
        direccion = request.POST.get('address')

        cliente, created = Cliente.objects.get_or_create(rut=rut)
        cliente.nombre = nombre_apellido
        cliente.email = email
        cliente.direccion = direccion
        cliente.save()

        return redirect('administrador') 
    else:
        return HttpResponse('Error: Se requiere una solicitud POST')

    return render(request, 'addcli.html')

def acliente(request):

    clientes=Cliente.objects.all()
    context = {"clientes":clientes}

    return render(request,'admincli.html',context)   

def addcliente(request):
    return render(request, 'addcli.html')


def eliminar_cliente(request, cliente_rut):
    cliente = get_object_or_404(Cliente, rut=cliente_rut)
    
    if request.method == 'GET':
        cliente.delete()
        return redirect('administrador')
    else:
        return HttpResponse('Error: Se requiere una solicitud GET')
    
def boletas(request):

    boletas = Boleta.objects.all()
    detalle_boletas = Detalle_Boleta.objects.all()
   
    context = {
        "boletas": boletas,
        "detalle_boletas": detalle_boletas
    }

    return render(request,'adminbol.html',context)



class LoginSystem(auth_views.LoginView):
    template_name = 'index.html' 

    def form_valid(self, form):

        if self.request.user.is_superuser:
            return super().form_valid(form)
        else:
            return HttpResponseRedirect('home')


def alterclientes(request, cliente_rut):

    cliente = Cliente.objects.get(rut = cliente_rut)
    context={"cliente":cliente}
    return render(request,'altercli.html',context)

def modclientes(request, cliente_rut):
 
    if request.method == 'POST':
       
        nombre_apellido = request.POST.get('firstName')
        email = request.POST.get('email')
        direccion = request.POST.get('address')

        cliente = Cliente.objects.get(rut = cliente_rut)
    
        cliente.nombre = nombre_apellido
        cliente.email = email
        cliente.direccion = direccion
        cliente.save()

        return redirect('acliente') 
    else:
        return HttpResponse('Error: Se requiere una solicitud POST')
 
# Registro de usuario y Inicio de sesion
def registro(request):
    if request.method == 'POST':
        form = ClienteCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio_sesion')
    else:
        form = ClienteCreationForm()
    return render(request, 'regi2.html', {'form': form})

def inicio_sesion(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            rut = form.cleaned_data['rut']
            password = form.cleaned_data['password']
            
            cliente = authenticate(request, username=rut, password=password)
            if cliente is not None:
                login(request, cliente)
                request.session['nombre_cliente'] = cliente.nombre  
                return redirect('home')
            else:
                context = {'form': LoginForm(), 'error': 'Credenciales inválidas. Intente nuevamente.'}
                return render(request, 'login.html', context)
        else:
            context = {'form': form}
            return render(request, 'login.html', context)
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    
def cerrar_sesion(request):
    logout(request)
    return redirect('login')

def buscar(request):
    query = request.GET.get('q', '')
    productos = []
    if query:
        productos = Producto.objects.filter(nombre__icontains=query)

    context = {
        'productos': productos,
        'query': query,
    }
    return render(request, 'buscar.htmL', context)