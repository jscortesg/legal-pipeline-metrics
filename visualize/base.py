# visualize/base.py

from pathlib import Path


class BasePlot:

    def save(
        self,
        plot,
        filename: str
    ):

        output_dir = Path(
            "output/charts"
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        plot.save(
            output_dir / filename,
            width=8,
            height=5,
            dpi=300
        )