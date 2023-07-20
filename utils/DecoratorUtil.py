from fastapi import Form
# import inspect


class DecoratorUtil:
    def form_body(self, cls):
        cls.__signature__ = cls.__signature__.replace(
            parameters=[
                arg.replace(default=Form(...))
                for arg in cls.__signature__.parameters.values()
            ]
        )

        return cls

    # def form_body():
    #     def decorator(cls):
    #         parameters = [
    #             arg.replace(default=Form(...))
    #             for arg in inspect.signature(cls).parameters.values()
    #         ]
    #         new_signature = inspect.signature(cls).replace(parameters=parameters)
    #         setattr(cls, '__signature__', new_signature)
    #         return cls
    #
    #     return decorator
