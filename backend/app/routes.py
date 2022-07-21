def register_routes(app, root="api"):

    from app.routers.User import register_routes as attach_user
    from app.routers.CodeWars import register_routes as attach_code_wars

    # from app.routers.Habitica import Habitica
    # from app.widget import register_routes as attach_widget
    # from app.fizz import register_routes as attach_fizz

    # Add routes
    attach_user(app)
    attach_code_wars(app)
    # attach_widget(app)
    # attach_fizz(app)
