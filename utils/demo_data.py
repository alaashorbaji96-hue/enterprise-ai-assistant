import pandas as pd


def get_demo_dataframe():

    import pandas as pd
    import numpy as np

    np.random.seed(42)

    # ================= TIME =================
    dates = pd.date_range(start="2023-01-01", end="2024-12-31", freq="D")

    df = pd.DataFrame({"date": dates})

    # ================= SEASONALITY =================
    df["day_of_year"] = df["date"].dt.dayofyear

    # Trend (growth over time)
    trend = np.linspace(10000, 50000, len(df))

    # Seasonality (waves)
    seasonality = 5000 * np.sin(2 * np.pi * df["day_of_year"] / 365)

    # Random noise
    noise = np.random.normal(0, 2000, len(df))

    # ================= REVENUE =================
    df["revenue"] = trend + seasonality + noise

    # ================= MARKETING =================
    df["marketing_spend"] = df["revenue"] * np.random.uniform(0.15, 0.25, len(df))

    # ================= CUSTOMERS =================
    df["customers"] = (df["revenue"] / 100).astype(int)

    # ================= CONVERSION =================
    df["conversion_rate"] = np.clip(
        np.random.normal(3.5, 0.7, len(df)),
        1.5,
        6.5
    )

    # ================= REGIONS =================
    regions = ["US", "EU", "MENA", "Asia"]
    df["region"] = np.random.choice(regions, len(df))

    # ================= CHANNEL =================
    channels = ["Google Ads", "Facebook", "LinkedIn", "Email"]
    df["channel"] = np.random.choice(channels, len(df))

    # ================= PRODUCT =================
    products = ["Basic", "Pro", "Enterprise"]
    df["product"] = np.random.choice(products, len(df))

    # ================= SATISFACTION =================
    df["customer_satisfaction"] = np.clip(
        70 + (df["revenue"] / 1000) + np.random.normal(0, 5, len(df)),
        60,
        95
    )

    # ================= DROP EVENTS (REALISM 💀) =================
    drop_days = np.random.choice(len(df), size=10)
    df.loc[drop_days, "revenue"] *= 0.6

    # ================= BOOST EVENTS =================
    boost_days = np.random.choice(len(df), size=10)
    df.loc[boost_days, "revenue"] *= 1.4

    # Clean columns
    df["month"] = df["date"].dt.month_name()
    df["year"] = df["date"].dt.year

    return df
def get_demo_chunks():

    return [

        {
            "text": "This report provides a comprehensive analysis of a SaaS company's performance over a two-year period, focusing on revenue growth, customer acquisition, and strategic scalability.",
            "source": "Enterprise_Growth_Strategy_Report.pdf",
            "page": 1
        },

        {
            "text": "The company achieved strong revenue growth, increasing from approximately $10,000 per month to over $50,000, driven by improved marketing strategies and product-market alignment.",
            "source": "Enterprise_Growth_Strategy_Report.pdf",
            "page": 2
        },

        {
            "text": "A clear upward trend in customer acquisition indicates that demand for the product is increasing, with total customers growing consistently over time.",
            "source": "Enterprise_Growth_Strategy_Report.pdf",
            "page": 3
        },

        {
            "text": "Marketing spend showed a direct impact on revenue, suggesting that performance marketing channels such as Google Ads and LinkedIn were highly effective.",
            "source": "Enterprise_Growth_Strategy_Report.pdf",
            "page": 4
        },

        {
            "text": "Seasonal fluctuations were observed, with higher performance during Q3 and Q4, likely due to increased market activity and targeted campaigns.",
            "source": "Enterprise_Growth_Strategy_Report.pdf",
            "page": 5
        },

        {
            "text": "Conversion rates improved significantly from 2.5% to over 5%, indicating better user experience, improved funnels, and stronger value propositions.",
            "source": "Enterprise_Growth_Strategy_Report.pdf",
            "page": 6
        },

        {
            "text": "The US market generated the highest revenue, while emerging markets such as MENA and Asia showed faster growth rates, presenting future expansion opportunities.",
            "source": "Enterprise_Growth_Strategy_Report.pdf",
            "page": 7
        },

        {
            "text": "Product segmentation analysis revealed that enterprise plans contributed the highest revenue, while basic plans were effective in onboarding new users.",
            "source": "Enterprise_Growth_Strategy_Report.pdf",
            "page": 8
        },

        {
            "text": "Customer satisfaction increased from 70% to over 90%, reflecting improvements in product quality, onboarding, and customer support.",
            "source": "Enterprise_Growth_Strategy_Report.pdf",
            "page": 9
        },

        {
            "text": "Operational efficiency improved through automation and AI-driven analytics, reducing manual workloads and enabling faster decision-making.",
            "source": "Enterprise_Growth_Strategy_Report.pdf",
            "page": 10
        },

        {
            "text": "Despite growth, the company experienced temporary performance drops due to campaign inefficiencies and market fluctuations, highlighting the need for better forecasting.",
            "source": "Enterprise_Growth_Strategy_Report.pdf",
            "page": 11
        },

        {
            "text": "The analysis identifies a strong correlation between marketing investment and revenue, emphasizing the importance of optimizing budget allocation.",
            "source": "Enterprise_Growth_Strategy_Report.pdf",
            "page": 12
        },

        {
            "text": "Future strategies include leveraging AI for predictive analytics, enabling the company to forecast customer behavior and optimize pricing strategies.",
            "source": "Enterprise_Growth_Strategy_Report.pdf",
            "page": 13
        },

        {
            "text": "The company is recommended to scale high-performing channels, invest in emerging markets, and continue improving customer retention strategies.",
            "source": "Enterprise_Growth_Strategy_Report.pdf",
            "page": 14
        },

        {
            "text": "In conclusion, the organization demonstrates strong growth potential, supported by data-driven strategies, scalable operations, and increasing market demand.",
            "source": "Enterprise_Growth_Strategy_Report.pdf",
            "page": 15
        }

    ]