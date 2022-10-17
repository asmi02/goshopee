from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMultiAlternatives
from django.db.models import Sum
from django.http import HttpResponseRedirect, request
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from django.contrib import messages

from goshopee import settings
from productshopping.forms import MyRegisterForm, MyLoginForm, ProfileForm
from productshopping.models import Product, ShoppingCart, Order, Order_Details, SubCategory, Profile, Wishlist, \
    Category, Sizes


# Create your views here.

def showhome(request):
    productsdata = Product.objects.filter(featured_product=True)
    # print(productsdata)
    sizedetails = Sizes.objects.get(product_id=productsdata[0].id)
    l1 = sizedetails.size.split(",")
    # print(l1[0])
    catobj = Category.objects.get(category_name='Womens')
    womenproductsdata = Product.objects.filter(featured_product=True, category=catobj)
    catobj = Category.objects.get(category_name='Mens')
    menproductsdata = Product.objects.filter(featured_product=True, category=catobj)
    return render(request,"index.html",{'pdata': productsdata, 'womenpdata': womenproductsdata, 'menpdata': menproductsdata,'size':l1[0]})


def showproductdetails(request, pid):
    pdetails = Product.objects.get(id=pid)
    sizedetails = Sizes.objects.get(product_id=pid)
    l1=sizedetails.size.split(",")
    # print(l1)
    return render(request, "product_details.html", {'productdetailsdata': pdetails,'sizedetailslist':l1})

# def showproductsizedetails(request, pid):
#     sizedetails = Sizes.objects.get(product_id=pid)
#     return render(request,"product_details.html",{'sizedetails':sizedetails})

def addtoshoppingcart(request):
    pid=int(request.POST.get("item_id"))
    price=int(float(request.POST.get("amount")))
    qty=int(request.POST.get("qty"))
    size=(request.POST.get("size"))
    totalcost=price * qty

    # print(pid)
    # print(price)
    # print(qty)
    # print(totalcost)

    shoppingcartobj=ShoppingCart()
    shoppingcartobj.pid=Product(id=pid)
    shoppingcartobj.price=price
    shoppingcartobj.qty=qty
    shoppingcartobj.size=size
    shoppingcartobj.total_cost=totalcost

    if not request.session or not request.session.session_key:
        request.session.save()
        request.session["sid"] = request.session.session_key
    shoppingcartobj.sessionid = request.session["sid"]
    shoppingcartobj.save()
    return HttpResponseRedirect(reverse_lazy('shoppingcart'))


def showshoppingcart(request):
    if not request.session or not request.session.session_key:
        request.session.save()
        request.session["sid"] = request.session.session_key
    shoppingcartdata = ShoppingCart.objects.filter(sessionid=request.session["sid"])
    cartsum = ShoppingCart.objects.filter(sessionid=request.session["sid"]).aggregate(Sum('total_cost'))
    request.session["cartsum"] = cartsum
    return render(request, "shoppingcart.html", {'cartdata': shoppingcartdata, 'cartsum': cartsum})

def deleteproductfromcart(request,id):
    cartobj=ShoppingCart.objects.filter(id=id)
    cartobj.delete()
    return HttpResponseRedirect(reverse_lazy('shoppingcart'))

def addtowishlist(request):
    pid = int(request.POST.get("item_id"))
    # print(pid)
    # print(price)
    # print(qty)
    # print(totalcost)

    Wishlistobj = Wishlist()
    Wishlistobj.pid = Product(id=pid)
    Wishlistobj.username = User.objects.get(username=request.session['myusername'])

    if not request.session or not request.session.session_key:
        request.session.save()
        request.session["sid"] = request.session.session_key
    Wishlistobj.sessionid = request.session["sid"]
    Wishlistobj.save()
    return HttpResponseRedirect(reverse_lazy('showwishlist'))


def showwishlist(request):
    if not request.session or not request.session.session_key:
        request.session.save()
        request.session["sid"] = request.session.session_key
    wishlistdata = Wishlist.objects.filter(sessionid=request.session["sid"])
    return render(request, "wishlist.html", {'wishdata': wishlistdata})


