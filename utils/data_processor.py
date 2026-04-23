import pandas as pd


class DataProcessor:

    @staticmethod
    def clean_data(df):
        # Clean column names
        df.columns = df.columns.str.strip()

        # Remove completely empty rows
        df = df.dropna(how="all")

        return df

    @staticmethod
    def detect_types(df):
        df = df.copy()

        # --- Detect numeric columns ---
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

        # --- Detect datetime columns (smart detection) ---
        date_cols = []
        for col in df.columns:
            if col in numeric_cols:
                continue

            converted = pd.to_datetime(df[col], errors='coerce')

            # If at least 70% of values are valid dates → consider it datetime
            if converted.notna().sum() > len(df) * 0.7:
                df[col] = converted
                date_cols.append(col)

        # --- Categorical columns ---
        cat_cols = [col for col in df.columns if col not in numeric_cols + date_cols]

        return numeric_cols, date_cols, cat_cols

    @staticmethod
    def dataset_overview(df):
        total_cells = df.shape[0] * df.shape[1]
        missing = df.isna().sum().sum()

        return {
            "rows": df.shape[0],
            "columns": df.shape[1],
            "missing": int(missing),
            "missing_percent": round((missing / total_cells) * 100, 2) if total_cells > 0 else 0
        }

    @staticmethod
    def handle_missing(df):
        df = df.copy()

        # Fill numeric with median
        for col in df.select_dtypes(include=['number']).columns:
            df[col] = df[col].fillna(df[col].median())

        # Fill categorical with mode
        for col in df.select_dtypes(include=['object']).columns:
            if not df[col].mode().empty:
                df[col] = df[col].fillna(df[col].mode()[0])

        return df