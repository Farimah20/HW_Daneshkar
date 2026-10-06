# Import ABC and abstractmethod to enable abstract class definition
from abc import ABC, abstractmethod

# Import Any and List type hints for flexible and readable type annotations
from typing import Any, List

# Import the re module to use regular expressions for punctuation removal
import re

# Import json module to read and write JSON files (used for saving/loading data)
import json

# 1. PipelineStep  (Abstract Base Class)

# Define the abstract base class that every pipeline step must inherit from
class PipelineStep(ABC):
    """
    An abstract base class representing a single step in a processing pipeline.
    """

    # Declare process as abstract — every subclass MUST implement this method
    @abstractmethod
    def process(self, data: Any) -> Any:
        """
        Processes the input data and returns the result.
        This method must be implemented by all concrete subclasses.
        """
        # pass is a placeholder; real logic lives in each concrete subclass
        pass

# 2. DataLoader  (Step 1 — load lines from a text file)

# Define DataLoader as a concrete subclass of PipelineStep
class DataLoader(PipelineStep):
    """
    Loads data from a text file, returning a list of lines.
    """

    # Override the abstract process method to implement file reading
    def process(self, filepath: str) -> List[str]:
        """
        Reads a file from the given filepath and returns its lines as a list of strings.
        Handles FileNotFoundError and other potential exceptions.
        """
        # Use try-except to safely handle file I/O errors
        try:
            # Open the file in read mode with UTF-8 encoding
            with open(filepath, "r", encoding="utf-8") as f:
                # Read all lines and strip trailing newline characters from each line
                lines = [line.rstrip("\n") for line in f.readlines()]
            # Return the cleaned list of lines
            return lines

        # Catch the specific error raised when the file does not exist
        except FileNotFoundError:
            # Inform the user that the file could not be found
            print(f"[DataLoader] Error: File not found — '{filepath}'")
            # Return an empty list so downstream steps receive a valid input
            return []

        # Catch any other unexpected exception during file reading
        except Exception as e:
            # Print the unexpected error message for debugging
            print(f"[DataLoader] Unexpected error: {e}")
            # Return an empty list as a safe fallback
            return []

# 3. Preprocessor  (Step 2 — clean / normalise text)

# Define Preprocessor as a concrete subclass of PipelineStep
class Preprocessor(PipelineStep):
    """
    Cleans a list of text strings by converting to lowercase, removing punctuation,
    and stripping extra whitespace.
    """

    # Constructor accepts a regex pattern that defines characters to remove
    def __init__(self, punctuation_to_remove: str = r'[^\w\s]'):
        # Compile the regex pattern once for efficient reuse across all lines
        self.punctuation_pattern = re.compile(punctuation_to_remove)

    # Override the abstract process method to implement text cleaning logic
    def process(self, data: List[str]) -> List[str]:
        """
        Applies cleaning steps to each string in the input list.
        """
        # Initialise an empty list to collect cleaned lines
        cleaned = []

        # Iterate over every line in the input data list
        for text in data:
            # Step 1: Convert the line to lowercase
            text = text.lower()

            # Step 2: Remove punctuation using the compiled regex pattern
            text = self.punctuation_pattern.sub(" ", text)

            # Step 3: Collapse multiple whitespace characters and strip leading/trailing spaces
            text = " ".join(text.split())

            # Append the fully cleaned line to the result list
            cleaned.append(text)

        # Return the list of all cleaned lines
        return cleaned

# 4. Analyzer  (Step 3 — compute basic text statistics)

