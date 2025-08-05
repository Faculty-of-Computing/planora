from flask import make_response, redirect


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
