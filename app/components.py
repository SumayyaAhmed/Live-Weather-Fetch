import reflex as rx
from app.state import WeatherState


def weather_card(data: rx.Var[dict]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                f"{data['city']}, {data['country']}",
                class_name="text-xl font-semibold text-gray-700",
            ),
            rx.el.p(data["weather_emoji"], class_name="text-8xl mt-4 mb-2"),
            rx.el.p(
                f"{data['temperature'].to_string()}°C",
                class_name="text-6xl font-bold text-gray-800",
            ),
            rx.el.p(
                data["weather_description"],
                class_name="text-lg text-gray-600 font-medium mt-2 capitalize",
            ),
            class_name="flex flex-col items-center",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("droplets", class_name="text-blue-500"),
                    rx.el.p("Humidity", class_name="text-sm text-gray-500"),
                    class_name="flex items-center gap-2",
                ),
                rx.el.p(
                    f"{data['humidity']}%",
                    class_name="text-lg font-semibold text-gray-800",
                ),
                class_name="text-center",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("wind", class_name="text-blue-500"),
                    rx.el.p("Wind", class_name="text-sm text-gray-500"),
                    class_name="flex items-center gap-2",
                ),
                rx.el.p(
                    f"{data['wind_speed'].to_string()} km/h",
                    class_name="text-lg font-semibold text-gray-800",
                ),
                class_name="text-center",
            ),
            class_name="flex justify-around w-full mt-8 pt-6 border-t border-gray-200",
        ),
        class_name="bg-white/80 backdrop-blur-md rounded-2xl p-8 shadow-lg border border-gray-100/50 w-full max-w-md transition-all duration-300 transform hover:scale-105 hover:shadow-xl",
    )


def error_display() -> rx.Component:
    return rx.cond(
        WeatherState.error_message != "",
        rx.el.div(
            rx.icon("flag_triangle_right", class_name="text-red-500 mr-2"),
            rx.el.p(WeatherState.error_message, class_name="text-red-600 font-medium"),
            class_name="flex items-center bg-red-100 p-3 rounded-lg mt-4 border border-red-200",
        ),
        None,
    )


def loading_spinner() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            class_name="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"
        ),
        class_name="flex justify-center items-center p-8",
    )