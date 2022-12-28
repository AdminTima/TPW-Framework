import json
import inspect


class TsunamiSerializer:

    def serialize(self, obj, include=None):
        result_dict = {}
        if include:
            for attribute in include:
                value = obj.__dict__[attribute]
                result_dict[attribute] = value
        result = json.dumps(result_dict) if result_dict else json.dumps(obj.__dict__)
        return result

    def deserialize(self, json_string, to_instance):
        assert inspect.isclass(to_instance), "to_instance must be a class."

        result = json.loads(json_string)

        if "__init__" in to_instance.__dict__:
            print("init in")
            result = to_instance(**result)
        else:
            result = to_instance()
            for key, value in result.items():
                setattr(result, key, value)
        return result


