import click
import subprocess, json, requests, datetime

@click.group()
def cli():
    """Bouvet CLI
    Dette er eit enkelt CLI som kan gjere eit par enkle ting.
    """

@cli.command()
@click.argument("namn", type=str, nargs=1)
def hei(namn: str):
    """Seiar hei til <NAMN>."""
    click.echo(f"Hei, {namn}!")

@cli.command()
def gs():
    """Snarveg for 'git status'."""
    subprocess.call("git status")

@cli.command()
def branch():
    """Snarveg for å finne noverande branch."""
    resultat = subprocess.check_output("git status")
    resultat = resultat.decode("utf8").split("\n")[0].replace("On branch ", "")
    click.echo(f"Du er på branch '{resultat}'.")

@cli.command()
@click.argument("sider", type=int, nargs=1)
def rull(sider: int):
    """Rull ein terning med kor enn mange sidar du treng."""
    import random
    rulla = random.randint(1, sider)
    click.echo(f"Du rulla {rulla}")

    if rulla == sider:
        click.echo("Perfekt rull!")
    if rulla == 1:
        click.echo("Uff då...")

@cli.command()
@click.option("-d", "--dag", default=None, help="Dagen du vil sjekke lunsjen for", required=False)
@click.option("-o", "--oppe", is_flag=True, default=False, help="Kantina i Solheimsgaten 13", required=False)
@click.option("-n", "--nede", is_flag=True, default=False, help="Kantina i Skipsbyggerhallen", required=False)
def lunsj(dag: str, oppe: bool, nede: bool):
    """Finn ut kva det er til lunsj i dag."""
    if oppe is False and nede is False:
        oppe, nede = True, True

    base_url = "https://kantinemeny.azurewebsites.net/ukesmeny"
    oppe_url = f"{base_url}?lokasjon=TFN.Solheimsgaten13@toma.no"
    oppe_suppe = f"{base_url}suppe?lokasjon=TFN.Solheimsgaten13@toma.no"

    nede_url = f"{base_url}?lokasjon=skipsbyggerhallen@albatross-as.no"
    nede_suppe = f"{base_url}suppe?lokasjon=skipsbyggerhallen@albatross-as.no"
