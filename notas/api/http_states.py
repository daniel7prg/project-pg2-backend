from rest_framework import status

estados = {
    'ok': status.HTTP_200_OK,
    'created': status.HTTP_201_CREATED,
    'accepted': status.HTTP_202_ACCEPTED,
    'no_content': status.HTTP_204_NO_CONTENT,
    'bad_request': status.HTTP_400_BAD_REQUEST,
    'unauthorized': status.HTTP_401_UNAUTHORIZED,
    'forbidden': status.HTTP_403_FORBIDDEN,
    'not_found': status.HTTP_404_NOT_FOUND
}