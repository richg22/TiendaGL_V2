from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# Create your models here.

class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    precio = models.IntegerField()
    descripcion = models.CharField(max_length=500, default="Descripcion")
    anno_lanzamiento = models.CharField(max_length=4, default="0")
    clasificacion  = models.CharField(max_length=2,default="")
    desarrollador = models.CharField(max_length=50,default="")
    genero = models.CharField(max_length=100,default="")
    id_video = models.CharField(max_length=30, default="")
    imagen = models.ImageField(upload_to='imagenes/')

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'tiendaweb_producto'

class ClienteManager(BaseUserManager):
    def create_user(self, email, nombre, rut, password=None, **extra_fields):
        if not email:
            raise ValueError('El email debe ser proporcionado')
        email = self.normalize_email(email)
        cliente = self.model(email=email, nombre=nombre, rut=rut, **extra_fields)
        cliente.set_password(password)
        cliente.save(using=self._db)
        return cliente

    def create_superuser(self, email, nombre, rut, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, nombre, rut, password, **extra_fields)

class Cliente(AbstractBaseUser, PermissionsMixin):
    rut = models.CharField(primary_key=True, max_length=9)
    nombre = models.CharField(max_length=200)
    email = models.CharField(max_length=100, default=" ")
    direccion = models.CharField(max_length=500)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='cliente_set',  
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='cliente_permissions_set',  
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    objects = ClienteManager()

    USERNAME_FIELD = 'rut'
    REQUIRED_FIELDS = ['nombre', 'email']

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'tiendaweb_cliente'
        
class Boleta(models.Model):
    id = models.AutoField(primary_key=True)
    total = models.CharField(max_length=7, default="0")
    cant_productos = models.CharField(max_length=7, default="0")
    rut_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    fecha = models.CharField(max_length=30, default="--/--/--_--:--:--")
    tipo_pago = models.CharField(max_length=30, default=" ")
    nro_orden = models.CharField(max_length=100, default="0")

    def __str__(self):
        return str(self.id) 
    
    class Meta:
        db_table = 'tiendaweb_boleta'

class Detalle_Boleta(models.Model):
    id = models.AutoField(primary_key=True)
    producto = models.CharField(max_length=500)
    id_boleta = models.ForeignKey(Boleta, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
    
    class Meta:
        db_table = 'tiendaweb_detalle_boleta'

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    password =  models.CharField(max_length=20)

    def __str__(self):
        return str(self.id)
    
    class Meta:
        db_table = 'tiendaweb_usuario'
