from __future__ import annotations

import pandas as pd
import plotly.express as px


def build_chart(df: pd.DataFrame):
    if df.empty or len(df.columns) < 2:
        return None

    first, second = df.columns[0], df.columns[1]
    numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    if second in numeric_cols:
        return px.bar(df, x=first, y=second, title=f"{second} by {first}")

    if first in numeric_cols and len(df.columns) >= 2:
        return px.bar(df, x=second, y=first, title=f"{first} by {second}")

    if len(numeric_cols) >= 1:
        return px.bar(df, x=first, y=numeric_cols[0], title=f"{numeric_cols[0]} by {first}")

    return None
