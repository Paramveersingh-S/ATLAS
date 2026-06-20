import click
from scripts.benchmark_turboquant import run_benchmarks

@click.group()
def cli():
    """ATLAS Command Line Interface"""
    pass

@cli.command()
@click.argument('path', type=click.Path(exists=True))
def ingest(path):
    """Ingest a file or directory into the knowledge base"""
    click.echo(f"Ingesting {path}...")
    click.echo("Done.")

@cli.command()
def chat():
    """Start an interactive chat session"""
    click.echo("Starting ATLAS chat... (Press Ctrl+C to exit)")
    while True:
        try:
            q = input("\nYou: ")
            print("ATLAS: ...")
        except KeyboardInterrupt:
            break

@cli.command()
@click.argument('query')
def search(query):
    """Run semantic search over the index"""
    click.echo(f"Searching for: {query}")
    
@cli.command()
def stats():
    """Print compression statistics"""
    click.echo("TurboQuant Stats:")

@cli.command()
def benchmark():
    """Run TurboQuant benchmarks"""
    run_benchmarks()

if __name__ == "__main__":
    cli()
