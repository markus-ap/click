import click
from click import progressbar
from flask import Flask
import subprocess, json, requests, datetime

app = Flask("Bouvet")

@click.group()
def cli():
    """Bouvet CLI
    Dette er eit enkelt CLI som kan gjere eit par enkle ting.
    """

@cli.command()
@click.argument("namn", type=str, nargs=1)
@app.route("/hei/<namn>", methods=["GET"])
def hei(namn: str):
    """Seiar hei til <NAMN>."""
    resultat = f"Hei, {namn}!"
    click.echo(resultat)
    return {"melding": resultat}

@cli.command()
def hallo():
    """Seiar hallo til deg, og spør om namnet ditt."""
    namn = click.prompt("Hallo, der! Kva er namnet ditt?")

    if namn[0] == namn[0].lower():
        nytt_namn = namn[0].upper() + namn[1:]
        svar = click.confirm(f"Heitar du egenleg {nytt_namn}?", default=False)
        if svar:
            namn = nytt_namn

    click.echo(f"Hallo, {namn}! Hyggleg å møte deg.")

@cli.command()
def last_inn():
    """Laster inn noko treigt."""
    from time import sleep

    click.echo("Byrjar innlastning...")
    with progressbar(range(5)) as liste:
        for ting in liste:
            sleep(1)
    click.echo("Ferdig med innlasting!")
    

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

    nede_url = f"{base_url}?lokasjon=skipsbyggerhallen@albatross-as.no"

    if dag is not None:    
        dag = dag.lower()
        vekedagar = ["mandag", "tysdag", "tirsdag", "onsdag", "torsdag", "fredag"]
        helgedagar = ["lørdag", "laurdag", "sundag", "søndag"]
        gyldige_dagar = vekedagar + helgedagar
        
        if dag not in gyldige_dagar:
            click.echo(f"Kjenner ikkje til dagen {dag}.")
            return
        
        if dag in helgedagar:
            click.echo("Ingen lunsj i helga.")
            return   
        
        nynorsk = {
            "tysdag": "tirsdag",
            "laurdag": "lørdag",
            "sundag": "søndag"
        }
        if dag in nynorsk:
            dag = nynorsk[dag]

    else:
        tidspunkt = datetime.datetime.now().hour
        idag = datetime.date.today()
        if tidspunkt > 13:
            idag = idag + datetime.timedelta(days=1)
            
        dag = idag.strftime('%A')   
        dagsnamn = {
            "Monday": "MANDAG",
            "Tuesdag": "TIRSDAG",
            "Wednesday": "ONSDAG",
            "Thursday": "TORSDAG",
            "Friday": "FREDAG"
        }
        if dag not in dagsnamn:
            click.echo("Ingen lunsj i helga.")
            return
        dag = dagsnamn[dag]

    dag = dag.upper()
    
    click.echo(f"Mat for {dag.lower()}")
    if oppe:
        click.echo("Oppe:")
        oppe_lunsj, oppe_suppe = hent_lunsj(oppe_url, dag)
        click.echo(f"Varmmat: {oppe_lunsj}")
        click.echo(f"Suppe: {oppe_suppe}\n")

    if nede:
        click.echo("Nede:")
        nede_lunsj, nede_suppe = hent_lunsj(nede_url, dag)
        click.echo(f"Varmmat: {nede_lunsj}")
        click.echo(f"Suppe: {nede_suppe}")


def hent_lunsj(sti: str, idag: str) -> str:
    idag = idag.lower()
    days = {
        "mandag": "monday",
        "tirsdag": "tuesday",
        "onsdag":  "wednesday",
        "torsdag": "thursday",
        "fredag": "friday"
    }
    if idag in days:
        idag = days[idag]
    from bs4 import BeautifulSoup
    resultat = requests.get(sti)
    suppe = BeautifulSoup(resultat.text, "html.parser")

    js = suppe.find("script").text
    js = js.replace("var uke = ", "").strip()[:-1]
    js = json.loads(js)
    dagensmat = js[idag]

    varm = dagensmat["h_navn"]
    grat = dagensmat["h_garnityr"]
    suppe = dagensmat["s_navn"]
    if grat is None: grat = ""
    if varm is None: varm = ""
    if suppe is None: suppe = ""

    varm = varm.strip()
    grat = grat.strip()
    suppe = suppe.strip()

    return f"{varm} {grat}", suppe


if __name__ == "__main__":
    app.run()