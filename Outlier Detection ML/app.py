from shiny import App, ui, reactive

# Header
header = ui.page_navbar(
    title="Outlier Detection ML",  
    id="page",  
    bg="dark",
)  

# Dropdown options
source_options = ["SQL", "Oracle", "GCP"]

# Card to select from DB sources
db_sources = ui.card(
                        ui.input_select("source", "Select Source", source_options, multiple=False),
                        ui.output_ui("db_inputs")
                     )

# Card to upload files
upload_file = ui.card(
                        ui.input_file("data_file", "Upload File", accept=".csv", multiple=False),
                    )

# Button to connect to DB
btn_connect = ui.div(
                    ui.input_action_button("connect_btn", "Connect / Upload", class_="btn btn-primary"),
                    class_="d-flex justify-content-center mt-3"
                )

# Card to select Data Source
data_source_selection = ui.card(
                ui.p("Select a Data Source", class_="text-center"),
                ui.layout_columns(
                    db_sources,
                    upload_file,
                    width = 1/2
                ),
                btn_connect,
            )

# Main UI
main_ui = ui.div(
    ui.div(
        data_source_selection,
        class_="mx-auto"
    ),
    class_="d-flex align-items-center justify-content-center min-vh-100"
)

# Footer
footer = ui.div(
    ui.hr(),
    ui.p("Copyright by PwC @ 2025", class_="text-center text-muted mb-2"),
    class_="mt-auto"
)

# App UI
def app_ui(response):
    return ui.page_fluid(
        header,
        main_ui,
        footer,
    )

# Server logic
def server(input, output, session):
    def db_inputs():
        if input.source() in ["SQL", "Oracle", "GCP"]:
            return ui.div(
                ui.input_text("server_name", "Server Name"),
                ui.input_text("db_name", "Database Name"),
                ui.input_text("username", "Username"),
                ui.input_password("password", "Password")
            )
        return ui.div()

app = App(app_ui, server)
