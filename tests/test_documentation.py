"""Test all documentation examples to ensure they work correctly.

This test suite validates that all Python code examples in the documentation
use the correct API and execute without errors. This provides better visibility
than pytest-markdown-docs plugin alone.
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

import pytest


class TestDocumentationExamples:
    """Test all documentation examples for correctness."""

    @staticmethod
    def get_documentation_files() -> List[Path]:
        """Get all documentation files that should contain Python examples."""
        docs_dir = Path(__file__).parent.parent / "docs"
        readme = Path(__file__).parent.parent / "README.md"

        doc_files: List[Path] = []

        # Add README if it exists
        if readme.exists():
            doc_files.append(readme)

        # Add all markdown files in docs/
        if docs_dir.exists():
            doc_files.extend(docs_dir.rglob("*.md"))

        return sorted(doc_files)

    @staticmethod
    def run_markdown_docs_test(file_path: Path) -> Tuple[bool, str, int]:
        """
        Run pytest-markdown-docs on a specific file.

        Returns:
            Tuple of (success, output, test_count)
        """
        cmd = [
            sys.executable,
            "-m",
            "pytest",
            str(file_path),
            "--markdown-docs",
            "--tb=short",
            "-v",
        ]

        try:
            # Always run from project root
            project_root = Path(__file__).parent.parent
            result = subprocess.run(
                cmd, capture_output=True, text=True, cwd=project_root
            )

            # Count how many tests were collected - look for CodeFence patterns
            test_count = 0
            lines = result.stdout.split("\n")
            for line in lines:
                if "[CodeFence#" in line:
                    test_count += 1

            success = result.returncode == 0
            output = result.stdout + result.stderr

            return success, output, test_count

        except Exception as e:
            return False, f"Error running test: {e}", 0

    def test_readme_examples(self):
        """Test that all Python examples in README.md work correctly."""
        readme = Path(__file__).parent.parent / "README.md"

        if not readme.exists():
            pytest.skip("README.md not found")

        success, output, test_count = self.run_markdown_docs_test(readme)

        if test_count == 0:
            pytest.skip("No Python code blocks found in README.md")

        if not success:
            pytest.fail(
                f"README.md documentation tests failed ({test_count} tests):\n"
                f"Run: uv run pytest README.md --markdown-docs\n\n"
                f"Output:\n{output}"
            )

    def test_main_index_examples(self):
        """Test that all Python examples in docs/index.md work correctly."""
        index_file = Path(__file__).parent.parent / "docs" / "index.md"

        if not index_file.exists():
            pytest.skip("docs/index.md not found")

        success, output, test_count = self.run_markdown_docs_test(index_file)

        if test_count == 0:
            pytest.skip("No Python code blocks found in docs/index.md")

        if not success:
            pytest.fail(
                f"docs/index.md documentation tests failed ({test_count} tests):\n"
                f"Run: uv run pytest docs/index.md --markdown-docs\n\n"
                f"Output:\n{output}"
            )

    def test_api_documentation_examples(self):
        """Test that all Python examples in API documentation work correctly."""
        api_dir = Path(__file__).parent.parent / "docs" / "api"

        if not api_dir.exists():
            pytest.skip("docs/api/ directory not found")

        api_files = list(api_dir.rglob("*.md"))
        if not api_files:
            pytest.skip("No markdown files found in docs/api/")

        failed_files: List[Tuple[Path, str, int]] = []
        total_tests = 0

        for api_file in api_files:
            success, output, test_count = self.run_markdown_docs_test(api_file)
            total_tests += test_count

            if test_count > 0 and not success:
                failed_files.append((api_file, output, test_count))

        if total_tests == 0:
            pytest.skip("No Python code blocks found in API documentation")

        if failed_files:
            error_msg = (
                f"API documentation tests failed in {len(failed_files)} files:\n\n"
            )

            for file_path, output, test_count in failed_files:
                rel_path = file_path.relative_to(Path(__file__).parent.parent)
                error_msg += f"❌ {rel_path} ({test_count} tests failed)\n"
                error_msg += f"   Run: uv run pytest {rel_path} --markdown-docs\n\n"

            # Show output for first failed file
            if failed_files:
                first_file, first_output, _ = failed_files[0]
                error_msg += f"Sample output from {first_file.name}:\n{first_output}\n"

            pytest.fail(error_msg)

    def test_guide_documentation_examples(self):
        """Test that all Python examples in guide documentation work correctly."""
        guide_dir = Path(__file__).parent.parent / "docs" / "guide"

        if not guide_dir.exists():
            pytest.skip("docs/guide/ directory not found")

        guide_files = list(guide_dir.rglob("*.md"))
        if not guide_files:
            pytest.skip("No markdown files found in docs/guide/")

        # Skip pydantic.md if pydantic is not installed
        try:
            import pydantic
        except ImportError:
            guide_files = [f for f in guide_files if f.name != "pydantic.md"]

        failed_files: List[Tuple[Path, str, int]] = []
        total_tests = 0

        for guide_file in guide_files:
            success, output, test_count = self.run_markdown_docs_test(guide_file)
            total_tests += test_count

            if test_count > 0 and not success:
                failed_files.append((guide_file, output, test_count))

        if total_tests == 0:
            pytest.skip("No Python code blocks found in guide documentation")

        if failed_files:
            error_msg = (
                f"Guide documentation tests failed in {len(failed_files)} files:\n\n"
            )

            for file_path, output, test_count in failed_files:
                rel_path = file_path.relative_to(Path(__file__).parent.parent)
                error_msg += f"❌ {rel_path} ({test_count} tests failed)\n"
                error_msg += f"   Run: uv run pytest {rel_path} --markdown-docs\n\n"

            pytest.fail(error_msg)

    def test_getting_started_examples(self):
        """Test that all Python examples in getting-started documentation work correctly."""
        getting_started_dir = Path(__file__).parent.parent / "docs" / "getting-started"

        if not getting_started_dir.exists():
            pytest.skip("docs/getting-started/ directory not found")

        getting_started_files = list(getting_started_dir.rglob("*.md"))
        if not getting_started_files:
            pytest.skip("No markdown files found in docs/getting-started/")

        failed_files: List[Tuple[Path, str, int]] = []
        total_tests = 0

        for gs_file in getting_started_files:
            success, output, test_count = self.run_markdown_docs_test(gs_file)
            total_tests += test_count

            if test_count > 0 and not success:
                failed_files.append((gs_file, output, test_count))

        if total_tests == 0:
            pytest.skip("No Python code blocks found in getting-started documentation")

        if failed_files:
            error_msg = f"Getting-started documentation tests failed in {len(failed_files)} files:\n\n"

            for file_path, output, test_count in failed_files:
                rel_path = file_path.relative_to(Path(__file__).parent.parent)
                error_msg += f"❌ {rel_path} ({test_count} tests failed)\n"
                error_msg += f"   Run: uv run pytest {rel_path} --markdown-docs\n\n"

            pytest.fail(error_msg)

    def test_examples_documentation(self):
        """Test that all Python examples in examples documentation work correctly."""
        examples_dir = Path(__file__).parent.parent / "docs" / "examples"

        if not examples_dir.exists():
            pytest.skip("docs/examples/ directory not found")

        example_files = list(examples_dir.rglob("*.md"))
        if not example_files:
            pytest.skip("No markdown files found in docs/examples/")

        failed_files: List[Tuple[Path, str, int]] = []
        total_tests = 0

        for example_file in example_files:
            success, output, test_count = self.run_markdown_docs_test(example_file)
            total_tests += test_count

            if test_count > 0 and not success:
                failed_files.append((example_file, output, test_count))

        if total_tests == 0:
            pytest.skip("No Python code blocks found in examples documentation")

        if failed_files:
            error_msg = (
                f"Examples documentation tests failed in {len(failed_files)} files:\n\n"
            )

            for file_path, output, test_count in failed_files:
                rel_path = file_path.relative_to(Path(__file__).parent.parent)
                error_msg += f"❌ {rel_path} ({test_count} tests failed)\n"
                error_msg += f"   Run: uv run pytest {rel_path} --markdown-docs\n\n"

            pytest.fail(error_msg)

    def test_development_documentation_examples(self):
        """Test that all Python examples in development documentation work correctly."""
        dev_dir = Path(__file__).parent.parent / "docs" / "development"

        if not dev_dir.exists():
            pytest.skip("docs/development/ directory not found")

        dev_files = list(dev_dir.rglob("*.md"))
        if not dev_files:
            pytest.skip("No markdown files found in docs/development/")

        failed_files: List[Tuple[Path, str, int]] = []
        total_tests = 0

        for dev_file in dev_files:
            success, output, test_count = self.run_markdown_docs_test(dev_file)
            total_tests += test_count

            if test_count > 0 and not success:
                failed_files.append((dev_file, output, test_count))

        if total_tests == 0:
            pytest.skip("No Python code blocks found in development documentation")

        if failed_files:
            error_msg = f"Development documentation tests failed in {len(failed_files)} files:\n\n"

            for file_path, output, test_count in failed_files:
                rel_path = file_path.relative_to(Path(__file__).parent.parent)
                error_msg += f"❌ {rel_path} ({test_count} tests failed)\n"
                error_msg += f"   Run: uv run pytest {rel_path} --markdown-docs\n\n"

            pytest.fail(error_msg)

    def test_all_documentation_summary(self):
        """Provide a summary test that shows overall documentation health."""
        doc_files = self.get_documentation_files()

        if not doc_files:
            pytest.skip("No documentation files found")

        total_files = 0
        total_tests = 0
        failed_files: List[Tuple[Path, str, int]] = []

        for doc_file in doc_files:
            success, _, test_count = self.run_markdown_docs_test(doc_file)

            if test_count > 0:
                total_files += 1
                total_tests += test_count

                if not success:
                    failed_files.append(
                        (
                            doc_file.relative_to(Path(__file__).parent.parent),
                            "",
                            test_count,
                        )
                    )

        if total_tests == 0:
            pytest.skip("No Python code blocks found in any documentation")

        # This test passes even if there are failures, but provides a summary
        print("\n📊 Documentation Test Summary:")
        print(f"   📁 Files with Python examples: {total_files}")
        print(f"   🧪 Total Python code blocks: {total_tests}")
        print(f"   ❌ Files with failures: {len(failed_files)}")

        if failed_files:
            print("\n❌ Files needing attention:")
            for failed_file in failed_files:
                print(f"   - {failed_file}")
            print("\n💡 Fix command: uv run pytest docs/ README.md --markdown-docs")


if __name__ == "__main__":
    pytest.main([__file__])
