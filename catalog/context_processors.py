def product_views(request):
    return {'product_views': ['product_list', 'product_detail', 'product_create', 'product_update', 'product_delete',
                              'login', 'register', 'new_password',
                              'profile', 'profile_edit', 'profile_delete']}
