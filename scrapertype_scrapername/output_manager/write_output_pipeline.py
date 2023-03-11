import secrets
import string


def save_output_data(data_to_save, is_running_local: bool):
    """
    Create
    :param data_to_save:
    :param is_running_local:
    :return:
    """
    base_path = "/" if is_running_local else "./"
    outputs_path = base_path + "output.txt"
    print(f"Saving output>  {outputs_path}")
    with open(outputs_path, 'w') as f:
        f.write(data_to_save)


def create_random_code(range_code=6):
    """
    This function is responsible for generate a random code, containing strings and numbers, with range 6.
    return str: random code
    """
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(range_code))
