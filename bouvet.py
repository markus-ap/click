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

@cli.command()
def fail():
    result = subprocess.run("dotnet build", capture_output=True, shell=True, cwd="./../../equinor/bravo-api/terraform/bravo-webapi/main")
    
    print(result)
    if result.returncode != 0:
        click.echo("Wow! It failed, wtf.")
        #click.echo(result.stderr.decode())
    else:
        click.echo("It worked!")
        #click.echo(result.stdout.decode())
    

@cli.command()
def test():
    import os
    result = subprocess.check_output(f"echo %PATH%", shell=True)
    paths = result.decode().split(";")
    terraform_path = [path for path in paths if "terraform" in path]

    if len(terraform_path) < 1:
        print("Found no path containing terraform")
        return
    elif len(terraform_path) > 1:
        print("Found more than one path.")
        for index, path in enumerate(terraform_path):
            print(index, path)
        valid_indexes = [str(i) for i in range(0, len(terraform_path))]
        index = click.prompt("Please select index of path.", type=click.Choice(valid_indexes))
        terraform_path = terraform_path[int(index)]
    else:
        terraform_path= terraform_path[0]

    files = os.listdir(terraform_path)
    files = [file for file in files if file == "terraform.exe"]

    if len(files) < 1:
        print("Found no file called terraform.exe. Is it called something else?")
        
        files = os.listdir(terraform_path)
        for index, file in enumerate(files):
            print(index, file)
        valid_indexes = [str(i) for i in range(0, len(files))] + [str(-1)]
        index = click.prompt("Please select index of file.", type=click.Choice(valid_indexes))
        file = files[int(index)]
    elif len(files) > 1:
        print("Found more than one terraform.exe file.")
        for index, file in enumerate(files):
            print(index, file)
        valid_indexes = [str(i) for i in range(0, len(files))]
        index = click.prompt("Please select index of path.", type=click.Choice(valid_indexes))
        file = files[int(index)]
    else:
        file = files[0]
    
    download_terraform(terraform_path)
    
    print(file)

def download_terraform(download_to: str):
    import shutil, os
    from zipfile import ZipFile
    response = requests.get("https://releases.hashicorp.com/terraform/1.6.3/terraform_1.6.3_windows_386.zip")
    with open("terraform_latest.zip", mode="wb") as file:
        file.write(response.content)
    
    with ZipFile("terraform_latest.zip", "r") as zObject:
        zObject.extractall("terraform_download")
    os.remove(f"{download_to}/terraform.exe")
    shutil.move("./terraform_download/terraform.exe", download_to)

    os.remove("terraform_latest.zip")
    os.rmdir("terraform_download")
    

    

