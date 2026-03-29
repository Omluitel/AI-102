import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.prompt import Prompt

# Initialize the Rich console
console = Console()

def authenticate_client(endpoint, key):
    return TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def display_sentiment(response):
    """Creates a clean, color-coded terminal table for the results."""
    sentiment = response.sentiment
    scores = response.confidence_scores
    
    # Determine color theme based on sentiment
    theme_color = "green" if sentiment == "positive" else "yellow" if sentiment == "neutral" else "red"
    
    # Build the table
    table = Table(title=f"[bold {theme_color}]Analysis Result[/bold {theme_color}]", border_style=theme_color)
    table.add_column("Sentiment Category", style="cyan")
    table.add_column("Confidence Score", justify="right")
    
    table.add_row("Positive", f"{scores.positive:.0%}")
    table.add_row("Neutral", f"{scores.neutral:.0%}")
    table.add_row("Negative", f"{scores.negative:.0%}")
    
    # Print the result inside a nice box
    console.print(Panel(table, title=f"[bold white]{sentiment.upper()}[/bold white]", expand=False, border_style=theme_color))

def main():
    # Replace with your actual key if the one below is expired/inactive
    endpoint = ""
    key = ""
    
    try:
        client = authenticate_client(endpoint, key)
        
        # Header UI
        console.print(Panel.fit(
            "[bold cyan]Azure AI Sentiment Terminal[/bold cyan]\n[dim]Type 'quit' or 'exit' to stop[/dim]", 
            border_style="cyan"
        ))

        while True:
            # 1. Ask for input
            text = Prompt.ask("\n[bold white]What's on your mind?[/bold white]")
            
            if text.lower() in ["exit", "quit"]:
                console.print("[italic yellow]Shutting down... Goodbye![/italic yellow]")
                break
            
            if not text.strip():
                continue

            # 2. Show a loading spinner while Azure processes
            with console.status("[bold green]Consulting the AI..."):
                try:
                    result = client.analyze_sentiment([text])[0]
                    # 3. Present the data
                    display_sentiment(result)
                except Exception as e:
                    console.print(f"[bold red]API Error:[/bold red] {e}")

    except Exception as e:
        console.print(f"[bold red]Auth Error:[/bold red] Check your Key and Endpoint.")

if __name__ == "__main__":
    main()