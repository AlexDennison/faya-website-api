from django.core.exceptions import ObjectDoesNotExist
# from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, GenericAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from .models import User, Product
from .serializers import UserSerializer, ProductSerializer
from datetime import datetime, timedelta
from django.utils import timezone


# Create your views here.
class CustomerCreate(GenericAPIView):

    def post(self, request, *args, **kwargs):
        """
        API for creating a customer
        :param request: POST
        :param args: NA
        :param kwargs: NA
        :return: Returns created customer details
        """
        user_obj = User.objects.create(first_name=request.data.get('first_name'),
                                       last_name=request.data.get('last_name'),
                                       email=request.data.get('email'),
                                       username=request.data.get('username'),
                                       password=make_password(request.data.get('password')),
                                       address=request.data.get('address'),
                                       phone=request.data.get('phone'),
                                       )
        serializer = UserSerializer(user_obj)
        return Response({"success": True, "message": "User Created", "results": serializer.data},
                        status=status.HTTP_201_CREATED)


class CustomerUpdate(UpdateAPIView):

    def patch(self, request, *args, **kwargs):
        """
        API for updating customer details
        :param request: PATCH
        :param args: NA
        :param kwargs: pk - customer_id
        :return: Returns updated details of customer
        """
        try:
            user_obj = User.objects.get(id=kwargs.get('pk'))
        except:
            return Response({'message': 'Invalid User ID', "success": False}, status=status.HTTP_400_BAD_REQUEST)
        fields = ['email', 'first_name', 'last_name', 'address', 'phone']
        for field in fields:
            if field in request.data:
                setattr(user_obj, field, request.data[field])
        user_obj.save()
        serializer = UserSerializer(user_obj, context={'request': request})
        return Response({'message': 'Profile Updated Successfully', 'success': True, 'results': serializer.data})


class CustomerList(ListAPIView):

    def get(self, request, *args, **kwargs):
        """
        API for listing 10 customers per page
        :param request: GET
        :param args: NA
        :param kwargs: NA
        :return: Returns paginated list of all customers
        """
        try:
            paginator = PageNumberPagination()
            paginator.page_size = 10
            customer_list_obj = User.objects.all()
            result_page = paginator.paginate_queryset(customer_list_obj, request)
            serializer = UserSerializer(result_page, many=True, context={'request': request})
            response = paginator.get_paginated_response(serializer.data)
            response.data['success'] = True
            response.data['message'] = "List of Customers"
            return Response(response.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e), "success": False}, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetail(RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        """
        APi for Detail View of Customer
        :param request: GET
        :param args: NA
        :param kwargs: pk - customer_id
        :return: Returns Details of customer
        """
        try:
            customer_object = User.objects.get(id=kwargs.get('pk'))
            serializer_class = UserSerializer(customer_object, context={'request': request})
            return Response({"success": True,
                             "message": "Details of Customer",
                             "results": serializer_class.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e), "success": False}, status=status.HTTP_400_BAD_REQUEST)


class CustomerDelete(DestroyAPIView):

    def delete(self, request, *args, **kwargs):
        """
        API for deleting a customer
        :param request: DELETE
        :param args: NA
        :param kwargs: pk - customer_id
        :return: Delete customer successfully
        """
        try:
            customer_delete_obj = User.objects.get(id=kwargs.get('pk'))
            customer_delete_obj.delete()
            return Response({"message": "Customer deleted", "success": True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e), "success": False}, status=status.HTTP_400_BAD_REQUEST)


class ProductCreate(GenericAPIView):

    def post(self, request, *args, **kwargs):
        """
        API for creating Product
        :param request: POST
        :param args: NA
        :param kwargs: NA
        :return: Create product successfully
        """
        try:
            customer_obj = User.objects.get(id=request.data.get("customer_id"))
        except ObjectDoesNotExist:
            return Response({'message': 'Invalid Customer ID', 'success': False}, status=status.HTTP_400_BAD_REQUEST)
        product_create_obj = Product(product_name=request.data.get("product_name"),
                                     product_price=request.data.get("product_price"),
                                     product_quantity=request.data.get("product_quantity"),
                                     owner_id_id=customer_obj.id)
        serializer = ProductSerializer(product_create_obj)
        product_create_obj.save()
        return Response({"message": "Product Created Successfully", "success": True, "results": serializer.data},
                        status=status.HTTP_201_CREATED)


class ProductUpdate(UpdateAPIView):

    def patch(self, request, *args, **kwargs):
        """
        API for updating product details
        :param request: PATCH
        :param args: NA
        :param kwargs: pk - product_id
        :return: Returns updated product details
        """
        try:
            product_update_object = Product.objects.get(id=kwargs.get('pk'))
        except ObjectDoesNotExist:
            return Response({"message": "No Product with this ID", "success": False},
                            status=status.HTTP_400_BAD_REQUEST)
        if product_update_object.buildup_date and product_update_object.product_status is True:
            two_months_ago = timezone.now() - timedelta(days=60)
            if product_update_object.buildup_date < two_months_ago:
                product_update_object.product_status = False
            else:
                product_update_object.product_status = True
        fields = ['product_name', 'product_price', 'product_quantity', 'product_status']
        for field in fields:
            if field in request.data:
                setattr(product_update_object, field, request.data[field])
        product_update_object.save()
        serializer = ProductSerializer(product_update_object, context={'request': request})
        return Response({"success": True, "message": "Product Updated Successfully", "results": serializer.data},
                        status=status.HTTP_200_OK)


class ProductList(ListAPIView):

    def get(self, request, *args, **kwargs):
        """
        API for listing 10 products per page
        :param request: GET
        :param args: NA
        :param kwargs: NA
        :return: Return paginated list of products
        """
        paginator = PageNumberPagination()
        paginator.page_size = 10
        try:
            product_list_obj = Product.objects.all()
            result_page = paginator.paginate_queryset(product_list_obj, request)
            serializer = ProductSerializer(result_page, many=True, context={'request': request})
            response = paginator.get_paginated_response(serializer.data)
            response.data['success'] = True
            response.data['message'] = "List of Products"

            return Response(response.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e), "success": False}, status=status.HTTP_400_BAD_REQUEST)


class ProductDetail(RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        """
        API for returning product details
        :param request: GET
        :param args: NA
        :param kwargs: pk - product_id
        :return: Return Product Details
        """
        try:
            product_details_object = Product.objects.get(id=kwargs.get('pk'))
            serializer = ProductSerializer(product_details_object, context={'request': request})
            return Response({"success": True, "message": "Product Details", "results": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e), "success": False}, status=status.HTTP_400_BAD_REQUEST)


class ProductDelete(DestroyAPIView):

    def delete(self, request, *args, **kwargs):
        """
        API for deleting product
        :param request: DELETE
        :param args: NA
        :param kwargs: pk - product_id
        :return: Returns success if product deleted
        """
        try:
            product_delete_obj = User.objects.get(id=kwargs.get('pk'))
            product_delete_obj.delete()
            return Response({"message": "Product deleted", "success": True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e), "success": False}, status=status.HTTP_400_BAD_REQUEST)