def deleteproductfromwishlist(request,id):
    wishobj=Wishlist.objects.filter(id=id)
    wishobj.delete()
    return HttpResponseRedirect(reverse_lazy('showwishlist'))


def productcategories(request, cid):
    productsdata = Product.objects.filter(subcategory=cid)
    subcategoryobj = SubCategory.objects.get(id=cid)
    return render(request, "category_products.html",
                  {"productsdata": productsdata, "categoryname": subcategoryobj.subcategory_name})

class MySignUpClass(SuccessMessageMixin, CreateView):
    form_class=MyRegisterForm
    template_name = 'signup.html'
    success_url = reverse_lazy('signup')
    success_message = 'Sign Up Successful. You Can login now. '

    # message = EmailMultiAlternatives(
    #     'Message from GoShopee',  # Subject
    #     'Your Sign Up is successful. Your can place your orders now',  # Email Body
    #     to=[request.session['emailid']],  # where you receive the contact emails
    #     from_email=settings.EMAIL_HOST_USER,
    #     reply_to=['goshopee.shop@outlook.com'])


    def dispatch(self, *args, **kwargs):
        return super(MySignUpClass, self).dispatch(*args,**kwargs)

def showlogin(request):
    formobj = MyLoginForm(request.POST or None)
    if formobj.is_valid():
        redirect_to = request.POST.get('next')
        username1 = formobj.cleaned_data.get("username1")
        userobj = User.objects.get(username__iexact=username1)
        login(request, userobj)
        request.session['myusername'] = username1
        request.session['emailid'] = userobj.email
        if not "sid" in request.session:
            request.session["sid"] = request.session.session_key
        if redirect_to:
            return redirect(redirect_to)
        else:
            return HttpResponseRedirect(reverse('home'))
    else:
        return render(request, "signin.html", {"myform":formobj})


def mylogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


@login_required()
def mycheckout(request):
    return render(request, "checkout.html")


def finalorder(request):
    username1=request.session['myusername']
    name=request.POST.get("name")
    address=request.POST.get("address")
    phone=request.POST.get("phone")
    pincode=request.POST.get("pincode")
    city=request.POST.get("city")
    state=request.POST.get("state")
    payment_mode=request.POST.get("paymentmode")
    gtotal=request.session["cartsum"]
    grandtotal=gtotal.get("total_cost__sum")

    orderobj=Order()

    orderobj.username=User.objects.get(username=username1)
    orderobj.name=name
    orderobj.address=address
    orderobj.phone=phone
    orderobj.pincode=pincode
    orderobj.city=city
    orderobj.state=state
    orderobj.payment_mode=payment_mode
    orderobj.grandtotal=grandtotal

    orderobj.save()

    orderno=Order.objects.latest('id')

    shoppingcartdata=ShoppingCart.objects.filter(sessionid=request.session["sid"])
    for data in shoppingcartdata:
        orderdetails=Order_Details()
        orderdetails.product_id=Product(id=data.pid).id
        orderdetails.price=data.price
        orderdetails.qty=data.qty
        orderdetails.size=data.size
        orderdetails.total_cost=data.total_cost
        orderdetails.orderno=orderno

        orderdetails.save()
        productobj = Product.objects.get(id=data.pid.id)
        # print(data.pid)
        # print(productobj.qty)
        # print(orderdetails.qty)
        # print(data.pid.qty)
        pqty=int(productobj.qty)
        pqty -= int(orderdetails.qty)
        productobj.qty=pqty
        productobj.save()


        shoppingcartdata.delete()       #empty the shopping cart after placing order




    # message = EmailMultiAlternatives(
    #     'Message from GoShopee',  # Subject
    #     'Your order has been placed successfully. Your Order No. is ' + str(orderno),  # Email Body
    #     to=[request.session['emailid']],  # where you receive the contact emails
    #     from_email=settings.EMAIL_HOST_USER,
    #     reply_to=['goshopee.shop@outlook.com'])
    # result = message.send(fail_silently=False)
    # request.session["result"] = result
    # return HttpResponseRedirect(reverse_lazy('ordersuccess'))

    message = EmailMultiAlternatives(
        'Message from GoShopee',  # Subject
        'Your order has been placed successfully. Your Order No. is ' + str(orderno),  # Email Body
        to=[request.session['emailid']],  # where you receive the contact emails
        from_email=settings.EMAIL_HOST_USER,
        reply_to=['goshopee.shoppers@outlook.com'])
    result = message.send(fail_silently=False)
    request.session["result"] = result
    return HttpResponseRedirect(reverse_lazy('ordersuccess'))

    # shoppingcartdata.delete()
    #
    # message = EmailMultiAlternatives(
    #     'Message from Goshopee',  # Subject
    #     'Your order has been placed successfully. Your Order No. is ' + str(orderno),  # Email Body
    #     to=[request.session['emailid']],  # where you receive the contact emails
    #     from_email=settings.EMAIL_HOST_USER,
    #     reply_to=['goshopee.shop@outlook.com'])
    # result = message.send(fail_silently=False)
    # request.session["result"] = result
    # return HttpResponseRedirect(reverse_lazy('ordersuccess'))


