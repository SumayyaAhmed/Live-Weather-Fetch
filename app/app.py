import reflex as rx
from app.state import WeatherState
from app.components import weather_card, error_display, loading_spinner


def index() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Weather Fetcher 🌍",
                    class_name="text-4xl font-bold text-gray-800 mb-2",
                ),
                rx.el.p(
                    "Enter a city to get the latest weather",
                    class_name="text-gray-500 mb-8",
                ),
                rx.el.form(
                    rx.el.div(
                        rx.el.input(
                            name="city",
                            placeholder="e.g., London",
                            class_name="w-full h-14 px-4 bg-white/70 border-2 border-gray-200 rounded-l-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all duration-300 placeholder-gray-400 font-medium",
                        ),
                        rx.el.button(
                            "Search",
                            type_="submit",
                            class_name="h-14 px-8 bg-blue-500 text-white font-semibold rounded-r-xl hover:bg-blue-600 transition-colors duration-300 shadow-md hover:shadow-lg disabled:bg-gray-400 disabled:shadow-none",
                            disabled=WeatherState.is_loading,
                        ),
                        class_name="flex w-full max-w-md shadow-sm rounded-xl",
                    ),
                    on_submit=WeatherState.get_weather,
                    prevent_default=True,
                    class_name="flex justify-center",
                ),
                error_display(),
                rx.el.div(
                    rx.cond(
                        WeatherState.is_loading,
                        loading_spinner(),
                        rx.cond(
                            WeatherState.weather_data,
                            weather_card(WeatherState.weather_data),
                            rx.el.div(
                                rx.icon(
                                    "cloud-sun", size=48, class_name="text-gray-300"
                                ),
                                rx.el.p(
                                    "Weather will be shown here",
                                    class_name="text-gray-400 mt-4",
                                ),
                                class_name="mt-10 flex flex-col items-center justify-center p-8 border-2 border-dashed border-gray-300 rounded-2xl",
                            ),
                        ),
                    ),
                    class_name="mt-8",
                ),
                class_name="w-full text-center",
            ),
            class_name="container mx-auto p-4 sm:p-8 flex flex-col items-center justify-center min-h-screen",
        ),
        class_name="font-['JetBrains_Mono'] bg-gray-50",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, title="Weather Fetcher")