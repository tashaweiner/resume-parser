# backend/main.py

from parser.parseFiles import parse_resumes
from search.searchParsed import search_and_rank, print_ranked

def main():
    print("👋 Welcome to Resume Parser + AI Search\n")

    # Step 1: Parse resumes into output/
    parse_resumes()

    # Step 2: Prompt user for question
    question = input("\n🔍 What do you want to find in the resumes?\n> ").strip()

    if question:
        results = search_and_rank(question)
        print_ranked(results)
    else:
        print("⚠️ No search query entered. Exiting.")

if __name__ == "__main__":
    main()
