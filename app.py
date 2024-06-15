from dash import Dash, dcc, html, page_container, page_registry
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.YETI, dbc.icons.BOOTSTRAP])

navbar = dbc.Navbar(
            dbc.Container(
                [
                    dbc.Row([
                        dbc.Col([
                            dbc.NavbarBrand("Software-Product-Analysis-Specification-Project")
                        ], width={"size": "auto"})
                    ], align="center"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Nav([
                                dbc.NavItem(dbc.NavLink('Prova', href='/')),
                                dbc.NavItem(dbc.NavLink('AC1', href='/pg1')),
                                dbc.NavItem(dbc.NavLink('AC2', href='/pg2')),
                                dbc.NavItem(dbc.NavLink('AC3', href='/pg3'))
                            ], navbar=True
                            )
                        ], width={"size": "auto"})
                    ], align="center"),
                    dbc.Row([
                        dbc.Col(
                             dbc.Collapse(
                                dbc.Nav([
                                    dbc.NavItem(dbc.NavLink(html.I(className="bi bi-github"), href="https://github.com/LeonardoTeodoroSantos/Software-Product-Analysis-Specification-Project-Implementation.", external_link=True)),
                                    dbc.NavItem(dbc.NavLink(html.I(className="bi bi-youtube"), href="https://www.youtube.com/@LeonardoTeodorodosSantos/videos", external_link=True)),
                                ]
                                ),
                                id="navbar-collapse",
                                is_open=False,
                                navbar=True
                             )
                        )
                    ], align="center")
                ],
                fluid=True
            ),
            color="secondary"
)


app.layout = html.Div([
    navbar,
    page_container
])


if __name__ == "__main__":
    app.run(debug=True)

# dbc.NavItem(dbc.NavLink('Prova', href='/')),
#         dbc.NavItem(dbc.NavLink('AC1', href='/pg1')),
#         dbc.NavItem(dbc.NavLink('AC2', href='/pg2')),
#         dbc.NavItem(dbc.NavLink('AC3', href='/pg3')),
#         dbc.NavItem(dbc.NavLink(html.I(className="bi bi-github"), href="https://github.com/LeonardoTeodoroSantos/Software-Product-Analysis-Specification-Project-Implementation.", external_link=True)),
#         dbc.NavItem(dbc.NavLink(html.I(className="bi bi-youtube"), href="https://www.youtube.com/@LeonardoTeodorodosSantos/videos", external_link=True))

