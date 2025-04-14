import math


def jaccard_similarity(set1, set2) -> float:
    """
    Calculates the Jaccard similarity between two sets.

    Args:
        set1: The first set.
        set2: The second set.

    Returns:
        The Jaccard similarity between the two sets.
        Return values is always between 0 and 1.
    """

    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    if union == 0:
        return 0.0
    return intersection / union


def haversine(units: str, lat1, lon1, lat2, lon2):
    """
    Calculates the distance between two locations using lat and lon.

    Args:
        units: Options - feet, miles, meters, default is kilometers
        lat1: First Latitude.
        lon2: First Longitude.
        lat2: Second Latitude.
        lon2: Second Longitude.

    Returns:
        The Distance between the two points, units can vary depending on unit parameter.
    """

    # Converting degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # For formula
    dist_lon = lon2 - lon1
    dist_lat = lat2 - lat1

    a = math.sin(dist_lat/2)**2 + math.cos(lat1) * \
        math.cos(lat2) * math.sin(dist_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    # radius of the Earth in kilometers (mean radius)
    r = 6371
    d = r * c

    if units == "feet":
        return (d * 3281)
    elif units == "miles":
        return (d * 1.609)
    elif units == "meters":
        return (d * 1000)

    # default is kilometers
    return d
