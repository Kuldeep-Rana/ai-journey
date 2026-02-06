import pandas as pd
import json

# ---------- Load users into Pandas DataFrame ----------
def load_users(path):
    try:
        df = pd.read_csv(
            path,
            names=["name", "email", "age", "role"],
            header=None
        )
        df["age"] = pd.to_numeric(df["age"], errors="coerce")
        df = df.dropna(subset=["age"])
        df["age"] = df["age"].astype(int)
        return df
    except Exception as e:
        print(f"Error loading file: {e}")
        return pd.DataFrame()


# ---------- Find user by email ----------
def find_user_by_email(df, email):
    result = df[df["email"] == email]
    return None if result.empty else result.iloc[0].to_dict()


# ---------- Sort users ----------
def sort_users(df, by="age", order="asc"):
    ascending = order == "asc"
    return df.sort_values(by=by, ascending=ascending)


# ---------- Get top N oldest users ----------
def get_top_n_oldest_users(df, n):
    return df.sort_values(by="age", ascending=False).head(n)


# ---------- Generate summary ----------
def generate_summary(df):
    if df.empty:
        return {}

    return {
        "total_users": int(len(df)),
        "roles": df["role"].value_counts().to_dict(),
        "age_stats": {
            "min": int(df["age"].min()),
            "max": int(df["age"].max()),
            "average": round(df["age"].mean(), 2)
        }
    }


# ---------- Write summary to JSON ----------
def write_summary_json(summary, path):
    with open(path, "w") as f:
        json.dump(summary, f, indent=2)


# ---------- Main ----------
if __name__ == "__main__":
    users_df = load_users("day7/users.txt")

    sorted_by_age = sort_users(users_df, by="age", order="desc")
    oldest_users = get_top_n_oldest_users(users_df, 2)
    summary = generate_summary(users_df)

    write_summary_json(summary, "day7/summary.json")
