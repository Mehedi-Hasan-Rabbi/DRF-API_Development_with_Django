from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from api.models import Product
from django.core.cache import cache

"""
A Django signal is a way for one part of your application to notify 
another part that something has happened, without the two parts being directly connected.
In simple word: “When X happens, automatically do Y.”

Here when we try to save/delete in Product (Model) throught DB then cache will be deleted [cache.delete_pattern('*product_list*')]
Because when new product is added or some product is deleted then cached data is irrelavent.
"""
@receiver([post_save, post_delete], sender=Product)
def invalidate_product_cache(sender, instance, **kwargs):
    """
    Invalidate product list caches when a product is created, updated, or deleted
    """
    print("Clearing product cache")
    
    # Clear product list caches
    cache.delete_pattern('*product_list*')