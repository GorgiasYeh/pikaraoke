"""Tests for the phone's More page."""

from pikaraoke.routes.home import home_bp
from tests.conftest import make_route_app


def _more_page(admin: bool) -> str:
    app = make_route_app(home_bp, [], admin=admin)
    app.config["SITE_NAME"] = "PiKaraoke"
    client = app.test_client()
    response = client.get("/more")
    assert response.status_code == 200
    return response.get_data(as_text=True)


def test_more_page_lists_the_menu_pages():
    body = _more_page(admin=False)
    list_html = body[body.index('class="more-list"') :]
    for path in ("/rankings", "/history", "/settings", "/info"):
        assert f'class="panel-block" href="{path}"' in list_html


def test_more_page_shows_sessions_to_the_host_only():
    assert 'class="panel-block" href="/sessions"' in _more_page(admin=True)
    assert 'class="panel-block" href="/sessions"' not in _more_page(admin=False)


def test_more_tab_stays_lit_on_the_pages_it_opens():
    body = _more_page(admin=False)
    assert 'data-nav="more rankings history sessions settings info"' in body