def showordersuccess(request):
    userobj = User.objects.get(username=request.session["myusername"])
    ordersdata = Order.objects.filter(username=userobj).order_by('-id')[:1]

    result = request.session["result"]
    if result == 1:
        return render(request, "success.html", {'orderno': ordersdata[0]})
    else:
        return render(request, "success.html",
                      {'orderno': ordersdata[0], "error": "Error Occured. We will send confirmation mail later on"})


# return render(request, "success.html",{'orderno': ordersdata[0]})


def orderhistory(request):
    userobj=User.objects.get(username=request.session["myusername"])
    ordersdata=Order.objects.filter(username=userobj)
    return render(request, "orderhistory.html", {'ordersdata': ordersdata})

def orderdetails(request, oid):
    orderdetailsdata=Order_Details.objects.filter(orderno=oid)
    return render(request,"orderdetails.html",{'orderdetailsdata':orderdetailsdata})

def changepswd(request):
    if request.method=="POST":
        myformdata=request.POST
        oldpswd=myformdata.get("oldpassword","0")
        newpswd=myformdata.get("newpassword","1")
        confirmpswd=myformdata.get("confirmpassword","2")

        if newpswd==confirmpswd:
            myusername=request.session["myusername"]
            userobj=authenticate(username=myusername,password=oldpswd)

            if userobj is not None:
                userobj.set_password(confirmpswd)
                userobj.save()
                logout(request)
                messages.success(request,'Password Changed Successfully.Login Again')
                return HttpResponseRedirect(reverse('signin'))

            else:
                mymessage={"messages":"Wrong old Password"}
                return render(request,"changepassword.html",mymessage)

        else:
            mymessage={"messages":"New Password and Confirm Password doesn't match"}
            return render(request,"changepassword.html",mymessage)

    else:
        return render(request,"changepassword.html")


class updateprofile(SuccessMessageMixin, UpdateView):
    model=User
    template_name = 'updateprofile.html'
    fields = ['email']
    success_message = 'Profile Updated Successfully'

    def get_success_url(self):
        pk=self.kwargs["pk"]
        return reverse("updateprofile",kwargs={"pk":pk})



def add_user(request):
    pform = ProfileForm(request.POST or None, request.FILES, instance=request.user.profile)
    if pform.is_valid():
            # user=pform.save()
            pform.save()

            # profile = Profile.objects.create(user=request.user)

            # Profile.objects.create(**{
            #     'profile_pic': "", 'phone': '','birth_date': '','address': '', 'user': user
            # })
            return render(request, "profile.html", {'form': pform, "messages": "Profile Updated Successfully"})
    return render(request, "profile.html", {'form': pform})