# Define Analyzer as a concrete subclass of PipelineStep
class Analyzer(PipelineStep):
    """
    Analyzes the text data to compute basic statistics.
    """

    # Override the abstract process method to implement statistical analysis
    def process(self, data: List[str]) -> dict:
        """
        Calculates total lines, average words per line, and number of unique words.
        """
        # Handle the edge case where input is empty to avoid division by zero
        if not data:
            # Return zeroed statistics when no lines are present
            return {
                "total_lines": 0,
                "avg_length": 0.0,
                "unique_words": 0,
            }

        # Count the total number of lines in the dataset
        total_lines = len(data)

        # Build a flat list of all words by splitting each line on whitespace
        all_words = []
        # Loop through every line and extend the master word list
        for line in data:
            # Split the current line into individual words and add them to all_words
            all_words.extend(line.split())

        # Calculate the average number of words per line
        avg_length = len(all_words) / total_lines

        # Use a set to find unique words — sets automatically deduplicate elements
        unique_words = len(set(all_words))

        # Return all statistics packed into a dictionary, rounded to 2 decimal places
        return {
            "total_lines": total_lines,
            "avg_length": round(avg_length, 2),
            "unique_words": unique_words,
        }

# 5. ReportGenerator  (Output — print or save results)

# Define ReportGenerator — it is NOT a PipelineStep; it is a terminal output component
class ReportGenerator:
    """
    Generates and outputs reports from the analysis statistics.
    """

    # Method to print statistics to the standard console output
    def print_to_console(self, stats: dict):
        """
        Prints the statistics in a formatted way to the console.
        """
        # Print a decorative header separator
        print("\n" + "=" * 40)
        # Print the report title
        print("  AI Pipeline — Analysis Report")
        # Print a separator line below the title
        print("=" * 40)

        # Loop through every key-value pair in the statistics dictionary
        for key, value in stats.items():
            # Replace underscores with spaces and title-case the key for readability
            label = key.replace("_", " ").title()
            # Print the label and its value in an aligned format
            print(f"  {label:<20}: {value}")

        # Print a closing separator line
        print("=" * 40 + "\n")

    # Method to save statistics to a plain-text file on disk
    def save_to_file(self, stats: dict, filepath: str):
        """
        Saves the statistics in a formatted way to a text file.
        """
        # Use try-except to handle potential file write errors gracefully
        try:
            # Open (or create) the target file in write mode with UTF-8 encoding
            with open(filepath, "w", encoding="utf-8") as f:
                # Write the report header to the file
                f.write("=" * 40 + "\n")
                # Write the report title line
                f.write("  AI Pipeline — Analysis Report\n")
                # Write a separator line after the title
                f.write("=" * 40 + "\n")

                # Iterate over every key-value pair in the stats dictionary
                for key, value in stats.items():
                    # Format the key the same way as in the console output
                    label = key.replace("_", " ").title()
                    # Write one formatted line per statistic
                    f.write(f"  {label:<20}: {value}\n")

                # Write a closing separator at the end of the report file
                f.write("=" * 40 + "\n")

            # Confirm to the user that the report file was saved successfully
            print(f"[ReportGenerator] Report saved to '{filepath}'")

        # Catch any file-system or permission errors during writing
        except Exception as e:
            # Inform the user that saving the report failed
            print(f"[ReportGenerator] Failed to save report: {e}")

# 6. AIPipeline  (Orchestrator — run all steps in sequence)


# Define AIPipeline to orchestrate multiple PipelineStep objects in order
class AIPipeline:
    """
    Orchestrates a series of pipeline steps to process data.
    """

    # Constructor accepts a variable number of PipelineStep instances
    def __init__(self, *steps: PipelineStep):
        # Store the ordered collection of steps as an instance attribute
        self.steps = steps

    # run() executes all steps sequentially, chaining outputs to inputs
    def run(self, initial_input: Any) -> Any:
        """
        Executes all steps in the pipeline sequentially.
        """
        # Initialise the running data with the caller-provided starting value
        data = initial_input

        # Iterate over every step in the pipeline in insertion order
        for step in self.steps:
            # Retrieve the class name for informative progress logging
            step_name = step.__class__.__name__
            # Log which pipeline step is currently executing
            print(f"[AIPipeline] Running step: {step_name}")
            # Call process() on the current step and capture its output as the next input
            data = step.process(data)

        # Return the final transformed data after all steps have completed
        return data
