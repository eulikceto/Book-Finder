from googlesearch import search
import click
import requests
import re

def get_pdf(url: str, filename: str) -> 'Downloads file from url':
    response = requests.get(url)    
    file = open(filename, 'wb')
    file.write(response.content)
    file.close()
    click.secho(f'{filename} downloaded', fg='green')

#args configuration
@click.command()
@click.argument('name', type=str, nargs=-1)
@click.option('-r','--results', type=int, default=10, help='Number of results', show_default=True)
@click.option('-d','--delay', type=int, default=2, help='Number of seconds to wait between searchs', show_default=True)
@click.option('-e', '--extension', type=str, default='pdf', help='File extension search', show_default=True)
@click.option('-D', '--download', is_flag=True, help='Download book as file')

def main(name,results,delay,extension,download):
    dork = lambda n, f: f'intext: {n} filetype:{f}' #generate the dorks to search
    get_name = lambda x, f: re.findall(fr'[\w_-]*.{f}', x)[0] if (re.search(fr'\w*.{f}', x)) else (f'{x.split("/")[-1]}.{f}')
    for l in search(dork(''.join(name), extension), tld="co.in", num=results, stop=results, pause=delay):
        click.secho(l, fg="yellow")
        if download: get_pdf(l, get_name(l, extension)) #if the flag Download is true, download the book
main()