from markdown import Markdown


def markdown_to_html(body):
    md = Markdown(extensions=[
        'fenced_code',
        'tables'])
    content = md.convert(body)

    return content
