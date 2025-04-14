""" Helper Functions to be used throughout the codebase. """


def is_float(check: str) -> bool:
    """
    Checks if a string is a float number or not.

    Args:
        check: the string to be tested for float data type. (string)

    Returns:
        A boolean value of either True or False.
    """
    try:
        float(check)
        return True
    except Exception as e:
        return False


def parseStructuredResponse(response: str) -> dict[str, str]:
    """
    Parses the structured AI response into a data structure for use.

    Args:
        response: the structured AI response from compare functions (string)

    Returns:
        a dictionary of all revelant response information (dict)
    """
    dict_response: dict = {'justification': []}
    r: list = response.split('\n')
    r = r[1:-1]

    for idx, line in enumerate(r):
        if idx < 2:
            ls: list = line.split(':')
            assert len(ls) <= 2, f"{idx} line in AI response is {len(ls)}"
            if idx == 0:
                dict_response[str(ls[0]).lower()] = ls[1]
            elif idx == 1:
                pass

            continue

        line = line.replace("-", " ")
        line = line.lstrip(" ")
        dict_response['justification'].append(line)

    return dict_response
