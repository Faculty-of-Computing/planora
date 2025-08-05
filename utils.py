from flask import make_response, redirect, request


def set_user_cookie_and_recirect(
    user_id: int,
):
    response = make_response(redirect("/home"))
    response.set_cookie(
        "user_id",
        str(user_id),
        max_age=60 * 60 * 24 * 30,
        httponly=True,
        samesite="Lax",
    )
    return response


def user_is_authenticated() -> bool:
    user_id = request.cookies.get("user_id")
    if not user_id:
        return False
    else:
        return True
