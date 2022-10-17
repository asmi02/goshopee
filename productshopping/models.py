from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

#creating category table

class Category(models.Model):
     category_name=models.CharField(max_length=100)

     def __str__(self):
         return self.category_name

class SubCategory(models.Model):
    category_type=models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    subcategory_name=models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.subcategory_name



#creating product table

class Product(models.Model):
    product_name=models.CharField(max_length=150)
    details=RichTextField()
    description=RichTextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory=models.ForeignKey(SubCategory, on_delete=models.CASCADE,blank=True,null=True)
    featured_product=models.BooleanField()
    datetime_of_entry=models.DateTimeField()
    product_pic=models.ImageField(upload_to='productpics',blank=True,null=True)
    product_pic2=models.ImageField(upload_to='productpics',blank=True,null=True)
    product_pic3=models.ImageField(upload_to='productpics',blank=True,null=True)

    values=(('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10'),
            ('11','11'),('12','12'),('13','13'),('14','14'),('15','15'),('16','16'),('17','17'),('18','18'),('19','19'),
            ('20','20'),('21','21'),('22','22'),('23','23'),('24','24'),('25','25'),('26','26'),('27','27'),
            ('28','28'),('29','29'),('30','30'),('31','31'),('32','32'),('33','33'),('34','34'),('35','35'),
            ('36','36'),('37','37'),('38','38'),('39','39'),('40','40'),('41','41'),('42','42'),('43','43'),('44','44'),('45','45'),
            ('46','46'),('47','47'),('48','48'),('49','49'),('50','50'))
    qty=models.CharField(choices=values,max_length=1000,null=True)

    # sizes=(('XXXL','XXXL'),('XXL','XXL'),('XL','XL'),('L','L'),('M','M'),('S','S'))
    # size=models.CharField(choices=sizes,max_length=4,null=True)
    # size=models.ForeignKey(Sizes, on_delete=models.CASCADE,null=True)


    def __str__(self):
        return self.product_name


class Sizes(models.Model):
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    size= models.CharField(max_length=100,null=True)
    def __str__(self):
        return str(self.id)




class ShoppingCart(models.Model):
    pid=models.ForeignKey(Product,on_delete=models.CASCADE)
    price=models.IntegerField()
    size=models.CharField(max_length=50,null=True)
    qty=models.IntegerField()
    total_cost=models.IntegerField()
    sessionid=models.CharField(max_length=500,null=True)

class Wishlist(models.Model):
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    username=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    sessionid = models.CharField(max_length=500, null=True)

class Order(models.Model):
    username=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    address=models.TextField()
    phone=models.IntegerField()
    pincode=models.IntegerField()
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    values=(('cod','Cash On Delivery'),('gpay','Google Pay on 98989898998'))
    payment_mode = models.CharField(choices=values, max_length=4,null=True)

    grandtotal=models.IntegerField()
    order_date=models.DateField(auto_now_add=True)
    order_update_date=models.DateField(auto_now=True)
    values=(('received','Order Received'),('process','Order In Process'),('Shipped','Order Shipped'),('delivered','Order Delivered'),('pending','Order Pending'),('delayed','Order Delayed'),('Cancelled','Order Cancelled'))
    order_status=models.CharField(choices=values,max_length=10,null=True,default='received')

    def __str__(self):
        return str(self.id)


class Order_Details(models.Model):
    orderno=models.ForeignKey(Order,on_delete=models.CASCADE)
    product_id=models.ForeignKey(Product, on_delete=models.CASCADE)
    price=models.IntegerField()
    qty=models.IntegerField()
    size=models.CharField(max_length=50,null=True)
    total_cost=models.IntegerField()

    def __str__(self):
        return str(self.orderno)


class Profile(models.Model):
    profile_pic=models.ImageField(null=True)
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date=models.DateField(null=True, blank=True)
    address=models.TextField(null=True)
    phone=models.CharField(null=True,max_length=10)





@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_user_profile(sender,instance,**kwargs):
    instance.profile.save()

