class Urls:
   STELLAR_BURGERS_URL = "https://qa-stellarburgers.education-services.ru"
   CREATE_USER = "/api/auth/register"
   LOGIN_USER = "/api/auth/login"
   DELETE_USER = "/api/auth/user"
   GET_INGREDIENTS = "/api/ingredients"
   CREATE_ORDER = "/api/orders"

class ResponseMessages:
   DUPLICATE_USER = 'User already exists'
   ERROR_CREATE_WITHOUT_REQUIRED_FIELD = 'Email, password and name are required fields'
   ERROR_INCORRECT_LOGIN_PASSWORD = 'email or password are incorrect'
   ERROR_ORDER_WITHOUT_INGREDIENTS = 'Ingredient ids must be provided'
   ERROR_INCORRECT_INGREDIENT = 'One or more ids provided are incorrect'
