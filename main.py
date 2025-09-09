#!/usr/bin/env python3
"""Main entry point for the SQL Agent with Synthetic Data Generation."""

import sys
import os
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from agent import SQLAgent


def main():
    """Main function to run the SQL Agent."""
    try:
        agent = SQLAgent()
        agent.run_interactive()
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"Error starting agent: {str(e)}")
        print("Make sure you have set up your .env file with GRADIENT_ACCESS_TOKEN and GRADIENT_WORKSPACE_ID")


if __name__ == "__main__":
    main()
