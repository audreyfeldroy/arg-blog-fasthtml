# Generated from 2025-01-23-Using-My-Blog-to-Rewrite-Itself.ipynb then edited manually

# %% auto 0
__all__ = ['app', 'rt', 'get_nb_paths', 'get_title_and_desc', 'get_date_from_iso8601_prefix', 'NBCard', 'mk_nbcard_from_nb_path',
           'index', 'StyledCode', 'StyledMd', 'StyledCell', 'notebook']

# %% 2025-01-23-Using-My-Blog-to-Rewrite-Itself.ipynb 3
from datetime import datetime
from execnb.nbio import read_nb
from nb2fasthtml.core import render_code_output
from fasthtml.common import *
from fasthtml.jupyter import *
from IPython.display import display, HTML
from monsterui import franken
from monsterui.all import Theme
import mistletoe
import pygments
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

# %% 2025-01-23-Using-My-Blog-to-Rewrite-Itself.ipynb 8
app,rt = fast_app(pico=False)

# %% 2025-01-23-Using-My-Blog-to-Rewrite-Itself.ipynb 14
def get_nb_paths(): return L(sorted(Path().glob("nbs/*.ipynb"), reverse=True))

# %% 2025-01-23-Using-My-Blog-to-Rewrite-Itself.ipynb 19
def get_title_and_desc(fpath):
    nb = read_nb(fpath)
    title = nb.cells[0].source.lstrip("# ")
    desc = nb.cells[1].source
    return title,desc

# %% 2025-01-23-Using-My-Blog-to-Rewrite-Itself.ipynb 27
def get_date_from_iso8601_prefix(fname):
    "Gets date from first 10 chars YYYY-MM-DD of `fname`, where `fname` is like `2025-01-12-Get-Date-From-This.whatever"
    try:
        return datetime.fromisoformat(str(fname)[4:14])
    except ValueError: return None

# %% 2025-01-23-Using-My-Blog-to-Rewrite-Itself.ipynb 36
def NBCard(title,desc,href,date):
    return A(
        franken.Card(
        franken.CardTitle(franken.H3(title)), 
        franken.PSmall(f"{date:%a, %b %-d, %Y}", cls="uk-text-muted"),
        franken.P(desc),
        body_cls='space-y-2'
    ), href=href)

# %% 2025-01-23-Using-My-Blog-to-Rewrite-Itself.ipynb 37
def mk_nbcard_from_nb_path(nb_path):
    date = get_date_from_iso8601_prefix(nb_path)
    return NBCard(*get_title_and_desc(nb_path), href=f'/nbs/{nb_path.name[:-6]}', date=date)

# %% 2025-01-23-Using-My-Blog-to-Rewrite-Itself.ipynb 41
@rt
def index():
    nb_paths = get_nb_paths()
    return (
        Theme.blue.headers(),
        Title("audrey.feldroy.com"),
        franken.Container(
            Div(
                franken.H1('audrey.feldroy.com'), franken.PParagraph("The experimental Jupyter notebooks of Audrey M. Roy Greenfeld. This website and all its notebooks are open-source at ", franken.A("github.com/audreyfeldroy/arg-blog-fasthtml", href="https://github.com/audreyfeldroy/arg-blog-fasthtml"), cls="mb-6"),
            ),
            franken.Grid(*nb_paths.map(mk_nbcard_from_nb_path), cols_sm=1, cols_md=1, cols_lg=2, cols_xl=3)
        )
    )

# %% 2025-01-23-Using-My-Blog-to-Rewrite-Itself.ipynb 50
def StyledCode(c, style='monokai'):
    fm = HtmlFormatter(style=style, cssclass=style)
    h = highlight(c, PythonLexer(), fm)
    sd = fm.get_style_defs(f".{style}")
    return Div(Style(sd), NotStr(h), id=style)

# %% 2025-01-23-Using-My-Blog-to-Rewrite-Itself.ipynb 55
def StyledMd(m):
    return Safe(mistletoe.markdown(m))

# %% 2025-01-23-Using-My-Blog-to-Rewrite-Itself.ipynb 59
def StyledCell(c):
    if c.cell_type == "markdown": return StyledMd(c.source)
    if c.cell_type == "code": 
        if not c.outputs: return StyledCode(c.source)
        return StyledCode(c.source), render_code_output(c)

# %% 2025-01-23-Using-My-Blog-to-Rewrite-Itself.ipynb 63
@rt("/nbs/{name}")
def notebook(name:str):
    fpath = Path(f'nbs/{name}.ipynb')
    nb = read_nb(fpath)
    title = nb.cells[0].source.lstrip("# ")
    desc = nb.cells[1].source
    if "MonsterUI" in title:
        return (
            Theme.slate.headers(),
            Title(title),
            franken.Container(
                franken.H1(title), # Title
                franken.P(desc), # Desc
                *L(nb.cells[2:]).map(StyledCell),
                cls="space-y-5"
            )
    )
    return (
        Style(':root {font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", sans-serif; color-scheme: light dark;} body {background-color: light-dark(#ffffff, #1a1a1a); color: light-dark(#1a1a1a, #ffffff);} p {line-height: 1.5;}'),
        Title(title),
        Div(
            H1(title), # Title
            P(desc), # Desc
            *L(nb.cells[2:]).map(StyledCell),
            cls="space-y-5"
        )
    )

# %% 2025-01-23-Using-My-Blog-to-Rewrite-Itself.ipynb 77
serve()
