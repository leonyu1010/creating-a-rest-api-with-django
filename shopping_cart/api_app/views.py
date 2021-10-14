#from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import os
from os.path import dirname, abspath
import subprocess
from .models import CartItem

# Create your views heretvalre.


@method_decorator(csrf_exempt, name='dispatch')
class ShoppingCart(View):

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))  
        p_name = data.get('product_name')
        p_price = data.get('product_price')
        p_quantity = data.get('product_quantity')

        product_data = {
            'product_name': p_name,
            'product_price': p_price,
            'product_quantity': p_quantity,
        }

        cart_item = CartItem.objects.create(**product_data)

        data = {
            "message": f"New item added to Cart with id: {cart_item.id}"}
        return JsonResponse(data, status=200)

    def get(self, request):
        items_count = CartItem.objects.count() 
        items = CartItem.objects.all()  

        items_data = []  
        for item in items:
            items_data.append({
                'product_name': item.product_name,
                'product_price': item.product_price,
                'product_quantity': item.product_quantity,
            })

        data = {
            'items': items_data,
            'count': items_count,
        }
        return JsonResponse(data)
           


@method_decorator(csrf_exempt, name='dispatch')
class ShoppingCartUpdate(View):

    def patch(self, request, item_id):
        data = json.loads(request.body.decode("utf-8"))
        item = CartItem.objects.get(id=item_id)
        item.product_quantity = data['product_quantity']
        item.save()
        
        data = {
            'message': f'Item {item_id} has been updated'
        }

        return JsonResponse(data)

    def delete(self, request, item_id):
        item = CartItem.objects.get(id=item_id)
        item.delete()
        
        data = {
            'message': f'Item {item_id} has been deleted'
        }

        return JsonResponse(data)

@method_decorator(csrf_exempt, name='dispatch')
class ShowCommit(View):

    def get(self, request):
        cwd = os.getcwd()
        print(cwd)
        print(os.path.dirname(os.getcwd()))
        
        config_repo = dirname(abspath(__file__)).replace("api_app", "config-repo")
        print(__file__)
        print(config_repo)
        cmd = ('ls', config_repo)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        lines = p.stdout.readlines()
        print(lines)
        retval = p.wait()
        if retval != 0:
            return JsonResponse({"msg" : "cannot ls {}".format(config_repo)})
        
        os.chdir(config_repo)
        print(os.getcwd())
        
        
        branch = request.GET['branch']
        dataset = request.GET['dataset']
        metrics = request.GET['metrics']
        commit_id = request.GET['commit_id']
        print(branch, dataset, metrics, commit_id)


        
        path = "test_config"
        query = "{}:{}".format(commit_id, path)
        cmd = ('git', 'cat-file', '-p', query)
        print(' '.join(cmd))
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        lines = p.stdout.readlines()
        print(lines)
        retvalue = p.wait()
        if retvalue != 0:
            msg = "unable to read config (retval={}): {}".format(retvalue, path)
            data = {
            'msg': msg,
            }
            return JsonResponse(data)
        
        try:
           msg = json.loads("".join(lines))   
            
           data = {
               'msg': msg,
           }
           return JsonResponse(data)
       
        except Exception:
           msg = str(lines)
            
           data = {
               'commit': msg,
           }
           return JsonResponse(data)