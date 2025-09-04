import marimo

__generated_with = "0.15.1"
app = marimo.App(width="full")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    from markmap_anywidget import MarkmapWidget

    # from https://gist.githubusercontent.com/raw/af76a4c245b302206b16aec503dbe07b/markmap.md
    markmap_markdown = r"""---
    title: markmap
    markmap:
      colorFreezeLevel: 2
      activeNode:
        placement: center
      maxWidth: 300
    ---

    ## Links

    - [Website](https://markmap.js.org/)
    - [GitHub](https://github.com/gera2ld/markmap)

    ## Related Projects

    - [coc-markmap](https://github.com/gera2ld/coc-markmap) for Neovim
    - [markmap-vscode](https://marketplace.visualstudio.com/items?itemName=gera2ld.markmap-vscode) for VSCode
    - [eaf-markmap](https://github.com/emacs-eaf/eaf-markmap) for Emacs

    ## Features

    Note that if blocks and lists appear at the same level, the lists will be ignored.

    ### Lists

    - **strong** ~~del~~ *italic* ==highlight==
    - `inline code`
    - [x] checkbox
    - Katex: $x = {-b \pm \sqrt{b^2-4ac} \over 2a}$ <!-- markmap: fold -->
      - [More Katex Examples](#?d=gist:af76a4c245b302206b16aec503dbe07b:katex.md)
    - Now we can wrap very very very very long text with the `maxWidth` option
    - Ordered list
      1. item 1
      2. item 2

    ### Blocks

    ```js
    console.log('hello, JavaScript')
    ```

    | Products | Price |
    |-|-|
    | Apple | 4 |
    | Banana | 2 |

    ![](https://markmap.js.org/favicon.png)"""
    return MarkmapWidget, markmap_markdown, mo


@app.cell(hide_code=True)
def _(markmap_markdown, mo):
    text_area = mo.ui.text_area(value=markmap_markdown, rows=50, full_width=True)
    return (text_area,)


@app.cell(hide_code=True)
def _(MarkmapWidget, mo, text_area):
    widget = mo.ui.anywidget(MarkmapWidget(markdown_content=text_area.value))
    return (widget,)


@app.cell(hide_code=True)
def _(mo, text_area, widget):
    mo.hstack(items=[text_area, widget], widths="equal")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
