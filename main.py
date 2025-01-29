# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/2025-01-29-This-Site-Is-Now-Powered-by-This-Notebook-Part-4.ipynb.

# %% auto 0
__all__ = ['app', 'rt', 'get_nb_paths', 'get_title_and_desc', 'get_date_from_iso8601_prefix', 'NBCard', 'mk_nbcard_from_nb_path',
           'index', 'StyledCode', 'StyledMd', 'StyledCell', 'notebook', 'versions', 'wellknown']

# %% nbs/2025-01-29-This-Site-Is-Now-Powered-by-This-Notebook-Part-4.ipynb 3
from datetime import datetime
from execnb.nbio import read_nb
from nb2fasthtml.core import render_code_output
from fasthtml.common import *
from fasthtml.jupyter import *
from importlib.metadata import distributions
from IPython.display import display, HTML
from monsterui import franken
from monsterui.all import Theme
import mistletoe
import pygments
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

# %% nbs/2025-01-29-This-Site-Is-Now-Powered-by-This-Notebook-Part-4.ipynb 6
app,rt = fast_app(pico=False)

# %% nbs/2025-01-29-This-Site-Is-Now-Powered-by-This-Notebook-Part-4.ipynb 9
def get_nb_paths(): 
    root = Path() if IN_NOTEBOOK else Path("nbs/")
    return L(root.glob("*.ipynb")).sorted(reverse=True)

# %% nbs/2025-01-29-This-Site-Is-Now-Powered-by-This-Notebook-Part-4.ipynb 11
def get_title_and_desc(fpath):
    nb = read_nb(fpath)
    title = nb.cells[0].source.lstrip("# ")
    desc = nb.cells[1].source
    return title,desc

# %% nbs/2025-01-29-This-Site-Is-Now-Powered-by-This-Notebook-Part-4.ipynb 13
def get_date_from_iso8601_prefix(fname):
    "Gets date from first 10 chars YYYY-MM-DD of `fname`, where `fname` is like `2025-01-12-Get-Date-From-This.whatever"
    try:
        return datetime.fromisoformat(str(fname)[0:10])
    except ValueError: return datetime.now()

# %% nbs/2025-01-29-This-Site-Is-Now-Powered-by-This-Notebook-Part-4.ipynb 17
def NBCard(title,desc,href,date):
    return A(
        franken.Card(
        franken.CardTitle(franken.H3(title)), 
        franken.P(f"{date:%a, %b %-d, %Y}", cls=franken.TextPresetsT.caption),
        franken.P(desc),
        body_cls='space-y-2'
    ), href=href)

# %% nbs/2025-01-29-This-Site-Is-Now-Powered-by-This-Notebook-Part-4.ipynb 18
def mk_nbcard_from_nb_path(nb_path):
    date = get_date_from_iso8601_prefix(nb_path.name) or datetime.now()
    return NBCard(*get_title_and_desc(nb_path), href=f'/nbs/{nb_path.name[:-6]}', date=date)

# %% nbs/2025-01-29-This-Site-Is-Now-Powered-by-This-Notebook-Part-4.ipynb 20
@rt
def index():
    nb_paths = get_nb_paths()
    return (
        Theme.blue.headers(),
        Title("audrey.feldroy.com"),
        franken.Container(
            Div(
                franken.H1('audrey.feldroy.com'), franken.P("The experimental Jupyter notebooks of Audrey M. Roy Greenfeld. This website and all its notebooks are open-source at ", franken.A("github.com/audreyfeldroy/arg-blog-fasthtml", href="https://github.com/audreyfeldroy/arg-blog-fasthtml"), cls="mb-6"),
            ),
            franken.Grid(*nb_paths.map(mk_nbcard_from_nb_path), cols_sm=1, cols_md=1, cols_lg=2, cols_xl=3)
        )
    )

# %% nbs/2025-01-29-This-Site-Is-Now-Powered-by-This-Notebook-Part-4.ipynb 22
def StyledCode(c, style='monokai'):
    fm = HtmlFormatter(style=style, cssclass=style, prestyles="padding:10px 0;")
    h = highlight(c, PythonLexer(), fm)
    sd = fm.get_style_defs(f".{style}")
    return Style(sd), NotStr(h)

# %% nbs/2025-01-29-This-Site-Is-Now-Powered-by-This-Notebook-Part-4.ipynb 23
def StyledMd(m):
    return Safe(mistletoe.markdown(m))

# %% nbs/2025-01-29-This-Site-Is-Now-Powered-by-This-Notebook-Part-4.ipynb 24
def StyledCell(c):
    if c.cell_type == "markdown": return StyledMd(c.source)
    if c.cell_type == "code": 
        if not c.outputs: return StyledCode(c.source)
        return StyledCode(c.source), render_code_output(c)

# %% nbs/2025-01-29-This-Site-Is-Now-Powered-by-This-Notebook-Part-4.ipynb 26
@rt("/nbs/{name}")
def notebook(name:str):
#     root = Path() if IN_NOTEBOOK else Path("nbs/")
    fname = f"{name}.ipynb" if IN_NOTEBOOK else f"nbs/{name}.ipynb"
    fpath = Path(fname)
    nb = read_nb(fpath)
    title = nb.cells[0].source.lstrip("# ")
    date = get_date_from_iso8601_prefix(fname.lstrip("nbs/"))
    desc = nb.cells[1].source
    if "MonsterUI" in title:
        return (
            Theme.slate.headers(),
            Title(title),
            franken.Container(
                Header(
                    franken.H1(title),
                    franken.P(f"by Audrey M. Roy Greenfeld | {date:%a, %b %-d, %Y}", cls=(franken.TextPresetsT.subheading, franken.PaddingT.lg, "m-b-10")),
                    franken.P(desc),
                    Hr()
                ),
                *L(nb.cells[2:]).map(StyledCell),
                cls="space-y-5"
            )
    )
    return (
        Style(':root {font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", sans-serif; color-scheme: light dark;} body {background-color: light-dark(#ffffff, #1a1a1a); color: light-dark(#1a1a1a, #ffffff);} p {line-height: 1.5;}'),
        Title(title),
        Div(
            H1(title), # Title
            P(Small(f"by Audrey M. Roy Greenfeld | {date:%a, %b %-d, %Y}")),
            P(desc),
            Hr(),
            *L(nb.cells[2:]).map(StyledCell),
            cls="space-y-5"
        )
    )

# %% nbs/2025-01-29-This-Site-Is-Now-Powered-by-This-Notebook-Part-4.ipynb 28
@rt
def versions():
    dists = L([NS(name=dist.metadata['Name'], version=dist.version) for dist in distributions()]).sorted('name')
    dists = [Li(f'{d.name}: {d.version}') for d in dists]
    return (Title('Python Package Versions'),
        Style(':root {font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", sans-serif; color-scheme: light dark;} body {background-color: light-dark(#ffffff, #1a1a1a); color: light-dark(#1a1a1a, #ffffff);} p {line-height: 1.5;}'),   
        Div(
            H1('Python Package Versions'),
            Ul(*dists)          
        )       
    )

# %% nbs/2025-01-29-This-Site-Is-Now-Powered-by-This-Notebook-Part-4.ipynb 30
@rt('/.well-known/{fname}')
def wellknown(fname: str):
    fpath = f"../.well-known/{fname}" if IN_NOTEBOOK else f".well-known/{fname}"
    return Path(fpath).read_text()

# %% nbs/2025-01-29-This-Site-Is-Now-Powered-by-This-Notebook-Part-4.ipynb 32
serve()
