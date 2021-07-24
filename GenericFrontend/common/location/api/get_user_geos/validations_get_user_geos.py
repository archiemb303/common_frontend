"""
No validation needed for this API as the input required is profile_id which is there in the
APIDetails section of request object.
User Geo is also calculated using the ip address of the user and calling a third party api,
but this step is optional or rather if this step yeilds negative results then we find the user's geo from its city_id
"""
