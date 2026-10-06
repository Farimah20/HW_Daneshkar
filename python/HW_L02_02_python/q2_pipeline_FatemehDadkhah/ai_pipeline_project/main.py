# Import all required classes from the pipeline module
from pipeline import (
    DataLoader,
    Preprocessor,
    Analyzer,
    ReportGenerator,
    AIPipeline
)

# Only run the following code when this script is executed directly (not imported)
if __name__ == "__main__":

    #Component Definitions

    # Create a DataLoader instance — responsible for reading lines from a text file
    loader = DataLoader()

    # Create a Preprocessor instance — lowercases text, removes punctuation and extra spaces
    preprocessor = Preprocessor()

    # Create an Analyzer instance — computes total lines, avg words, and unique words
    basic_analyzer = Analyzer()

    # Create a ReportGenerator instance — prints and/or saves the final report
    reporter = ReportGenerator()

    # Define the path to the sample input text file that the pipeline will process
    input_filepath = "sample_data.txt"

    # Pipeline

    # Print a section header to clearly mark the start of pipeline execution
    print("\n--- Running Pipeline ---")

    # Build the pipeline by chaining: DataLoader → Preprocessor → Analyzer
    basic_pipeline = AIPipeline(loader, preprocessor, basic_analyzer)

    # Execute the pipeline with the input file path as the starting value
    basic_results = basic_pipeline.run(input_filepath)

    # Print the resulting statistics to the console in a formatted layout
    reporter.print_to_console(basic_results)

    # Save the same statistics to a text file for later review
    reporter.save_to_file(basic_results, "report.txt")
