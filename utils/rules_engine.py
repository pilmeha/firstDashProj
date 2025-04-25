def apply_rules(plan_df, sales_df):
    # Пример простой логики: вычисление % выполнения
    merged = plan_df.merge(sales_df, on="product", how="left")
    merged["percent_complete"] = (merged["actual"] / merged["plan"]) * 100
    merged["status"] = merged["percent_complete"].apply(lambda x: "green" if x > 90 else "red" if x < 50 else "yellow")
    return merged
